#!/usr/bin/env python3
"""
Test file for PyProtect Enhanced features
"""

def hello_world():
    """Simple function to test obfuscation"""
    message = "Hello, Enhanced PyProtect!"
    print(message)
    return message

def calculate_sum(a, b):
    """Calculate sum of two numbers"""
    result = a + b
    print("Sum of " + str(a) + " and " + str(b) + " is " + str(result))
    return result

def test_loops():
    """Test loop obfuscation"""
    test_string = "This string will be encrypted"
    print("Testing string encryption: " + test_string)
    
    for i in range(3):
        print("Loop iteration: " + str(i))

def main():
    """Main function"""
    hello_world()
    result = calculate_sum(15, 25)
    test_loops()
    
    # Test variable assignments
    my_variable = "Another test string"
    another_var = "Yet another string"
    
    print("Variables: " + my_variable + " and " + another_var)

if __name__ == "__main__":
    main()