

class ValueMapping:

	def __init__(self):
		self.size       = 100
		self.oddsList   = []
		self.stdList    = []
		self.resultList = []

	def addElement(self, odds, stdDev, result):

		self.oddsList.append(odds)
		self.stdList.append(stdDev)
		self.resultList.append(result)
