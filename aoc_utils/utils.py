"""
Advent of Code Utility Functions
"""

import re

def ints_line(line):
    digits = r'\d+'

    return re.findall(digits, line)

def ints_file(f):
    return [ints_line(line) for line in f]
    

print(ints_file(open('test.txt', 'r')))