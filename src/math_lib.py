#!usr/bin/python

##
# @file: math_lib.py
# @brief: Math Library for IVS project 2.
# @author for the basic math operations: Norman Babiak <xbabia01@fit.vutbr.cz>
# @Created: 2023-03-14
# @Last Modified: 2023-03-14
##

# @brief: Basic math operations

##
# @brief: Addition (+)
# @param a: First operand
# @param b: Second operand
# @return: Addition of a and b
#
def add(a, b):
    return a + b

##
# @brief: Subtraction (-)
# @param a: First operand
# @param b: Second operand
# @return: Subtraction of a and b
#
def sub(a, b):
    return a - b

##
# @brief: Multiplication (*)
# @param a: First operand
# @param b: Second operand
# @return: Multiplication of a and b
#
def mul(a, b):
    return a * b

##
# @brief: Division (/)
# @param a: First operand
# @param b: Second operand
# @return: Division of a and b
# @exception ZeroDivisionError if the second operand (divisor) is zero.
#
def div(a, b):
    if(b == 0):
        raise ZeroDivisionError("Cannot divide by zero.")
    return a / b