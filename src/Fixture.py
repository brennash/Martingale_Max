import datetime
import statistics

class Fixture:


	def __init__(self, header, data):
		self.header = [x.upper() for x in header]
		self.data   = data


	def getDiv(self):
		return self.getElement('Div')

	def getDate(self):
		dateStr = self.getElement('Date')
		date    = datetime.datetime.strptime(dateStr, '%d/%m/%y')
		return date

	def getResult(self):
		return self.getElement('FTR')

	def getHTResult(self):
		return self.getElement('HTR')

	def getHomeTeam(self):
		return self.getElement('HomeTeam')

	def getAwayTeam(self):
		return self.getElement('AwayTeam')

	def getHomeFT(self):
		return self.getElement('FTHG')

	def getAwayFT(self):
		return self.getElement('FTAG')

	def isHomeWin(self):
		result = self.getResult()
		if result == 'H':
			return True
		return False

	def isDraw(self):
		result = self.getResult()
		if result == 'D':
			return True
		return False

	def isAwayWin(self):
		result = self.getResult()
		if result == 'A':
			return True
		return False

	def getAvgHomeOdds(self):
		oddsList = self.getHomeOddsList()
		if len(oddsList) > 0:
			return (sum(oddsList) / len(oddsList))
		else:
			return None

	def getStdDevHomeOdds(self):
		oddsList = self.getHomeOddsList()
		if len(oddsList) == 0:
			return None
		elif len(oddsList) == 1:
			return 0.0
		else:
			return statistics.stdev(oddsList)

	def getHomeOddsList(self):
		results  = []
		homeOdds = [ 'B365H','BWH','IWH','LBH','WHH','PSH','WHH','VCH' ]
		for headerName in homeOdds:
			odds = self.getElement(headerName)
			if odds is not None:
				results.append(odds)
		return results

	def getElement(self, elementName):
		try:
			index = self.header.index(elementName.strip().upper())
			return self.data[index]
		except:
			return None
