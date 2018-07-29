
import re
import csv

from mappings import HeaderColumnMapping, AnswerLetterMapping, NumberAnswerMapping, IntegrationMapping

""" A class that takes the SurveyMonkey quiz responses and modifies these for automatic marking. """
class ResponsesTransformer:

	def __init__(self, responses, mappings_directory):
		""" Create the Responses Transformer object and load all of the mappings from files. """
		self.responses = responses
		self.mappings_directory = mappings_directory

		self.transformed_headers = []
		self.answer_heading_mappings = []
		self.answer_mappings = []
		self.number_answer_mappings = []
		self.integration_mappings = []
		self.included_columns = []

		self.question_match_regex = re.compile(r'https:\/\/cs4s.github.io\/cc_quiz\/(\w+)\/q(\d+)\/question(\w*).png')
		self.answer_match_regex = re.compile(r'https:\/\/cs4s.github.io\/cc_quiz\/(\w+)\/q(\d+)\/answer_(\w).png')

		self.load_answer_heading_mappings()
		self.load_answer_mappings()
		self.load_number_answers()
		self.load_integration_mappings()


	def load_answer_heading_mappings(self):
		""" Load the heading mappings for the questions to standardised heading name. """
		self.answer_heading_mappings = []
		answer_heading_mappings_filename = '{}/answer_headings.csv'.format(self.mappings_directory)

		with open(answer_heading_mappings_filename, 'r', encoding = 'utf-8-sig') as mappings_file:
			mappings_reader = csv.DictReader(mappings_file)
			for row in mappings_reader:
				answer_heading_mapping = HeaderColumnMapping()
				answer_heading_mapping.original_title = row['OriginalTitle']
				answer_heading_mapping.modified_title = row['ModifiedTitle']
				self.answer_heading_mappings.append(answer_heading_mapping)


	def load_answer_mappings(self):
		""" Load the answer mappings, that map an answer to the appropriate letter. """
		self.answer_mappings = []
		answer_mappings_filename = '{}/answers.csv'.format(self.mappings_directory)

		with open(answer_mappings_filename, 'r', encoding = 'utf-8-sig') as mappings_file:
			mappings_reader = csv.DictReader(mappings_file)
			for row in mappings_reader:
				answer_mapping = AnswerLetterMapping()
				answer_mapping.category = row['Category']
				answer_mapping.question_number = row['QuestionNumber']
				answer_mapping.original_answer = row['OriginalAnswer']
				answer_mapping.modified_answer = row['ModifiedAnswer']
				self.answer_mappings.append(answer_mapping)


	def load_number_answers(self):
		""" Load the mappings that indicate whether an answer is not multiple choice (just a number answer) """
		self.number_answer_mappings = []
		number_answers_mappings_filename = '{}/number_answers.csv'.format(self.mappings_directory)

		with open(number_answers_mappings_filename, 'r', encoding = 'utf-8-sig') as mappings_file:
			mappings_reader = csv.DictReader(mappings_file)
			for row in mappings_reader:
				number_mapping = NumberAnswerMapping()
				number_mapping.category = row['Category']
				number_mapping.question_number = row['QuestionNumber']
				self.number_answer_mappings.append(number_mapping)

	def load_integration_mappings(self):
		""" Load the mappings to change the integration column name for a column used in analysis """
		self.integration_mappings = []
		integration_mappings_filename = '{}/integration.csv'.format(self.mappings_directory)

		with open(integration_mappings_filename, 'r', encoding='utf-8-sig') as mappings_file:
			mappings_reader = csv.DictReader(mappings_file)
			for row in mappings_reader:
				integration_mapping = IntegrationMapping()
				integration_mapping.original_title = row['OriginalTitle']
				integration_mapping.modified_title = row ['ModifiedTitle']
				self.integration_mappings.append(integration_mapping)

	def modify_responses_heading(self, heading):
		""" Function to modify a heading title """
		question_match = self.question_match_regex.match(heading)
		if question_match:
			question_header = '{}_{}'.format(question_match.group(1), question_match.group(2))
			self.transformed_headers.append(question_header)
			return question_header

		elif (any(a.original_title == heading for a in self.answer_heading_mappings)):
			answer_heading_mapping = [a for a in self.answer_heading_mappings if a.original_title == heading][0]
			question_header = answer_heading_mapping.modified_title
			self.transformed_headers.append(question_header)
			return question_header

		elif (any(im.original_title == heading for im in self.integration_mappings)):
			integration_mapping = [im for im in self.integration_mappings if im.original_title == heading][0]
			question_header = integration_mapping.modified_title
			self.transformed_headers.append(question_header)
			return question_header

		else:			
			return heading


	def modify_headers(self, responses, result_file_path):
		""" Function that iterates through the headings in the first row and writes the responses to a file """
		header_row = []
		for column in responses[0]:
			modified_header = self.modify_responses_heading(column)
			header_row.append(modified_header)

		responses_with_modified_header = [ header_row ] + responses[1:]

		with open(result_file_path, 'w', encoding = 'utf-8-sig') as responses_with_modified_header_file:
			writer = csv.writer(responses_with_modified_header_file)
			writer.writerows(responses_with_modified_header)


	def modify_responses_answer(self, column_title, answer):
		""" Function to modify an answer in the responses, mapping it to a letter, based off the column title """
		if column_title == 'name':
			return answer

		elif column_title == 'stream':
			if answer == 'Coding & STEAM':
				return 'STEAM'
			else:
				return 'MATHS'
		
		elif (any(im.modified_title == column_title for im in self.integration_mappings)):
			if answer == '':
				return 'FALSE'
			else:
				return 'TRUE'

		elif answer == 'I don\'t know':
			return 'E'

		else:

			answer_match = self.answer_match_regex.match(answer)
			if answer_match:
				answer_letter = answer_match.group(3)
				return answer_letter.upper()

			elif (any(nm.category == column_title.split('_')[0] and nm.question_number == column_title.split('_')[1] for nm in self.number_answer_mappings)):
				return answer

			else: 
				column_title_split = column_title.split('_')
				category_name = column_title_split[0]
				question_number = column_title_split[1]
				filtered_answer_mappings = [am for am in self.answer_mappings if am.category == category_name]
				filtered_answer_mappings = [am for am in filtered_answer_mappings if am.question_number == question_number]

				if len(filtered_answer_mappings) != 0:
					filtered_answer_mappings = [am for am in filtered_answer_mappings if am.original_answer == answer]
					if len(filtered_answer_mappings) != 0:
						return filtered_answer_mappings[0].modified_answer
					else:
						print('Category: {} and question number: {} found, but could not map {} to letter.'.format(category_name, question_number, answer))
						return '??'

				else:
					print('Unknown category and/or question number, could not map {} to letter.'.format(answer))
					return '??'


	def modify_answers(self, responses, result_file_path):
		""" Function that iterates through the responses and modifies the answers in the quiz (so they are in a format for automarking) """
		modified_responses = []

		for response in responses[0:]:
			modified_response = {}
			for included_column in self.included_columns:

				if included_column.split('_')[0] == 'TSECT':
					modified_response[included_column] = response[included_column]
				else:
					answer_to_modify = response[included_column]
					modified_answer = self.modify_responses_answer(included_column, answer_to_modify)
					modified_response[included_column] = modified_answer

			modified_responses.append(modified_response)

		with open(result_file_path, 'w', encoding = 'utf-8-sig') as responses_with_modified_answers_file:
			writer = csv.writer(responses_with_modified_answers_file)
			writer.writerow(self.included_columns)
			for modified_response in modified_responses:
				row_to_write = []
				for included_column in self.included_columns:
					row_to_write.append(modified_response[included_column])	
				writer.writerow(row_to_write)


	def filter_responses(self, responses):
		""" Function that filters the responses to only the columns needed for the quiz and TSECT scale  """
		filtered_responses = []
		header_row = self.included_columns
		for response in responses:
			modified_response = []
			for included_column in self.included_columns:
				modified_response.append(response[included_column])
			filtered_responses.append(modified_response)
			
		return [ header_row ] + filtered_responses

	def perform_transformation(self, included_columns):
		""" A function that performs all of the steps necessary to transform the responses to a format for automarking.  """
		self.included_columns = included_columns

		transformed_headers_file_path = 'mid/transformed_headers.csv'

		# Modify the headers and write to a csv
		self.modify_headers(self.responses, transformed_headers_file_path)

		# Reload the responses with modified headers
		modified_responses = []
		with open(transformed_headers_file_path, 'r', encoding = 'utf-8-sig') as transformed_headers_file:
			reader = csv.DictReader(transformed_headers_file)
			for row in reader:
				modified_responses.append(row)

		# Filter the responses to only include the columns we are interested in
		filtered_responses_file_path = 'mid/filtered_responses.csv'
		filtered_responses = self.filter_responses(modified_responses)

		# Write these filtered responses to a csv
		with open(filtered_responses_file_path, 'w', encoding = 'utf-8-sig') as filtered_responses_file:
			writer = csv.writer(filtered_responses_file)
			writer.writerows(filtered_responses)

		# Read mid filtered responses csv and turn it into a list of DictReader responses
		filtered_responses = []
		with open(filtered_responses_file_path, 'r', encoding = 'utf-8-sig') as filtered_responses_file:
			reader = csv.DictReader(filtered_responses_file)
			for row in reader:
				filtered_responses.append(row)

		# Modify the answers and write to a csv
		modified_answers_file_path = 'mid/modified_answers.csv'

		# Map the given answers in the responses to the answer letter
		self.modify_answers(filtered_responses, modified_answers_file_path)









