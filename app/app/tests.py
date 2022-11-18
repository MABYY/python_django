'''
Sample Tests

'''

from django.test import SimpleTestCase
from . import calc

class CalcTests(SimpleTestCase):
    def test_add_numbers(self):
        res = calc.add(8,3)
        print('res', res)
        self.assertEqual(res, 11)
        
    def test_substract_numbers(self):
        res = calc.substract(8,3)
        print('res', res)
        self.assertEqual(res, 5)
        
        