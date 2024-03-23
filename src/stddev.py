#!/usr/bin/python3

##
# @file: stddev.py
# @brief: Standard deviation for IVS project 2.
# @author: X
# @Created: 2023-03-23
# @Last Modified: 2023-03-28
##

# @brief: Calculating standard deviation using math libraries math_lib.py, extended_math_lib.py

import sys

import extended_math_lib
import math_lib


##
# @brief: Mean
# @param a: Data set
# @return: Mean of numbers from data set
#
def mean_function(data):
    n = len(data)
    sum_data = data[0]
    for i in range(1, n):
        sum_data = math_lib.add(sum_data, data[i])
    return math_lib.div(sum_data, n)

##
# @brief: Variance
# @param a: Data set
# @param b: Mean
# @return: Variance of numbers fro data set
#
def variance_function(data, mean):
    n = len(data)
    numerator = 0
    for x in data:
        numerator = math_lib.add(numerator, extended_math_lib.power(math_lib.sub(x, mean), 2))
    denominator = math_lib.sub(n, 1)
    return math_lib.div(numerator, denominator)

##
# @brief: Standard deviation
# @param a: Data set
# @return: Standard deviation of numbers from data set
#
def standard_deviation(data):
    mean = mean_function(data)
    variance = variance_function(data, mean)
    std_dev =extended_math_lib.sqrt(variance)
    return std_dev

##
# @brief: Retrieving data from input text file, printing result of standard deviation to standard output 
#
data = []
for line in sys.stdin:
    	for num in line.split():
        	data.append(float(num))

std_dev = standard_deviation(data)
print(std_dev)
