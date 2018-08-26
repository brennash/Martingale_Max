import os
import re
import sys
import datetime
from optparse import OptionParser


class MartingaleMax:

	def __init__(self, verboseFlag=False):
		self.verbose    = verboseFlag
		self.fileList   = []
		self.topLeagues = ['E0','F1','D1','SP1','I1','SC0']
		self.fixtures   = []


	def run(self, directory, oddsLimit, oddsBounds):
		# Read in the fixtures
		self.readFixtures(directory)

		# Process the odds
		self.processOdds(oddsLimit, oddsBounds)


	def readFixtures(self, directory):
		# Iterate through the list
		for root, dirs, files in os.walk(directory):
			path = root.split(os.sep)
			for file in files:
				if '.csv' in file and self.topLeagueCheck(file):
					filepath = '{0}/{1}'.format(root, file)
					self.fileList.append(filepath)

		# Process each file
		for filename in self.fileList:
			header   = None
			data     = None
			fileData = open(filename, 'r')
			for index, line in enumerate(fileData):
				if index == 0:
					header = line.strip()
				elif index > 0:
					data = line.strip()
					fixture = Fixture(filename, header, data)
					if not fixture.isValid():
						print('Problem reading {0} line on {1}'.format(index, filename))
					self.fixtures.append(fixture)


	def topLeagueCheck(self, filename):
		""" Used to check if a filename contains top-league data
		"""
		for element in self.topLeagues:
			if element in filename:
				return True
		return False


	def processOdds(self, oddsLimit, oddsBounds):
		inRangeFixtures = []
		for fixture in self.fixtures:
			if fixture.inOddsRange(oddsLimit, oddsBounds):
				fixture.printFixture()
				inRangeFixtures.append(fixture)

		sortedList = sorted(inRangeFixtures, key=lambda fixture: fixture.getDate(), reverse=False)

		pot = 0.0
		for fixture in sortedList:
			if fixture.isHomeWin():
				odds  = fixture.getLowestOdds()
				pot  += (odds-1.0)
				print('Win,',pot)
			else:
				print('Lose',pot-1.0)


class Fixture:

	def __init__(self, filename, header, data):
		headerTokens   = header.split(',')
		dataTokens     = data.split(',')
		self.valid     = False
		self.homeOdds  = []

		try:
			for index, element in enumerate(headerTokens):
				if element == 'Date':
					self.date = datetime.datetime.strptime(dataTokens[index], '%d/%m/%y')
				elif element == 'HomeTeam':
					self.homeTeam = dataTokens[index]
				elif element == 'AwayTeam':
					self.awayTeam = dataTokens[index]
				elif element == 'FTHG':
					self.homeFT = int(dataTokens[index])
				elif element == 'FTAG':
					self.awayFT = int(dataTokens[index])
				elif element == 'FTR':
					self.resultFT = dataTokens[index]
				elif element == 'BWH' and len(dataTokens[index]) > 0:
					self.homeOdds.append(float(dataTokens[index]))
				elif element == 'LBH' and len(dataTokens[index]) > 0:
					self.homeOdds.append(float(dataTokens[index]))
				elif element == 'IWH' and len(dataTokens[index]) > 0:
					self.homeOdds.append(float(dataTokens[index]))
				elif element == 'WHH' and len(dataTokens[index]) > 0:
					self.homeOdds.append(float(dataTokens[index]))
				elif element == 'B365H' and len(dataTokens[index]) > 0:
					self.homeOdds.append(float(dataTokens[index]))
				self.valid = True
		except Exception as error:
			print(filename, header, data, error)

	def getDate(self):
		return self.date

	def isValid(self):
		return self.valid

	def getResult(self):
		return self.resultFT

	def isHomeWin(self):
		if self.resultFT == 'H':
			return True
		return False

	def getLowestOdds(self):
		return min(self.homeOdds)

	def inOddsRange(self, odds, oddsBound):
		lowerLimit =  float(odds) - float(oddsBound)
		upperLimit =  float(odds) + float(oddsBound)
		avgOdds    =  sum(self.homeOdds) / float(len(self.homeOdds))
		if lowerLimit <= avgOdds and avgOdds <= upperLimit:
			return True
		else:
			return False

	def printFixture(self):
		outputString  = '{0},'.format(self.date.strftime('%Y%m%d'))
		outputString += '{0},'.format(self.homeTeam)
		outputString += '{0},'.format(self.awayTeam)
		outputString += '{0},'.format(self.homeFT)
		outputString += '{0},'.format(self.awayFT)
		outputString += '{0},'.format(self.resultFT)
		avgOdds    =  sum(self.homeOdds) / float(len(self.homeOdds))
		outputString += '{0},'.format(avgOdds)
		print(outputString)

def main(argv):
	parser = OptionParser(usage="Usage: MartingaleMax <data-folder> [odds-limits] [odds-bounds]")
	(options, filename) = parser.parse_args()
	if len(filename) == 3:
		if os.path.exists(filename[0]) and os.path.isdir(filename[0]):
			mm = MartingaleMax()
			mm.run(filename[0], float(filename[1]), float(filename[2]))
		else:
			parser.print_help()
			print ('\nYou need to provide an existing input folder.')
			exit(1)
	else:
		parser.print_help()
		print ('\nYou need to provide an input folder.')
		exit(1)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
