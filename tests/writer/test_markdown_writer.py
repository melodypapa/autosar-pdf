"""Tests for markdown writer.

Test coverage for markdown_writer.py targeting 100%.
"""

from autosar_pdf2txt.models import AutosarClass, AutosarPackage
from autosar_pdf2txt.writer.markdown_writer import MarkdownWriter, write_markdown


class TestMarkdownWriter:
    """Tests for MarkdownWriter class."""

    def test_init_default(self) -> None:
        """Test initialization with default settings."""
        writer = MarkdownWriter()
        assert writer.deduplicate is True
        assert writer._seen_packages == set()
        assert writer._seen_classes == set()

    def test_init_no_deduplication(self) -> None:
        """Test initialization with deduplication disabled."""
        writer = MarkdownWriter(deduplicate=False)
        assert writer.deduplicate is False

    def test_write_single_empty_package(self) -> None:
        """Test writing a single empty package."""
        pkg = AutosarPackage(name="TestPackage")
        writer = MarkdownWriter()
        result = writer.write_packages([pkg])
        expected = "* TestPackage\n"
        assert result == expected

    def test_write_package_with_class(self) -> None:
        """Test writing a package with a class."""
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="MyClass", is_abstract=False))
        writer = MarkdownWriter()
        result = writer.write_packages([pkg])
        expected = "* TestPackage\n    * MyClass\n"
        assert result == expected

    def test_write_package_with_abstract_class(self) -> None:
        """Test writing a package with an abstract class."""
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="AbstractClass", is_abstract=True))
        writer = MarkdownWriter()
        result = writer.write_packages([pkg])
        expected = "* TestPackage\n    * AbstractClass (abstract)\n"
        assert result == expected

    def test_write_package_with_multiple_classes(self) -> None:
        """Test writing a package with multiple classes."""
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="Class1", is_abstract=False))
        pkg.add_class(AutosarClass(name="Class2", is_abstract=True))
        pkg.add_class(AutosarClass(name="Class3", is_abstract=False))
        writer = MarkdownWriter()
        result = writer.write_packages([pkg])
        expected = (
            "* TestPackage\n"
            "    * Class1\n"
            "    * Class2 (abstract)\n"
            "    * Class3\n"
        )
        assert result == expected

    def test_write_nested_packages(self) -> None:
        """Test writing nested packages."""
        root = AutosarPackage(name="RootPackage")
        child = AutosarPackage(name="ChildPackage")
        child.add_class(AutosarClass(name="GrandchildClass", is_abstract=False))
        root.add_subpackage(child)
        writer = MarkdownWriter()
        result = writer.write_packages([root])
        expected = (
            "* RootPackage\n"
            "  * ChildPackage\n"
            "      * GrandchildClass\n"
        )
        assert result == expected

    def test_write_complex_hierarchy(self) -> None:
        """Test writing complex nested hierarchy."""
        # * AUTOSARTemplates
        #   * BswModuleTemplate
        #     * BswBehavior
        #         * BswInternalBehavior
        #         * ExecutableEntity (abstract)
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
            "        * BswInternalBehavior\n"
            "        * ExecutableEntity (abstract)\n"
        )
        assert result == expected

    def test_write_multiple_top_level_packages(self) -> None:
        """Test writing multiple top-level packages."""
        pkg1 = AutosarPackage(name="Package1")
        pkg1.add_class(AutosarClass(name="Class1", is_abstract=False))
        pkg2 = AutosarPackage(name="Package2")
        pkg2.add_class(AutosarClass(name="Class2", is_abstract=True))
        writer = MarkdownWriter()
        result = writer.write_packages([pkg1, pkg2])
        expected = (
            "* Package1\n"
            "    * Class1\n"
            "* Package2\n"
            "    * Class2 (abstract)\n"
        )
        assert result == expected

    def test_write_deeply_nested_hierarchy(self) -> None:
        """Test writing deeply nested package structure."""
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
            "        * DeepClass\n"
        )
        assert result == expected

    def test_deduplicate_classes_across_calls(self) -> None:
        """Test that duplicate classes across multiple write calls are skipped."""
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="MyClass", is_abstract=False))
        writer = MarkdownWriter(deduplicate=True)

        # First write
        result1 = writer.write_packages([pkg])
        assert result1 == "* TestPackage\n    * MyClass\n"

        # Second write - everything should be skipped due to deduplication
        result2 = writer.write_packages([pkg])
        assert result2 == ""

    def test_deduplicate_classes_same_path(self) -> None:
        """Test that duplicate classes in the same hierarchy path are skipped."""
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="MyClass", is_abstract=False))
        pkg.add_class(AutosarClass(name="OtherClass", is_abstract=False))
        writer = MarkdownWriter(deduplicate=True)

        # First write
        result1 = writer.write_packages([pkg])
        assert result1 == "* TestPackage\n    * MyClass\n    * OtherClass\n"

        # Create same package structure again - both classes should be skipped
        pkg2 = AutosarPackage(name="TestPackage")
        pkg2.add_class(AutosarClass(name="MyClass", is_abstract=False))
        pkg2.add_class(AutosarClass(name="OtherClass", is_abstract=False))
        result2 = writer.write_packages([pkg2])
        assert result2 == ""

    def test_deduplicate_subpackages_across_calls(self) -> None:
        """Test that duplicate subpackages across multiple write calls are skipped."""
        parent = AutosarPackage(name="ParentPackage")
        sub = AutosarPackage(name="ChildPackage")
        sub.add_class(AutosarClass(name="ChildClass", is_abstract=False))
        parent.add_subpackage(sub)
        writer = MarkdownWriter(deduplicate=True)

        # First write
        result1 = writer.write_packages([parent])
        assert "* ParentPackage\n" in result1
        assert "* ChildPackage\n" in result1

        # Second write - everything should be skipped
        result2 = writer.write_packages([parent])
        assert result2 == ""

    def test_no_deduplicate_mode(self) -> None:
        """Test that deduplication can be disabled."""
        pkg1 = AutosarPackage(name="TestPackage")
        pkg1.add_class(AutosarClass(name="MyClass", is_abstract=False))
        pkg2 = AutosarPackage(name="TestPackage")
        pkg2.add_class(AutosarClass(name="OtherClass", is_abstract=False))
        writer = MarkdownWriter(deduplicate=False)
        result = writer.write_packages([pkg1, pkg2])
        # Both packages should be written even though they have the same name
        expected = (
            "* TestPackage\n"
            "    * MyClass\n"
            "* TestPackage\n"
            "    * OtherClass\n"
        )
        assert result == expected

    def test_write_empty_package_list(self) -> None:
        """Test writing an empty package list."""
        writer = MarkdownWriter()
        result = writer.write_packages([])
        expected = ""
        assert result == expected

    def test_write_package_with_both_classes_and_subpackages(self) -> None:
        """Test writing package with both classes and subpackages."""
        pkg = AutosarPackage(name="ParentPackage")
        pkg.add_class(AutosarClass(name="DirectClass", is_abstract=False))
        subpkg = AutosarPackage(name="ChildPackage")
        subpkg.add_class(AutosarClass(name="ChildClass", is_abstract=True))
        pkg.add_subpackage(subpkg)
        writer = MarkdownWriter()
        result = writer.write_packages([pkg])
        expected = (
            "* ParentPackage\n"
            "    * DirectClass\n"
            "  * ChildPackage\n"
            "      * ChildClass (abstract)\n"
        )
        assert result == expected

    def test_multiple_calls_with_deduplication(self) -> None:
        """Test that deduplication persists across multiple calls."""
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="MyClass", is_abstract=False))
        writer = MarkdownWriter(deduplicate=True)

        # First call
        result1 = writer.write_packages([pkg])
        assert result1 == "* TestPackage\n    * MyClass\n"

        # Second call - package and class should be skipped
        result2 = writer.write_packages([pkg])
        assert result2 == ""

    def test_nested_duplicate_tracking(self) -> None:
        """Test duplicate tracking works across nested structures."""
        # Create structure where same class name appears in different packages
        pkg1 = AutosarPackage(name="Package1")
        pkg1.add_class(AutosarClass(name="CommonClass", is_abstract=False))

        pkg2 = AutosarPackage(name="Package2")
        pkg2.add_class(AutosarClass(name="CommonClass", is_abstract=False))

        root = AutosarPackage(name="Root")
        root.add_subpackage(pkg1)
        root.add_subpackage(pkg2)

        writer = MarkdownWriter(deduplicate=True)
        result = writer.write_packages([root])
        # Both CommonClass instances should be written (different parents)
        assert "CommonClass" in result
        assert result.count("* CommonClass") == 2


