"""Tests for utility functions."""

import pytest
from autosar_pdf2txt.utils import detect_format


class TestDetectFormat:
    """Test format detection from file extensions."""

    def test_markdown_extension(self) -> None:
        """Test .md extension detects markdown format."""
        assert detect_format("output.md") == "markdown"

    def test_markdown_long_extension(self) -> None:
        """Test .markdown extension detects markdown format."""
        assert detect_format("output.markdown") == "markdown"

    def test_json_extension(self) -> None:
        """Test .json extension detects json format."""
        assert detect_format("output.json") == "json"

    def test_unknown_extension_raises_error(self) -> None:
        """Test unknown extension raises ValueError."""
        with pytest.raises(ValueError, match="Unknown format \\.xyz"):
            detect_format("output.xyz")

    def test_no_extension_defaults_to_markdown(self) -> None:
        """Test no extension defaults to markdown."""
        assert detect_format("output") == "markdown"

    def test_uppercase_markdown_extension(self) -> None:
        """Test uppercase .MD extension detects markdown format."""
        assert detect_format("output.MD") == "markdown"

    def test_uppercase_json_extension(self) -> None:
        """Test uppercase .JSON extension detects json format."""
        assert detect_format("output.JSON") == "json"

    def test_mixed_case_markdown_extension(self) -> None:
        """Test mixed case .Md extension detects markdown format."""
        assert detect_format("output.Md") == "markdown"

    def test_mixed_case_json_extension(self) -> None:
        """Test mixed case .Json extension detects json format."""
        assert detect_format("output.Json") == "json"
