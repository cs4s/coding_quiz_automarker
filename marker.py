import csv


def get_quiz_responses():

	responses_filename = 'results/test.csv'

	quiz_rows = []

	with open(responses_filename) as responses_file:
		responses_reader = csv.reader(responses_file)
		for (index, row) in enumerate(responses_reader):
			# We don't want the second row of the responses (because the headings are not useful in this case)
			if index != 1:
				quiz_rows.append(row)

	return quiz_rows



modified_responses = []
quiz_responses = get_quiz_responses()
print(quiz_responses)