class TestFunctionalInterface:
    """Tests for functional interface."""

    def test_write_markdown_function(self) -> None:
        """Test write_markdown function."""
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="MyClass", is_abstract=False))
        result = write_markdown([pkg])
        expected = "* TestPackage\n    * MyClass\n"
        assert result == expected

    def test_write_markdown_with_deduplicate_false(self) -> None:
        """Test write_markdown with deduplication disabled."""
        pkg1 = AutosarPackage(name="TestPackage")
        pkg1.add_class(AutosarClass(name="MyClass", is_abstract=False))
        pkg2 = AutosarPackage(name="TestPackage")
        pkg2.add_class(AutosarClass(name="OtherClass", is_abstract=False))
        result = write_markdown([pkg1, pkg2], deduplicate=False)
        # Both packages should be written
        assert result.count("* TestPackage") == 2
        assert "MyClass" in result
        assert "OtherClass" in result

    def test_write_markdown_with_deduplicate_true(self) -> None:
        """Test write_markdown with deduplication enabled."""
        pkg1 = AutosarPackage(name="TestPackage")
        pkg1.add_class(AutosarClass(name="MyClass", is_abstract=False))
        pkg2 = AutosarPackage(name="TestPackage")
        pkg2.add_class(AutosarClass(name="OtherClass", is_abstract=False))
        result = write_markdown([pkg1, pkg2], deduplicate=True)
        # Only first package and class should be written
        expected = "* TestPackage\n    * MyClass\n"
        assert result == expected

    def test_write_markdown_empty_list(self) -> None:
        """Test write_markdown with empty package list."""
        result = write_markdown([])
        expected = ""
        assert result == expected
