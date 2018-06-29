"""
Program to unit test google places query and sort by review sentiments

@author: Suresh
"""
# Imports
import os
import re
import unittest

from query import validateZipCode

class unitTestForReviews(unittest.TestCase):
	def test_zipSuccess(self):
	    result = validateZipCode("53154")
	    self.assertTrue(result)

	def test_zipFailure(self):
	    result = validateZipCode("53154123")
	    self.assertFalse(result)
	'''
	def test_neg(capsys):
	    analyze(os.path.join(RESOURCES, 'neg.txt'))
	    out, err = capsys.readouterr()
	    score = float(re.search('score of (.+?) with', out).group(1))
	    magnitude = float(re.search('magnitude of (.+?)', out).group(1))
	    assert score * magnitude < 0


	def test_mixed(capsys):
	    analyze(os.path.join(RESOURCES, 'mixed.txt'))
	    out, err = capsys.readouterr()
	    score = float(re.search('score of (.+?) with', out).group(1))
	    assert score <= 0.3
	    assert score >= -0.3


	def test_neutral(capsys):
	    analyze(os.path.join(RESOURCES, 'neutral.txt'))
	    out, err = capsys.readouterr()
	    magnitude = float(re.search('magnitude of (.+?)', out).group(1))
	    assert magnitude <= 2.0
	'''
