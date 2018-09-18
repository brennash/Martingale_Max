import os
import re
import sys
import datetime
from optparse import OptionParser


class MartingaleMax:

	def __init__(self, verboseFlag=False):
		self.verbose    = verboseFlag
		self.topLeagues = ['E0','F1','D1','SP1','I1','SC0']


	def run(self, directory, lowerOddsLimit, upperOddsLimit):

		# Read in the fixtures
		fixtureList = self.readFixtures(directory, lowerOddsLimit, upperOddsLimit)

		# Process the odds
		#self.processOdds(oddsLimit, oddsBounds)


	def readFixtures(self, directory, lowerLimit, upperLimit):

		# The list of valid files
		fileList    = []

		# The list of fixtures
		fixtureList = []

		# Iterate through the list
		for root, dirs, files in os.walk(directory):
			path = root.split(os.sep)
			for file in files:
				if '.csv' in file and self.topLeagueCheck(file):
					filepath = '{0}/{1}'.format(root, file)
					fileList.append(filepath)

		# Process each file
		for filename in fileList:
			header   = None
			data     = None
			fileData = open(filename, 'r')
			for index, line in enumerate(fileData):
				if index == 0:
					header = line.strip()
				elif index > 0:
					data = line.strip()
					fixture = Fixture(filename, header, data)

					if fixture.isValid() and fixture.inOddsRange(lowerLimit, upperLimit):
						fixtureList.append(fixture)

		# Sort and return fixture list
		sortedList = sorted(fixtureList, key=lambda fixture: fixture.getDate(), reverse=False)
		print ('Found {0} fixtures within odds limit ({1:.3f},{2:.3f})'.format(len(sortedList), lowerLimit, upperLimit))

		# Verbose output prints fixtures
		if self.verbose:
			for fixture in sortedList:
				fixture.printFixture()
		else:
			totalWins  = 0.0
			sumOdds    = 0.0
			totalCount = 0.0
			for fixture in sortedList:
				if fixture.isHomeWin():
					totalWins += 1.0
					sumOdds   += fixture.getAvgOdds()
				totalCount += 1.0

			if totalCount == 0.0:
				ratio = 0.0
				odds  = 0.0
			else:
				ratio = totalWins/totalCount
				odds  = sumOdds/totalWins


			print ('{0:.0f} wins from {1:.0f} fixtures - win ratio {2:.4f}, avg. odds {3:.4f}, inv-avg. odds {4:.4f}'.format(totalWins, totalCount, ratio, odds, 1.0/odds))

		return sortedList

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

	def getAvgOdds(self):
		avgOdds    =  sum(self.homeOdds) / float(len(self.homeOdds))
		return avgOdds

	def isHomeWin(self):
		if self.resultFT == 'H':
			return True
		return False

	def getLowestOdds(self):
		return min(self.homeOdds)

	def inOddsRange(self, lowerLimit, upperLimit):
		avgOdds    =  sum(self.homeOdds) / float(len(self.homeOdds))
		if lowerLimit <= avgOdds and avgOdds <= upperLimit:
			return True
		else:
			return False

	def printFixture(self):
		outputString  = '{0},'.format(self.date.strftime('%Y%m%d'))
		outputString += '{0},'.format(self.resultFT)
		outputString += '{0},'.format(self.homeTeam)
		outputString += '{0},'.format(self.awayTeam)
		outputString += '{0},'.format(self.homeFT)
		outputString += '{0},'.format(self.awayFT)
		avgOdds    =  sum(self.homeOdds) / float(len(self.homeOdds))
		outputString += '{0},'.format(avgOdds)
		print(outputString)

def main(argv):
	parser = OptionParser(usage="Usage: MartingaleMax <data-folder> [odds-start-range] [odds-end-range]")

	parser.add_option("-v", "--verbose",
		action="store_true",
		dest="verboseFlag",
		default=False,
		help="verbose output")

	(options, filename) = parser.parse_args()
	if len(filename) == 3:
		if os.path.exists(filename[0]) and os.path.isdir(filename[0]):
			mm = MartingaleMax(options.verboseFlag)
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
