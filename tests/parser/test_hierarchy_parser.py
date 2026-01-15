"""Tests for hierarchy parser.

Test coverage for hierarchy_parser.py targeting 100%.
"""


from autosar_pdf2txt.parser.hierarchy_parser import HierarchyParser, parse_hierarchy


class TestHierarchyParserInit:
    """Tests for HierarchyParser initialization."""

    def test_init(self) -> None:
        """Test initialization."""
        text = "* Package\n    * Class"
        parser = HierarchyParser(text)
        assert parser.text == text
        assert parser.lines == ["* Package", "    * Class"]


class TestParseLine:
    """Tests for _parse_line method."""

    def test_parse_line_valid_hierarchy(self) -> None:
        """Test parsing valid hierarchy line."""
        parser = HierarchyParser("* Package")
        level, name, is_abstract = parser._parse_line("* Package")
        assert level == 0
        assert name == "Package"
        assert is_abstract is False

    def test_parse_line_with_leading_spaces(self) -> None:
        """Test parsing line with leading spaces."""
        parser = HierarchyParser("* Package")
        level, name, is_abstract = parser._parse_line("  * SubPackage")
        assert level == 2
        assert name == "SubPackage"

    def test_parse_line_with_abstract(self) -> None:
        """Test parsing line with abstract marker."""
        parser = HierarchyParser("* Package")
        level, name, is_abstract = parser._parse_line("* ClassName (abstract)")
        assert name == "ClassName"
        assert is_abstract is True

    def test_parse_line_abstract_with_spaces(self) -> None:
        """Test parsing abstract marker with spaces before it."""
        parser = HierarchyParser("* Package")
        level, name, is_abstract = parser._parse_line("    * ClassName (abstract)")
        assert name == "ClassName"
        assert is_abstract is True
        assert level == 4

    def test_parse_line_no_asterisk(self) -> None:
        """Test parsing line without asterisk."""
        parser = HierarchyParser("* Package")
        level, name, is_abstract = parser._parse_line("Just text")
        assert level == -1
        assert name == ""

    def test_parse_line_empty_content_after_asterisk(self) -> None:
        """Test parsing line with empty content after asterisk."""
        parser = HierarchyParser("* Package")
        level, name, is_abstract = parser._parse_line("*     ")
        assert level == 0
        assert name == ""

    def test_parse_line_empty_line(self) -> None:
        """Test parsing empty line."""
        parser = HierarchyParser("")
        level, name, is_abstract = parser._parse_line("")
        assert level == -1


class TestIsPackageLine:
    """Tests for _is_package_line method."""

    def test_is_package_line_with_children(self) -> None:
        """Test line with children is identified as package."""
        parser = HierarchyParser("")
        lines = [(0, "Package", False), (2, "Class", False)]
        is_pkg = parser._is_package_line(lines, 0)
        assert is_pkg is True

    def test_is_package_line_last_line(self) -> None:
        """Test last line is not identified as package."""
        parser = HierarchyParser("")
        lines = [(0, "Class", False)]
        is_pkg = parser._is_package_line(lines, 0)
        assert is_pkg is False

    def test_is_package_line_no_children(self) -> None:
        """Test line without children is not identified as package."""
        parser = HierarchyParser("")
        lines = [(0, "Package", False), (0, "Sibling", False)]
        is_pkg = parser._is_package_line(lines, 0)
        assert is_pkg is False


