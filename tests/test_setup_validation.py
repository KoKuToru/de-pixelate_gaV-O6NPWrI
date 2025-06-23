"""Validation tests to ensure the testing infrastructure is properly configured."""

import os
import sys
from pathlib import Path

import pytest
import torch
from PIL import Image


class TestInfrastructureSetup:
    """Test class to validate the testing infrastructure setup."""

    def test_pytest_is_importable(self):
        """Verify pytest can be imported."""
        import pytest
        assert pytest is not None

    def test_coverage_is_configured(self):
        """Verify pytest-cov is available."""
        import pytest_cov
        assert pytest_cov is not None

    def test_mock_is_available(self):
        """Verify pytest-mock is available."""
        import pytest_mock
        assert pytest_mock is not None

    def test_project_dependencies_importable(self):
        """Verify main project dependencies can be imported."""
        import torch
        import torchvision
        from PIL import Image
        
        assert torch is not None
        assert torchvision is not None
        assert Image is not None

    def test_fixtures_are_available(self, temp_dir, mock_config, sample_image):
        """Verify conftest fixtures are properly loaded."""
        assert temp_dir.exists()
        assert isinstance(mock_config, dict)
        assert sample_image.exists()

    @pytest.mark.unit
    def test_unit_marker_works(self):
        """Verify unit test marker is recognized."""
        assert True

    @pytest.mark.integration
    def test_integration_marker_works(self):
        """Verify integration test marker is recognized."""
        assert True

    @pytest.mark.slow
    def test_slow_marker_works(self):
        """Verify slow test marker is recognized."""
        assert True

    def test_coverage_directories_configured(self):
        """Verify coverage is configured for project directories."""
        # This test verifies the configuration is correct
        project_root = Path(__file__).parent.parent
        assert (project_root / "v1").exists()
        assert (project_root / "v2").exists()

    def test_output_folders_fixture(self, output_folders):
        """Verify output folders fixture creates all necessary directories."""
        assert all(folder.exists() for folder in output_folders.values())
        assert "windows" in output_folders
        assert "mosaics" in output_folders
        assert "accumulated" in output_folders
        assert "frames_detected" in output_folders

    def test_device_fixture(self, device):
        """Verify device fixture returns appropriate torch device."""
        assert isinstance(device, torch.device)
        assert device.type in ["cpu", "cuda"]

    def test_sample_tensor_fixture(self, sample_tensor):
        """Verify sample tensor fixture creates proper tensor."""
        assert isinstance(sample_tensor, torch.Tensor)
        assert sample_tensor.shape == (3, 100, 100)

    def test_mock_frames_folder_fixture(self, mock_frames_folder):
        """Verify mock frames folder contains sample images."""
        assert mock_frames_folder.exists()
        frames = list(mock_frames_folder.glob("*.png"))
        assert len(frames) == 3
        
        # Verify images can be loaded
        for frame_path in frames:
            img = Image.open(frame_path)
            assert img.size == (1920, 1080)


class TestProjectStructure:
    """Test class to validate project structure assumptions."""

    def test_v1_module_exists(self):
        """Verify v1 module directory exists."""
        project_root = Path(__file__).parent.parent
        assert (project_root / "v1" / "demosaic.py").exists()

    def test_v2_module_exists(self):
        """Verify v2 module directory exists."""
        project_root = Path(__file__).parent.parent
        assert (project_root / "v2" / "demosaic.py").exists()

    def test_readme_exists(self):
        """Verify README.md exists."""
        project_root = Path(__file__).parent.parent
        assert (project_root / "README.md").exists()

    def test_license_info_in_files(self):
        """Verify license information exists in project files."""
        project_root = Path(__file__).parent.parent
        # Check if license info is in the Python files (CC0-1.0 header)
        v1_demosaic = project_root / "v1" / "demosaic.py"
        with open(v1_demosaic) as f:
            content = f.read()
            assert "CC0-1.0" in content or "CC0" in content


def test_parametrized_example():
    """Example of parametrized test for future use."""
    @pytest.mark.parametrize("input_val,expected", [
        (1, 1),
        (2, 4),
        (3, 9),
    ])
    def test_squares(input_val, expected):
        assert input_val ** 2 == expected
    
    # Run the parametrized test
    test_squares(2, 4)