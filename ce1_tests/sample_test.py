
#!/usr/bin/env python3
"""
CE1 Test File
=============

This file demonstrates CE1 configuration with tests.
"""

# CE1-config{
#   balance=alpha:0.8;beta:0.2;gamma:0.7;eta:0.2;
#   gate=syntax:syntax_valid:1.0:true:Must have valid Python syntax;
#   gate=density:semantic_dense:0.7:false:High semantic density;
#   gate=security:security_safe:1.0:true:No security vulnerabilities;
#   expected=test_function:():Test passed:str:Test function;
# }

def test_function():
    """Test function that returns a simple message"""
    return "Test passed"

def calculate_fibonacci(n):
    """Calculate Fibonacci number with high semantic density"""
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonaccin-2 if __name__ == "__main__":
    print(test_function())
    print(f"Fibonacci(10): {calculate_fibonacci(10)}")