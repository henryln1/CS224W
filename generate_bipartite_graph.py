import networkx as nx
import pandas as pd
import sys
import csv

'''
Takes in a list of csv files and generates a bipartite graph from that from users to subreddits. It is 
an undirected weighted graph with edge weight being the number of times the user has commented 
in that subreddit for that given month.
'''

csv_directory = '../reddit_data/processed_csv/'

test_files = ['RC_2016-01.bz2_csv_Libertarian.csv', 'RC_2016-01.bz2_csv_The_Donald.csv', 'RC_2016-01.bz2_csv_socialism.csv']

test_files = ['RC_2016-01.bz2_csv_Libertarian.csv']

def generate_graph(files):
	print('hello')
	bipartite_graph = nx.Graph()

	for file in files:
		with open(file, newline = '') as f:
			reader = csv.reader(f)
			for line in reader:
				if line[0] == '':
					continue
				print(line)
	return bipartite_graph

def save_graph(graph, file_name):
	pass


def main():
	file_names = test_files #may change this to be a command line input later
	files = [csv_directory + x for x in file_names]
	graph = generate_graph(files)
	graph_out_file_path = ''
	save_graph(graph, graph_out_file_path)
	print('Finished generating graph..')

if __name__ == "__main__":
	main()
