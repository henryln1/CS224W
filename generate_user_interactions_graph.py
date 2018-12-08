import networkx as nx
import sys
import csv
from os import listdir
from os.path import isfile, join
import random
from collections import defaultdict
random.seed(42)

'''
Takes in the csv files for a given month (each csv file covers one subreddit) 
and generates a user relation graph where the edge weight between any two users
is the number of times they have commented on the same submission.


How it works:
For each csv file:
	read in all the users into a set
	create a dict of thread id to users that commented there 


using our two dictionaries, we can iterate over to add all nodes to our graph,
then we can add all edges that we are interested in to our graph with appropriate
weights.
'''

csv_directory = '../reddit_data/processed_csv/'
graph_directory = '../reddit_data/graphs/'



def save_graph(graph, month):
	graph_out_txt_file_path = graph_directory + month + '_user_comments.txt'
	graph_out_gml_file_path = graph_directory + month + '_user_comments.gml'
	graph_out_gexf_file_path = graph_directory + month + '_user_comments.gexf'
	nx.write_edgelist(graph, graph_out_txt_file_path)
	nx.write_gml(graph, graph_out_gml_file_path)
	nx.write_gexf(graph, graph_out_gexf_file_path)



def generate_monthly_users(files):
	users = set()
	for file in files:
		with open(file, newline = '') as f:
			reader = csv.reader(f)
			for line in reader:
				if not line or line[0] == '' or len(line) < 4 or '[deleted]' == line[2]:
					continue
				user = line[2]
				users.add(user)
	return users

def generate_threads_dict(files, users):
	thread_to_user_dict = {}
	for file in files:
		with open(file, newline = '') as f:
			reader = csv.reader(f)
			for line in reader:
				if not line or line[0] == '' or len(line) < 4 or '[deleted]' == line[2]:
					continue
				user = line[2]
				parent_id = line[3]
				if 't3_' not in parent_id or user not in users: #if parent is not a submission or it's a user that isn't around all year, we ignore
					continue 		
				if parent_id not in thread_to_user_dict:
					thread_to_user_dict[parent_id] = set()
				thread_to_user_dict[parent_id].add(user)
	return thread_to_user_dict

def generate_dictionaries(files):
	users = set()
	thread_to_user_dict = {}
	for file in files:
		with open(file, newline = '') as f:
			reader = csv.reader(f)
			for line in reader:
				if not line or line[0] == '' or len(line) < 4 or '[deleted]' == line[2]:
					continue
				user = line[2]
				parent_id = line[3]
				if 't3_' not in parent_id: #if parent is not a submission, we ignore
					continue 
				if parent_id not in thread_to_user_dict:
					thread_to_user_dict[parent_id] = set()
					thread_to_user_dict[parent_id].add(user)
				else:
					thread_to_user_dict[parent_id].add(user)
				users.add(user)

	return users, thread_to_user_dict


def generate_user_graph(users, thread_to_user_dict):
	user_comments_graph = nx.Graph()
	for user in users:
		user_comments_graph.add_node(user)
	print('Total Number of Threads: ', len(thread_to_user_dict.keys()))
	weights_dict = defaultdict(int)
	counter = 0
	for thread in thread_to_user_dict:
		if counter % 3000 == 0:
			print(counter)
		counter += 1
		users_that_commented = list(thread_to_user_dict[thread])
		len_users = len(users_that_commented)
		for index in range(len_users):
			for index2 in range(index + 1, len_users):
				user_1 = users_that_commented[index]
				user_2 = users_that_commented[index2]
				if user_1 == user_2:
					print('ERROR same users appearing in 1 and 2')
					print(thread)
					print(users_that_commented)
				#if user_comments_graph.has_node(user_1) and user_comments_graph.has_node(user_2):
				try:
					weights_dict[tuple(sorted([user_1, user_2]))] += 1
				except:
					continue

	counter = 0 
	for pair in weights_dict:
		user1, user2 = pair
		user_comments_graph.add_edge(user1, user2, weight = weights_dict[pair])

	return user_comments_graph	



def main():
	try:
		year = sys.argv[1]
	except:
		print('Need to enter a year like 2016')
		return
	if len(year) != 4:
		print('Invalid year')
		return


	months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
	#months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10'] #this is for 2018
	continuous_users = set()
	for month in months:
		print('Month: ', month)
		month = year + '-' + month
		files = [f for f in listdir(csv_directory) if isfile(join(csv_directory, f)) and month in f]
		files = [csv_directory + f for f in files]
		users = generate_monthly_users(files)
		if len(continuous_users) == 0:
			continuous_users = users
		else:
			continuous_users = continuous_users.intersection(users) #we only want users that have stayed the entire year
	print('Size of continuous users: ', len(continuous_users))
	#sample 1000 random users:
	#continuous_users = random.sample(continuous_users, 10000)
	print('Number sampled: ', len(continuous_users))

	for month in months: #reiterate and create our graph for each month
		print(month)
		month = year + '-' + month
		files = [f for f in listdir(csv_directory) if isfile(join(csv_directory, f)) and month in f]
		files = [csv_directory + f for f in files]
		thread_to_users_dict = generate_threads_dict(files, continuous_users)
		graph = generate_user_graph(continuous_users, thread_to_users_dict)
		save_graph(graph, month)

	save_graph(graph, month)




if __name__ == "__main__":
	main()