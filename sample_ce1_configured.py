#!/usr/bin/env python3
"""
Sample CE1 Configured File
=========================

This file demonstrates how to embed CE1 configuration directly in Python files.
Each file can define its own gates, balance parameters, and expected outputs.
"""

# CE1-config{
#   balance=alpha:0.8;beta:0.2;gamma:0.7;eta:0.2;
#   gate=syntax:syntax_valid:1.0:true:Must have valid Python syntax;
#   gate=density:semantic_dense:0.6:false:High semantic density;
#   gate=security:security_safe:1.0:true:No security vulnerabilities;
#   gate=performance:performance_optimal:0.8:false:Performance optimized;
#   expected=hello_world:():Hello, World!:str:Simple greeting function;
#   expected=calculate_sum:[1,2,3,4,5]:15:int:Sum calculation function;
# }

def hello_world():
    """A simple hello world function"""
    return "Hello, World!"


def calculate_sum(numbers):
    """Calculate the sum of numbers"""
    return sum(numbers)


def process_data(data):
    """Process data with high semantic density"""
    # This function demonstrates high semantic density
    return [item * 2 for item in data if item > 0]


def main():
    """Main function that demonstrates the file's capabilities"""
    print(hello_world())
    print(f"Sum: {calculate_sum([1, 2, 3, 4, 5])}")
    print(f"Processed: {process_data([1, -2, 3, -4, 5])}")


if __name__ == "__main__":
    main()
