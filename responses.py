class ParticipantResponse:
	"""  """

	def __init__(self):
		""" """
		self.category = ''
		self.question_number = ''
		self.response_answer = ''
		self.is_quiz_question = False
		self.is_correct = False

	def __repr__():
		display = 'Category: {}\n'.format(self.category)
		display += 'Question Number: {}\n'.format(self.question_number)
		display += 'Response Answer: {}\n'.format(self.is_quiz_question)
		if self.is_quiz_question:
			display += 'This was a response to a quiz question, the response was '
			display += 'correct' if self.is_correct else 'incorrect'
			display += '.'
		else:
			'This was not a response to a quiz question.'
		return display


class Participant:
	"""  """

	def __init__(self):
		""" """
		self.name = ''
		self.participant_responses = []


	def __repr__(self):
		""" """
		display = '\n###\nName: {}\n'.format(self.name)
		display += 'Responses \n###\n'
		for participant_response in self.participant_responses:
			display += '{} Q{}: answered {}'
			if participant_response.is_quiz_question:
				display += '- which was '
				display += 'correct.' if participant_response.is_correct else 'incorrect.'
		return display


	def get_total_for_category(category):
		""" """
		return len([r for r in self.participant_responses if r.category == category and r.is_correct])


	def get_average_for_category_from_sum(category):
		""" """
		category_responses = [r for r in self.participant_responses if r.category == category]
		total = sum([r.response_answer for r in category_responses])
		n = len(category_responses)
		return total / n


