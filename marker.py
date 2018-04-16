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
				quiz_rows.append(row)

	return quiz_rows


def main():

	responses_transformer = ResponsesTransformer(get_quiz_responses(), 'mapping_files/')
	modified_responses = responses_transformer.get_transformed_responses()

	print('The following answer headers are a result of transformation:')
	[print(h) for h in responses_transformer.transformed_headers]
	print()

	for column in modified_responses[0]:
		print(column)


if __name__ == "__main__":
	main()