class TestParseHierarchy:
    """Tests for _parse_hierarchy method."""

    def test_parse_empty_text(self) -> None:
        """Test parsing empty text."""
        parser = HierarchyParser("")
        result = parser._parse_hierarchy()
        assert result == []

    def test_parse_no_valid_lines(self) -> None:
        """Test parsing text with no valid lines."""
        parser = HierarchyParser("Just random text\nWithout asterisks")
        result = parser._parse_hierarchy()
        assert result == []

    def test_parse_single_package(self) -> None:
        """Test parsing single package."""
        text = "* Package"
        parser = HierarchyParser(text)
        result = parser.parse()
        assert len(result) == 1
        assert result[0].name == "Package"

    def test_parse_package_with_class(self) -> None:
        """Test parsing package with class."""
        text = """* Package
    * Class"""
        parser = HierarchyParser(text)
        packages = parser._parse_hierarchy()
        assert len(packages) == 1
        assert packages[0].name == "Package"
        assert len(packages[0].classes) == 1
        assert packages[0].classes[0].name == "Class"

    def test_parse_nested_packages(self) -> None:
        """Test parsing nested packages."""
        text = """* RootPackage
  * SubPackage
      * Class"""
        parser = HierarchyParser(text)
        packages = parser._parse_hierarchy()
        assert len(packages) == 1
        assert packages[0].name == "RootPackage"
        assert len(packages[0].subpackages) == 1
        assert packages[0].subpackages[0].name == "SubPackage"
        assert len(packages[0].subpackages[0].classes) == 1

    def test_parse_multiple_top_level_packages(self) -> None:
        """Test parsing multiple top-level packages."""
        text = """* Package1
    * Class1
* Package2
    * Class2"""
        parser = HierarchyParser(text)
        packages = parser._parse_hierarchy()
        assert len(packages) == 2
        assert packages[0].name == "Package1"
        assert packages[1].name == "Package2"

    def test_parse_abstract_class(self) -> None:
        """Test parsing abstract class."""
        text = """* Package
    * ConcreteClass
    * AbstractClass (abstract)"""
        parser = HierarchyParser(text)
        packages = parser._parse_hierarchy()
        assert len(packages[0].classes) == 2
        assert packages[0].classes[0].is_abstract is False
        assert packages[0].classes[1].is_abstract is True

    def test_parse_duplicate_detection(self) -> None:
        """Test duplicate detection."""
        text = """* Package
    * MyClass
    * MyClass"""
        parser = HierarchyParser(text)
        packages = parser._parse_hierarchy()
        # Only first class should be added
        assert len(packages[0].classes) == 1
        assert packages[0].classes[0].name == "MyClass"

    def test_parse_complex_hierarchy(self) -> None:
        """Test parsing complex hierarchy."""
        text = """* AUTOSARTemplates
  * AutosarTopLevelStructure
      * AUTOSAR
  * BswModuleTemplate
    * BswBehavior
        * BswInternalBehavior
        * ExecutableEntity (abstract)
        * BswModuleEntity (abstract)"""
        parser = HierarchyParser(text)
        packages = parser._parse_hierarchy()

        assert len(packages) == 1
        root = packages[0]
        assert root.name == "AUTOSARTemplates"
        assert len(root.subpackages) == 2

        subpkg1 = root.subpackages[0]
        assert subpkg1.name == "AutosarTopLevelStructure"
        assert len(subpkg1.classes) == 1
        assert subpkg1.classes[0].name == "AUTOSAR"

        subpkg2 = root.subpackages[1]
        assert subpkg2.name == "BswModuleTemplate"
        assert len(subpkg2.subpackages) == 1

        behavior = subpkg2.subpackages[0]
        assert behavior.name == "BswBehavior"
        assert len(behavior.classes) == 3
        assert behavior.classes[0].name == "BswInternalBehavior"
        assert behavior.classes[1].name == "ExecutableEntity"
        assert behavior.classes[1].is_abstract is True
        assert behavior.classes[2].name == "BswModuleEntity"
        assert behavior.classes[2].is_abstract is True

    def test_parse_with_blank_lines(self) -> None:
        """Test parsing with blank lines."""
        text = """* Package

    * Class

    * AnotherClass"""
        parser = HierarchyParser(text)
        packages = parser._parse_hierarchy()
        assert len(packages) == 1
        assert len(packages[0].classes) == 2


class TestParse:
    """Tests for parse method."""

    def test_parse_method(self) -> None:
        """Test parse method."""
        text = "* Package\n    * Class"
        parser = HierarchyParser(text)
        packages = parser.parse()
        assert len(packages) == 1


class TestFunctionalInterface:
    """Tests for functional interface."""

    def test_parse_hierarchy_function(self) -> None:
        """Test parse_hierarchy function."""
        text = """* Package
    * Class1
    * Class2 (abstract)"""
        packages = parse_hierarchy(text)
        assert len(packages) == 1
        assert packages[0].name == "Package"
        assert len(packages[0].classes) == 2
        assert packages[0].classes[1].is_abstract is True
