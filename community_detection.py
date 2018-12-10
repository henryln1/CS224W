import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import *
import random
from sklearn.cluster import spectral_clustering
import time
from collections import Counter
import collections

years = {"2016":12}
user_id_mapping = {}
id_user_mapping = {}

def get_adjacency_matrix(Graph):
    '''
    Compute adjacency matrix of weighted graph
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

def get_subgraph(G, assignments, num_clusters):
    global id_user_mapping
    print("Original number of nodes: {0}".format(G.number_of_nodes()))
    cluster_sizes = Counter(assignments)
    print("Original cluster sizes")
    print(cluster_sizes)
    cluster_nodes = []
    for cluster in range(num_clusters):
        cluster_nodes.append([i for i, x in enumerate(assignments) if x == cluster])
    subgraph_node_labels = []
    cluster_mapping = {}

    for i in range(num_clusters):
        nodes = cluster_nodes[i]
        num_random = max(1, cluster_sizes[i]/10)
        rand_nodes = random.sample(nodes, num_random)
        print("Rand nodes")

        rand_node_labels = [id_user_mapping[id] for id in rand_nodes]
        for label in rand_node_labels:
            cluster_mapping[label] = i
        
        subgraph_node_labels += rand_node_labels

    Gs = G.subgraph(subgraph_node_labels)
    print("Final number of nodes: {0}".format(Gs.number_of_nodes()))
    return Gs, cluster_mapping

def main():
    global id_user_mapping
    global user_id_mapping
    directory = "NewUserGraphEdgeLists/"
    num_clusters_mapping = {"02":3}

    for year in years.keys():

        months = ["0"+str(2)]

        for month in months:
            num_clusters = num_clusters_mapping[month] 
            # Read in graph
            filename = directory + year + "-" + month + "_user_comments.gml"
            a = time.time()
            print("reading in graph")
            G = nx.read_gml(filename)
            b = time.time()
            print("Done reading in graph")
            print(b-a)
            
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

            print("Graph has {0} nodes".format(G.number_of_nodes()))

            # Compute adjacency matrix A
            print("Getting A")
            A = get_adjacency_matrix(G)
            f = time.time()
            print("Done getting A")
            print(f-d)
            
            # Perform spectral clustering
            o = time.time()
            print("Spectral clustering")
            assignments = spectral_clustering(A, n_clusters=num_clusters)
            h = time.time()
            print("Done with spectral clustering")
            print(h-o)
            
            # Get subgraph of original graph for visualization purposes
            print("Getting subgraph")
            Gs, cluster_mapping = get_subgraph(G, assignments, num_clusters)
            p = time.time()
            print("Done getting subgraph")
            print(p-h)

            # Store graph
            nx.set_node_attributes(Gs, 'cluster', cluster_mapping)
            nx.write_gml(Gs, "usergraph_community"+month+"-"+year+".gml")

if __name__ == "__main__":
	main()