import csv

from transform_responses import ResponsesTransformer

def get_quiz_responses():

	responses_filename = 'results/test.csv'
	quiz_rows = []

	with open(responses_filename, encoding = 'utf-8-sig') as responses_file:
		responses_reader = csv.reader(responses_file)
		for (index, row) in enumerate(responses_reader):

			# We don't want the second row of the responses (because the headings are not useful in this case)
			if index != 1:
				row_to_add = []
				for column in row:
					# Get rid of the quotation mark characters in the SurveyMonkey response files
					cleaned_column = column.replace('“', '"')
					cleaned_column = cleaned_column.replace('”', '"')
					row_to_add.append(cleaned_column)

				quiz_rows.append(row_to_add)

	return quiz_rows


def main():

	responses_transformer = ResponsesTransformer(get_quiz_responses(), 'mapping_files/')
	modified_responses = responses_transformer.perform_transformation()

if __name__ == "__main__":
	main()