"""Tests for JsonWriter class."""

import json
from pathlib import Path
from unittest.mock import patch

import pytest
from autosar_pdf2txt.writer import JsonWriter
from autosar_pdf2txt.models import AutosarPackage, AutosarClass


class TestJsonWriter:
    """Test cases for JsonWriter class.

    Requirements:
        SWR_WRITER_00010: JSON Writer Initialization
    """

    def test_init(self):
        """Test JsonWriter initialization.

        Requirements:
            SWR_WRITER_00010: JSON Writer Initialization
        """
        writer = JsonWriter()
        assert writer is not None

    def test_write_packages_to_files_creates_directories(self, tmp_path):
        """Test write_packages_to_files creates package directories.

        Requirements:
            SWR_WRITER_00011: JSON Directory Structure Creation
        """
        writer = JsonWriter()
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass("TestClass", "TestPackage", False))

        # Write to temporary directory
        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        # Verify packages directory was created
        packages_dir = tmp_path / "packages"
        assert packages_dir.exists()
        assert packages_dir.is_dir()
