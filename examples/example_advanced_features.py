#!/usr/bin/env python3
"""
Example: Advanced Features of Test Generator

This example demonstrates advanced features like orphaned test detection,
custom directory handling, and error scenarios.
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path

from example_to_test.example_test_generator import (
    find_orphaned_test_files, 
    clean_orphaned_tests,
    extract_functions_from_file,
    generate_test_content,
    parse_cli_arguments,
    find_example_files
)


def example_orphaned_test_detection():
    """Example of detecting orphaned test files."""
    print("=== Orphaned Test Detection Example ===")
    
    # Create a temporary test directory with some orphaned files
    with tempfile.TemporaryDirectory() as temp_dir:
        test_dir = os.path.join(temp_dir, "tests")
        examples_dir = os.path.join(temp_dir, "examples")
        
        # Create test directory structure
        os.makedirs(test_dir, exist_ok=True)
        os.makedirs(examples_dir, exist_ok=True)
        
        # Create an example file
        example_file = os.path.join(examples_dir, "example_test.py")
        with open(example_file, 'w') as f:
            f.write('''
def example_function():
    """Example function."""
    pass
''')
        
        # Create a test file that matches the example
        test_file = os.path.join(test_dir, "test_example_test.py")
        with open(test_file, 'w') as f:
            f.write("# Valid test file")
        
        # Create an orphaned test file (no corresponding example)
        orphaned_test = os.path.join(test_dir, "test_orphaned_example.py")
        with open(orphaned_test, 'w') as f:
            f.write("# Orphaned test file")
        
        # Detect orphaned files
        orphaned_files = find_orphaned_test_files(examples_dir, test_dir)
        print(f"Found {len(orphaned_files)} orphaned test files:")
        for file in orphaned_files:
            print(f"  - {file}")


def example_function_extraction():
    """Example of extracting functions from Python files."""
    print("=== Function Extraction Example ===")
    
    # Create a temporary Python file with example functions
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write('''
#!/usr/bin/env python3

def example_function_1():
    """First example function."""
    return "Hello from function 1"

def example_function_2():
    """Second example function."""
    return "Hello from function 2"

def regular_function():
    """This function should not be extracted (doesn't start with example_)."""
    return "Regular function"

def example_function_3():
    """Third example function."""
    return "Hello from function 3"
''')
        temp_file = f.name
    
    try:
        # Extract functions
        functions = extract_functions_from_file(temp_file)
        print(f"Extracted {len(functions)} example functions:")
        for func_name, func in functions.items():
            print(f"  - {func_name}: {func.__doc__}")
            
    finally:
        # Clean up
        os.unlink(temp_file)


def example_test_content_generation():
    """Example of generating test content from functions."""
    print("=== Test Content Generation Example ===")
    
    # Create a temporary Python file with example functions
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write('''
def example_simple_function():
    """A simple example function."""
    return "Hello, World!"

def example_function_with_args(name):
    """An example function with arguments."""
    return f"Hello, {name}!"
''')
        temp_file = f.name
    
    try:
        # Extract functions
        functions = extract_functions_from_file(temp_file)
        
        # Generate test content
        test_content = generate_test_content(temp_file, functions, "examples")
        
        print("Generated test content preview:")
        print("=" * 50)
        print(test_content[:500] + "..." if len(test_content) > 500 else test_content)
        print("=" * 50)
        
    finally:
        # Clean up
        os.unlink(temp_file)


def example_cli_argument_parsing():
    """Example of CLI argument parsing."""
    print("=== CLI Argument Parsing Example ===")
    
    # Test different argument combinations
    test_cases = [
        ['--help'],
        ['--clean'],
        ['--regenerate'],
        ['--clean-orphaned'],
        ['--examples-dir', 'custom_examples'],
        ['--tests-dir', 'custom_tests'],
        ['--examples-dir', 'examples', '--tests-dir', 'tests'],
        ['--regenerate', '--examples-dir', 'examples', '--tests-dir', 'tests']
    ]
    
    for args in test_cases:
        try:
            parsed_args = parse_cli_arguments(args)
            print(f"Args: {args}")
            print(f"  examples_dir: {parsed_args.examples_dir}")
            print(f"  tests_dir: {parsed_args.tests_dir}")
            print(f"  clean: {parsed_args.clean}")
            print(f"  regenerate: {parsed_args.regenerate}")
            print(f"  clean_orphaned: {parsed_args.clean_orphaned}")
            print()
        except SystemExit:
            print(f"Args: {args} -> SystemExit (help or error)")
            print()


def example_error_handling():
    """Example of error handling scenarios."""
    print("=== Error Handling Example ===")
    
    # Test with non-existent directory
    print("Testing with non-existent examples directory:")
    example_files = find_example_files("non_existent_directory")
    print(f"Found {len(example_files)} files (expected: 0)")
    
    # Test with non-existent Python file
    print("\nTesting function extraction from non-existent file:")
    functions = extract_functions_from_file("non_existent_file.py")
    print(f"Extracted {len(functions)} functions (expected: 0)")
    
    # Test with invalid Python file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write('''
This is not valid Python code
def example_function():
    return "Hello"
''')
        invalid_file = f.name
    
    try:
        print("\nTesting function extraction from invalid Python file:")
        functions = extract_functions_from_file(invalid_file)
        print(f"Extracted {len(functions)} functions")
    finally:
        os.unlink(invalid_file)


if __name__ == "__main__":
    # Run all examples
    example_orphaned_test_detection()
    print()
    
    example_function_extraction()
    print()
    
    example_test_content_generation()
    print()
    
    example_cli_argument_parsing()
    print()
    
    example_error_handling()
    print()
    
    print("All advanced features examples completed!") 