import os
import re
import csv
import sys
import time
import random
import datetime
from Fixture import Fixture
from ValueMapping import ValueMapping
from optparse import OptionParser


class MartingaleMax:

	def __init__(self, verboseFlag=False):
		self.verbose        = verboseFlag

		self.topLeaguesOnly = True
		self.topLeagues     = ['E0','F1','D1','SP1','I1']
		self.fixtureList    = []
		self.trainFixtures  = []
		self.evalFixtures   = []

		self.valueMapping   = None


	def run(self, directory):

		# Read in the fixtures
		self.readFixtures(directory)

		# Create the training and evaluation datasets
		self.createTrainingData()

		# Create the value mapping with the training data
		self.createValueMapping()

		# Process the evaluation data
		self.processValueBets()


	def createTrainingData(self):
		for fixture in self.fixtureList:
			threshold = random.random()
			if threshold <= 0.7:
				self.trainFixtures.append(fixture)
			else:
				self.evalFixtures.append(fixture)


	def readFixtures(self, directory):

		# The list of valid files
		fileList    = []

		# The list of fixtures
		fixtureList = []

		# Iterate through the list
		for root, dirs, files in os.walk(directory):
			path = root.split(os.sep)
			for file in files:
				if '.csv' in file:
					filepath = '{0}/{1}'.format(root, file)
					fileList.append(filepath)

		# Process each file
		for filename in fileList:
			header    = None
			data      = None
			inputFile = open(filename, 'r')
			index     = 0

			try:
				reader    = csv.reader( (line.replace('\0','') for line in inputFile), delimiter=',' )
				for row in reader:
					if index == 0:
						header = row
					else:
						data   = row
						fixture = Fixture(header, data)
						div     = fixture.getDiv()
						if div in self.topLeagues and self.topLeaguesOnly:
							fixtureList.append(fixture)
						elif div not in self.topLeagues and self.topLeaguesOnly:
							break
						else:
							fixtureList.append(fixture)
					index += 1
			except:
				print('Error reading {0}, line {1}'.format(filename, index))
				

		# Sort and return fixture list
		self.fixtureList = sorted(fixtureList, key=lambda fixture: fixture.getDate(), reverse=False)

	
	def createValueMapping(self):
		self.valueMapping = ValueMapping()
		for fixture in self.trainFixtures:
			odds   = fixture.getWorstHomeOdds()
			std    = fixture.getStdDevHomeOdds()
			result = fixture.getResult()
			date   = fixture.getDate()

			self.valueMapping.addElement(odds, std, result)
		self.valueMapping.calculate()
		#self.valueMapping.printMatrix()


	def processValueBets(self):

		bank             = 200.0
		stake            = 1.0
		wins             = 0.0
		losses           = 0.0
		prevDate         = None

		maxLosingStreak  = 0
		losingStreak     = 0
		currentStake     = stake
		prevLosses       = 0.0

		fixtureBatch = []

		for fixture in self.evalFixtures:
			currentDate   = fixture.getDate()
			fixtureStd    = fixture.getStdDevHomeOdds()
			fixtureOdds   = fixture.getWorstHomeOdds()
			
			if prevDate is None:
				if self.valueMapping.isValueBet(fixtureOdds, fixtureStd) and fixtureOdds < 2.5:
					fixtureBatch.append(fixture)
			elif currentDate == prevDate:
				if self.valueMapping.isValueBet(fixtureOdds, fixtureStd) and fixtureOdds < 2.5:
					fixtureBatch.append(fixture)
			else:
				if len(fixtureBatch) > 0:
					selectedFixture = self.valueMapping.getHighestValue(fixtureBatch)
					selectedOdds    = selectedFixture.getWorstHomeOdds()

					if selectedFixture.isHomeWin():
						currentSteak  = ((prevLosses + stake)/selectedOdds)
						bank         -= currentSteak
						bank         += (selectedOdds*currentSteak)
						wins         += 1
						prevLosses    = 0.0
					else:
						currentSteak  = ((prevLosses + stake)/selectedOdds)
						prevLosses   += currentSteak + stake
						bank         -= currentSteak
						losses       += 1
						losingStreak = 1
						if losingStreak > maxLosingStreak:
							maxLosingStream = losingStreak
						
						print('losses',prevLosses)
						#time.sleep(1)


					print('{0},{1},{2} v {3},{4:.2f}, Stake:{5:.2f},Bank:{6:.2f}'.format(selectedFixture.getDate(), selectedFixture.getResult(), selectedFixture.getHomeTeam(), selectedFixture.getAwayTeam(), selectedFixture.getWorstHomeOdds(), currentStake, bank))

				
				fixtureBatch = []
				if self.valueMapping.isValueBet(fixtureOdds, fixtureStd) and fixtureOdds < 2.5:
					fixtureBatch.append(fixture)
					
			prevDate = currentDate

		print('Bank: {0:.2f}, Wins: {1:.0f}, Losses: {2:.2f}, Max Losing Streak: {3:.2f}'.format(bank, wins, losses, maxLosingStreak))
		


def main(argv):
	parser = OptionParser(usage="Usage: MartingaleMax <data-folder>")

	parser.add_option("-v", "--verbose",
		action="store_true",
		dest="verboseFlag",
		default=False,
		help="verbose output")

	(options, filename) = parser.parse_args()
	if len(filename) == 1:
		if os.path.exists(filename[0]) and os.path.isdir(filename[0]):
			mm = MartingaleMax(options.verboseFlag)
			mm.run(filename[0])
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
