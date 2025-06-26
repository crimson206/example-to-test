# Example-to-Test

A Python tool that automatically generates test files from example files. This project helps maintain consistency between your example code and test coverage by automatically creating test files for all functions that start with `example_` in your example files.

## Features

- **Automatic Test Generation**: Scans `examples/` directory for `example_*.py` files and generates corresponding test files
- **CLI Interface**: Command-line tool for easy integration into your workflow
- **Smart Test Environment**: Creates isolated test environments with proper setup/teardown
- **Orphaned Test Cleanup**: Removes test files when corresponding example files are deleted
- **Regeneration Support**: Option to regenerate all tests from scratch
- **Type Hints**: Full type annotation support for better code quality

## Installation

### Prerequisites

- Python 3.10 or higher

### Install from Source

```bash
# Clone the repository
git clone https://github.com/crimson206/example-to-test
cd example-to-test

# Install in development mode
pip install -e .
```

### Install directly from GitHub

```bash
# Install directly from GitHub repository
pip install git+https://github.com/crimson206/example-to-test.git
```

After installation, you can use the `example-to-test` command directly:

```bash
# Show help
example-to-test --help

# Generate tests
example-to-test --examples-dir examples --tests-dir tests/from_examples
```

## Usage in Your Project

This tool is designed to be used in **your own projects** to generate tests from your example files. Here's how to set it up:

### 1. Create Your Examples Directory

In your project, create an `examples/` directory and add example files:

```
your-project/
├── examples/                    # Your example files go here
│   ├── example_basic_usage.py
│   ├── example_advanced_features.py
│   └── example_integration_workflow.py
├── src/
├── tests/
└── ...
```

### 2. Write Example Files

Create example files with functions that start with `example_`. These functions should demonstrate how to use your code:

```python
# examples/example_my_feature.py
def example_basic_functionality():
    """Example of basic functionality."""
    from my_module import MyClass
    
    # Create an instance
    obj = MyClass()
    
    # Demonstrate basic usage
    result = obj.basic_method("test")
    print(f"Result: {result}")
    
    # Add assertions to verify expected behavior
    assert result is not None
    assert isinstance(result, str)

def example_advanced_usage():
    """Example of advanced usage with error handling."""
    from my_module import MyClass
    
    try:
        obj = MyClass()
        result = obj.advanced_method(param1="value1", param2="value2")
        print(f"Advanced result: {result}")
        
        # Verify the result
        assert result.success is True
        assert result.data is not None
        
    except Exception as e:
        print(f"Error occurred: {e}")
        # Re-raise to make the test fail
        raise

def example_integration_workflow():
    """Example of a complete workflow."""
    from my_module import MyClass, Config
    
    # Setup
    config = Config(debug=True)
    obj = MyClass(config=config)
    
    # Execute workflow
    step1_result = obj.step1()
    assert step1_result.status == "completed"
    
    step2_result = obj.step2(step1_result.data)
    assert step2_result.status == "completed"
    
    # Final verification
    final_result = obj.get_final_result()
    assert final_result.is_valid()
```

### 3. Generate Tests

Use the CLI to generate tests from your examples:

```bash
# Basic usage - generate tests in default locations
example-to-test

# Specify custom directories
example-to-test --examples-dir examples --tests-dir tests/from_examples

# Regenerate all tests (useful after major changes)
example-to-test --regenerate --examples-dir examples --tests-dir tests/from_examples
```

### 4. Run Your Tests

The generated tests will be in your `tests/from_examples/` directory:

```bash
# Run all generated tests
pytest tests/from_examples/

# Run with verbose output
pytest tests/from_examples/ -v

# Run with coverage
pytest tests/from_examples/ --cov=your_module
```

## CLI Commands

### Basic Commands

```bash
# Generate tests from examples
example-to-test

# Clean all generated tests
example-to-test --clean

# Regenerate all tests (clean + generate)
example-to-test --regenerate

# Show help
example-to-test --help
```

### Advanced Usage

