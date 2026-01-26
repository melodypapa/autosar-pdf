"""Tests for markdown writer.

Test coverage for markdown_writer.py targeting 100%.
"""

from pathlib import Path

from autosar_pdf2txt.models import (
    ATPType,
    AttributeKind,
    AutosarAttribute,
    AutosarClass,
    AutosarEnumLiteral,
    AutosarEnumeration,
    AutosarPackage,
)
from autosar_pdf2txt.writer.markdown_writer import MarkdownWriter


class TestMarkdownWriter:
    """Tests for MarkdownWriter class.

    Requirements:
        SWR_WRITER_00001: Markdown Writer Initialization
        SWR_WRITER_00002: Markdown Package Hierarchy Output
        SWR_WRITER_00003: Markdown Class Output Format
        SWR_WRITER_00004: Bulk Package Writing
        SWR_WRITER_00005: Directory-Based Class File Output
    """

    def test_init_default(self) -> None:
        """SWUT_WRITER_00001: Test initialization with default settings.

        Requirements:
            SWR_WRITER_00001: Markdown Writer Initialization
        """
        writer = MarkdownWriter()
        # No deduplicate attribute or tracking sets anymore
        assert writer is not None

    def test_write_single_empty_package(self) -> None:
        """SWUT_WRITER_00002: Test writing a single empty package.

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
        """SWUT_WRITER_00003: Test writing a package with a class.

        Requirements:
            SWR_WRITER_00002: Markdown Package Hierarchy Output
            SWR_WRITER_00003: Markdown Class Output Format
        """
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="MyClass", package="M2::Test", is_abstract=False))
        writer = MarkdownWriter()
        result = writer.write_packages([pkg])
        expected = "* TestPackage\n  * MyClass\n"
        assert result == expected

    def test_write_package_with_abstract_class(self) -> None:
        """SWUT_WRITER_00004: Test writing a package with an abstract class.

        Requirements:
            SWR_WRITER_00002: Markdown Package Hierarchy Output
            SWR_WRITER_00003: Markdown Class Output Format
        """
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="AbstractClass", package="M2::Test", is_abstract=True))
        writer = MarkdownWriter()
        result = writer.write_packages([pkg])
        expected = "* TestPackage\n  * AbstractClass\n"
        assert result == expected

    def test_write_package_with_multiple_classes(self) -> None:
        """SWUT_WRITER_00005: Test writing a package with multiple classes.

        Requirements:
            SWR_WRITER_00002: Markdown Package Hierarchy Output
            SWR_WRITER_00003: Markdown Class Output Format
        """
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="Class1", package="M2::Test", is_abstract=False))
        pkg.add_class(AutosarClass(name="Class2", package="M2::Test", is_abstract=True))
        pkg.add_class(AutosarClass(name="Class3", package="M2::Test", is_abstract=False))
        writer = MarkdownWriter()
        result = writer.write_packages([pkg])
        expected = (
            "* TestPackage\n"
            "  * Class1\n"
            "  * Class2\n"
            "  * Class3\n"
        )
        assert result == expected

    def test_write_nested_packages(self) -> None:
        """SWUT_WRITER_00006: Test writing nested packages.

        Requirements:
            SWR_WRITER_00002: Markdown Package Hierarchy Output
        """
        root = AutosarPackage(name="RootPackage")
        child = AutosarPackage(name="ChildPackage")
        child.add_class(AutosarClass(name="GrandchildClass", package="M2::Test", is_abstract=False))
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
        """SWUT_WRITER_00007: Test writing complex nested hierarchy.

        Requirements:
            SWR_WRITER_00002: Markdown Package Hierarchy Output
            SWR_WRITER_00003: Markdown Class Output Format

        Test structure:
            * AUTOSARTemplates
              * BswModuleTemplate
                * BswBehavior
                  * BswInternalBehavior
                  * ExecutableEntity
        """
        root = AutosarPackage(name="AUTOSARTemplates")
        bsw = AutosarPackage(name="BswModuleTemplate")
        behavior = AutosarPackage(name="BswBehavior")
        behavior.add_class(AutosarClass(name="BswInternalBehavior", package="M2::Test", is_abstract=False))
        behavior.add_class(AutosarClass(name="ExecutableEntity", package="M2::Test", is_abstract=True))
        bsw.add_subpackage(behavior)
        root.add_subpackage(bsw)

        writer = MarkdownWriter()
        result = writer.write_packages([root])
        expected = (
            "* AUTOSARTemplates\n"
            "  * BswModuleTemplate\n"
            "    * BswBehavior\n"
            "      * BswInternalBehavior\n"
            "      * ExecutableEntity\n"
        )
        assert result == expected

    def test_write_multiple_top_level_packages(self) -> None:
        """SWUT_WRITER_00008: Test writing multiple top-level packages.

        Requirements:
            SWR_WRITER_00002: Markdown Package Hierarchy Output
            SWR_WRITER_00004: Bulk Package Writing
        """
        pkg1 = AutosarPackage(name="Package1")
        pkg1.add_class(AutosarClass(name="Class1", package="M2::Test", is_abstract=False))
        pkg2 = AutosarPackage(name="Package2")
        pkg2.add_class(AutosarClass(name="Class2", package="M2::Test", is_abstract=True))
        writer = MarkdownWriter()
        result = writer.write_packages([pkg1, pkg2])
        expected = (
            "* Package1\n"
            "  * Class1\n"
            "* Package2\n"
            "  * Class2\n"
        )
        assert result == expected

    def test_write_deeply_nested_hierarchy(self) -> None:
        """SWUT_WRITER_00009: Test writing deeply nested package structure.

        Requirements:
            SWR_WRITER_00002: Markdown Package Hierarchy Output
        """
        level1 = AutosarPackage(name="Level1")
        level2 = AutosarPackage(name="Level2")
        level3 = AutosarPackage(name="Level3")
        level3.add_class(AutosarClass(name="DeepClass", package="M2::Test", is_abstract=False))
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
        """SWUT_WRITER_00010: Test writing an empty package list.

        Requirements:
            SWR_WRITER_00004: Bulk Package Writing
        """
        writer = MarkdownWriter()
        result = writer.write_packages([])
        expected = ""
        assert result == expected

    def test_write_package_with_both_classes_and_subpackages(self) -> None:
        """SWUT_WRITER_00011: Test writing package with both classes and subpackages.

        Requirements:
            SWR_WRITER_00002: Markdown Package Hierarchy Output
            SWR_WRITER_00003: Markdown Class Output Format
        """
        pkg = AutosarPackage(name="ParentPackage")
        pkg.add_class(AutosarClass(name="DirectClass", package="M2::Test", is_abstract=False))
        subpkg = AutosarPackage(name="ChildPackage")
        subpkg.add_class(AutosarClass(name="ChildClass", package="M2::Test", is_abstract=True))
        pkg.add_subpackage(subpkg)
        writer = MarkdownWriter()
        result = writer.write_packages([pkg])
        expected = (
            "* ParentPackage\n"
            "  * DirectClass\n"
            "  * ChildPackage\n"
            "    * ChildClass\n"
        )
        assert result == expected

    def test_multiple_writes_same_structure(self) -> None:
        """SWUT_WRITER_00012: Test that multiple writes of the same structure produce identical output.

        Requirements:
            SWR_WRITER_00002: Markdown Package Hierarchy Output
            SWR_WRITER_00003: Markdown Class Output Format
        """
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="MyClass", package="M2::Test", is_abstract=False))
        writer = MarkdownWriter()

        # First write
        result1 = writer.write_packages([pkg])
        expected = "* TestPackage\n  * MyClass\n"
        assert result1 == expected

        # Second write - should produce the same output (no writer-level deduplication)
        result2 = writer.write_packages([pkg])
        assert result2 == expected

    def test_model_level_duplicate_prevention(self) -> None:
        """SWUT_WRITER_00013: Test that model-level duplicate prevention works with sources merging.

        Requirements:
            SWR_MODEL_00006: Add Class to Package
            SWR_WRITER_00002: Markdown Package Hierarchy Output
            SWR_WRITER_00003: Markdown Class Output Format

        Note:
            Duplicate classes have their sources merged instead of being skipped.
        """
        from autosar_pdf2txt.models.base import AutosarDocumentSource
        from unittest.mock import patch, MagicMock

        pkg = AutosarPackage(name="TestPackage")
        source1 = AutosarDocumentSource("file1.pdf", 1)
        source2 = AutosarDocumentSource("file2.pdf", 2)
        pkg.add_class(AutosarClass(name="MyClass", package="M2::Test", is_abstract=False, sources=[source1]))

        # Mock the logger to capture the info log
        with patch("logging.getLogger") as mock_get_logger:
            mock_logger = MagicMock()
            mock_get_logger.return_value = mock_logger
            pkg.add_class(AutosarClass(name="MyClass", package="M2::Test", is_abstract=False, sources=[source2]))

            # Verify info was logged about merging sources
            mock_logger.info.assert_called_once()
            call_args = mock_logger.info.call_args[0]
            assert "Type '%s' already exists in package '%s', merging %d new source(s)" in call_args[0]
            assert mock_logger.info.call_args[0][1] == "MyClass"
            assert mock_logger.info.call_args[0][2] == "TestPackage"
            assert mock_logger.info.call_args[0][3] == 1

        # Writer should only output the first class
        writer = MarkdownWriter()
        result = writer.write_packages([pkg])
        expected = "* TestPackage\n  * MyClass\n"
        assert result == expected

    def test_write_multiple_packages_same_name_different_content(self) -> None:
        """SWUT_WRITER_00014: Test writing multiple packages with same name but different content.

        Requirements:
            SWR_WRITER_00002: Markdown Package Hierarchy Output
            SWR_WRITER_00004: Bulk Package Writing
        """
        pkg1 = AutosarPackage(name="TestPackage")
        pkg1.add_class(AutosarClass(name="Class1", package="M2::Test", is_abstract=False))

        pkg2 = AutosarPackage(name="TestPackage")
        pkg2.add_class(AutosarClass(name="Class2", package="M2::Test", is_abstract=False))

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
        """SWUT_WRITER_00015: Test that same class names in different packages are both written.

        Requirements:
            SWR_MODEL_00006: Add Class to Package
            SWR_WRITER_00002: Markdown Package Hierarchy Output
            SWR_WRITER_00003: Markdown Class Output Format
        """
        # Create structure where same class name appears in different packages
        pkg1 = AutosarPackage(name="Package1")
        pkg1.add_class(AutosarClass(name="CommonClass", package="M2::Test", is_abstract=False))

        pkg2 = AutosarPackage(name="Package2")
        pkg2.add_class(AutosarClass(name="CommonClass", package="M2::Test", is_abstract=False))

        root = AutosarPackage(name="Root")
        root.add_subpackage(pkg1)
        root.add_subpackage(pkg2)

        writer = MarkdownWriter()
        result = writer.write_packages([root])
        # Both CommonClass instances should be written (different parents)
        assert "CommonClass" in result
        assert result.count("* CommonClass") == 2


class TestMarkdownWriterClassHierarchy:
    """Tests for MarkdownWriter class hierarchy output.

    Requirements:
        SWR_WRITER_00002: Markdown Package Hierarchy Output
    """

    def test_write_class_hierarchy_empty(self) -> None:
        """Test writing class hierarchy with no root classes.

        Requirements:
            SWR_WRITER_00007: Class Hierarchy Output
        """
        writer = MarkdownWriter()
        result = writer.write_class_hierarchy([])
        assert result == ""

    def test_write_class_hierarchy_single_root(self) -> None:
        """Test writing class hierarchy with a single root class.

        Requirements:
            SWR_WRITER_00007: Class Hierarchy Output
        """
        root_cls = AutosarClass(name="RootClass", package="M2::Test", is_abstract=False)
        writer = MarkdownWriter()
        result = writer.write_class_hierarchy([root_cls])
        assert "## Class Hierarchy" in result
        assert "* RootClass" in result

    def test_write_class_hierarchy_with_abstract(self) -> None:
        """Test writing class hierarchy with abstract class.

        Requirements:
            SWR_WRITER_00007: Class Hierarchy Output
        """
        root_cls = AutosarClass(name="AbstractClass", package="M2::Test", is_abstract=True)
        writer = MarkdownWriter()
        result = writer.write_class_hierarchy([root_cls])
        assert "## Class Hierarchy" in result
        assert "* AbstractClass (abstract)" in result

    def test_write_class_hierarchy_with_subclasses(self) -> None:
        """Test writing class hierarchy with subclasses.

        Requirements:
            SWR_WRITER_00007: Class Hierarchy Output
        """
        root_cls = AutosarClass(name="RootClass", package="M2::Test", is_abstract=False)
        child_cls = AutosarClass(name="ChildClass", package="M2::Test", is_abstract=False, parent="RootClass")
        writer = MarkdownWriter()
        result = writer.write_class_hierarchy([root_cls], [root_cls, child_cls])
        assert "## Class Hierarchy" in result
        assert "* RootClass" in result
        assert "  * ChildClass" in result

    def test_write_class_hierarchy_multiple_levels(self) -> None:
        """Test writing class hierarchy with multiple levels.

        Requirements:
            SWR_WRITER_00007: Class Hierarchy Output
        """
        root_cls = AutosarClass(name="RootClass", package="M2::Test", is_abstract=False)
        child_cls = AutosarClass(name="ChildClass", package="M2::Test", is_abstract=False, parent="RootClass")
        grandchild_cls = AutosarClass(name="GrandchildClass", package="M2::Test", is_abstract=False, parent="ChildClass")
        writer = MarkdownWriter()
        result = writer.write_class_hierarchy([root_cls], [root_cls, child_cls, grandchild_cls])
        assert "## Class Hierarchy" in result
        assert "* RootClass" in result
        assert "  * ChildClass" in result
        assert "    * GrandchildClass" in result

    def test_write_class_hierarchy_multiple_roots(self) -> None:
        """Test writing class hierarchy with multiple root classes.

        Requirements:
            SWR_WRITER_00007: Class Hierarchy Output
        """
        root1 = AutosarClass(name="Root1", package="M2::Test", is_abstract=False)
        root2 = AutosarClass(name="Root2", package="M2::Test", is_abstract=False)
        writer = MarkdownWriter()
        result = writer.write_class_hierarchy([root1, root2], [root1, root2])
        assert "## Class Hierarchy" in result
        assert "* Root1" in result
        assert "* Root2" in result

    def test_write_class_hierarchy_without_all_classes(self) -> None:
        """Test writing class hierarchy without providing all_classes parameter."""
        root_cls = AutosarClass(name="RootClass", package="M2::Test", is_abstract=False)
        writer = MarkdownWriter()
        result = writer.write_class_hierarchy([root_cls])
        assert "## Class Hierarchy" in result
        assert "* RootClass" in result
        # Should not include subclasses since all_classes not provided

    def test_collect_classes_from_package(self) -> None:
        """Test collecting classes from a package."""
        pkg = AutosarPackage(name="TestPackage")
        cls1 = AutosarClass(name="Class1", package="M2::Test", is_abstract=False)
        cls2 = AutosarClass(name="Class2", package="M2::Test", is_abstract=True)
        pkg.add_type(cls1)
        pkg.add_type(cls2)

        writer = MarkdownWriter()
        classes = writer._collect_classes_from_package(pkg)
        assert len(classes) == 2
        assert cls1 in classes
        assert cls2 in classes

    def test_collect_classes_from_nested_package(self) -> None:
        """Test collecting classes from nested packages."""
        subpkg = AutosarPackage(name="SubPackage")
        subcls = AutosarClass(name="SubClass", package="M2::Test::Sub", is_abstract=False)
        subpkg.add_type(subcls)

        root_pkg = AutosarPackage(name="RootPackage")
        rootcls = AutosarClass(name="RootClass", package="M2::Test", is_abstract=False)
        root_pkg.add_type(rootcls)
        root_pkg.add_subpackage(subpkg)

        writer = MarkdownWriter()
        classes = writer._collect_classes_from_package(root_pkg)
        assert len(classes) == 2
        assert rootcls in classes
        assert subcls in classes

    def test_write_class_hierarchy_with_cycle_detection(self) -> None:
        """Test write_class_hierarchy detects and handles circular references.

        Requirements:
            SWR_WRITER_00007: Class Hierarchy Output
        """
        # Create a class that references itself (self-cycle)
        cls_self = AutosarClass(name="SelfReferencing", package="M2::Test", is_abstract=False, parent="SelfReferencing")

        writer = MarkdownWriter()
        result = writer.write_class_hierarchy([cls_self], [cls_self])

        # Should detect the cycle
        assert "(cycle detected)" in result
        assert "SelfReferencing" in result


class TestMarkdownWriterFiles:
    """Tests for MarkdownWriter directory-based file output.

    Requirements:
        SWR_WRITER_00005: Directory-Based Class File Output
    """

    def test_write_single_class_to_file(self, tmp_path: Path) -> None:
        """SWUT_WRITER_00016: Test writing a single class to a file.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
            SWR_WRITER_00006: Individual Class Markdown File Content
        """
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="MyClass", package="M2::Test", is_abstract=False))

        writer = MarkdownWriter()
        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        # Check directory exists
        pkg_dir = tmp_path / "TestPackage"
        assert pkg_dir.is_dir()

        # Check file exists
        class_file = pkg_dir / "MyClass.md"
        assert class_file.is_file()

        # Check file content
        content = class_file.read_text(encoding="utf-8")
        assert "# MyClass\n\n" in content
        assert "## Package\n\n" in content
        assert "TestPackage\n\n" in content
        assert "## Type\n\n" in content
        assert "Concrete\n\n" in content

    def test_write_abstract_class_to_file(self, tmp_path: Path) -> None:
        """SWUT_WRITER_00017: Test writing an abstract class to a file.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
            SWR_WRITER_00006: Individual Class Markdown File Content
        """
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="AbstractClass", package="M2::Test", is_abstract=True))

        writer = MarkdownWriter()
        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        class_file = tmp_path / "TestPackage" / "AbstractClass.md"
        content = class_file.read_text(encoding="utf-8")
        assert "# AbstractClass (abstract)\n\n" in content
        assert "## Package\n\n" in content
        assert "TestPackage\n\n" in content
        assert "## Type\n\n" in content
        assert "Abstract\n\n" in content

    def test_write_multiple_classes_to_files(self, tmp_path: Path) -> None:
        """SWUT_WRITER_00018: Test writing multiple classes to separate files.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
        """
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="Class1", package="M2::Test", is_abstract=False))
        pkg.add_class(AutosarClass(name="Class2", package="M2::Test", is_abstract=True))
        pkg.add_class(AutosarClass(name="Class3", package="M2::Test", is_abstract=False))

        writer = MarkdownWriter()
        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        # Check all files exist
        pkg_dir = tmp_path / "TestPackage"
        assert (pkg_dir / "Class1.md").is_file()
        assert (pkg_dir / "Class2.md").is_file()
        assert (pkg_dir / "Class3.md").is_file()

    def test_write_nested_packages_to_files(self, tmp_path: Path) -> None:
        """SWUT_WRITER_00019: Test writing nested packages to directory structure.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
        """
        root = AutosarPackage(name="RootPackage")
        child = AutosarPackage(name="ChildPackage")
        child.add_class(AutosarClass(name="ChildClass", package="M2::Test", is_abstract=False))
        root.add_subpackage(child)

        writer = MarkdownWriter()
        writer.write_packages_to_files([root], base_dir=tmp_path)

        # Check directory structure
        child_dir = tmp_path / "RootPackage" / "ChildPackage"
        assert child_dir.is_dir()

        # Check class file exists in nested directory
        class_file = child_dir / "ChildClass.md"
        assert class_file.is_file()

        # Verify full package path is written to the file
        content = class_file.read_text(encoding="utf-8")
        assert "## Package\n\n" in content
        assert "RootPackage::ChildPackage\n\n" in content

    def test_write_class_with_attributes(self, tmp_path: Path) -> None:
        """SWUT_WRITER_00020: Test writing a class with attributes to file.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
            SWR_WRITER_00006: Individual Class Markdown File Content
        """
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(name="MyClass", package="M2::Test", is_abstract=False)
        cls.attributes["attr1"] = AutosarAttribute(name="attr1", type="String", is_ref=False, multiplicity="1", kind=AttributeKind.ATTR, note="")
        cls.attributes["attr2"] = AutosarAttribute(name="attr2", type="Integer", is_ref=True, multiplicity="1", kind=AttributeKind.ATTR, note="")
        pkg.add_class(cls)

        writer = MarkdownWriter()
        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        class_file = tmp_path / "TestPackage" / "MyClass.md"
        content = class_file.read_text(encoding="utf-8")

        assert "## Package\n\n" in content
        assert "TestPackage\n\n" in content
        assert "## Type\n\n" in content
        assert "Concrete\n\n" in content
        assert "## Attributes\n\n" in content
        assert "| Attribute | Type | Mult. | Kind | Note |" in content
        assert "| attr1 | String |" in content
        assert "| attr2 (ref) | Integer |" in content

    def test_write_class_with_base_classes(self, tmp_path: Path) -> None:
        """SWUT_WRITER_00021: Test writing a class with base classes to file.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
            SWR_WRITER_00006: Individual Class Markdown File Content
        """
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(name="DerivedClass", package="M2::Test", is_abstract=False)
        cls.bases = ["BaseClass1", "BaseClass2"]
        pkg.add_class(cls)

        writer = MarkdownWriter()
        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        class_file = tmp_path / "TestPackage" / "DerivedClass.md"
        content = class_file.read_text(encoding="utf-8")

        assert "## Package\n\n" in content
        assert "TestPackage\n\n" in content
        assert "## Type\n\n" in content
        assert "Concrete\n\n" in content
        assert "## Base Classes\n\n" in content
        assert "* BaseClass1\n" in content
        assert "* BaseClass2\n" in content

    def test_write_class_with_parent(self, tmp_path: Path) -> None:
        """SWUT_WRITER_00023: Test writing a class with parent to file.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
            SWR_WRITER_00006: Individual Class Markdown File Content
            SWR_MODEL_00022: AUTOSAR Class Parent Attribute
        """
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(name="ChildClass", package="M2::Test", is_abstract=False)
        cls.bases = ["ParentClass"]
        cls.parent = "ParentClass"
        pkg.add_class(cls)

        writer = MarkdownWriter()
        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        class_file = tmp_path / "TestPackage" / "ChildClass.md"
        content = class_file.read_text(encoding="utf-8")

        assert "## Package\n\n" in content
        assert "TestPackage\n\n" in content
        assert "## Type\n\n" in content
        assert "Concrete\n\n" in content
        assert "## Parent\n\n" in content
        assert "ParentClass\n\n" in content

    def test_write_class_without_parent(self, tmp_path: Path) -> None:
        """SWUT_WRITER_00024: Test writing a class without parent to file.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
            SWR_WRITER_00006: Individual Class Markdown File Content
            SWR_MODEL_00022: AUTOSAR Class Parent Attribute
        """
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(name="RootClass", package="M2::Test", is_abstract=False)
        pkg.add_class(cls)

        writer = MarkdownWriter()
        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        class_file = tmp_path / "TestPackage" / "RootClass.md"
        content = class_file.read_text(encoding="utf-8")

        assert "## Package\n\n" in content
        assert "TestPackage\n\n" in content
        assert "## Type\n\n" in content
        assert "Concrete\n\n" in content
        assert "## Parent\n\n" not in content

    def test_write_class_with_note(self, tmp_path: Path) -> None:
        """SWUT_WRITER_00022: Test writing a class with a note to file.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
            SWR_WRITER_00006: Individual Class Markdown File Content
        """
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(name="MyClass", package="M2::Test", is_abstract=False)
        cls.note = "This is a documentation note."
        pkg.add_class(cls)

        writer = MarkdownWriter()
        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        class_file = tmp_path / "TestPackage" / "MyClass.md"
        content = class_file.read_text(encoding="utf-8")

        assert "## Package\n\n" in content
        assert "TestPackage\n\n" in content
        assert "## Type\n\n" in content
        assert "Concrete\n\n" in content
        assert "## Note\n\n" in content
        assert "This is a documentation note." in content

    def test_write_complete_class_to_file(self, tmp_path: Path) -> None:
        """SWUT_WRITER_00023: Test writing a class with all fields to file.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
            SWR_WRITER_00006: Individual Class Markdown File Content
        """
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(name="CompleteClass", package="M2::Test", is_abstract=True)
        cls.bases = ["BaseClass"]
        cls.attributes["attr1"] = AutosarAttribute(name="attr1", type="String", is_ref=False, multiplicity="1", kind=AttributeKind.ATTR, note="")
        cls.note = "Complete documentation."

        pkg.add_class(cls)

        writer = MarkdownWriter()
        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        class_file = tmp_path / "TestPackage" / "CompleteClass.md"
        content = class_file.read_text(encoding="utf-8")

        assert "# CompleteClass (abstract)\n\n" in content
        assert "## Package\n\n" in content
        assert "TestPackage\n\n" in content
        assert "## Type\n\n" in content
        assert "Abstract\n\n" in content
        assert "## Base Classes\n\n" in content
        assert "* BaseClass\n" in content
        assert "## Attributes\n\n" in content
        assert "| Attribute | Type | Mult. | Kind | Note |" in content
        assert "| attr1 | String |" in content
        assert "## Note\n\n" in content
        assert "Complete documentation." in content

    def test_class_file_content_structure(self, tmp_path: Path) -> None:
        """SWUT_WRITER_00024: Test that class file content follows SWR_WRITER_00006 structure.

        Requirements:
            SWR_WRITER_00006: Individual Class Markdown File Content

        Verifies that all required fields are present and in the correct order:
        1. Package name
        2. Abstract class indicator (Type)
        3. Base classes
        4. Note as description
        5. Attributes list
        """
        pkg = AutosarPackage(name="AUTOSAR")
        cls = AutosarClass(name="BswInternalBehavior", package="M2::Test", is_abstract=True)
        cls.bases = ["IBswInternalBehavior", "IReferable"]
        cls.attributes["swDataDefProps"] = AutosarAttribute(name="swDataDefProps", type="SwDataDefProps", is_ref=True, multiplicity="1", kind=AttributeKind.ATTR, note="")
        cls.note = "This class represents the internal behavior of a BSW module."

        pkg.add_class(cls)

        writer = MarkdownWriter()
        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        class_file = tmp_path / "AUTOSAR" / "BswInternalBehavior.md"
        content = class_file.read_text(encoding="utf-8")

        # Verify title with abstract suffix
        assert content.startswith("# BswInternalBehavior (abstract)\n\n")

        # Find sections and verify order
        package_idx = content.find("## Package\n\n")
        type_idx = content.find("## Type\n\n")
        base_classes_idx = content.find("## Base Classes\n\n")
        note_idx = content.find("## Note\n\n")
        attributes_idx = content.find("## Attributes\n\n")

        # Verify all sections exist
        assert package_idx != -1, "Package section missing"
        assert type_idx != -1, "Type section missing"
        assert base_classes_idx != -1, "Base Classes section missing"
        assert note_idx != -1, "Note section missing"
        assert attributes_idx != -1, "Attributes section missing"

        # Verify correct order: Package < Type < Base Classes < Note < Attributes
        assert package_idx < type_idx, "Package should come before Type"
        assert type_idx < base_classes_idx, "Type should come before Base Classes"
        assert base_classes_idx < note_idx, "Base Classes should come before Note"
        assert note_idx < attributes_idx, "Note should come before Attributes"

        # Verify package name
        assert "AUTOSAR\n\n" in content

        # Verify type
        assert "Abstract\n\n" in content

        # Verify base classes list
        assert "* IBswInternalBehavior\n" in content
        assert "* IReferable\n" in content

        # Verify note content
        assert "This class represents the internal behavior of a BSW module." in content

        # Verify attributes table with reference indicator
        assert "| Attribute | Type | Mult. | Kind | Note |" in content
        assert "| swDataDefProps (ref) | SwDataDefProps |" in content

    def test_concrete_class_type_indicator(self, tmp_path: Path) -> None:
        """SWUT_WRITER_00025: Test that concrete classes have correct type indicator.

        Requirements:
            SWR_WRITER_00006: Individual Class Markdown File Content
        """
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(name="ConcreteClass", package="M2::Test", is_abstract=False)
        pkg.add_class(cls)

        writer = MarkdownWriter()
        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        class_file = tmp_path / "TestPackage" / "ConcreteClass.md"
        content = class_file.read_text(encoding="utf-8")

        # Verify type section shows Concrete
        assert "## Type\n\n" in content
        assert "Concrete\n\n" in content

        # Verify it does not show Abstract
        assert "Abstract\n\n" not in content

    def test_write_empty_package_to_files(self, tmp_path: Path) -> None:
        """SWUT_WRITER_00026: Test writing an empty package creates directory but no files.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
        """
        pkg = AutosarPackage(name="EmptyPackage")

        writer = MarkdownWriter()
        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        # Directory should exist
        pkg_dir = tmp_path / "EmptyPackage"
        assert pkg_dir.is_dir()

        # No class files should exist
        assert len(list(pkg_dir.glob("*.md"))) == 0

    def test_write_multiple_top_level_packages_to_files(self, tmp_path: Path) -> None:
        """SWUT_WRITER_00027: Test writing multiple top-level packages to files.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
        """
        pkg1 = AutosarPackage(name="Package1")
        pkg1.add_class(AutosarClass(name="Class1", package="M2::Test", is_abstract=False))

        pkg2 = AutosarPackage(name="Package2")
        pkg2.add_class(AutosarClass(name="Class2", package="M2::Test", is_abstract=False))

        writer = MarkdownWriter()
        writer.write_packages_to_files([pkg1, pkg2], base_dir=tmp_path)

        # Both directories should exist
        assert (tmp_path / "Package1").is_dir()
        assert (tmp_path / "Package2").is_dir()

        # Both class files should exist
        assert (tmp_path / "Package1" / "Class1.md").is_file()
        assert (tmp_path / "Package2" / "Class2.md").is_file()

    def test_write_packages_with_pathlib_path(self, tmp_path: Path) -> None:
        """SWUT_WRITER_00028: Test writing packages with pathlib.Path object.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
        """
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="MyClass", package="M2::Test", is_abstract=False))

        writer = MarkdownWriter()
        # Use pathlib.Path directly instead of string
        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        class_file = tmp_path / "TestPackage" / "MyClass.md"
        assert class_file.is_file()

    def test_write_packages_with_output_path(self, tmp_path: Path) -> None:
        """SWUT_WRITER_00029: Test writing packages with output_path parameter.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output

        The root directory should be the same as the output markdown file location.
        """
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="MyClass", package="M2::Test", is_abstract=False))

        writer = MarkdownWriter()
        output_file = tmp_path / "output.md"
        writer.write_packages_to_files([pkg], output_path=output_file)

        # Root directory should be the same as output file location (tmp_path)
        pkg_dir = tmp_path / "TestPackage"
        assert pkg_dir.is_dir()

        class_file = pkg_dir / "MyClass.md"
        assert class_file.is_file()

    def test_write_packages_with_output_path_nested(self, tmp_path: Path) -> None:
        """SWUT_WRITER_00030: Test writing packages with output_path in subdirectory.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output

        The root directory should be the same as the output markdown file location.
        """
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="MyClass", package="M2::Test", is_abstract=False))

        writer = MarkdownWriter()

        # Create output file in a subdirectory
        output_dir = tmp_path / "subdir"
        output_dir.mkdir()
        output_file = output_dir / "output.md"
        writer.write_packages_to_files([pkg], output_path=output_file)

        # Root directory should be the output_dir (same as output file location)
        pkg_dir = output_dir / "TestPackage"
        assert pkg_dir.is_dir()

        class_file = pkg_dir / "MyClass.md"
        assert class_file.is_file()

    def test_write_packages_invalid_both_parameters(self) -> None:
        """SWUT_WRITER_00031: Test that providing both output_path and base_dir raises ValueError.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
        """
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="MyClass", package="M2::Test", is_abstract=False))

        writer = MarkdownWriter()

        # Test with both parameters
        try:
            writer.write_packages_to_files([pkg], output_path="/tmp/output.md", base_dir="/tmp")
            assert False, "Expected ValueError for both parameters"
        except ValueError as e:
            assert "both" in str(e).lower() or "cannot specify both" in str(e).lower()

    def test_write_packages_invalid_neither_parameter(self) -> None:
        """SWUT_WRITER_00032: Test that providing neither output_path nor base_dir raises ValueError.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
        """
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="MyClass", package="M2::Test", is_abstract=False))

        writer = MarkdownWriter()

        # Test with neither parameter
        try:
            writer.write_packages_to_files([pkg])  # type: ignore
            assert False, "Expected ValueError for neither parameter"
        except ValueError as e:
            assert "must specify" in str(e).lower() or "either" in str(e).lower()

    def test_write_packages_invalid_base_dir(self) -> None:
        """SWUT_WRITER_00033: Test that invalid base directory raises ValueError.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
        """
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="MyClass", package="M2::Test", is_abstract=False))

        writer = MarkdownWriter()

        # Test with empty string
        try:
            writer.write_packages_to_files([pkg], base_dir="")
            assert False, "Expected ValueError for empty base_dir"
        except ValueError as e:
            assert "base_dir" in str(e).lower()

    def test_write_packages_invalid_output_path(self) -> None:
        """SWUT_WRITER_00034: Test that invalid output path raises ValueError.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
        """
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="MyClass", package="M2::Test", is_abstract=False))

        writer = MarkdownWriter()

        # Test with empty string
        try:
            writer.write_packages_to_files([pkg], output_path="")
            assert False, "Expected ValueError for empty output_path"
        except ValueError as e:
            assert "output_path" in str(e).lower()

    def test_write_deeply_nested_packages_to_files(self, tmp_path: Path) -> None:
        """SWUT_WRITER_00035: Test writing deeply nested package structure.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
        """
        level1 = AutosarPackage(name="Level1")
        level2 = AutosarPackage(name="Level2")
        level3 = AutosarPackage(name="Level3")
        level3.add_class(AutosarClass(name="DeepClass", package="M2::Test", is_abstract=False))
        level2.add_subpackage(level3)
        level1.add_subpackage(level2)

        writer = MarkdownWriter()
        writer.write_packages_to_files([level1], base_dir=tmp_path)

        # Check deep directory structure
        deep_dir = tmp_path / "Level1" / "Level2" / "Level3"
        assert deep_dir.is_dir()

        # Check class file in deep directory
        class_file = deep_dir / "DeepClass.md"
        assert class_file.is_file()

        # Verify full package path is written to the file
        content = class_file.read_text(encoding="utf-8")
        assert "## Package\n\n" in content
        assert "Level1::Level2::Level3\n\n" in content

    def test_sanitize_filename_normal_name(self) -> None:
        """SWUT_WRITER_00036: Test sanitizing a normal class name.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
        """
        writer = MarkdownWriter()
        result = writer._sanitize_filename("NormalClass")
        assert result == "NormalClass"

    def test_sanitize_filename_invalid_chars(self) -> None:
        """SWUT_WRITER_00037: Test sanitizing class name with invalid characters.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
        """
        writer = MarkdownWriter()
        # Test with angle brackets
        result = writer._sanitize_filename("<<atpVariation>>Class")
        assert result == "__atpVariation__Class"

        # Test with colon
        result = writer._sanitize_filename("Class:Name")
        assert result == "Class_Name"

        # Test with backslash
        result = writer._sanitize_filename("Class\\Name")
        assert result == "Class_Name"

        # Test with multiple invalid chars
        result = writer._sanitize_filename('Class<>:"/\\|?*Name')
        assert result == "Class_________Name"

    def test_sanitize_filename_leading_trailing_spaces(self) -> None:
        """SWUT_WRITER_00038: Test sanitizing class name with leading/trailing spaces and dots.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
        """
        writer = MarkdownWriter()
        result = writer._sanitize_filename("  .ClassName.  ")
        assert result == "ClassName"

    def test_sanitize_filename_empty_result(self) -> None:
        """SWUT_WRITER_00039: Test sanitizing class name that becomes empty.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
        """
        writer = MarkdownWriter()
        result = writer._sanitize_filename("<<<")
        assert result == "UnnamedClass"

    def test_write_class_with_invalid_filename_chars(self, tmp_path: Path) -> None:
        """SWUT_WRITER_00040: Test writing a class with invalid filename characters.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
            SWR_WRITER_00006: Individual Class Markdown File Content
        """
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="<<atpVariation>>Class", package="M2::Test", is_abstract=False))

        writer = MarkdownWriter()
        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        # Check that the file was created with sanitized name
        class_file = tmp_path / "TestPackage" / "__atpVariation__Class.md"
        assert class_file.is_file()

        # Check that the content still has the original class name
        content = class_file.read_text(encoding="utf-8")
        assert "# <<atpVariation>>Class\n\n" in content
        assert "## Package\n\n" in content
        assert "TestPackage\n\n" in content
        assert "## Type\n\n" in content
        assert "Concrete\n\n" in content

    def test_write_class_with_atp_variation_only(self, tmp_path: Path) -> None:
        """SWUT_WRITER_00041: Test writing class with only atpVariation type.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
            SWR_WRITER_00006: Individual Class Markdown File Content
        """
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(name="MyClass", package="M2::Test", is_abstract=False, atp_type=ATPType.ATP_VARIATION)
        pkg.add_class(cls)

        writer = MarkdownWriter()
        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        class_file = tmp_path / "TestPackage" / "MyClass.md"
        content = class_file.read_text(encoding="utf-8")

        assert "## ATP Type\n\n" in content
        assert "* atpVariation\n" in content
        # Should not show atpMixedString
        assert "atpMixedString" not in content

    def test_write_class_with_atp_mixed_string_only(self, tmp_path: Path) -> None:
        """SWUT_WRITER_00042: Test writing class with only atpMixedString type.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
            SWR_WRITER_00006: Individual Class Markdown File Content
        """
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(name="MyClass", package="M2::Test", is_abstract=False, atp_type=ATPType.ATP_MIXED_STRING)
        pkg.add_class(cls)

        writer = MarkdownWriter()
        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        class_file = tmp_path / "TestPackage" / "MyClass.md"
        content = class_file.read_text(encoding="utf-8")

        assert "## ATP Type\n\n" in content
        assert "* atpMixedString\n" in content
        # Should not show atpVariation
        assert "atpVariation" not in content

    def test_write_class_with_atp_mixed_only(self, tmp_path: Path) -> None:
        """SWUT_WRITER_00043: Test writing class with only atpMixed type.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
            SWR_WRITER_00006: Individual Class Markdown File Content
        """
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(name="MyClass", package="M2::Test", is_abstract=False, atp_type=ATPType.ATP_MIXED)
        pkg.add_class(cls)

        writer = MarkdownWriter()
        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        class_file = tmp_path / "TestPackage" / "MyClass.md"
        content = class_file.read_text(encoding="utf-8")

        assert "## ATP Type\n\n" in content
        assert "* atpMixed\n" in content
        # Should not show atpVariation or atpMixedString
        assert "atpVariation" not in content
        assert "atpMixedString" not in content

    def test_write_class_without_atp_type_no_section(self, tmp_path: Path) -> None:
        """SWUT_WRITER_00044: Test that class without ATP type doesn't show ATP section.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
            SWR_WRITER_00006: Individual Class Markdown File Content
        """
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(name="MyClass", package="M2::Test", is_abstract=False)
        pkg.add_class(cls)

        writer = MarkdownWriter()
        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        class_file = tmp_path / "TestPackage" / "MyClass.md"
        content = class_file.read_text(encoding="utf-8")

        # Should not have ATP Type section
        assert "## ATP Type\n\n" not in content

    def test_atp_section_order(self, tmp_path: Path) -> None:
        """SWUT_WRITER_00045: Test that ATP section appears after Type and before Base Classes.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
            SWR_WRITER_00006: Individual Class Markdown File Content
        """
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(name="MyClass", package="M2::Test",
    is_abstract=True,
            atp_type=ATPType.ATP_VARIATION,
            bases=["BaseClass"]
        )
        pkg.add_class(cls)

        writer = MarkdownWriter()
        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        class_file = tmp_path / "TestPackage" / "MyClass.md"
        content = class_file.read_text(encoding="utf-8")

        # Find section positions
        type_idx = content.find("## Type\n\n")
        atp_idx = content.find("## ATP Type\n\n")
        base_idx = content.find("## Base Classes\n\n")

        # Verify order: Type < ATP Type < Base Classes
        assert type_idx != -1
        assert atp_idx != -1
        assert base_idx != -1
        assert type_idx < atp_idx
        assert atp_idx < base_idx

    def test_write_class_with_children(self, tmp_path: Path) -> None:
        """SWUT_WRITER_00047: Test writing a class with children to a file.

        Requirements:
            SWR_MODEL_00026: AUTOSAR Class Children Attribute
            SWR_WRITER_00005: Directory-Based Class File Output
            SWR_WRITER_00006: Individual Class Markdown File Content
        """
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(
            name="ParentClass",
            package="M2::Test",
            is_abstract=False,
            children=["ChildClass1", "ChildClass2", "ChildClass3"]
        )
        pkg.add_class(cls)

        writer = MarkdownWriter()
        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        class_file = tmp_path / "TestPackage" / "ParentClass.md"
        content = class_file.read_text(encoding="utf-8")

        # Verify Children section exists
        assert "## Children\n\n" in content
        assert "* ChildClass1\n" in content
        assert "* ChildClass2\n" in content
        assert "* ChildClass3\n" in content

    def test_write_class_without_children_no_section(self, tmp_path: Path) -> None:
        """SWUT_WRITER_00048: Test writing a class without children doesn't create Children section.

        Requirements:
            SWR_MODEL_00026: AUTOSAR Class Children Attribute
            SWR_WRITER_00005: Directory-Based Class File Output
            SWR_WRITER_00006: Individual Class Markdown File Content
        """
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(
            name="MyClass",
            package="M2::Test",
            is_abstract=False
        )
        pkg.add_class(cls)

        writer = MarkdownWriter()
        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        class_file = tmp_path / "TestPackage" / "MyClass.md"
        content = class_file.read_text(encoding="utf-8")

        # Verify Children section does NOT exist
        assert "## Children\n\n" not in content

    def test_children_section_order(self, tmp_path: Path) -> None:
        """SWUT_WRITER_00049: Test Children section appears after Base Classes and before Note.

        Requirements:
            SWR_MODEL_00026: AUTOSAR Class Children Attribute
            SWR_WRITER_00006: Individual Class Markdown File Content
        """
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(
            name="MyClass",
            package="M2::Test",
            is_abstract=True,
            bases=["BaseClass"],
            children=["ChildClass"],
            note="This is a test class"
        )
        pkg.add_class(cls)

        writer = MarkdownWriter()
        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        class_file = tmp_path / "TestPackage" / "MyClass.md"
        content = class_file.read_text(encoding="utf-8")

        # Find section positions
        type_idx = content.find("## Type\n\n")
        base_idx = content.find("## Base Classes\n\n")
        children_idx = content.find("## Children\n\n")
        note_idx = content.find("## Note\n\n")

        # Verify all sections exist
        assert type_idx != -1
        assert base_idx != -1
        assert children_idx != -1
        assert note_idx != -1

        # Verify order: Type < Base Classes < Children < Note
        assert type_idx < base_idx
        assert base_idx < children_idx
        assert children_idx < note_idx

    def test_main_hierarchy_no_atp_markers(self) -> None:
        """SWUT_WRITER_00046: Test that main hierarchy output doesn't show ATP markers.

        Requirements:
            SWR_WRITER_00002: Markdown Package Hierarchy Output
            SWR_WRITER_00003: Markdown Class Output Format
        """
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(name="MyClass", package="M2::Test",
    is_abstract=False,
            atp_type=ATPType.ATP_VARIATION
        )
        pkg.add_class(cls)

        writer = MarkdownWriter()
        result = writer.write_packages([pkg])

        # Should only show class name, no ATP markers
        expected = "* TestPackage\n  * MyClass\n"
        assert result == expected
        assert "atpVariation" not in result
        assert "atpMixedString" not in result

    def test_write_packages_with_enumeration(self) -> None:
        """Test write_packages correctly handles enumerations.

        Requirements:
            SWR_WRITER_00002: Markdown Package Hierarchy Output
        """
        from autosar_pdf2txt.models import AutosarEnumeration

        pkg = AutosarPackage(name="TestPackage")
        enum = AutosarEnumeration(name="MyEnum", package="M2::Test")
        pkg.add_type(enum)

        writer = MarkdownWriter()
        result = writer.write_packages([pkg])

        # Should show enumeration
        assert "* TestPackage\n" in result
        assert "  * MyEnum\n" in result

    def test_write_enumeration_with_note(self) -> None:
        """Test write_packages correctly handles enumerations with notes.

        Requirements:
            SWR_WRITER_00002: Markdown Package Hierarchy Output
        """
        pkg = AutosarPackage(name="TestPackage")
        enum = AutosarEnumeration(name="MyEnum", package="M2::Test")
        enum.note = "This is a test enumeration"
        pkg.add_type(enum)

        writer = MarkdownWriter()
        result = writer.write_packages([pkg])

        # Should show enumeration
        assert "* TestPackage\n" in result
        assert "  * MyEnum\n" in result

    def test_write_enumeration_literals_with_descriptions(self) -> None:
        """Test write_packages correctly handles enumeration literals with descriptions.

        Requirements:
            SWR_WRITER_00002: Markdown Package Hierarchy Output
        """
        pkg = AutosarPackage(name="TestPackage")
        enum = AutosarEnumeration(name="MyEnum", package="M2::Test")
        enum.enumeration_literals = [
            AutosarEnumLiteral(name="VALUE1", index=0, description="First value"),
            AutosarEnumLiteral(name="VALUE2", index=1, description="Second value"),
        ]
        pkg.add_type(enum)

        writer = MarkdownWriter()
        result = writer.write_packages([pkg])

        # Should show enumeration
        assert "* TestPackage\n" in result
        assert "  * MyEnum\n" in result

    def test_write_packages_to_files_with_enumeration(self) -> None:
        """Test write_packages_to_files correctly handles enumerations.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
            SWR_WRITER_00006: Individual Class Markdown File Content
        """
        import tempfile

        pkg = AutosarPackage(name="TestPackage")
        enum = AutosarEnumeration(name="MyEnum", package="M2::Test")
        enum.enumeration_literals = [
            AutosarEnumLiteral(name="VALUE1", index=0),
            AutosarEnumLiteral(name="VALUE2", index=1),
        ]
        pkg.add_type(enum)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "output.md"
            output_path.touch()

            writer = MarkdownWriter()
            writer.write_packages_to_files([pkg], output_path=output_path)

            # Check that enumeration file was created
            enum_file = Path(tmpdir) / "TestPackage" / "MyEnum.md"
            assert enum_file.exists()

            # Check enumeration file content
            content = enum_file.read_text()
            assert "# Package: TestPackage" in content
            assert "## Enumeration" in content
            assert "**MyEnum**" in content
            assert "VALUE1" in content
            assert "VALUE2" in content

    def test_write_packages_creates_directory_if_not_exists(self, tmp_path: Path) -> None:
        """Test that directories are created automatically if they don't exist.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output

        This test verifies that the writer creates destination directories
        automatically without requiring manual creation.
        """
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="MyClass", package="M2::Test", is_abstract=False))

        writer = MarkdownWriter()

        # Use a non-existent subdirectory path
        output_dir = tmp_path / "nonexistent" / "subdir"
        assert not output_dir.exists(), "Output directory should not exist initially"

        writer.write_packages_to_files([pkg], base_dir=output_dir)

        # Verify directory was created
        assert output_dir.exists(), "Output directory should be created"
        assert output_dir.is_dir(), "Output should be a directory"

        # Verify package directory was created
        pkg_dir = output_dir / "TestPackage"
        assert pkg_dir.exists(), "Package directory should be created"
        assert pkg_dir.is_dir(), "Package should be a directory"

        # Verify class file was created
        class_file = pkg_dir / "MyClass.md"
        assert class_file.exists(), "Class file should be created"
        assert class_file.is_file(), "Class should be a file"

    def test_subclasses_sorted_alphabetically(self, tmp_path: Path) -> None:
        """SWUT_WRITER_00050: Test Subclasses section is sorted alphabetically.

        Requirements:
            SWR_MODEL_00001: AUTOSAR Class Model
            SWR_WRITER_00006: Individual Class Markdown File Content
        """
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(
            name="ParentClass",
            package="M2::Test",
            is_abstract=False,
            subclasses=["Zulu", "Alpha", "Bravo", "Delta", "Charlie"]
        )
        pkg.add_class(cls)

        writer = MarkdownWriter()
        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        class_file = tmp_path / "TestPackage" / "ParentClass.md"
        content = class_file.read_text(encoding="utf-8")

        # Verify Subclasses section exists
        assert "## Subclasses\n\n" in content

        # Extract the Subclasses section
        subclasses_start = content.find("## Subclasses\n\n")
        subclasses_end = content.find("\n\n", subclasses_start + len("## Subclasses\n\n"))
        subclasses_section = content[subclasses_start:subclasses_end]

        # Verify subclasses are in alphabetical order
        lines = [line.strip() for line in subclasses_section.split("\n") if line.strip().startswith("*")]
        expected_order = ["* Alpha", "* Bravo", "* Charlie", "* Delta", "* Zulu"]
        assert lines == expected_order, f"Expected {expected_order}, got {lines}"

    def test_children_sorted_alphabetically(self, tmp_path: Path) -> None:
        """SWUT_WRITER_00051: Test Children section is sorted alphabetically.

        Requirements:
            SWR_MODEL_00026: AUTOSAR Class Children Attribute
            SWR_WRITER_00006: Individual Class Markdown File Content
        """
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(
            name="ParentClass",
            package="M2::Test",
            is_abstract=False,
            children=["Zulu", "Alpha", "Bravo", "Delta", "Charlie"]
        )
        pkg.add_class(cls)

        writer = MarkdownWriter()
        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        class_file = tmp_path / "TestPackage" / "ParentClass.md"
        content = class_file.read_text(encoding="utf-8")

        # Verify Children section exists
        assert "## Children\n\n" in content

        # Extract the Children section
        children_start = content.find("## Children\n\n")
        children_end = content.find("\n\n", children_start + len("## Children\n\n"))
        children_section = content[children_start:children_end]

        # Verify children are in alphabetical order
        lines = [line.strip() for line in children_section.split("\n") if line.strip().startswith("*")]
        expected_order = ["* Alpha", "* Bravo", "* Charlie", "* Delta", "* Zulu"]
        assert lines == expected_order, f"Expected {expected_order}, got {lines}"

    def test_write_class_with_source_and_note(self, tmp_path: Path) -> None:
        """Test writing a class with source and note sections.

        Requirements:
            SWR_WRITER_00006: Individual Class Markdown File Content
            SWR_WRITER_00008: Markdown Source Information Output
        """
        from autosar_pdf2txt.models.base import AutosarDocumentSource

        pkg = AutosarPackage(name="TestPackage")
        source = AutosarDocumentSource("AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf", 42)
        cls = AutosarClass(
            name="TestClass",
            package="M2::Test",
            is_abstract=False,
            sources=[source],
            note="This is a test note for the class."
        )
        pkg.add_class(cls)

        writer = MarkdownWriter()
        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        class_file = tmp_path / "TestPackage" / "TestClass.md"
        content = class_file.read_text(encoding="utf-8")

        # Verify Source section with table format
        assert "## Document Source\n\n" in content
        assert "| PDF File | Page | AUTOSAR Standard | Standard Release |" in content
        assert "|----------|------|------------------|------------------|" in content
        assert "| AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf | 42 | - | - |" in content

        # Verify Note section
        assert "## Note\n\n" in content
        assert "This is a test note for the class." in content

    def test_write_enumeration_with_source_note_and_literals(self, tmp_path: Path) -> None:
        """Test writing an enumeration with source, note, and literals.

        Requirements:
            SWR_WRITER_00006: Individual Class Markdown File Content
            SWR_WRITER_00008: Markdown Source Information Output
        """
        from autosar_pdf2txt.models.base import AutosarDocumentSource

        pkg = AutosarPackage(name="TestPackage")
        source = AutosarDocumentSource("AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf", 42)
        enum = AutosarEnumeration(
            name="TestEnum",
            package="M2::Test",
            sources=[source],
            note="This is a test note for the enumeration."
        )
        enum.enumeration_literals = [
            AutosarEnumLiteral(name="LITERAL1", index=0, description="First literal"),
            AutosarEnumLiteral(name="LITERAL2", index=1, description="Second literal"),
        ]
        pkg.add_enumeration(enum)

        writer = MarkdownWriter()
        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        enum_file = tmp_path / "TestPackage" / "TestEnum.md"
        content = enum_file.read_text(encoding="utf-8")

        # Verify Source section with table format
        assert "## Document Source\n\n" in content
        assert "| PDF File | Page | AUTOSAR Standard | Standard Release |" in content
        assert "|----------|------|------------------|------------------|" in content
        assert "| AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf | 42 | - | - |" in content

        # Verify Note section
        assert "## Note\n\n" in content
        assert "This is a test note for the enumeration." in content

        # Verify Enumeration Literals section
        assert "## Enumeration Literals\n\n" in content
        assert "* LITERAL1 (index=0)" in content
        assert "  * First literal" in content
        assert "* LITERAL2 (index=1)" in content
        assert "  * Second literal" in content

    def test_write_class_with_multiple_sources(self, tmp_path: Path) -> None:
        """Test writing a class with multiple sources in table format.

        Requirements:
            SWR_WRITER_00006: Individual Class Markdown File Content
            SWR_WRITER_00008: Markdown Source Information Output
        """
        from autosar_pdf2txt.models.base import AutosarDocumentSource

        pkg = AutosarPackage(name="TestPackage")
        source1 = AutosarDocumentSource("AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf", 42)
        source2 = AutosarDocumentSource("AUTOSAR_CP_TPS_SoftwareComponentTemplate.pdf", 15)
        cls = AutosarClass(
            name="TestClass",
            package="M2::Test",
            is_abstract=False,
            sources=[source1, source2]
        )
        pkg.add_class(cls)

        writer = MarkdownWriter()
        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        class_file = tmp_path / "TestPackage" / "TestClass.md"
        content = class_file.read_text(encoding="utf-8")

        # Verify Source section with table format
        assert "## Document Source\n\n" in content
        assert "| PDF File | Page | AUTOSAR Standard | Standard Release |" in content
        assert "|----------|------|------------------|------------------|" in content
        # Verify both sources are present (sorted alphabetically by PDF filename)
        assert "| AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf | 42 | - | - |" in content
        assert "| AUTOSAR_CP_TPS_SoftwareComponentTemplate.pdf | 15 | - | - |" in content

    def test_write_class_with_source_and_standard_info(self, tmp_path: Path) -> None:
        """Test writing a class with source including AUTOSAR standard information.

        Requirements:
            SWR_WRITER_00006: Individual Class Markdown File Content
            SWR_WRITER_00008: Markdown Source Information Output
        """
        from autosar_pdf2txt.models.base import AutosarDocumentSource

        pkg = AutosarPackage(name="TestPackage")
        source = AutosarDocumentSource(
            "AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf",
            42,
            autosar_standard="Classic Platform",
            standard_release="R23-11"
        )
        cls = AutosarClass(
            name="TestClass",
            package="M2::Test",
            is_abstract=False,
            sources=[source]
        )
        pkg.add_class(cls)

        writer = MarkdownWriter()
        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        class_file = tmp_path / "TestPackage" / "TestClass.md"
        content = class_file.read_text(encoding="utf-8")

        # Verify Source section with table format including standard info
        assert "## Document Source\n\n" in content
        assert "| PDF File | Page | AUTOSAR Standard | Standard Release |" in content
        assert "|----------|------|------------------|------------------|" in content
        assert "| AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf | 42 | Classic Platform | R23-11 |" in content
