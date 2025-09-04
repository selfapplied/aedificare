#!/usr/bin/env python3
"""
Test file with intentional syntax errors to demonstrate CE1 learning
"""

# This file has intentional syntax errors for learning demonstration

from from pathlib import Path  # Double 'from' error
import import os              # Double 'import' error

def broken_function():
    print "This is Python 2 style print"  # Missing parentheses
    data = [1, 2, 3, 4, 5  # Missing closing bracket
    
    if True:
    print("This line has wrong indentation")  # Indentation error
    
    return data

class TestClass:
    def method(self):
        from from typing import List  # Another double 'from'
        return "test"
