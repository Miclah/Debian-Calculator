#!usr/bin/python

##
# @file: math_lib.py
# @brief: Extended Math Library for IVS project 2.
# @author Danyleyko Kirill (xdanyl00)
# @Created: 2023-03-25
# @Last Modified: 2023-03-25
##


# @brief: Extended math operations


##
# @brief: Factorial (n!)
# @param n: First operand
# @return: Factorial of n
# @exception ValueError if the operand is negative.
#
def factorial(n):
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

##
# @brief: Power (base^exponent)
# @param base: First operand
# @param exponent: Second operand
# @return: Power of base by exponent
#
def power(base, exponent):
    """
        Calculates the power of a given base raised to the given exponent
    """
    if exponent == 0:
        return 1

    if isinstance(exponent, float) and exponent == int(exponent):
        exponent = int(exponent)
        result = 1
        for i in range(abs(exponent)):
            result *= base
        if exponent < 0:
            return 1 / result
        else:
            return result
    else:
        return base ** exponent

##
# @brief: Sqrt
# @param n: First operand
# @return: Returns the square root
# @exception ValueError if the operand is negative.
#
def sqrt(n):
    """
        Calculates the square root of a positive number
    """
    if n == 0:
        return 0
    elif n < 0:
        raise ValueError("Cannot compute square root of negative number")
    else:
        guess = n
        while True:
            new_guess = (guess + n / guess) / 2
            if abs(new_guess - guess) < 1e-6:
                return new_guess
            guess = new_guess