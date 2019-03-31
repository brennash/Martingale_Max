import os
import re
import csv
import sys
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

	def run(self, directory):

		# Read in the fixtures
		self.readFixtures(directory)

		# Create the value mapping
		self.createValueMapping()


	def readFixtures(self, directory):

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
			header    = None
			data      = None
			inputFile = open(filename, 'r')
			reader    = csv.reader( (line.replace('\0','') for line in inputFile), delimiter=',' )
			index     = 0

			for row in reader:
				if index == 0:
					header = row
				elif index > 0:
					data   = row
					fixture = Fixture(header, data)
					fixtureList.append(fixture)
				index += 1

		# Sort and return fixture list
		self.fixtureList = sorted(fixtureList, key=lambda fixture: fixture.getDate(), reverse=False)

	
	def createValueMapping(self):
		for fixture in self.fixtureList:
			odds = fixture.getAvgHomeOdds()
			std  = fixture.getStdDevHomeOdds()
			result = fixture.getResult()




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
