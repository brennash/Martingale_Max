import re
import sys
import json
import logging
import unittest
import datetime
from Fixture import Fixture

class Test(unittest.TestCase):

	def test_initSetup(self):
		""" 
		Tests the test class itself to verify it is working. 
		Should all other tests fail, at least this test should pass.
		"""
		self.assertTrue(True)

	def test_getDiv_1(self):
		data    = ['IRL1','Bohs','Rovers']
		header  = ['Div','HomeTeam','AwayTeam']
		fixture = Fixture(header, data)
		result  = fixture.getDiv()
		self.assertEquals(result,'IRL1')

	def test_getDate_1(self):
		header = ['Div','Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR','HTHG','HTAG','HTR']
		data   = ['E0','11/08/17','Arsenal','Leicester','4','3','H','2','2','D']
		fixture = Fixture(header, data)
		result  = fixture.getDate()
		resultStr = result.strftime('%Y%m%d')
		self.assertEquals(resultStr,'20170811')

	def test_getAvgHomeOdds_1(self):
		header = ['Div','Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR','HTHG','HTAG','HTR','B365H','LBH']
		data   = ['E0','11/08/17','Arsenal','Leicester','4','3','H','2','2','D',2.0,1.0]
		fixture = Fixture(header, data)
		result  = fixture.getAvgHomeOdds()
		self.assertEquals(result,1.5)

	def test_getAvgHomeOdds_2(self):
		header = ['Div','Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR','HTHG','HTAG','HTR']
		data   = ['E0','11/08/17','Arsenal','Leicester','4','3','H','2','2','D']
		fixture = Fixture(header, data)
		result  = fixture.getAvgHomeOdds()
		self.assertIsNone(result)

	def test_getStdDevHomeOdds_1(self):
		header = ['Div','Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR','HTHG','HTAG','HTR','B365H','LBH']
		data   = ['E0','11/08/17','Arsenal','Leicester','4','3','H','2','2','D',2.0,2.0]
		fixture = Fixture(header, data)
		result  = fixture.getStdDevHomeOdds()
		self.assertEquals(result,0.0)

	def test_getStdDevHomeOdds_2(self):
		header = ['Div','Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR','HTHG','HTAG','HTR','B365H','LBH','WHH']
		data   = ['E0','11/08/17','Arsenal','Leicester','4','3','H','2','2','D',2.0,1.3,1.75]
		fixture = Fixture(header, data)
		result  = fixture.getStdDevHomeOdds()
		self.assertTrue(result > 0.0)


def main():
    unittest.main()

if __name__ == '__main__':
    main()

