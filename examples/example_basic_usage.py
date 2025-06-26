#!/usr/bin/env python3
"""
Example: Basic Usage of Test Generator

This example demonstrates how to use the test generator CLI
for basic test generation from example files.
"""

import sys
import os
from pathlib import Path
from example_to_test.example_test_generator import run_cli, generate_tests, find_example_files


def example_basic_test_generation():
    """Example of basic test generation functionality."""
    print("=== Basic Test Generation Example ===")
    
    # Find example files
    example_files = find_example_files("examples")
    print(f"Found {len(example_files)} example files:")
    for file in example_files:
        print(f"  - {file}")
    
    # Generate tests
    generated_files = generate_tests("examples", "tests/from_examples")
    print(f"Generated {len(generated_files)} test files")


def example_cli_help():
    """Example of using CLI help functionality."""
    print("=== CLI Help Example ===")
    
    # Simulate running with --help
    try:
        run_cli(['--help'])
    except SystemExit:
        # argparse help exits with SystemExit, which is expected
        print("Help command executed successfully")


def example_cli_generate():
    """Example of using CLI to generate tests."""
    print("=== CLI Generate Example ===")
    
    # Simulate running the generate command
    result = run_cli(['--examples-dir', 'examples', '--tests-dir', 'tests/from_examples'])
    print(f"CLI execution result: {result}")


def example_cli_clean():
    """Example of using CLI to clean generated tests."""
    print("=== CLI Clean Example ===")
    
    # Simulate running the clean command
    result = run_cli(['--clean', '--tests-dir', 'tests/from_examples'])
    print(f"CLI clean execution result: {result}")


def example_cli_regenerate():
    """Example of using CLI to regenerate tests."""
    print("=== CLI Regenerate Example ===")
    
    # Simulate running the regenerate command
    result = run_cli(['--regenerate', '--examples-dir', 'examples', '--tests-dir', 'tests/from_examples'])
    print(f"CLI regenerate execution result: {result}")


if __name__ == "__main__":
    # Run all examples
    example_basic_test_generation()
    print()
    
    example_cli_help()
    print()
    
    example_cli_generate()
    print()
    
    example_cli_clean()
    print()
    
    example_cli_regenerate()
    print()
    
    print("All basic usage examples completed!") 