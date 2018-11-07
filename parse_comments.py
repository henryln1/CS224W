import sys
import csv
from collections import Counter
import matplotlib.pyplot as plt
import string
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import numpy as np

'''
Make sure you have created directories ../reddit_data and ../reddit_data/processed_csv
Sample input is python process_raw_json.py 3 RC_2016-01.bz2, where 3 refers to the number
of files given (each representing, for example, one month of data).
'''

def get_tokens(file_path):
    tokens = []
    # tokenize data
    with open(file_path) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count > 0 and row["body"] is not None:
                tokens += (row["body"]).split()
                line_count += 1
            else:
                line_count += 1
        print('Processed %d' %line_count)
    print("Original word count %d" %len(tokens))
    return (tokens)

def get_clean_tokens(tokens):
    # convert to lower case
    tokens = [w.lower() for w in tokens]
    # remove punctuation from each word
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    # remove remaining tokens that are not alphabetic
    words = [word for word in stripped if word.isalpha()]
    # filter out stop words
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]
    # stem words
    porter = PorterStemmer()
    words = [porter.stem(word.lower()) for word in words if word not in stop_words]
    print("Final word count %d" %len(words))
    return (words)

def get_word_distrib(words):
    n = len(words)*1.0
    word_distrib = Counter(words).most_common(100)
    word_distrib = [(i,np.divide(j,n)) for (i,j) in word_distrib]
    #print(word_distrib)
    X = range(len(word_distrib))
    y = [j for (i,j) in word_distrib]
    return (word_distrib, X, y)

def get_word_counts(wds):
    if (len(wds) < 2):
        print("Only one word distribution given. Must have 2+ to match word distributions.")
    Ps = []
    Qs = []
    for k in range(len(wds)-1):
        P = (np.array([j for (i,j) in wds[k]]))
        Ps.append(P)
        P_words = [i for (i,j) in wds[k]]
        # Match words in Q to words in P, set # occurrences for words in P 
        # but not in Q to 0
        Q_orig = (np.array([j for (i,j) in wds[k+1]]))
        Q_orig_words = [i for (i,j) in wds[k+1]]
        Q = np.ones(len(P)) * (min(Q_orig)/10.0)
        for i in range(len(P_words)):
            word = P_words[i]
            if word in Q_orig_words:
                idx = Q_orig_words.index(word)
                Q[i] = Q_orig[idx]
        Qs.append(Q)
    return Ps, Qs

def compute_metrics(Ps, Qs):
    '''
    Kullback-Leibler (KL) divergence is defined as:
        KL(P,Q) = sum_i (P(i)log(P(i)/Q(i)))
    where P is the true distribution. We consider
    word distribution 1 to be P. Larger KL values
    indicate bigger differences in distribution.

    Spearman's Rank Correlation Coefficient (SRCC) is defined as:
        SRCC = 1 - (6*sum_i((d_i)^2)/(n*(n^2 - 1)))
    where d_i is the difference between the ranks of word i in the
    two rankings and n is the total number of words.
    '''
    KL, SRCC = [], []
    n = len(Ps) + 1
    if (n < 2):
        print("Only one word distribution given. Must have 2+ to compute KL.")
    for k in range(len(Ps)):
        # KL
        P, Q = Ps[k], Qs[k]
        kl = np.dot(P, np.log(np.divide(P,Q)))
        KL.append(kl)
        # SRCC
        d = np.dot((P-Q), (P-Q))
        srcc = 1 - ((6.0*d)/(n*(n*n - 1)))
        SRCC.append(srcc)
    return (KL, SRCC)

def compute_dynamicity(wds):
    '''
    Dynamicity (DYN) is defined as:
        DYN = avg(V_w) where V_w is the volatility of word w:
            V_w = log(P_ct(w)/P_cT(w))
            where P_ct(w) is the (normalized) frequency of w in time slice t and
            where P_cT(w) is the (normalized) entire frequency history T of w
    '''
    DYN = 0.0
    P_cT = []
    P_o = np.array([j for (i,j) in wds[0]])
    P_o_words = [i for (i,j) in wds[0]]
    for wd in wds:
        if wd != wds[0]:
            P_i = np.array([j for (i,j) in wd])
            P_i_words = [i for (i,j) in wd]
            P_ct = np.zeros(len(P_o))
            for i in range(len(P_o_words)):
                word = P_o_words[i]
                if word in P_i_words:
                    idx = P_i_words.index(word)
                    P_ct[i] = P_i[idx]
        else:
            P_ct = np.array([j for (i,j) in wd])
        P_cT.append(P_ct)
        DYN += np.log(P_ct)
    DYN -= (len(P_cT) * np.log(sum(P_cT)))
    DYN = np.mean(DYN)
    return DYN

def plot_word_distribs(Xs, ys, title):
    fig = plt.figure()
    
    plot1, = plt.plot(Xs[0], ys[0])
    plot2, = plt.plot(Xs[1], ys[1])
    plot3, = plt.plot(Xs[2], ys[2])
    
    plt.xlabel("Word (represented as integer)")
    plt.ylabel("Number of occurrences (normalized over number of words)")
    plt.title("Word Distribution: Subreddit \"{0}\"".format(title))
    plt.legend( [plot1, plot2, plot3],  ['2014', '2015', '2016'], loc= 4 )
    plt.savefig("100_{0}.png".format(title))
    #plt.show()

def main():
    word_distribs = []
    Xs, ys = [], []
    for i in range(int(sys.argv[1])):
        file_directory = './reddit_data/'
        file_name = sys.argv[i+2]
        file_path = file_directory + file_name
        tokens = get_tokens(file_path)
        words = get_clean_tokens(tokens)
        word_distrib, X, y = get_word_distrib(words)
        word_distribs.append(word_distrib)
        Xs.append(X)
        ys.append(y)
    Ps, Qs = get_word_counts(word_distribs)
    print ("KL and SRCC")
    print (compute_metrics(Ps, Qs))
    #print ("DYN %d" %compute_dynamicity(word_distribs))
    plot_word_distribs(Xs, ys, (file_name.split('_csv_')[1]).split('.csv')[0])

if __name__ == "__main__":
	main()