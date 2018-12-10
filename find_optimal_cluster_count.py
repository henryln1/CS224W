import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import *
import random
from sklearn.cluster import spectral_clustering
import time

years = {"2016":12}
user_id_mapping = {}
id_user_mapping = {}

def get_adjacency_matrix(Graph):
    '''
    Build adjacency matrix for weighted graph
    '''
    n = Graph.number_of_nodes()
    A = np.zeros((n, n))
    weights = nx.get_edge_attributes(Graph,'weight')
    for edge, weight in weights.items():
        (s, e) = edge
        s_id = user_id_mapping[str(s)]
        e_id = user_id_mapping[str(e)]
        A[s_id][e_id] = weight
        A[e_id][s_id] = weight
    return A

def get_sparse_degree_matrix(Graph, A):
    '''
    Build degree matrix of weighted graph
    '''
    number_nodes = Graph.number_of_nodes()
    D = np.zeros((number_nodes, number_nodes))
    for node in Graph:
        node_id = user_id_mapping[node]
        D[node_id][node_id] = sum(A[node_id,:])
    return D

def modularity(Graph, A, D, assignments, num_clusters):
    '''
    Computes and returns modularity of cut assignments into num_clusters
    '''
    D_diag = np.diagonal(D)
    D_ = np.matmul(D_diag, D_diag.T)
    S = np.zeros((Graph.number_of_nodes(), num_clusters))
    S[np.arange(Graph.number_of_nodes()),assignments] = 1
    denominator = float(sum(sum(A)))
    B = A - (D/denominator)
    mod = np.trace(np.matmul(np.matmul(S.T, B),S))/denominator
    return mod

def plot_modularity_maximization(X, modularities):
    '''
    Plot graphs of modularity for different cluster sizes
    '''
    fig = plt.figure()
    plot2, = plt.plot(X, modularities[0], label = 'Feb. 2016')
    plot6, = plt.plot(X, modularities[1], label = 'June 2016')
    i = 0
    for mods in modularities:
        print(i)
        i += 1
        print(mods)
        print("max modularity")
        print(max(mods))
        print("argmax modularities")
        print(np.argmax(mods))
    plt.title("Users: Modularities for Different Cluster Sizes")
    plt.xlabel("Number of Clusters")
    plt.ylabel("Modularity")
    plt.legend()
    plt.savefig("user_comments_modularities.png")
    plt.show()

def main():
    directory = "NewUserGraphEdgeLists/"
    all_modularities = []

    for year in years.keys():
        
        months = ["0"+str(6), str(12)]
        for month in months:
            modularities = []
            filename = directory + year + "-" + month + "_user_comments.gml"
            a = time.time()

            # Read in graph
            print("reading in graph")
            Go = nx.read_gml(filename)
            b = time.time()
            print("Done reading in graph")
            print(b-a)
            
            # Get largets connected component
            print("getting largest connected component")
            G = max(nx.connected_component_subgraphs(Go), key=len)
            c = time.time()
            print("done getting largest connected component")
            print(c-b)
            
            # Create user <-> id mapping
            print("creating user-id mapping")
            i = 0
            for node in G:
                user_id_mapping[str(node)] = i
                i += 1
            id_user_mapping = dict(zip(user_id_mapping.values(), user_id_mapping.keys()))
            d = time.time()
            print("Done creating user-id mapping")
            print(d-b)

            # Write largest connected component of graph to gml file
            print("Graph has {0} nodes".format(G.number_of_nodes()))
            print("writing to gml file")
            nx.write_gml(G, "usergraph_connected"+month+"-"+year+".gml")
            print("Done writing to gml file")
            e = time.time()
            print(e-d)

            # Compute adjacency matrix A and degree matrix D
            print("Getting A")
            A = get_adjacency_matrix(G)
            f = time.time()
            print("Done getting A")
            print(f-e)
            print("Getting D")
            D = get_sparse_degree_matrix(G, A)
            print("Done getting D")
            g = time.time()
            print(g-f)
            
            # Find number of clusters that maximizes modularity 
            for num_clusters in range(3, 20):
                o = time.time()
                print("Spectral clustering")
                assignments = spectral_clustering(A, n_clusters=num_clusters)
                h = time.time()
                print("Done with spectral clustering")
                print(h-o)
                print("Modularity")
                mod = modularity(G, A, D, assignments, num_clusters)
                k = time.time()
                print("Done getting modularity")
                print(k-h)
                print("Clusters: {0}".format(num_clusters))
                modularities.append(mod)
                print(modularities)
                assignmentMappings = {}
            all_modularities.append(modularities)
            
    l = time.time()
    print("Plot modularity")            
    plot_modularity_maximization(range(3, 20), all_modularities)
    print("Done plotting modularity")
    m = time.time()
    print(m-l)

if __name__ == "__main__":
	main()