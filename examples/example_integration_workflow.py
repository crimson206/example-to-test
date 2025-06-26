#!/usr/bin/env python3
"""
Example: Complete Integration Workflow

This example demonstrates a complete workflow of using the test generator
in a real project scenario, including setup, generation, and cleanup.
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path

from example_to_test.example_test_generator import (
    run_cli, 
    generate_tests, 
    clean_generated_tests,
    find_example_files,
    find_orphaned_test_files
)


def example_complete_workflow():
    """Example of a complete workflow from setup to cleanup."""
    print("=== Complete Integration Workflow Example ===")
    
    # Create a temporary project structure
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = temp_dir
        examples_dir = os.path.join(project_root, "examples")
        tests_dir = os.path.join(project_root, "tests", "from_examples")
        
        # Create directory structure
        os.makedirs(examples_dir, exist_ok=True)
        os.makedirs(tests_dir, exist_ok=True)
        
        print(f"Created project structure in: {project_root}")
        
        # Step 1: Create some example files
        example_files = [
            ("example_math.py", '''
def example_addition():
    """Example of addition operation."""
    result = 2 + 3
    assert result == 5
    return result

def example_multiplication():
    """Example of multiplication operation."""
    result = 4 * 5
    assert result == 20
    return result
'''),
            ("example_strings.py", '''
def example_string_concat():
    """Example of string concatenation."""
    result = "Hello" + " " + "World"
    assert result == "Hello World"
    return result

def example_string_format():
    """Example of string formatting."""
    name = "Alice"
    result = f"Hello, {name}!"
    assert "Alice" in result
    return result
'''),
            ("example_lists.py", '''
def example_list_creation():
    """Example of list creation."""
    my_list = [1, 2, 3, 4, 5]
    assert len(my_list) == 5
    return my_list

def example_list_operations():
    """Example of list operations."""
    my_list = [1, 2, 3]
    my_list.append(4)
    assert len(my_list) == 4
    assert my_list[-1] == 4
    return my_list
''')
        ]
        
        for filename, content in example_files:
            file_path = os.path.join(examples_dir, filename)
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"Created: {filename}")
        
        # Step 2: Generate tests using CLI
        print("\n--- Step 2: Generating Tests ---")
        original_cwd = os.getcwd()
        os.chdir(project_root)
        
        try:
            # Use CLI to generate tests
            result = run_cli(['--examples-dir', 'examples', '--tests-dir', 'tests/from_examples'])
            print(f"CLI generation result: {result}")
            
            # Check what was generated
            generated_tests = list(Path(tests_dir).glob("test_*.py"))
            print(f"Generated {len(generated_tests)} test files:")
            for test_file in generated_tests:
                print(f"  - {test_file.name}")
                
        finally:
            os.chdir(original_cwd)
        
        # Step 3: Verify the generated tests
        print("\n--- Step 3: Verifying Generated Tests ---")
        for test_file in generated_tests:
            with open(test_file, 'r') as f:
                content = f.read()
                print(f"\n{test_file.name} preview:")
                print("-" * 40)
                print(content[:300] + "..." if len(content) > 300 else content)
        
        # Step 4: Simulate adding a new example file
        print("\n--- Step 4: Adding New Example File ---")
        new_example = os.path.join(examples_dir, "example_new.py")
        with open(new_example, 'w') as f:
            f.write('''
def example_new_function():
    """A new example function."""
    return "New functionality"
''')
        print("Added: example_new.py")
        
        # Step 5: Regenerate tests to include the new file
        print("\n--- Step 5: Regenerating Tests ---")
        os.chdir(project_root)
        try:
            result = run_cli(['--regenerate', '--examples-dir', 'examples', '--tests-dir', 'tests/from_examples'])
            print(f"CLI regeneration result: {result}")
            
            # Check updated test files
            updated_tests = list(Path(tests_dir).glob("test_*.py"))
            print(f"Now have {len(updated_tests)} test files:")
            for test_file in updated_tests:
                print(f"  - {test_file.name}")
                
        finally:
            os.chdir(original_cwd)
        
        # Step 6: Simulate removing an example file (creating orphaned test)
        print("\n--- Step 6: Creating Orphaned Test ---")
        os.remove(os.path.join(examples_dir, "example_math.py"))
        print("Removed: example_math.py")
        
        # Check for orphaned tests
        orphaned_files = find_orphaned_test_files(examples_dir, tests_dir)
        print(f"Found {len(orphaned_files)} orphaned test files:")
        for orphaned_file in orphaned_files:
            print(f"  - {orphaned_file}")
        
        # Step 7: Clean up orphaned tests
        print("\n--- Step 7: Cleaning Orphaned Tests ---")
        # Note: In real usage, this would prompt for confirmation
        # For this example, we'll just show what would be cleaned
        print("Orphaned tests that would be cleaned:")
        for orphaned_file in orphaned_files:
            print(f"  - {orphaned_file}")
        
        # Step 8: Final cleanup
        print("\n--- Step 8: Final Cleanup ---")
        os.chdir(project_root)
        try:
            result = run_cli(['--clean', '--tests-dir', 'tests/from_examples'])
            print(f"CLI cleanup result: {result}")
            
            # Verify cleanup
            remaining_tests = list(Path(tests_dir).glob("test_*.py"))
            print(f"Remaining test files: {len(remaining_tests)}")
            
        finally:
            os.chdir(original_cwd)
        
        print("\n=== Workflow Completed Successfully ===")


def example_custom_directory_structure():
    """Example of using custom directory structure."""
    print("=== Custom Directory Structure Example ===")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create custom directory structure
        custom_examples = os.path.join(temp_dir, "my_examples")
        custom_tests = os.path.join(temp_dir, "my_tests", "generated")
        
        os.makedirs(custom_examples, exist_ok=True)
        os.makedirs(custom_tests, exist_ok=True)
        
        # Create example file in custom location
        example_file = os.path.join(custom_examples, "example_custom.py")
        with open(example_file, 'w') as f:
            f.write('''
def example_custom_function():
    """Example function in custom directory."""
    return "Custom example"
''')
        
        print(f"Created custom example in: {custom_examples}")
        
        # Generate tests in custom location
        original_cwd = os.getcwd()
        os.chdir(temp_dir)
        
        try:
            result = run_cli(['--examples-dir', 'my_examples', '--tests-dir', 'my_tests/generated'])
            print(f"Custom directory generation result: {result}")
            
            # Check generated files
            generated_files = list(Path(custom_tests).glob("test_*.py"))
            print(f"Generated {len(generated_files)} test files in custom location:")
            for test_file in generated_files:
                print(f"  - {test_file}")
                
        finally:
            os.chdir(original_cwd)


def example_error_recovery():
    """Example of handling and recovering from errors."""
    print("=== Error Recovery Example ===")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        examples_dir = os.path.join(temp_dir, "examples")
        tests_dir = os.path.join(temp_dir, "tests")
        
        os.makedirs(examples_dir, exist_ok=True)
        os.makedirs(tests_dir, exist_ok=True)
        
        # Create an example file with syntax error
        bad_example = os.path.join(examples_dir, "example_bad.py")
        with open(bad_example, 'w') as f:
            f.write('''
def example_bad_function():
    """Example function with syntax error."""
    return "Hello"  # Missing closing quote
''')
        
        # Create a good example file
        good_example = os.path.join(examples_dir, "example_good.py")
        with open(good_example, 'w') as f:
            f.write('''
def example_good_function():
    """Example function without errors."""
    return "Hello, World!"
''')
        
        print("Created example files (one with error, one without)")
        
        # Try to generate tests (should handle the error gracefully)
        original_cwd = os.getcwd()
        os.chdir(temp_dir)
        
        try:
            result = run_cli(['--examples-dir', 'examples', '--tests-dir', 'tests'])
            print(f"Generation result: {result}")
            
            # Check what was generated despite the error
            generated_files = list(Path(tests_dir).glob("test_*.py"))
            print(f"Generated {len(generated_files)} test files despite errors:")
            for test_file in generated_files:
                print(f"  - {test_file.name}")
                
        finally:
            os.chdir(original_cwd)


if __name__ == "__main__":
    # Run all integration examples
    example_complete_workflow()
    print()
    
    example_custom_directory_structure()
    print()
    
    example_error_recovery()
    print()
    
    print("All integration workflow examples completed!") 