
class HeaderColumnMapping:

	def __init__(self):
		self.original_title = ''
		self.modified_title = ''

	def __repr__(self):
		display = 'Original Title: {}\n'.format(self.original_title)
		display += 'Modified Title: {}\n'.format(self.modified_title)
		return display
	
class AnswerLetterMapping:

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

	def __init__(self):
		self.category = ''
		self.question_number = 0
		self.correct_answer = ''

class NumberAnswerMapping:
	""" """

	def __init__(self):
		self.category = ''
		self.question_number = 0

	def __repr__(self):
		display = 'Category: {}\n'.format(self.category)
		display += 'Question Number: {}\n'.format(self.question_number)
		return display