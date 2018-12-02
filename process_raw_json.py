import bz2
import json
import pandas as pd 
import sys
import lzma

'''
Make sure you have created directories ../reddit_data and ../reddit_data/processed_csv
Sample input is python process_raw_json.py RC_2016-01.bz2.
I think I can probably just run this and generate all the csvs and then upload those files 
to the github hopefully so you guys won't have to worry about the data preprocessing.

'''



# files = ['../reddit_data/RC_2016-01.bz2']

relevant_subreddits = ['The_Donald', 'PoliticalDiscussion', 'politics', 
						'socialism', 'Libertarian', 'NeutralPolitics',
						'Ask_Politics', 'AskTrumpSupporters', 'moderatepolitics', 
						'democrats', 'Conservative', 'Republican', 
						'Liberal']

subreddits_dict = dict((key, []) for key in relevant_subreddits) #subreddit to comments from that subreddit

def process_bz2_file(file_path):

	'''
	Will open up a bz2 file and iterate through it and save the information 
	into a CSV file which will be easier to work with later (hopefully). Currently
	the bz2 files are too big and contain a lot of information that we don't care about
	'''
	if file_path[-3:] == 'bz2':
		with bz2.BZ2File(file_path, 'rb') as file:
			write_to_csv_buffer = []
			counter = 0
			for line in file:
				json_format_line = json.loads(line)
				subreddit = json_format_line['subreddit']
				if subreddit in relevant_subreddits:
					#we want to save this entry
					user_id = json_format_line['author']
					parent_id = json_format_line['parent_id']
					timestamp = json_format_line['created_utc']
					content = json_format_line['body']
					controversiality = json_format_line['controversiality']
					score = json_format_line['score']
					subreddits_dict[subreddit].append((subreddit, user_id, parent_id, timestamp, content, controversiality, score))
				counter += 1
				if counter % 5000000 == 0:
					print(counter, ' lines processed.')
	elif file_path[-2:] == 'xz':
		with lzma.open(file_path) as file:
			write_to_csv_buffer = []
			counter = 0
			for line in file:
				json_format_line = json.loads(line)
				subreddit = json_format_line['subreddit']
				if subreddit in relevant_subreddits:
					#we want to save this entry
					user_id = json_format_line['author']
					parent_id = json_format_line['parent_id']
					timestamp = json_format_line['created_utc']
					content = json_format_line['body']
					controversiality = json_format_line['controversiality']
					score = json_format_line['score']
					subreddits_dict[subreddit].append((subreddit, user_id, parent_id, timestamp, content, controversiality, score))
				counter += 1
				if counter % 5000000 == 0:
					print(counter, ' lines processed.')



def generate_csv_name(file_name):
	directory = '../reddit_data/processed_csv/'
	return directory + file_name + '_csv_'

def write_dict_to_csv_files(csv_file_template):
	print('Writing information to new csv files...')
	column_names = ['subreddit', 'author', 'parent_id', 'created_utc', 'body', 'controversiality', 'score']

	for subreddit in subreddits_dict:
		csv_file_name = csv_file_template + subreddit + '.csv'
		table = subreddits_dict[subreddit]
		df = pd.DataFrame(table, columns = column_names)
		df.to_csv(csv_file_name)
	return




def main():
	print('Beginning to process bz2 or xz file...')
	file_directory = '../reddit_data/'
	#file_names = ['RC_2017-07.bz2', 'RC_2017-08.bz2', 'RC_2017-09.bz2', 'RC_2017-10.bz2', 'RC_2017-11.bz2']
	file_names = ['RC_2018-01.xz', 'RC_2018-02.xz', 'RC_2018-03.xz', 'RC_2018-04.xz', 'RC_2018-05.xz', 'RC_2018-06.xz']
	#file_name = sys.argv[1]
	for file_name in file_names:
		file_path = file_directory + file_name
		csv_out_file_name_template = generate_csv_name(file_name)
		process_bz2_file(file_path)
		write_dict_to_csv_files(csv_out_file_name_template)
		print('Finished processing ' + file_name) # + '. Exiting.')

if __name__ == "__main__":
	main()
