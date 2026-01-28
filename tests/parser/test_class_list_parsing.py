"""Unit tests for class list parsing (Base, Subclasses, Aggregated by).

These tests verify that Base classes and Subclasses use the same parsing algorithm
with support for multi-line and comma delimiter.

Requirements:
    SWR_PARSER_00021: Multi-Line Attribute Parsing for AutosarClass
"""

from autosar_pdf2txt.parser.class_parser import AutosarClassParser


class TestClassListParsing:
    """Test that Base and Subclass parsing use identical algorithms.

    Requirements:
        SWR_PARSER_00021: Multi-Line Attribute Parsing for AutosarClass
    """

    def test_base_and_subclass_patterns_are_identical_structure(self) -> None:
        """Verify BASE_PATTERN and SUBCLASS_PATTERN have identical structure.

        Both patterns should:
        - Start with keyword at beginning of line
        - Capture everything after the keyword
        - Use the same regex structure

        Requirements:
            SWR_PARSER_00021: Multi-Line Attribute Parsing for AutosarClass
        """
        parser = AutosarClassParser()

        # Check patterns exist
        assert parser.BASE_PATTERN is not None
        assert parser.SUBCLASS_PATTERN is not None

        # Both should match lines starting with their respective keywords
        base_line = "Base Class1, Class2, Class3"
        subclass_line = "Subclasses Sub1, Sub2, Sub3"

        base_match = parser.BASE_PATTERN.match(base_line)
        subclass_match = parser.SUBCLASS_PATTERN.match(subclass_line)

        assert base_match is not None, "BASE_PATTERN should match base line"
        assert subclass_match is not None, "SUBCLASS_PATTERN should match subclass line"

        # Both should capture the comma-separated list
        assert base_match.group(1) == "Class1, Class2, Class3"
        assert subclass_match.group(1) == "Sub1, Sub2, Sub3"

    def test_parse_class_list_line_handles_comma_delimiter(self) -> None:
        """Verify _parse_class_list_line correctly splits by comma.

        This should work identically for both Base and Subclasses.

        Requirements:
            SWR_PARSER_00021: Multi-Line Attribute Parsing for AutosarClass
        """
        parser = AutosarClassParser()

        # Test with Base pattern
        base_line = "Base Class1, Class2, Class3"
        base_match = parser.BASE_PATTERN.match(base_line)
        items, last_item, last_item_complete = parser._parse_class_list_line(base_match)

        assert items == ["Class1", "Class2", "Class3"]
        assert last_item == "Class3"
        assert last_item_complete is False  # Line doesn't end with comma

        # Test with Subclass pattern
        subclass_line = "Subclasses Sub1, Sub2, Sub3"
        subclass_match = parser.SUBCLASS_PATTERN.match(subclass_line)
        items, last_item, last_item_complete = parser._parse_class_list_line(subclass_match)

        assert items == ["Sub1", "Sub2", "Sub3"]
        assert last_item == "Sub3"
        assert last_item_complete is False  # Line doesn't end with comma

    def test_parse_class_list_line_handles_trailing_comma(self) -> None:
        """Verify trailing comma indicates complete item.

        Requirements:
            SWR_PARSER_00021: Multi-Line Attribute Parsing for AutosarClass
        """
        parser = AutosarClassParser()

        # Base with trailing comma
        base_line = "Base Class1, Class2,"
        base_match = parser.BASE_PATTERN.match(base_line)
        items, last_item, last_item_complete = parser._parse_class_list_line(base_match)

        assert items == ["Class1", "Class2"]
        assert last_item == "Class2"
        assert last_item_complete is True  # Line ends with comma

        # Subclass with trailing comma
        subclass_line = "Subclasses Sub1, Sub2,"
        subclass_match = parser.SUBCLASS_PATTERN.match(subclass_line)
        items, last_item, last_item_complete = parser._parse_class_list_line(subclass_match)

        assert items == ["Sub1", "Sub2"]
        assert last_item == "Sub2"
        assert last_item_complete is True  # Line ends with comma

    def test_handle_class_list_continuation_handles_multi_line(self) -> None:
        """Verify multi-line continuation works for both Base and Subclasses.

        When last_item_complete=False, the first item on the continuation line
        is concatenated with the last item (for split class names).

        Requirements:
            SWR_PARSER_00021: Multi-Line Attribute Parsing for AutosarClass
        """
        parser = AutosarClassParser()

        # Test Base continuation with incomplete last item (concatenation)
        initial_items = ["Class1", "Class2"]
        continuation_line = "Class3, Class4"

        (items, last_item), complete = parser._handle_class_list_continuation(
            continuation_line, initial_items, "Class2", last_item_complete=False
        )

        # "Class2" + "Class3" because last_item_complete=False
        assert items == ["Class1", "Class2Class3", "Class4"]
        assert last_item == "Class4"
        assert complete is False

        # Test Subclass continuation (identical algorithm)
        initial_items = ["Sub1", "Sub2"]
        continuation_line = "Sub3, Sub4"

        (items, last_item), complete = parser._handle_class_list_continuation(
            continuation_line, initial_items, "Sub2", last_item_complete=False
        )

        # "Sub2" + "Sub3" because last_item_complete=False
        assert items == ["Sub1", "Sub2Sub3", "Sub4"]
        assert last_item == "Sub4"
        assert complete is False

    def test_handle_class_list_continuation_with_trailing_comma(self) -> None:
        """Verify multi-line with trailing comma indicates more items coming.

        When last_item_complete=True (trailing comma), items are NOT concatenated.

        Requirements:
            SWR_PARSER_00021: Multi-Line Attribute Parsing for AutosarClass
        """
        parser = AutosarClassParser()

        # Base with trailing comma (complete last item, no concatenation)
        initial_items = ["Class1"]
        continuation_line = "Class2, Class3,"

        (items, last_item), complete = parser._handle_class_list_continuation(
            continuation_line, initial_items, "Class1", last_item_complete=True
        )

        # No concatenation because last_item_complete=True
        assert items == ["Class1", "Class2", "Class3"]
        assert last_item == "Class3"
        assert complete is True  # Trailing comma indicates more coming

        # Subclass with trailing comma (identical algorithm)
        initial_items = ["Sub1"]
        continuation_line = "Sub2, Sub3,"

        (items, last_item), complete = parser._handle_class_list_continuation(
            continuation_line, initial_items, "Sub1", last_item_complete=True
        )

        # No concatenation because last_item_complete=True
        assert items == ["Sub1", "Sub2", "Sub3"]
        assert last_item == "Sub3"
        assert complete is True  # Trailing comma indicates more coming

    def test_finalize_pending_class_lists_handles_both_sections(self) -> None:
        """Verify _finalize_pending_class_lists handles both base_classes and subclasses.

        Requirements:
            SWR_PARSER_00021: Multi-Line Attribute Parsing for AutosarClass
        """
        from autosar_pdf2txt.models import AutosarClass

        parser = AutosarClassParser()
        test_class = AutosarClass(
            name="TestClass",
            is_abstract=False,
            atp_type=None,
            attributes={},
            bases=[],
            package="TestPackage"
        )

        # Set up pending lists for both base_classes and subclasses
        parser._pending_class_lists = {
            "base_classes": (["Base1", "Base2"], "Base2", True),
            "subclasses": (["Sub1", "Sub2"], "Sub2", True),
            "aggregated_by": (["Agg1"], "Agg1", True),
        }

        # Finalize should add all to the model
        parser._finalize_pending_class_lists(test_class)

        assert test_class.bases == ["Base1", "Base2"]
        assert test_class.subclasses == ["Sub1", "Sub2"]
        assert test_class.aggregated_by == ["Agg1"]

        # Lists should be reset
        assert parser._pending_class_lists["base_classes"] == (None, None, True)
        assert parser._pending_class_lists["subclasses"] == (None, None, True)
        assert parser._pending_class_lists["aggregated_by"] == (None, None, True)

    def test_finalize_pending_class_lists_splits_atp_interfaces(self) -> None:
        """Verify base classes starting with 'Atp' are moved to implements field.

        Requirements:
            SWR_PARSER_00021: Multi-Line Attribute Parsing for AutosarClass
        """
        from autosar_pdf2txt.models import AutosarClass

        parser = AutosarClassParser()
        test_class = AutosarClass(
            name="TestClass",
            is_abstract=False,
            atp_type=None,
            attributes={},
            bases=[],
            package="TestPackage"
        )

        # Set up pending lists with mix of Atp and non-Atp bases
        parser._pending_class_lists = {
            "base_classes": (["AtpInterface", "RegularBase", "AtpVariation", "AnotherBase"], "AnotherBase", True),
        }

        # Finalize should split Atp interfaces from regular bases
        parser._finalize_pending_class_lists(test_class)

        # Atp interfaces should be in implements field
        assert test_class.implements == ["AtpInterface", "AtpVariation"]
        # Regular bases should be in bases field
        assert test_class.bases == ["RegularBase", "AnotherBase"]

    def test_finalize_pending_class_lists_with_only_atp_interfaces(self) -> None:
        """Verify when all base classes start with 'Atp', bases is empty.

        Requirements:
            SWR_PARSER_00021: Multi-Line Attribute Parsing for AutosarClass
        """
        from autosar_pdf2txt.models import AutosarClass

        parser = AutosarClassParser()
        test_class = AutosarClass(
            name="TestClass",
            is_abstract=False,
            atp_type=None,
            attributes={},
            bases=[],
            package="TestPackage"
        )

        # Set up pending lists with only Atp interfaces
        parser._pending_class_lists = {
            "base_classes": (["AtpInterface1", "AtpInterface2"], "AtpInterface2", True),
        }

        # Finalize should move all to implements
        parser._finalize_pending_class_lists(test_class)

        # All should be in implements field
        assert test_class.implements == ["AtpInterface1", "AtpInterface2"]
        # bases should be empty
        assert test_class.bases == []

    def test_finalize_pending_class_lists_with_only_regular_bases(self) -> None:
        """Verify when no base classes start with 'Atp', implements is empty.

        Requirements:
            SWR_PARSER_00021: Multi-Line Attribute Parsing for AutosarClass
        """
        from autosar_pdf2txt.models import AutosarClass

        parser = AutosarClassParser()
        test_class = AutosarClass(
            name="TestClass",
            is_abstract=False,
            atp_type=None,
            attributes={},
            bases=[],
            package="TestPackage"
        )

        # Set up pending lists with only regular bases
        parser._pending_class_lists = {
            "base_classes": (["RegularBase1", "RegularBase2"], "RegularBase2", True),
        }

        # Finalize should keep all in bases
        parser._finalize_pending_class_lists(test_class)

        # implements should be empty
        assert test_class.implements == []
        # All should be in bases field
        assert test_class.bases == ["RegularBase1", "RegularBase2"]
