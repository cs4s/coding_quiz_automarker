
class HeaderColumnMapping:
	""" A class for mapping headers on responses to standardised form. """
	def __init__(self):
		self.original_title = ''
		self.modified_title = ''

	def __repr__(self):
		display = 'Original Title: {}\n'.format(self.original_title)
		display += 'Modified Title: {}\n'.format(self.modified_title)
		return display

	
class AnswerLetterMapping:
	""" A class for mapping the answers to the appropriate letter. """
	def __init__(self):
		self.category = ''
		self.question_number = 0
		self.original_answer = ''
		self.modified_answer = ''

	def __repr__(self):
		display = 'Category: {}\n'.format(self.category)
		display += 'Question Number: {}\n'.format(self.question_number)
		display += 'Survey Answer: {}\n'.format(self.original_answer)
		display += 'Modified Answer: {}\n'.format(self.modified_answer)
		return display


class AnswerMarkingMapping:
	""" A class for mapping the answer for each of the quiz responses. """
	def __init__(self):
		self.category = ''
		self.question_number = 0
		self.correct_answer = ''

	def __repr__(self):
		display = 'Category: {}'.format(self.category)
		display += 'Question Number: {}'.format(self.question_number)
		display += 'Correct Answer: {}'.format(self.correct_answer)
		return display


class NumberAnswerMapping:
	""" A class for mapping a question to being answered with a number (instead of a multiple choice letter) """

	def __init__(self):
		self.category = ''
		self.question_number = 0

	def __repr__(self):
		display = 'Category: {}\n'.format(self.category)
		display += 'Question Number: {}\n'.format(self.question_number)
		return display

class IntegrationMapping:
	""" A class for mapping a question about integrating coding into KLAs to a different column name """

	def __init__(self):
		self.original_title = ''
		self.modified_title = ''

	def __repr__(self):
		display = 'Original Title: {}\n'.format(self.original_title)
		display += 'Modified Title: {}\n'.format(self.modified_title)
		return display