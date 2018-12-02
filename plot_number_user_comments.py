from matplotlib import pyplot as plt
import sys
import csv
from os import listdir
from os.path import isfile, join
from collections import defaultdict
import networkx as nx



'''
Creates a graph over a given period of time showing for users in a given subreddit, 
their average number of comments per month.
'''

csv_directory = '../reddit_data/processed_csv/'
graph_directory = '../reddit_data/graphs/'
png_directory = '../reddit_data/pngs/'
months = ['01', '03', '05', '07', '09', '11']
#months = ['07', '09', '11']

'''
Henry's list of things to do for this
1. Figure out who the common users across the entire month are. This is to weed out one time users. 
We want users that have commented at least once in 2 separate months.

2. Create a dictionary of user to comments so dict[user][month number] returns #comments in that month

3. Average out the number of comments a month, so 12 averages

4. Plot this, x axis is number of months since commenting the first time, y axis is number of comments
'''

def create_month_to_users_dict(files):
	'''
	files should be 1,3,5,7,9,11 of a given year. files are csvs
	'''
	month_to_users_dict = {}
	for file in files:
		month_to_users_dict[file] = set()
		with open(file, newline = '') as f:
			reader = csv.reader(f)
			for line in reader:
				if not line or line[0] == '' or len(line) < 3 or '[deleted]' == line[2]:
					continue
				user_node = line[2]
				month_to_users_dict[file].add(user_node)

	return month_to_users_dict


def find_recurring_users(month_to_users_dict):
	#month_to_users_dict is month to all the users in that dict for a single subreddit

	user_recurrence_count = defaultdict(int)
	for month in month_to_users_dict:
		for user in month_to_users_dict[month]:
			user_recurrence_count[user] += 1

	recurring_users = [x for x in user_recurrence_count if user_recurrence_count[x] >= 2]
	temp = [1,2,3,4,5,6]
	for i in temp:
		print(i)
		print(len([x for x in user_recurrence_count if user_recurrence_count[x] >= i]))

	return recurring_users


def find_comment_counts(users, graph_files, subreddit):
	#graph_files have to be in chronological order

	users_comment_counts = defaultdict(list)
	for graph_file in graph_files:
		graph = nx.read_gml(graph_file)
		for user in users:
			if graph.has_edge(subreddit, user):
				users_comment_counts[user].append(graph[subreddit][user]['weight']) #add weight to user's history
	return users_comment_counts			


def calculate_average_comments_per_month(users_comment_counts, png_file_name = None):
	'''
	we are interested in calculating the average #comments in the first month of a user joining 
	a subreddit, the second month, etc... Interested in seeing if as a user stays in a political 
	subreddit, if they comment more and more on average
	'''

	average_comment_count_month = []
	x_axis = [int(x) for x in months] #number of month

	for i in range(len(x_axis)):
		counter_users = 0
		total_comments = 0
		for user in users_comment_counts:
			try:
				total_comments += users_comment_counts[user][i]
				counter_users += 1
			except:
				continue
		if counter_users != 0:
			average_comment_count_month.append(total_comments / counter_users)
		# else:
		# 	average_comment_count_month.append(0)
	return average_comment_count_month

	# plt.plot(x_axis, average_comment_count_month)
	# plt.xlabel('Months Active')
	# plt.ylabel('Average Number of Comments Per User')
	# plt.title('Average Number of Comments Per User vs. Months Active')
	# #plt.show()
	# plt.savefig(png_file_name)

def plot_all_lines(comment_counts_dict, png_file):
	x_axis = [int(x) for x in months]
	for subreddit in comment_counts_dict:
		print(subreddit)
		y_axis = comment_counts_dict[subreddit]
		print(x_axis)
		print(y_axis)
		len_y_axis = len(y_axis)
		plt.plot(x_axis[:len_y_axis], y_axis, label = subreddit)
	plt.xlabel('Months Active')
	plt.ylabel('Average Number of Comments Per User')
	plt.title('Average Number of Comments Per User vs. Months Active')
	plt.legend()
	plt.savefig(png_file)


def main():
	# try:
	# 	subreddit = sys.argv[1]
	# 	year = sys.argv[2]
	# except Exception as e:
	# 	print(e)
	# 	print('Please enter a year and a subreddit.')
	# 	return
	year = sys.argv[1]
	subreddits = ['Conservative', 'The_Donald', 'Republican', 'AskTrumpSupporters', 'politics']
	#subreddits = ['AskTrumpSupporters']
	subreddits_to_files_dict = {}
	for subreddit in subreddits:
		csv_files = []
		graph_files = []
		relevant_months = months
		for month in relevant_months:
			csv_file = csv_directory + 'RC_' + year + '-' + month + '.bz2_csv_' + subreddit + '.csv'
			csv_files.append(csv_file)
			graph_file = graph_directory + year + '-' + month + '_bipartite.gml'
			graph_files.append(graph_file)

		subreddits_to_files_dict[subreddit] = [csv_files, graph_files]

	comment_counts_dict = {}
	for subreddit in subreddits_to_files_dict:
		print(subreddit)
		csv_files = subreddits_to_files_dict[subreddit][0]
		graph_files = subreddits_to_files_dict[subreddit][1]
		month_to_users = create_month_to_users_dict(csv_files)
		recurring_users = find_recurring_users(month_to_users)
		comment_counts = find_comment_counts(recurring_users, graph_files, subreddit)
		comment_counts_dict[subreddit] = calculate_average_comments_per_month(comment_counts)

	png_file = png_directory +  'all_subreddits_' + year + '_user_comments_3.png'

	plot_all_lines(comment_counts_dict, png_file)

if __name__ == "__main__":
	main()
