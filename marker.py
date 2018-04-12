import csv
import re

def modify_responses_heading(heading):

	response_heading = ''
	question_match = re.match(r'https:\/\/cs4s.github.io\/cc_quiz\/(\w+)\/q(\d+)\/question(\w*).png', heading)
	if question_match:
		return '{}_{}'.format(question_match.group(1), question_match.group(2))

	return response_heading

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

# Counter to keep track of how many quiz question headers have been modified
question_count = 0

modified_responses = []
quiz_responses = get_quiz_responses()

for (index, row) in enumerate(quiz_responses):
	modified_row = []
	for cell in row:
		modified_cell = ''
		# The logic for modifying the responses header row is different to the other rows
		if index == 0:
			modified_cell = modify_responses_heading(cell)

		modified_row.append(modified_cell)

	modified_responses.append(modified_row)

# Write out the modified responses to a csv
print(modified_responses)