import csv

from mappings import AnswerMarkingMapping
from responses import Participant, ParticipantResponse

class AutoMarker:
	""" A class that performs the marking of the participant responses.  """

	def __init__(self, responses, mappings_directory):
		""" Create the AutoMarker and load the mappings for the correct answers. """
		self.responses = responses
		self.mappings_directory = mappings_directory

		self.answer_marking_mappings = []
		self.included_columns = []
		self.quiz_prefixes = []

		self.load_answer_marking_mappings()


	def load_answer_marking_mappings(self):
		""" Load the correct answers to the quiz into a list of mapping objects. """
		self.answer_marking_mappings = []
		answer_marking_mappings_filename = '{}/correct_answers.csv'.format(self.mappings_directory)

		with open(answer_marking_mappings_filename, 'r', encoding = 'utf-8-sig') as mappings_file:
			mappings_reader = csv.DictReader(mappings_file)
			for row in mappings_reader:
				answer_marking_mapping = AnswerMarkingMapping()
				answer_marking_mapping.category = row['Category']
				answer_marking_mapping.question_number = row['QuestionNumber']
				answer_marking_mapping.correct_answer = row['CorrectAnswer']
				self.answer_marking_mappings.append(answer_marking_mapping)


	def mark_question_from_answer(self, category, question_number, answer):
		""" Finds the correct answer for the given category and question number, and checks if the given answer matches that. """
		answer_for_question = [am for am in self.answer_marking_mappings if am.category == category and am.question_number == question_number]
		if len(answer_for_question) != 0:

			if len(answer_for_question) == 1:
				return (answer_for_question[0].correct_answer == answer)

			else:
				print('More than one mapping found for the Category: {}, Question Number: {}'.format(category, question_number))
				return False

		else:
			print('No answer mapping found for the Category: {} and Question Number: {}'.format(category, question_number))
			return False


	def get_participants_from_responses(self, included_columns, quiz_prefixes):
		""" A function that goes through all of the responses, creates Participant objects and marks their responses. """
		self.included_columns = included_columns
		participants = []

		for response in self.responses:
			participant = Participant()
			participant_responses = []
			for included_column in included_columns:

				if included_column != 'name' and included_column != 'stream':

					participant_response = ParticipantResponse()
					column_title_split = included_column.split('_')
					category_name = column_title_split[0]
					participant_response.category = category_name

					question_number = column_title_split[1]
					participant_response.question_number = question_number
					if category_name in quiz_prefixes:
						answer = response[included_column]
						participant_response.response_answer = response[included_column]
						participant_response.is_quiz_question = True
						participant_response.is_correct = self.mark_question_from_answer(category_name, question_number, answer)
					else:
						participant_response.response_answer = response[included_column]

					participant_responses.append(participant_response)

			participant.name = response['name']
			participant.stream = response['stream']
			participant.participant_responses = participant_responses
			participants.append(participant)

		return participants





