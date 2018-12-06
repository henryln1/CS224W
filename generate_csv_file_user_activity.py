import random
import sys
import csv
from os import listdir
from os.path import isfile, join
from collections import defaultdict
from generate_user_interactions_graph import *
import numpy as np
import pandas as pd
random.seed(42)

#headers = ['user_name', '01', '02', '03', '04', '05' , '06', '07', '08', '09', '10']

headers = ['user_name', '01']

users_to_month_to_subreddit_frequency = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))


def process_files_into_dict(month, files, users):
	for file in files:
		with open(file, newline = '') as f:
			reader = csv.reader(f)
			for line in reader:
				if not line or line[0] == '' or len(line) < 4 or '[deleted]' == line[2]:
					continue
				user = line[2]
				if user not in users:
					continue
				subreddit = line[1]
				users_to_month_to_subreddit_frequency[user][month][subreddit] += 1


def find_most_frequent_subreddit(user, month):
	most_frequent_count = float('-inf')
	curr_subreddit = ''
	for subreddit in users_to_month_to_subreddit_frequency[user][month]:
		if users_to_month_to_subreddit_frequency[user][month][subreddit] > most_frequent_count:
			most_frequent_count = users_to_month_to_subreddit_frequency[user][month][subreddit]
			curr_subreddit = subreddit
	return curr_subreddit
	#return max(users_to_month_to_subreddit_frequency[user][month].iterkeys(), key=(lambda key: users_to_month_to_subreddit_frequency[user][month][key]))


def main():
	headers = ['user_name', '01', '02', '03', '04', '05' , '06', '07', '08', '09', '10']
	try:
		year = sys.argv[1]
	except:
		print('Need to enter a year like 2016')
		return
	if len(year) != 4:
		print('Invalid year')
		return

	months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']
	#months = ['01']
	if year != '2018':
		months += ['11', '12']
		headers += ['11', '12']
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
	continuous_users = random.sample(continuous_users, 1000)
	print('Number sampled: ', len(continuous_users))

	for month in months:
		month = year + '-' + month
		files = [f for f in listdir(csv_directory) if isfile(join(csv_directory, f)) and month in f]
		files = [csv_directory + f for f in files]
		process_files_into_dict(month, files, continuous_users)

	user_most_popular_subreddit_history = defaultdict(list)
	for user in users_to_month_to_subreddit_frequency:
		for month in users_to_month_to_subreddit_frequency[user]:
			user_most_popular_subreddit_history[user].append(find_most_frequent_subreddit(user, month))


	#df = pd.DataFrame(columns = headers)
	list_of_lists = [headers]
	for user in user_most_popular_subreddit_history:
		row = [user] + user_most_popular_subreddit_history[user]
		list_of_lists.append(row)
	with open('test.txt', 'w') as f:
		for row in list_of_lists:
			f.write(','.join(row) + '\n')
		f.close()


if __name__ == "__main__":
	main()