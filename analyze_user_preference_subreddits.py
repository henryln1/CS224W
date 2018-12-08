

import sys









def main():
	try:
		file_name = sys.argv[1]
	except:
		print('Enter a file.')

	users_that_frequent_one = set()
	with open(file_name, 'r') as f:
		for line in f:
			list_form = line.split(',')
			if list_form[0] == 'user_name':
				continue
			user_name = list_form[0]
			for index in range(len(list_form)):
				list_form[index] = list_form[index].replace('\n', '')
			subreddits_frequented = set(list_form[1:])
			if len(subreddits_frequented) == 1:
				users_that_frequent_one.add(user_name)
	print('Number of users that had one favorite subreddit: ', len(users_that_frequent_one))




if __name__ == "__main__":
	main()