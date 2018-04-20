
class ParticipantResponse:
	""" A class that represents a response in the survey (including quiz questions and scale items)  """

	def __init__(self):
		""" Creates the Participant Response with empty fields. """
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
		display += '\n'
		return display


class Participant:
	""" A class representing a Participant that completed the survey. """

	def __init__(self):
		self.name = ''
		self.participant_responses = []


	def __repr__(self):
		display = '\n###\nName: {}\n### Responses ###\n'.format(self.name)
		for response in self.participant_responses:
			display += '{} Q{}: answered {}'.format(response.category, response.question_number, response.response_answer)
			if response.is_quiz_question:
				display += ' - which was '
				display += 'correct.' if response.is_correct else 'incorrect.'
			display += '\n'
		return display


	def get_correct_count_for_category(self, category):
		""" Returns the number of correct answers for a given   """
		return len([r for r in self.participant_responses if r.category == category and r.is_correct])


	def get_average_for_category_from_sum(self, category):
		""" Returns the average of results of a category. """
		category_responses = [r for r in self.participant_responses if r.category == category]
		total = sum([int(r.response_answer) for r in category_responses])
		n = len(category_responses)
		return (total / n)


