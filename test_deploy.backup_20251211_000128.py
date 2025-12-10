#!/usr/bin/env python3
"""
Test file for deploy mode testing
"""

def hello_world():
    """Simple function to test deploy mode"""
    message = "Hello from deploy mode test!"
    print(message)
    return message

def calculate_sum(a, b):
    """Calculate sum of two numbers"""
    result = a + b
    print("Sum of " + str(a) + " and " + str(b) + " is " + str(result))
    return result

def main():
    """Main function"""
    hello_world()
    result = calculate_sum(10, 20)
    
    # Test variables
    test_var = "This is a test variable"
    another_var = "Another variable for testing"
    
    print("Variables: " + test_var + " and " + another_var)

if __name__ == "__main__":
    main()