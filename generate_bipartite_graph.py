import networkx as nx
import pandas as pd
import sys
import csv
from os import listdir
from os.path import isfile, join


'''
Takes in a list of csv files and generates a bipartite graph from that from users to subreddits. It is 
an undirected weighted graph with edge weight being the number of times the user has commented 
in that subreddit for that given month.
'''

csv_directory = '../reddit_data/processed_csv/'
graph_directory = '../reddit_data/graphs/'

#test_files = ['RC_2016-01.bz2_csv_Libertarian.csv', 'RC_2016-01.bz2_csv_The_Donald.csv', 'RC_2016-01.bz2_csv_socialism.csv']

test_files = ['RC_2016-11.bz2_csv_Libertarian.csv']


def add_to_graph(graph, subreddit_node, user_node):
	#if user_node not in graph.Nodes:
	if not graph.has_node(user_node):
		graph.add_node(user_node)
	if not graph.has_node(subreddit_node):#subreddit_node not in graph.nodes:
		graph.add_node(subreddit_node)
	if not graph.has_edge(subreddit_node, user_node):
		#pass #add edge to graph with weight 1
		graph.add_edge(subreddit_node, user_node, weight = 1)
	else:
		#update edge weight
		graph[subreddit_node][user_node]['weight'] += 1


def generate_graph(files):
	print('Generating graph...')
	bipartite_graph = nx.Graph()

	for file in files:
		with open(file, newline = '') as f:
			reader = csv.reader(f)
			for line in reader:
				if not line or line[0] == '' or len(line) < 3 or '[deleted]' == line[2]:
					continue	
				subreddit_node = line[1]
				user_node = line[2]
				add_to_graph(bipartite_graph, subreddit_node, user_node)
	print('Graph generated.')
	return bipartite_graph

def save_graph(graph, month):
	graph_out_txt_file_path = graph_directory + month[:-4] + '.txt'
	graph_out_gml_file_path = graph_directory + month[:-4] + '.gml'
	graph_out_gexf_file_path = graph_directory + month[:-4] + '.gexf'
	nx.write_edgelist(graph, graph_out_txt_file_path)
	nx.write_gml(graph, graph_out_gml_file_path)
	nx.write_gexf(graph, graph_out_gexf_file_path)

def visualize_graph(graph, png_name):

	pass



def main():
	'''
	example command:
	python generate_bipartite_graph.py 2016-11.bz2
	'''
	try:
		month = sys.argv[1]
	except:
		print('Need to enter a month like 2016-11.bz2')
		return

	#file_names = test_files #may change this to be a command line input later
	files = [f for f in listdir(csv_directory) if isfile(join(csv_directory, f)) and month in f]
	files = [csv_directory + f for f in files]
	graph = generate_graph(files)
	graph_png_file_path = graph_directory + month[:-4] + '.png'
	visualize_graph(graph, graph_png_file_path)
	save_graph(graph, month)

if __name__ == "__main__":
	main()
