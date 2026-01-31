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

    def test_write_packages_to_files_creates_index(self, tmp_path):
        """Test write_packages_to_files creates index.json.

        Requirements:
            SWR_WRITER_00013: JSON Index File Output
        """
        import json

        writer = JsonWriter()
        pkg = AutosarPackage(name="M2")
        pkg.add_class(AutosarClass("TestClass", "M2::AUTOSAR", False))

        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        # Verify index.json was created
        index_file = tmp_path / "index.json"
        assert index_file.exists()

        # Verify index structure
        with open(index_file) as f:
            index = json.load(f)

        assert "version" in index
        assert index["version"] == "1.0"
        assert "metadata" in index
        assert "packages" in index

    def test_write_package_metadata_file(self, tmp_path):
        """Test package metadata JSON file has correct structure.

        Requirements:
            SWR_WRITER_00014: JSON Package Metadata File Output
        """
        import json

        writer = JsonWriter()
        pkg = AutosarPackage(name="M2::AUTOSAR::DataTypes")
        pkg.add_class(AutosarClass("TestClass", "M2::AUTOSAR::DataTypes", False))

        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        # Verify package file was created
        package_file = tmp_path / "packages" / "M2_AUTOSAR_DataTypes.json"
        assert package_file.exists()

        # Verify package structure
        with open(package_file) as f:
            data = json.load(f)

        assert data["name"] == "M2::AUTOSAR::DataTypes"
        assert data["path"] == "M2::AUTOSAR::DataTypes"
        assert "files" in data
        assert "summary" in data
