import csv

from transform_responses import ResponsesTransformer
from automarking import AutoMarker
from export import ExcelExporter

def get_included_columns():
	"""  Create and return a list of the quiz columns that we are interested in. """
	included_columns = []
	included_columns.append('name')
	included_columns.append('stream')

	categories = ['sequencing', 'repetition', 'conditionals']
	for category in categories:
		for i in range(1, 11):
			included_columns.append('{}_{}'.format(category, i))

	for i in range(1, 15):
		included_columns.append('TSECT_{}'.format(i))

	return included_columns


def get_quiz_responses():
	""" Create a list of the quiz responses (without the headers) """
	responses_filename = 'results/test.csv'
	quiz_rows = []

	with open(responses_filename, 'r', encoding = 'utf-8-sig') as responses_file:
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

	# Transform the responses to a format that the auto-marker can read and mark
	columns_to_include = get_included_columns()
	responses_transformer = ResponsesTransformer(get_quiz_responses(), 'mapping_files/')
	responses_transformer.perform_transformation(columns_to_include)

	# Load the transformed responses, for passing to the automarker
	modified_responses = []
	modified_responses_file_path = 'mid/modified_answers.csv'

	with open(modified_responses_file_path, 'r', encoding = 'utf-8-sig') as modified_responses_file:
		responses_reader = csv.DictReader(modified_responses_file)
		for row in responses_reader:
			modified_responses.append(row)

	# Perform the auto marking and get a list of participants, with marked responses
	quiz_response_prefixes = ['sequencing', 'repetition', 'conditionals']
	auto_marker = AutoMarker(modified_responses, 'mapping_files/')
	participants = auto_marker.get_participants_from_responses(columns_to_include, quiz_response_prefixes)

	# Perform the export to the excel spreadsheet, which summarises the responses from the participants
	scale_prefixes = [ 'TSECT' ]
	excel_exporter = ExcelExporter(participants, quiz_response_prefixes, scale_prefixes)
	excel_exporter.perform_export(columns_to_include)

if __name__ == "__main__":
	main()