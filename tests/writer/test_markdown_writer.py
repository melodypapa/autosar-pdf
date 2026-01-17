"""Tests for markdown writer.

Test coverage for markdown_writer.py targeting 100%.
"""

from autosar_pdf2txt.models import AutosarClass, AutosarPackage
from autosar_pdf2txt.writer.markdown_writer import MarkdownWriter


class TestMarkdownWriter:
    """Tests for MarkdownWriter class.

    Requirements:
        SWR_WRITER_00001: Markdown Writer Initialization
        SWR_WRITER_00002: Markdown Package Hierarchy Output
        SWR_WRITER_00003: Markdown Class Output Format
        SWR_WRITER_00004: Bulk Package Writing
    """

    def test_init_default(self) -> None:
        """Test initialization with default settings.

        Requirements:
            SWR_WRITER_00001: Markdown Writer Initialization
        """
        writer = MarkdownWriter()
        # No deduplicate attribute or tracking sets anymore
        assert writer is not None

    def test_write_single_empty_package(self) -> None:
        """Test writing a single empty package.

        Requirements:
            SWR_WRITER_00002: Markdown Package Hierarchy Output
            SWR_WRITER_00004: Bulk Package Writing
        """
        pkg = AutosarPackage(name="TestPackage")
        writer = MarkdownWriter()
        result = writer.write_packages([pkg])
        expected = "* TestPackage\n"
        assert result == expected

    def test_write_package_with_class(self) -> None:
        """Test writing a package with a class.

        Requirements:
            SWR_WRITER_00002: Markdown Package Hierarchy Output
            SWR_WRITER_00003: Markdown Class Output Format
        """
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="MyClass", is_abstract=False))
        writer = MarkdownWriter()
        result = writer.write_packages([pkg])
        expected = "* TestPackage\n  * MyClass\n"
        assert result == expected

    def test_write_package_with_abstract_class(self) -> None:
        """Test writing a package with an abstract class.

        Requirements:
            SWR_WRITER_00002: Markdown Package Hierarchy Output
            SWR_WRITER_00003: Markdown Class Output Format
        """
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="AbstractClass", is_abstract=True))
        writer = MarkdownWriter()
        result = writer.write_packages([pkg])
        expected = "* TestPackage\n  * AbstractClass (abstract)\n"
        assert result == expected

    def test_write_package_with_multiple_classes(self) -> None:
        """Test writing a package with multiple classes.

        Requirements:
            SWR_WRITER_00002: Markdown Package Hierarchy Output
            SWR_WRITER_00003: Markdown Class Output Format
        """
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="Class1", is_abstract=False))
        pkg.add_class(AutosarClass(name="Class2", is_abstract=True))
        pkg.add_class(AutosarClass(name="Class3", is_abstract=False))
        writer = MarkdownWriter()
        result = writer.write_packages([pkg])
        expected = (
            "* TestPackage\n"
            "  * Class1\n"
            "  * Class2 (abstract)\n"
            "  * Class3\n"
        )
        assert result == expected

    def test_write_nested_packages(self) -> None:
        """Test writing nested packages.

        Requirements:
            SWR_WRITER_00002: Markdown Package Hierarchy Output
        """
        root = AutosarPackage(name="RootPackage")
        child = AutosarPackage(name="ChildPackage")
        child.add_class(AutosarClass(name="GrandchildClass", is_abstract=False))
        root.add_subpackage(child)
        writer = MarkdownWriter()
        result = writer.write_packages([root])
        expected = (
            "* RootPackage\n"
            "  * ChildPackage\n"
            "    * GrandchildClass\n"
        )
        assert result == expected

    def test_write_complex_hierarchy(self) -> None:
        """Test writing complex nested hierarchy.

        Requirements:
            SWR_WRITER_00002: Markdown Package Hierarchy Output
            SWR_WRITER_00003: Markdown Class Output Format

        Test structure:
            * AUTOSARTemplates
              * BswModuleTemplate
                * BswBehavior
                  * BswInternalBehavior
                  * ExecutableEntity (abstract)
        """
        root = AutosarPackage(name="AUTOSARTemplates")
        bsw = AutosarPackage(name="BswModuleTemplate")
        behavior = AutosarPackage(name="BswBehavior")
        behavior.add_class(AutosarClass(name="BswInternalBehavior", is_abstract=False))
        behavior.add_class(AutosarClass(name="ExecutableEntity", is_abstract=True))
        bsw.add_subpackage(behavior)
        root.add_subpackage(bsw)

        writer = MarkdownWriter()
        result = writer.write_packages([root])
        expected = (
            "* AUTOSARTemplates\n"
            "  * BswModuleTemplate\n"
            "    * BswBehavior\n"
            "      * BswInternalBehavior\n"
            "      * ExecutableEntity (abstract)\n"
        )
        assert result == expected

    def test_write_multiple_top_level_packages(self) -> None:
        """Test writing multiple top-level packages.

        Requirements:
            SWR_WRITER_00002: Markdown Package Hierarchy Output
            SWR_WRITER_00004: Bulk Package Writing
        """
        pkg1 = AutosarPackage(name="Package1")
        pkg1.add_class(AutosarClass(name="Class1", is_abstract=False))
        pkg2 = AutosarPackage(name="Package2")
        pkg2.add_class(AutosarClass(name="Class2", is_abstract=True))
        writer = MarkdownWriter()
        result = writer.write_packages([pkg1, pkg2])
        expected = (
            "* Package1\n"
            "  * Class1\n"
            "* Package2\n"
            "  * Class2 (abstract)\n"
        )
        assert result == expected

    def test_write_deeply_nested_hierarchy(self) -> None:
        """Test writing deeply nested package structure.

        Requirements:
            SWR_WRITER_00002: Markdown Package Hierarchy Output
        """
        level1 = AutosarPackage(name="Level1")
        level2 = AutosarPackage(name="Level2")
        level3 = AutosarPackage(name="Level3")
        level3.add_class(AutosarClass(name="DeepClass", is_abstract=False))
        level2.add_subpackage(level3)
        level1.add_subpackage(level2)
        writer = MarkdownWriter()
        result = writer.write_packages([level1])
        expected = (
            "* Level1\n"
            "  * Level2\n"
            "    * Level3\n"
            "      * DeepClass\n"
        )
        assert result == expected

    def test_write_empty_package_list(self) -> None:
        """Test writing an empty package list.

        Requirements:
            SWR_WRITER_00004: Bulk Package Writing
        """
        writer = MarkdownWriter()
        result = writer.write_packages([])
        expected = ""
        assert result == expected

    def test_write_package_with_both_classes_and_subpackages(self) -> None:
        """Test writing package with both classes and subpackages.

        Requirements:
            SWR_WRITER_00002: Markdown Package Hierarchy Output
            SWR_WRITER_00003: Markdown Class Output Format
        """
        pkg = AutosarPackage(name="ParentPackage")
        pkg.add_class(AutosarClass(name="DirectClass", is_abstract=False))
        subpkg = AutosarPackage(name="ChildPackage")
        subpkg.add_class(AutosarClass(name="ChildClass", is_abstract=True))
        pkg.add_subpackage(subpkg)
        writer = MarkdownWriter()
        result = writer.write_packages([pkg])
        expected = (
            "* ParentPackage\n"
            "  * DirectClass\n"
            "  * ChildPackage\n"
            "    * ChildClass (abstract)\n"
        )
        assert result == expected

    def test_multiple_writes_same_structure(self) -> None:
        """Test that multiple writes of the same structure produce identical output.

        Requirements:
            SWR_WRITER_00002: Markdown Package Hierarchy Output
            SWR_WRITER_00003: Markdown Class Output Format
        """
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="MyClass", is_abstract=False))
        writer = MarkdownWriter()

        # First write
        result1 = writer.write_packages([pkg])
        expected = "* TestPackage\n  * MyClass\n"
        assert result1 == expected

        # Second write - should produce the same output (no writer-level deduplication)
        result2 = writer.write_packages([pkg])
        assert result2 == expected

    def test_model_level_duplicate_prevention(self) -> None:
        """Test that model-level duplicate prevention works with writer.

        Requirements:
            SWR_MODEL_00006: Add Class to Package
            SWR_WRITER_00002: Markdown Package Hierarchy Output
            SWR_WRITER_00003: Markdown Class Output Format
        """
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="MyClass", is_abstract=False))

        # Attempting to add duplicate class should raise ValueError
        try:
            pkg.add_class(AutosarClass(name="MyClass", is_abstract=False))
            assert False, "Expected ValueError for duplicate class"
        except ValueError as e:
            assert "already exists" in str(e)

        # Writer should only output the first class
        writer = MarkdownWriter()
        result = writer.write_packages([pkg])
        expected = "* TestPackage\n  * MyClass\n"
        assert result == expected

    def test_write_multiple_packages_same_name_different_content(self) -> None:
        """Test writing multiple packages with same name but different content.

        Requirements:
            SWR_WRITER_00002: Markdown Package Hierarchy Output
            SWR_WRITER_00004: Bulk Package Writing
        """
        pkg1 = AutosarPackage(name="TestPackage")
        pkg1.add_class(AutosarClass(name="Class1", is_abstract=False))

        pkg2 = AutosarPackage(name="TestPackage")
        pkg2.add_class(AutosarClass(name="Class2", is_abstract=False))

        writer = MarkdownWriter()
        result = writer.write_packages([pkg1, pkg2])
        # Both packages should be written (no writer-level deduplication)
        expected = (
            "* TestPackage\n"
            "  * Class1\n"
            "* TestPackage\n"
            "  * Class2\n"
        )
        assert result == expected

    def test_nested_same_class_names_different_packages(self) -> None:
        """Test that same class names in different packages are both written.

        Requirements:
            SWR_MODEL_00006: Add Class to Package
            SWR_WRITER_00002: Markdown Package Hierarchy Output
            SWR_WRITER_00003: Markdown Class Output Format
        """
        # Create structure where same class name appears in different packages
        pkg1 = AutosarPackage(name="Package1")
        pkg1.add_class(AutosarClass(name="CommonClass", is_abstract=False))

        pkg2 = AutosarPackage(name="Package2")
        pkg2.add_class(AutosarClass(name="CommonClass", is_abstract=False))

        root = AutosarPackage(name="Root")
        root.add_subpackage(pkg1)
        root.add_subpackage(pkg2)

        writer = MarkdownWriter()
        result = writer.write_packages([root])
        # Both CommonClass instances should be written (different parents)
        assert "CommonClass" in result
        assert result.count("* CommonClass") == 2
