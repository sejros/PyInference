﻿#This file was originally generated by PyScripter's unitest wizard

import unittest
from ddt import data, unpack, ddt
import sys

sys.path.append("..\\")
from fuzzycalc.set import *
from fuzzycalc.subset import Gaussian, Triangle

@ddt
class TestFuzzySet(unittest.TestCase):

    def setUp(self):
        self.A = FuzzySet(0, 100, name = 'Classifier')
        self.A.add_term(Gaussian(20, 10),     name = 'term1')
        self.A.add_term(Triangle(30, 50, 75), name = 'term2')

    def testadd_term(self):
        self.assertAlmostEqual(20, self.A['term1'].median)
        self.assertAlmostEqual(50, self.A['term2'].begin_tol)

    @data(
            (0,    22, 'term2'),
            (1,    50, 'term2'),
            (1,    20, 'term1'),
            (0.607,10, 'term1'),
         )
    @unpack
    def testfind(self, res, value, term):
        self.assertAlmostEqual(res, self.A.find(value, term), places=3)

    @data(
            ('term1', 15),
            ('term2', 55),
            ('term2', 40),
         )
    @unpack
    def testclassify(self, res, val):
        self.assertEquals(res, self.A.classify(val))
@ddt
class TestTriangleClassifier(unittest.TestCase):

    def setUp(self):
        self.names = ['1', '2', '3']

    @data(
            (0.5, False, 1),
            (0.5, False, 2),
            (0.5, False, 1.5),
            (0.5, True, 2),
            (0.5, True, 1),
         )
    @unpack
    def testpeak(self, res, edge, cross):
        A = TriangleClassifier(names=self.names, edge=edge, cross=cross)
        self.assertAlmostEqual(res, A['2'].begin_tol)

    @data(
            (0.25, False, 1),
            (0.0, False, 2),
            (0.125, False, 1.5),
            (0.25, True, 2),
            (0.333, True, 1),
         )
    @unpack
    def testbegin(self, res, edge, cross):
        A = TriangleClassifier(names=self.names, edge=edge, cross=cross)
        self.assertAlmostEqual(res, A['2'].domain.begin, places=3)

    @data(
            (0.75, False, 1),
            (1.0, False, 2),
            (0.875, False, 1.5),
            (0.75, True, 2),
            (0.667, True, 1),
         )
    @unpack
    def testend(self, res, edge, cross):
        A = TriangleClassifier(names=self.names, edge=edge, cross=cross)
        self.assertAlmostEqual(res, A['2'].domain.end, places=3)

    def testtrueedge(self):
        A = TriangleClassifier(names=self.names, edge=True, cross=1.0)
        self.assertAlmostEqual(0.0, A['1'].domain.begin)
        self.assertAlmostEqual(1.0, A['3'].domain.end)

@ddt
class TestGaussianClassifier(unittest.TestCase):

    def setUp(self):
        self.names = ['1', '2', '3']

    @data(
            (0.5, False, 1),
            (0.5, False, 2),
            (0.5, False, 1.5),
            (0.5, True, 2),
            (0.5, True, 1),
         )
    @unpack
    def testpeak(self, res, edge, cross):
        A = GaussianClassifier(names=self.names, edge=edge, cross=cross)
        self.assertAlmostEqual(res, A['2'].mode(), places=3)

    @data(
            (0.083, False, 1),
            (-0.333, False, 2),
            (-0.125, False, 1.5),
            (0.083, True, 2),
            (0.222, True, 1),
         )
    @unpack
    def testbegin(self, res, edge, cross):
        A = GaussianClassifier(names=self.names, edge=edge, cross=cross)
        self.assertAlmostEqual(res, A['2'].domain.begin, places=3)

    @data(
            (0.917, False, 1),
            (1.333, False, 2),
            (1.125, False, 1.5),
            (0.917, True, 2),
            (0.778, True, 1),
         )
    @unpack
    def testend(self, res, edge, cross):
        A = GaussianClassifier(names=self.names, edge=edge, cross=cross)
        self.assertAlmostEqual(res, A['2'].domain.end, places=3)

    def testtrueedge(self):
        A = TriangleClassifier(names=self.names, edge=True, cross=1.0)
        self.assertAlmostEqual(0.0, A['1'].domain.begin)
        self.assertAlmostEqual(1.0, A['3'].domain.end)

@ddt
class TestPartition(unittest.TestCase):

    @data(
            (13.0, 1),
            (13.43, 0.2)
         )
    @unpack
    def testpeaks(self, res, over):
        self.A = Partition(begin=10, end=20,
                             peaks=[10, 13, 18, 20],
                             overlap=over, name='sample classifier')
        self.assertAlmostEqual(res, self.A['1'].mom(), places=3)

    def testclassify(self):
        self.A = Partition(begin = 10, end = 20,
                             peaks = [10, 13, 18, 20],
                             overlap = 0.2, name = 'sample classifier')
        self.assertEqual('1', self.A.classify(14))
        self.assertEqual('2', self.A.classify(17))


if __name__ == '__main__':
    unittest.main()