import sys
import networkx as nx
import csv
from os import listdir
from os.path import isfile, join
from collections import defaultdict
import operator


'''
This file takes in a year and a graph type and calculates the temporal pagerank over the graphs of that year

'''


valid_graph_types = {'bipartite': 'bipartite.txt', 
					'community_relation': '_community_relation.txt', 
					'users': '_user_comments.txt'}

graph_directory = '../reddit_data/graphs/'


#values can be changed but for initial run they are taken from Jure's slides
beta = 0.0
alpha = 0.85


def normalize(r):
	'''
	r is a dict and we want to normalize the values
	'''
	total = 0.0
	for key in r:
		total += r[key]

	for key in r:
		r[key] = r[key] / total

	return r

def run_temporal_pagerank(edges, alpha = alpha, beta = beta):
	'''
	nodes is a set of all nodes we are examining with pagerank
	edges is a set of tuples, each tuple is (start_node, end_node, time_step)

	'''
	r = defaultdict(float) #temporal pagerank estimate of each node
	s = defaultdict(float) #number of active walks visiting each node u
	for edge in edges:
		u, v, time_step = edge
		r[u] += 1 - alpha
		s[u] += 1 - alpha
		r[v] += s[u] * alpha

		if beta > 0 and beta < 1:
			s[v] += s[u] * (1 - beta) * alpha
			s[u] *= beta
		elif beta == 1:
			s[v] += s[u] * alpha
			s[u] = 0

	r = normalize(r)
	return r


def find_files(year, months, graph_type):
	graph_name_template = valid_graph_types[graph_type]

	files = [] #tuple of (month, file_path)
	for month in months:
		file_path = graph_directory + year + '-' + month + graph_name_template
		files.append((month, file_path))

	return files

def read_degree_and_edges(files):
	edges = [] 
	average_degrees = defaultdict(int)
	for file in files:
		month, file_path = file
		graph = nx.read_edgelist(file_path)
		for edge in graph.edges:
			start, end = edge

			edges.append((start, end, month)) #we use month as a timestamp
		for node in graph.nodes:
			average_degrees[node] += graph.degree(node)

	for node in average_degrees:
		average_degrees[node] /= len(files)
	return average_degrees, edges

def sort_dict(x):
	return sorted(x.items(), key=operator.itemgetter(1))


def main():
	try:
		year = sys.argv[1]
		graph_type = sys.argv[2]
	except:
		print('Need to enter a year and valid graph type.')
		return
	if graph_type not in valid_graph_types.keys():
		print('Graph type entered not valid. Please re-examine.')
		print('Valid graph types are: ', str(valid_graph_types.keys()))
		return

	months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']
	if year != '2018':
		months += ['11', '12']

	files = find_files(year, months, graph_type)

	degrees, edges = read_degree_and_edges(files)
	pagerank_rankings = run_temporal_pagerank(edges)

	sorted_rankings = sort_dict(pagerank_rankings)
	print(sorted_rankings[-10:])
	sorted_degrees = sort_dict(degrees)
	print(sorted_degrees[-10:])

	sorted_degrees_set = set([x[0] for x in sorted_degrees][-100:])
	sorted_rankings_set = set([x[0] for x in sorted_rankings][-100:])
	print('Intersection size: ' , len(sorted_rankings_set.intersection(sorted_degrees_set)))

	with open('temporal_pagerank_' + year + '_' + graph_type + '.txt', 'w') as f:
		for temp in sorted_rankings:
			f.write(str(temp) + '\n')
		f.close()
	#print('Intersection of top 100: ', len(set(sorted_rankings[-100:]).intersection(set(sorted_degrees[-10:]))))










if __name__ == "__main__":
	main()

