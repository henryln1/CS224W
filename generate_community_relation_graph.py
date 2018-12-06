import networkx as nx
import sys
import csv
from os import listdir
from os.path import isfile, join


csv_directory = '../reddit_data/processed_csv/'
graph_directory = '../reddit_data/graphs/'


def create_subreddit_user_sets(files):
	subreddit_to_users_dict = {}
	for file in files:
		with open(file, newline = '') as f:
			reader = csv.reader(f)
			for line in reader:
				if not line or line[0] == '' or len(line) < 3 or '[deleted]' == line[2]:
					continue
				subreddit_node = line[1]
				user_node = line[2]
				if subreddit_node not in subreddit_to_users_dict:
					subreddit_to_users_dict[subreddit_node] = set()
				subreddit_to_users_dict[subreddit_node].add(user_node)
	return subreddit_to_users_dict						


def generate_graph(subreddit_to_users_dict):
	print('Generating community relation graph...')
	community_relation_graph = nx.Graph()
	for subreddit in subreddit_to_users_dict:
		community_relation_graph.add_node(subreddit)

	for subreddit1 in subreddit_to_users_dict:
		for subreddit2 in subreddit_to_users_dict:
			if subreddit1 == subreddit2 or community_relation_graph.has_edge(subreddit1, subreddit2):
				continue
			number_common_users = len(subreddit_to_users_dict[subreddit1].intersection(subreddit_to_users_dict[subreddit2]))
			community_relation_graph.add_edge(subreddit1, subreddit2, weight = number_common_users)

	print('Graph generated.')
	return community_relation_graph


def save_graph(graph, month):
	graph_out_txt_file_path = graph_directory + month[:-4] + '_community_relation.txt'
	graph_out_gml_file_path = graph_directory + month[:-4] + '_community_relation.gml'
	graph_out_gexf_file_path = graph_directory + month[:-4] + '_community_relation.gexf'
	nx.write_edgelist(graph, graph_out_txt_file_path)
	nx.write_gml(graph, graph_out_gml_file_path)
	nx.write_gexf(graph, graph_out_gexf_file_path)

def visualize_graph(graph, png_file):
	pass



def main():
	try:
		month = sys.argv[1]
	except:
		print('Need to enter a month like 2016-11.bz2')
		return
	files = [f for f in listdir(csv_directory) if isfile(join(csv_directory, f)) and month in f]
	files = [csv_directory + f for f in files]
	users_community_dict = create_subreddit_user_sets(files)
	graph = generate_graph(users_community_dict)
	if 'xz' in month:
		month += '2'
	save_graph(graph, month)




if __name__ == "__main__":
	main()