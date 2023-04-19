import math
import unittest
from src.math_lib import *
from src.extended_math_lib import *

##
# @file: UT_math_lib.py
# @brief: Unit Tests for Math Library for IVS project 2.
# @author Danyleyko Kirill (xdanyl00)
# @Created: 2023-03-06
# @Last Modified: 2023-03-25
##

class TestMathLibrary(unittest.TestCase):

    # Test Method for 'Addition(+)' function
    def test_add(self):
        """
        +
        """
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-2, 3), 1)
        self.assertEqual(add(-2, -3), -5)

    # Test Method for 'Subtraction(-)' function
    def test_sub(self):
        """
        -
        """
        self.assertEqual(sub(5, 3), 2)
        self.assertEqual(sub(-2, 3), -5)
        self.assertEqual(sub(-2, -3), 1)

    # Test Method for 'Multiplication(*)' function
    def test_multiplication(self):
        """
        *
        """
        self.assertEqual(mul(2, 3), 6)
        self.assertEqual(mul(-2, 3), -6)
        self.assertEqual(mul(-2, -3), 6)

    # Test Method for 'Division(/)' function
    def test_division(self):
        """
        /
        """
        self.assertEqual(div(6, 3), 2)
        self.assertEqual(div(-6, 3), -2)
        self.assertEqual(div(-6, -3), 2)
        with self.assertRaises(ZeroDivisionError):
            div(6, 0)

    # Test Method for 'Square Root(math.sqrt)' function
    def test_square_root(self):
        """
        sqrt
        """
        self.assertAlmostEqual(sqrt(4), 2)
        self.assertAlmostEqual(sqrt(9), 3)
        self.assertAlmostEqual(sqrt(121), 11)
        self.assertAlmostEqual(sqrt(2), math.sqrt(2))
        with self.assertRaises(ValueError):
            sqrt(-1)

    # Test Method for 'Power(x^2)' function
    def test_power(self):
        """
        x^2
        """
        self.assertEqual(power(2, 3), 8)
        self.assertEqual(power(-2, 3), -8)
        self.assertEqual(power(-2, 2), 4)
        self.assertAlmostEqual(power(2, 0.5), math.sqrt(2))
        self.assertAlmostEqual(power(2, -1), 0.5)

    # Test Method for 'Factorial(x!)' function
    def test_factorial(self):
        """
        x!
        """
        self.assertEqual(factorial(0), 1)
        self.assertEqual(factorial(1), 1)
        self.assertEqual(factorial(5), 120)
        with self.assertRaises(ValueError):
            factorial(-1)

    def test_ln(self):
        # Test basic inputs:
        self.assertEqual(ln(2), 0.6926474305598223)
        self.assertEqual(ln(1000000), 13.81551055796428)

        # Test input near 1:
        self.assertAlmostEqual(ln(1.001), 0.0009995001666249457)

        with self.assertRaises(ValueError):
            ln(-1)
            ln(0)
            ln(-0.001)

if __name__ == '__main__':
    unittest.main()