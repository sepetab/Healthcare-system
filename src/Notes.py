class Note():
	def __init__(self, author, note):
		self._author = author
		self._note = note

	@property
	def author(self):
		return self._author

	@property
	def note(self):
		return self._note

	@note.setter
	def note(self, note):
		self._note = note

class Prescription():
	def __init__(self, author, prescript):
		self._author = author
		self._prescript = prescript

	@property
	def author(self):
		return self._author

	@property
	def prescript(self):
		return self._prescript

	@prescript.setter
	def prescript(self, prescript):
		self._prescript = prescript