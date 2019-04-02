import numpy as np
from Fixture import Fixture

class ValueMapping:

	def __init__(self):
		self.oddsList   = []
		self.stdList    = []

		self.totalList  = []
		self.resultList = []

		self.oddsLimits = []
		self.stdLimits  = []

		self.valueList  = []

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

			lower = np.percentile(sortedStd, x)
			upper = np.percentile(sortedStd, x+5)
			self.stdLimits.append([lower, upper])

		# Setup the array of zeros
		wins    = np.zeros( (len(self.oddsLimits), len(self.stdLimits)) )
		losses  = np.zeros( (len(self.oddsLimits), len(self.stdLimits)) )
		ratios         = np.zeros( (len(self.oddsLimits), len(self.stdLimits)) )
		actual         = np.zeros( (len(self.oddsLimits), len(self.stdLimits)) )
		avgOdds        = np.zeros( (len(self.oddsLimits), len(self.stdLimits)) )
		self.valueList = np.zeros( (len(self.oddsLimits), len(self.stdLimits)) )

		# Create the result array
		for index, fixture in enumerate(self.resultList):
			odds   = self.oddsList[index]
			std    = self.stdList[index]
			result = self.resultList[index]
			for i in range(0, len(self.oddsLimits)):
				oddsTuple = self.oddsLimits[i]
				for j in range(0, len(self.stdLimits)):
					stdTuple = self.stdLimits[j]
					if oddsTuple[0] <= odds and odds < oddsTuple[1] and stdTuple[0] <= std and std < stdTuple[1]:
						if result == 'H':
							wins[i][j] += 1
						else:
							losses[i][j] += 1
						actual[i][j] += (1.0/odds)

		# Create the value array
		for i in range(0, len(self.oddsLimits)):
			for j in range(0, len(self.stdLimits)):
				total = wins[i][j] + losses[i][j]
				if total > 0:
					ratios[i][j]          = (wins[i][j] / total)
					avgOdds[i][j]         = (actual[i][j] / total)
					self.valueList[i][j]  = avgOdds[i][j] - ratios[i][j]



	def isValueBet(self, odds, std):
		for i in range(0, len(self.oddsLimits)):
			oddsTuple = self.oddsLimits[i]
			for j in range(0, len(self.stdLimits)):
				stdTuple = self.stdLimits[j]
				if oddsTuple[0] <= odds and odds < oddsTuple[1] and stdTuple[0] <= std and std < stdTuple[1]:
					if self.valueList[i][j] < 0.0:
						return True
					else:
						return False
		return False


	def getHighestValue(self, fixtureList):
		if fixtureList is None:
			return None
		elif len(fixtureList) == 1:
			return fixtureList[0]
		else:
			minValue = np.amax(self.valueList)
			for index, fixture in enumerate(fixtureList):
				odds = fixture.getAvgHomeOdds()
				std  = fixture.getStdDevHomeOdds()
				for i in range(0, len(self.oddsLimits)):
					oddsTuple = self.oddsLimits[i]
					for j in range(0, len(self.stdLimits)):
						stdTuple = self.stdLimits[j]
						if oddsTuple[0] <= odds and odds < oddsTuple[1] and stdTuple[0] <= std and std < stdTuple[1]:
							if self.valueList[i][j] <= minValue:
								minValue = self.valueList[i][j]
								minIndex = index
								break
			return fixtureList[minIndex]
			


	def printMatrix(self):
		print(self.valueList)
