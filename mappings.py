
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
		self.survey_answer = ''
		self.modified_answer = ''

class AnswerMarkingMapping:

	def __init__(self):
		self.category = ''
		self.question_number = 0
		self.correct_answer = ''

	