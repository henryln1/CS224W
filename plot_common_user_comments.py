from matplotlib import pyplot as plt
import sys
import csv
from os import listdir
from os.path import isfile, join
from collections import defaultdict
import networkx as nx


csv_directory = '../reddit_data/processed_csv/'
graph_directory = '../reddit_data/graphs/'
png_directory = '../reddit_data/pngs/'
months = ['01', '03', '05', '07', '09', '11']

from plot_number_user_comments import *


def main():
	'''
	Looks at 2 subreddits at a time
	'''

	year = sys.argv[1]
	subreddits = ['The_Donald', 'politics']
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
	politics_users_monthly = create_month_to_users_dict(subreddits_to_files_dict['politics'][0])
	donald_users_monthly = create_month_to_users_dict(subreddits_to_files_dict['The_Donald'][0])
	print('politics')
	recurring_users_politics = find_recurring_users(politics_users_monthly)
	print('donald')
	recurring_users_donald = find_recurring_users(donald_users_monthly)
	common_users = set(recurring_users_donald).intersection(set(recurring_users_politics))
	common_users_comment_history_politics = find_comment_counts(common_users, subreddits_to_files_dict['politics'][1], 'politics')
	comment_counts_dict['politics'] = calculate_average_comments_per_month(common_users_comment_history_politics)
	common_users_comment_history_donald = find_comment_counts(common_users, subreddits_to_files_dict['The_Donald'][1], 'The_Donald')
	comment_counts_dict['The_Donald'] = calculate_average_comments_per_month(common_users_comment_history_donald)
	png_file = png_directory +  '2_subreddits_' + year + 'common_user_comments.png'
	plot_all_lines(comment_counts_dict, png_file)
	






if __name__ == "__main__":
	main()