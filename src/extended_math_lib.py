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
        raise ValueError("Input must be > 0")
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
        raise ValueError("Input must be > 0")
    else:
        guess = n
        while True:
            new_guess = (guess + n / guess) / 2
            if abs(new_guess - guess) < 1e-6:
                return new_guess
            guess = new_guess

##
# @brief: Compute the natural logarithm (ln) of x.
# @param x: The input value.
# @param num_terms: The number of terms to use in the Taylor series expansion.
#                      Defaults to 1000.
# @return: The natural logarithm of x.
#
def ln(x, num_terms=1000):
    """
    Compute the natural logarithm (ln) of x.
    """
    if x <= 0:
        raise ValueError("Input must be > 0")
    if x == 1:
        return 0.0
    if x < 1:
        return -ln(1 / x, num_terms=num_terms)

    # Use the Taylor series expansion of ln(1+x) around x=0:
    if x > 2:
        y = x ** (1 / 2)
        return ln(y, num_terms=num_terms) + ln(x / y, num_terms=num_terms)

    # Compute the terms of the Taylor series expansion:
    total = 0.0
    power = x - 1
    for n in range(1, num_terms + 1):
        term = power / n
        if n % 2 == 0:
            term = -term
        total += term
        power *= (x - 1)
    return total



