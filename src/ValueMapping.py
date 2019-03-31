import numpy as np

class ValueMapping:

	def __init__(self):
		self.oddsList   = []
		self.stdList    = []

		self.totalList  = []
		self.resultList = []

		self.oddsLimits = []
		self.stdLimits  = []

	def addElement(self, odds, stdDev, result):
		self.oddsList.append(odds)
		self.stdList.append(stdDev)
		self.resultList.append(result)

	
	def calculate(self):
		sortedOdds = np.array(sorted(self.oddsList))
		sortedStd  = np.array(sorted(self.stdList))
	
		for x in range(0,100,5):
			lower = np.percentile(sortedOdds, x)
			upper = np.percentile(sortedOdds, x+5)
			self.oddsLimits.append([lower, upper])

			lower = np.percentile(sortedOdds, x)
			upper = np.percentile(sortedOdds, x+5)
			self.stdLimits.append([lower, upper])


		results = np.zeros( (len(self.oddsLimits), len(self.stdLimits)) )

		for index, fixture in enumerate(self.resultList):
			odds   = self.oddsList[index]
			std    = self.stdList[index]
			result = self.resultList[index]
			for i in range(0, len(self.oddsLimits)):
				oddsTuple = self.oddsLimits[i]
				for j in range(0, len(self.stdLimits)):
					stdTuple = self.stdLimits[j]
					#print(oddsTuple, stdTuple)
					if oddsTuple[0] <= odds and odds < oddsTuple[1] and stdTuple[0] <= std and std < stdTuple[1]:
						if result == 'H':
							results[i][j] += 1



		print(results)

					
