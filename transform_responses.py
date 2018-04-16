
import re
import csv

from mappings import HeaderColumnMapping

class ResponsesTransformer:

	def __init__(self, responses, mappings_directory):

		self.responses = responses
		self.mappings_directory = mappings_directory
		self.transformed_headers = []
		self.answer_heading_mappings = []
		self.question_match_regex = re.compile(r'https:\/\/cs4s.github.io\/cc_quiz\/(\w+)\/q(\d+)\/question(\w*).png')

		self.load_answer_heading_mappings()

	def load_answer_heading_mappings(self):

		answer_heading_mappings_filename = '{}/answer_headings.csv'.format(self.mappings_directory)

		with open(answer_heading_mappings_filename, encoding = 'utf-8-sig') as responses_file:
			responses_reader = csv.DictReader(responses_file)
			for row in responses_reader:
				answer_heading_mapping = HeaderColumnMapping()
				answer_heading_mapping.original_title = row["OriginalTitle"]
				answer_heading_mapping.modified_title = row["ModifiedTitle"]
				self.answer_heading_mappings.append(answer_heading_mapping)

	def modify_responses_headings(self, heading):

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

		else:			
			return heading

	def get_transformed_responses(self):

		modified_responses = []

		for (index, row) in enumerate(self.responses):

			modified_row = []

			for cell in row:

				# Some of the cells will be blank, but the cells that we want in the responses should always have something in them	
				if cell != '':

					modified_cell = ''

					# The logic for modifying the responses header row is different to the other rows
					if index == 0:
						modified_header = self.modify_responses_headings(cell)
						modified_row.append(modified_header)
					else:
						modified_row.append(modified_cell)

			modified_responses.append(modified_row)

		return modified_responses




