from matplotlib import pyplot as plt

#each of these should have 6 elements or less

politics_user_counts = [346927, 143957, 81796, 48924, 28685, 13348]
donald_user_counts = [214832, 65688, 32233, 16224, 7329, 543]
conservative_user_counts = [19595, 5556, 2765, 1504, 815, 385]
republican_user_counts = [3778, 990, 462, 239, 117, 44]
ask_trump_supporters_user_counts = [12684, 2947, 1091, 383, 128, 0]
months = ['01', '03', '05', '07', '09', '11']

png_directory = '../reddit_data/pngs/'


def calculate_user_retention(list_user_counts):

	return_list = [1]
	for i in range(1, len(list_user_counts)):
		current_month = list_user_counts[i]
		last_month = list_user_counts[i - 1]
		user_retention_percentage = current_month / list_user_counts[0]
		return_list.append(user_retention_percentage)
	return return_list

'''
colors
politics: purple
AskTrumpSupporters: Red
Republican: green
The_Donald: Orange
Conservative: blue

'''

def plot_user_retention_rates():
	x_axis = [int(x) for x in months]
	politics_retention = calculate_user_retention(politics_user_counts)
	plt.plot(x_axis[:len(politics_retention)], politics_retention, label = 'politics', color = 'purple')

	donald_retention = calculate_user_retention(donald_user_counts)
	plt.plot(x_axis[:len(donald_retention)], donald_retention, label = 'The_Donald', color = 'orange')

	conservative_retention = calculate_user_retention(conservative_user_counts)
	plt.plot(x_axis[:len(conservative_retention)], conservative_retention, label = 'Conservative', color = 'blue')

	republican_retention = calculate_user_retention(republican_user_counts)
	plt.plot(x_axis[:len(republican_retention)], republican_retention, label = 'Republican', color = 'green')

	ask_trump_retention = calculate_user_retention(ask_trump_supporters_user_counts)
	plt.plot(x_axis[:len(ask_trump_retention)], ask_trump_retention, label = 'AskTrumpSupporters', color = 'red')

	plt.title('User Retention vs Time, 2016')
	plt.xlabel('Months')
	plt.ylabel('Percentage Retained')
	plt.legend()
	plt.savefig(png_directory + 'retention_1.png')

plot_user_retention_rates()