```bash
# Custom directories
example-to-test --examples-dir my_examples --tests-dir my_tests/generated

# Clean specific directory
example-to-test --clean --tests-dir my_tests/generated

# Regenerate with custom paths
example-to-test --regenerate --examples-dir my_examples --tests-dir my_tests/generated
```

## CLI Options

| Option | Description | Default |
|--------|-------------|---------|
| `--examples-dir` | Directory containing example files | `examples` |
| `--tests-dir` | Directory to output generated tests | `tests/from_examples` |
| `--clean` | Remove all generated test files | `False` |
| `--regenerate` | Clean and regenerate all tests | `False` |
| `--help` | Show help message | - |

## Best Practices for Writing Examples

### 1. Function Naming
- All functions must start with `example_`
- Use descriptive names: `example_basic_usage()`, `example_error_handling()`

### 2. Documentation
- Add docstrings to explain what each example demonstrates
- Include context about when to use this pattern

### 3. Assertions
- Add assertions to verify expected behavior
- This helps catch regressions in your code

### 4. Error Handling
- Include examples of error scenarios
- Show how to handle exceptions properly

### 5. Realistic Scenarios
- Use realistic data and scenarios
- Demonstrate actual use cases from your project

### Example Structure

```python
def example_feature_name():
    """Brief description of what this example demonstrates."""
    # Setup - prepare any necessary objects or data
    from your_module import YourClass
    
    # Execute - demonstrate the feature
    obj = YourClass()
    result = obj.some_method()
    
    # Verify - add assertions to check expected behavior
    assert result is not None
    assert result.status == "success"
    
    # Optional: Cleanup or additional verification
    print(f"Example completed: {result}")
```

## Generated Test Structure

The tool automatically generates test files with:

- **Isolated Test Environment**: Each test runs in a temporary directory
- **Setup/Teardown**: Automatic cleanup after each test
- **Function Coverage**: One test method per `example_*` function
- **Error Handling**: Tests fail if example functions raise exceptions

Example generated test:

```python
# tests/from_examples/test_example_my_feature.py
class TestMy_Feature:
    def setup_method(self):
        """Setup test environment"""
        self.test_dir = tempfile.mkdtemp(prefix="test_")
        # ... setup code ...
    
    def test_example_basic_functionality(self):
        """Example of basic functionality."""
        example_module.example_basic_functionality()
        assert True
    
    def test_example_advanced_usage(self):
        """Example of advanced usage."""
        example_module.example_advanced_usage()
        assert True
```

## Python API

You can also use the tool programmatically in your scripts:

```python
from example_to_test.example_test_generator import generate_tests, find_example_files

# Find example files
example_files = find_example_files("examples")
print(f"Found {len(example_files)} example files")

# Generate tests
generated_files = generate_tests("examples", "tests/from_examples")
print(f"Generated {len(generated_files)} test files")
```

## Workflow Integration

### Pre-commit Hook

Add to your `.pre-commit-config.yaml`:

```yaml
- repo: local
  hooks:
    - id: regenerate-example-tests
      name: Regenerate example tests
      entry: example-to-test --regenerate
      language: system
      files: ^examples/
```

### CI/CD Pipeline

Add to your GitHub Actions workflow:

```yaml
- name: Generate example tests
  run: example-to-test --regenerate

- name: Run example tests
  run: pytest tests/from_examples/
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run only generated tests
pytest tests/from_examples/

# Run with coverage
pytest --cov=example_to_test
```

### Code Quality

The project follows strict code quality rules:

- **Function Rules**: Max 30 lines, max 3 levels of nesting, single responsibility
- **Type Hints**: Required for all functions
- **Documentation**: Simple docstrings for complex logic
- **Organization**: Related functions grouped into classes

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes following the code quality rules
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the terms specified in the LICENSE file.

## Author

- **Sisung Kim** - [sisung.kim1@gmail.com](mailto:sisung.kim1@gmail.com)

## Changelog

### v0.1.0
- Initial release
- Basic test generation functionality
- CLI interface
- Orphaned test cleanup
- Regeneration support