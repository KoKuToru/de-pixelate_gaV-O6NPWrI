# Testing Infrastructure

This directory contains the testing infrastructure for the video-depixelation project.

## Running Tests

### Using Poetry (Recommended)

```bash
# Run all tests
poetry run pytest

# Run with verbose output
poetry run pytest -v

# Run specific test file
poetry run pytest tests/test_setup_validation.py

# Run tests matching a pattern
poetry run pytest -k "test_infrastructure"

# Run only unit tests
poetry run pytest -m unit

# Run only integration tests
poetry run pytest -m integration

# Run tests excluding slow ones
poetry run pytest -m "not slow"
```

### Test Coverage

Coverage is automatically generated when running tests. To view coverage:

```bash
# View coverage in terminal
poetry run pytest --cov-report=term

# Generate HTML coverage report
poetry run pytest --cov-report=html
# Then open htmlcov/index.html in a browser

# Run without coverage (faster)
poetry run pytest --no-cov
```

## Test Structure

- `tests/unit/` - Fast, isolated unit tests
- `tests/integration/` - Tests that may use external resources
- `tests/conftest.py` - Shared fixtures and configuration

## Available Fixtures

Key fixtures available in `conftest.py`:

- `temp_dir` - Temporary directory cleaned up after test
- `mock_config` - Mock configuration dictionary
- `sample_image` - Creates a sample PIL image
- `sample_tensor` - Creates a sample PyTorch tensor
- `mock_frames_folder` - Creates folder with sample video frames
- `output_folders` - Creates all output directories
- `device` - Returns appropriate torch device (CPU/CUDA)

## Test Markers

- `@pytest.mark.unit` - Unit test (fast, isolated)
- `@pytest.mark.integration` - Integration test
- `@pytest.mark.slow` - Slow running test
- `@pytest.mark.gpu` - Test requiring GPU

## Writing Tests

1. Create test files prefixed with `test_` or suffixed with `_test.py`
2. Test functions should start with `test_`
3. Use descriptive test names that explain what is being tested
4. Group related tests in classes prefixed with `Test`

Example:

```python
import pytest
from pathlib import Path

class TestDemosaic:
    def test_load_png_frames(self, mock_frames_folder):
        """Test that PNG frames can be loaded correctly."""
        # Your test implementation
        assert mock_frames_folder.exists()
    
    @pytest.mark.slow
    def test_full_processing_pipeline(self):
        """Test the complete video processing pipeline."""
        # Your test implementation
        pass
```

## Configuration

Test configuration is in `pyproject.toml` under `[tool.pytest.ini_options]` and `[tool.coverage.*]` sections.

Currently configured to:
- Run tests from the `tests/` directory
- Generate coverage reports in multiple formats
- Use strict markers
- Show verbose output
- Coverage threshold is set to 0% (increase as tests are added)