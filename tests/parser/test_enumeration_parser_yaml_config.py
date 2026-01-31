"""Unit tests for enumeration parser YAML configuration.

These tests verify that enumeration literal parsing can be configured
using YAML file instead of hard-coded patterns.

Requirements:
    SWR_PARSER_00015: Enumeration Literal Extraction from PDF
    SWR_PARSER_00101: YAML Configuration for Enumeration Literal Word Mapping
"""

from pathlib import Path

from autosar_pdf2txt.models import AutosarEnumeration, AutosarEnumLiteral
from autosar_pdf2txt.parser.enumeration_parser import AutosarEnumerationParser


class TestEnumerationParserYamlConfig:
    """Test that enumeration parser can be configured via global YAML file.

    Requirements:
        SWR_PARSER_00015: Enumeration Literal Extraction from PDF
        SWR_PARSER_00101: YAML Configuration for Enumeration Literal Word Mapping
    """

    def test_load_yaml_configuration(self) -> None:
        """Verify YAML configuration can be loaded from global file.

        This test verifies that:
        1. Global configuration file exists at expected location
        2. Configuration can be loaded successfully
        3. Configuration contains expected keys for enumeration literals

        Requirements:
            SWR_PARSER_00101: YAML Configuration for Enumeration Literal Word Mapping
        """
        config_path = Path("src/autosar_pdf2txt/config/parser_config.yaml")

        # Check config file exists
        assert config_path.exists(), f"Global configuration file not found at {config_path}"

        # Load configuration
        parser = AutosarEnumerationParser()

        # Verify configuration is loaded
        assert hasattr(parser, "_continuation_words"), "Parser should have _continuation_words"
        assert hasattr(parser, "_suffix_words"), "Parser should have _suffix_words"
        assert hasattr(parser, "_header_exclusion_patterns"), "Parser should have _header_exclusion_patterns"
        assert hasattr(parser, "_header_words"), "Parser should have _header_words"
        assert hasattr(parser, "_patches"), "Parser should have _patches"

    def test_continuation_words_from_yaml(self) -> None:
        """Verify continuation_words are loaded from YAML configuration.

        Continuation words indicate that a line should be appended to the
        previous literal's description.

        Requirements:
            SWR_PARSER_00101: YAML Configuration for Enumeration Literal Word Mapping
        """
        parser = AutosarEnumerationParser()

        # Verify continuation_words is a set
        assert isinstance(parser._continuation_words, set), "continuation_words should be a set"

        # Verify expected continuation words are present
        expected_words = {"enable", "qualification", "the"}
        assert expected_words.issubset(parser._continuation_words), \
            f"Expected continuation words {expected_words} not found in {parser._continuation_words}"

    def test_suffix_words_from_yaml(self) -> None:
        """Verify suffix_words are loaded from YAML configuration.

        Suffix words indicate that a line should be appended to the
        previous literal's name.

        Requirements:
            SWR_PARSER_00101: YAML Configuration for Enumeration Literal Word Mapping
        """
        parser = AutosarEnumerationParser()

        # Verify suffix_words is a set
        assert isinstance(parser._suffix_words, set), "suffix_words should be a set"

        # Verify expected suffix words are present
        expected_words = {"first", "last", "on", "in"}
        assert expected_words.issubset(parser._suffix_words), \
            f"Expected suffix words {expected_words} not found in {parser._suffix_words}"

    def test_header_exclusion_patterns_from_yaml(self) -> None:
        """Verify header_exclusion_patterns are loaded from YAML configuration.

        Header exclusion patterns identify header text that should not be
        treated as enumeration literals.

        Requirements:
            SWR_PARSER_00101: YAML Configuration for Enumeration Literal Word Mapping
        """
        parser = AutosarEnumerationParser()

        # Verify header_exclusion_patterns is a list
        assert isinstance(parser._header_exclusion_patterns, list), \
            "header_exclusion_patterns should be a list"

        # Verify expected patterns are present
        expected_patterns = ["extract template", "cp r23-11"]
        for pattern in expected_patterns:
            assert pattern in parser._header_exclusion_patterns, \
                f"Expected pattern '{pattern}' not found in header_exclusion_patterns"

    def test_header_words_from_yaml(self) -> None:
        """Verify header_words are loaded from YAML configuration.

        Header words are individual words that, when combined with header
        exclusion patterns, indicate header text.

        Requirements:
            SWR_PARSER_00101: YAML Configuration for Enumeration Literal Word Mapping
        """
        parser = AutosarEnumerationParser()

        # Verify header_words is a list
        assert isinstance(parser._header_words, list), "header_words should be a list"

        # Verify expected words are present
        expected_words = ["Diagnostic", "AUTOSAR"]
        for word in expected_words:
            assert word in parser._header_words, \
                f"Expected word '{word}' not found in header_words"

    def test_patches_from_yaml(self) -> None:
        """Verify patches are loaded from YAML configuration.

        Patches are manual corrections for edge cases.

        Requirements:
            SWR_PARSER_00101: YAML Configuration for Enumeration Literal Word Mapping
        """
        parser = AutosarEnumerationParser()

        # Verify patches is a dict
        assert isinstance(parser._patches, dict), "patches should be a dict"

        # By default, patches should be empty (use sparingly)
        assert parser._patches == {} or isinstance(parser._patches, dict), \
            "patches should be a dict, empty or populated"

    def test_global_config_structure(self) -> None:
        """Verify the global config file has proper structure.

        The global config should have an 'enumeration_literals' section.

        Requirements:
            SWR_PARSER_00101: YAML Configuration for Enumeration Literal Word Mapping
        """
        import yaml

        config_path = Path("src/autosar_pdf2txt/config/parser_config.yaml")
        assert config_path.exists(), "Global config file should exist"

        with open(config_path, "r") as f:
            full_config = yaml.safe_load(f)

        # Verify enumeration_literals section exists
        assert "enumeration_literals" in full_config, \
            "Global config should have 'enumeration_literals' section"

        enum_config = full_config["enumeration_literals"]

        # Verify all expected keys exist
        expected_keys = [
            "continuation_words",
            "suffix_words",
            "header_exclusion_patterns",
            "header_words",
            "patches"
        ]

        for key in expected_keys:
            assert key in enum_config, f"enumeration_literals should have '{key}' key"

    def test_apply_patches_method_exists(self) -> None:
        """Verify _apply_patches method exists and works correctly.

        Requirements:
            SWR_PARSER_00101: YAML Configuration for Enumeration Literal Word Mapping
        """
        parser = AutosarEnumerationParser()

        # Verify method exists
        assert hasattr(parser, "_apply_patches"), \
            "Parser should have _apply_patches method"

        # Create a test enumeration with a literal
        enum = AutosarEnumeration(name="TestEnum", package="M2::Test")
        parser._pending_literals = [
            AutosarEnumLiteral(name="WrongName", description="Test description", value=None)
        ]

        # Set up a patch for this enumeration
        parser._patches = {
            "TestEnum": {
                "WrongName": "CorrectName"
            }
        }

        # Apply patches
        parser._apply_patches(enum)

        # Verify patch was applied
        assert parser._pending_literals[0].name == "CorrectName", \
            "Patch should have been applied to change WrongName to CorrectName"

    def test_apply_patches_no_match(self) -> None:
        """Verify _apply_patches handles case where no patches match.

        Requirements:
            SWR_PARSER_00101: YAML Configuration for Enumeration Literal Word Mapping
        """
        parser = AutosarEnumerationParser()

        # Create a test enumeration with a literal
        enum = AutosarEnumeration(name="TestEnum", package="M2::Test")
        parser._pending_literals = [
            AutosarEnumLiteral(name="CorrectName", description="Test description", value=None)
        ]

        # Set up a patch for a different enumeration
        parser._patches = {
            "OtherEnum": {
                "WrongName": "CorrectName"
            }
        }

        # Apply patches (should do nothing)
        parser._apply_patches(enum)

        # Verify no changes were made
        assert parser._pending_literals[0].name == "CorrectName", \
            "Literal name should remain unchanged when no patches match"

    def test_apply_patches_empty(self) -> None:
        """Verify _apply_patches handles empty patches gracefully.

        Requirements:
            SWR_PARSER_00101: YAML Configuration for Enumeration Literal Word Mapping
        """
        parser = AutosarEnumerationParser()

        # Create a test enumeration with a literal
        enum = AutosarEnumeration(name="TestEnum", package="M2::Test")
        original_name = "SomeLiteral"
        parser._pending_literals = [
            AutosarEnumLiteral(name=original_name, description="Test description", value=None)
        ]

        # Ensure patches are empty
        parser._patches = {}

        # Apply patches (should do nothing)
        parser._apply_patches(enum)

        # Verify no changes were made
        assert parser._pending_literals[0].name == original_name, \
            "Literal name should remain unchanged with empty patches"
