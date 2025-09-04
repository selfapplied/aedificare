#!/usr/bin/env python3
"""
Example: How to Use CE1 System
==============================

This file demonstrates how to add CE1 configuration to your Python files.
Each file can define its own gates, balance parameters, and expected outputs.
"""

# CE1-config{
#   balance=alpha:0.8;beta:0.2;gamma:0.7;eta:0.2;
#   gate=syntax:syntax_valid:1.0:true:Must have valid Python syntax;
#   gate=density:semantic_dense:0.6:false:High semantic density;
#   gate=security:security_safe:1.0:true:No security vulnerabilities;
#   expected=greet:John:Hello, John!:str:Greeting function;
#   expected=add_numbers:2,3:5:int:Addition function;
# }

def greet(name):
    """Greet someone by name"""
    return f"Hello, {name}!"


def add_numbers(a, b):
    """Add two numbers together"""
    return a + b


def process_list(items):
    """Process a list with high semantic density"""
    return [item * 2 for item in items if item > 0]


if __name__ == "__main__":
    print(greet("John"))
    print(f"2 + 3 = {add_numbers(2, 3)}")
    print(f"Processed: {process_list([1, -2, 3, -4, 5])}")
