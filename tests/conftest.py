"""Shared pytest fixtures and configuration for the video-depixelation project."""

import os
import shutil
import tempfile
from pathlib import Path
from typing import Generator

import pytest
import torch
from PIL import Image


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory that is cleaned up after the test."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def mock_config():
    """Provide a mock configuration for testing."""
    return {
        "mosaic_size": (25.0, 25.0),
        "window_size": (930, 1842),
        "frames_folder": "frames",
        "windows_folder": "windows",
        "mosaics_folder": "mosaics",
        "accumulated_folder": "accumulated",
    }


@pytest.fixture
def sample_image(temp_dir: Path) -> Path:
    """Create a sample image for testing."""
    img_path = temp_dir / "sample.png"
    img = Image.new("RGB", (100, 100), color="red")
    img.save(img_path)
    return img_path


@pytest.fixture
def sample_tensor():
    """Create a sample tensor for testing."""
    return torch.rand(3, 100, 100)


@pytest.fixture
def mock_frames_folder(temp_dir: Path) -> Path:
    """Create a mock frames folder with sample images."""
    frames_path = temp_dir / "frames"
    frames_path.mkdir()
    
    # Create a few sample frames
    for i in range(3):
        img = Image.new("RGB", (1920, 1080), color=(i * 50, i * 50, i * 50))
        img.save(frames_path / f"frame_{i:04d}.png")
    
    return frames_path


@pytest.fixture
def output_folders(temp_dir: Path) -> dict:
    """Create all output folders for testing."""
    folders = {
        "windows": temp_dir / "windows",
        "mosaics": temp_dir / "mosaics",
        "accumulated": temp_dir / "accumulated",
        "frames_detected": temp_dir / "frames_detected",
    }
    
    for folder in folders.values():
        folder.mkdir()
    
    return folders


@pytest.fixture
def device():
    """Provide the appropriate torch device for testing."""
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


@pytest.fixture(autouse=True)
def cleanup_cuda():
    """Ensure CUDA cache is cleared after each test if CUDA is available."""
    yield
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


@pytest.fixture
def monkeypatch_env(monkeypatch):
    """Fixture to safely modify environment variables."""
    return monkeypatch


def pytest_configure(config):
    """Configure pytest with custom settings."""
    # Add custom markers documentation
    config.addinivalue_line(
        "markers", "gpu: marks tests that require GPU (deselect with '-m \"not gpu\"')"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test location."""
    for item in items:
        # Add GPU marker to tests that use CUDA
        if "cuda" in item.nodeid or "gpu" in item.nodeid:
            item.add_marker(pytest.mark.gpu)
        
        # Automatically mark tests based on their directory
        if "/unit/" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "/integration/" in str(item.fspath):
            item.add_marker(pytest.mark.integration)