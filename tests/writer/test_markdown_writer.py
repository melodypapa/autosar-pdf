"""Tests for markdown writer.

Test coverage for markdown_writer.py targeting 100%.
"""

from pathlib import Path

from autosar_pdf2txt.models import AutosarAttribute, AutosarClass, AutosarPackage
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


class TestMarkdownWriterFiles:
    """Tests for MarkdownWriter directory-based file output.

    Requirements:
        SWR_WRITER_00005: Directory-Based Class File Output
    """

    def test_write_single_class_to_file(self, tmp_path: Path) -> None:
        """Test writing a single class to a file.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
            SWR_WRITER_00006: Individual Class Markdown File Content
        """
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="MyClass", is_abstract=False))

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
        """Test writing an abstract class to a file.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
            SWR_WRITER_00006: Individual Class Markdown File Content
        """
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="AbstractClass", is_abstract=True))

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
        """Test writing multiple classes to separate files.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
        """
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="Class1", is_abstract=False))
        pkg.add_class(AutosarClass(name="Class2", is_abstract=True))
        pkg.add_class(AutosarClass(name="Class3", is_abstract=False))

        writer = MarkdownWriter()
        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        # Check all files exist
        pkg_dir = tmp_path / "TestPackage"
        assert (pkg_dir / "Class1.md").is_file()
        assert (pkg_dir / "Class2.md").is_file()
        assert (pkg_dir / "Class3.md").is_file()

    def test_write_nested_packages_to_files(self, tmp_path: Path) -> None:
        """Test writing nested packages to directory structure.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
        """
        root = AutosarPackage(name="RootPackage")
        child = AutosarPackage(name="ChildPackage")
        child.add_class(AutosarClass(name="ChildClass", is_abstract=False))
        root.add_subpackage(child)

        writer = MarkdownWriter()
        writer.write_packages_to_files([root], base_dir=tmp_path)

        # Check directory structure
        child_dir = tmp_path / "RootPackage" / "ChildPackage"
        assert child_dir.is_dir()

        # Check class file exists in nested directory
        class_file = child_dir / "ChildClass.md"
        assert class_file.is_file()

    def test_write_class_with_attributes(self, tmp_path: Path) -> None:
        """Test writing a class with attributes to file.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
            SWR_WRITER_00006: Individual Class Markdown File Content
        """
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(name="MyClass", is_abstract=False)
        cls.attributes["attr1"] = AutosarAttribute(name="attr1", type="String", is_ref=False)
        cls.attributes["attr2"] = AutosarAttribute(name="attr2", type="Integer", is_ref=True)
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
        assert "* attr1 : String\n" in content
        assert "* attr2 : Integer (ref)\n" in content

    def test_write_class_with_base_classes(self, tmp_path: Path) -> None:
        """Test writing a class with base classes to file.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
            SWR_WRITER_00006: Individual Class Markdown File Content
        """
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(name="DerivedClass", is_abstract=False)
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

    def test_write_class_with_note(self, tmp_path: Path) -> None:
        """Test writing a class with a note to file.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
            SWR_WRITER_00006: Individual Class Markdown File Content
        """
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(name="MyClass", is_abstract=False)
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
        """Test writing a class with all fields to file.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
            SWR_WRITER_00006: Individual Class Markdown File Content
        """
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(name="CompleteClass", is_abstract=True)
        cls.bases = ["BaseClass"]
        cls.attributes["attr1"] = AutosarAttribute(name="attr1", type="String", is_ref=False)
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
        assert "* attr1 : String\n" in content
        assert "## Note\n\n" in content
        assert "Complete documentation." in content

    def test_class_file_content_structure(self, tmp_path: Path) -> None:
        """Test that class file content follows SWR_WRITER_00006 structure.

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
        cls = AutosarClass(name="BswInternalBehavior", is_abstract=True)
        cls.bases = ["IBswInternalBehavior", "IReferable"]
        cls.attributes["swDataDefProps"] = AutosarAttribute(
            name="swDataDefProps", type="SwDataDefProps", is_ref=True
        )
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

        # Verify attributes list with reference indicator
        assert "* swDataDefProps : SwDataDefProps (ref)\n" in content

    def test_concrete_class_type_indicator(self, tmp_path: Path) -> None:
        """Test that concrete classes have correct type indicator.

        Requirements:
            SWR_WRITER_00006: Individual Class Markdown File Content
        """
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(name="ConcreteClass", is_abstract=False)
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
        """Test writing an empty package creates directory but no files.

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
        """Test writing multiple top-level packages to files.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
        """
        pkg1 = AutosarPackage(name="Package1")
        pkg1.add_class(AutosarClass(name="Class1", is_abstract=False))

        pkg2 = AutosarPackage(name="Package2")
        pkg2.add_class(AutosarClass(name="Class2", is_abstract=False))

        writer = MarkdownWriter()
        writer.write_packages_to_files([pkg1, pkg2], base_dir=tmp_path)

        # Both directories should exist
        assert (tmp_path / "Package1").is_dir()
        assert (tmp_path / "Package2").is_dir()

        # Both class files should exist
        assert (tmp_path / "Package1" / "Class1.md").is_file()
        assert (tmp_path / "Package2" / "Class2.md").is_file()

    def test_write_packages_with_pathlib_path(self, tmp_path: Path) -> None:
        """Test writing packages with pathlib.Path object.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
        """
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="MyClass", is_abstract=False))

        writer = MarkdownWriter()
        # Use pathlib.Path directly instead of string
        writer.write_packages_to_files([pkg], base_dir=tmp_path)

        class_file = tmp_path / "TestPackage" / "MyClass.md"
        assert class_file.is_file()

    def test_write_packages_with_output_path(self, tmp_path: Path) -> None:
        """Test writing packages with output_path parameter.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output

        The root directory should be the same as the output markdown file location.
        """
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="MyClass", is_abstract=False))

        writer = MarkdownWriter()
        output_file = tmp_path / "output.md"
        writer.write_packages_to_files([pkg], output_path=output_file)

        # Root directory should be the same as output file location (tmp_path)
        pkg_dir = tmp_path / "TestPackage"
        assert pkg_dir.is_dir()

        class_file = pkg_dir / "MyClass.md"
        assert class_file.is_file()

    def test_write_packages_with_output_path_nested(self, tmp_path: Path) -> None:
        """Test writing packages with output_path in subdirectory.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output

        The root directory should be the same as the output markdown file location.
        """
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="MyClass", is_abstract=False))

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
        """Test that providing both output_path and base_dir raises ValueError.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
        """
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="MyClass", is_abstract=False))

        writer = MarkdownWriter()

        # Test with both parameters
        try:
            writer.write_packages_to_files([pkg], output_path="/tmp/output.md", base_dir="/tmp")
            assert False, "Expected ValueError for both parameters"
        except ValueError as e:
            assert "both" in str(e).lower() or "cannot specify both" in str(e).lower()

    def test_write_packages_invalid_neither_parameter(self) -> None:
        """Test that providing neither output_path nor base_dir raises ValueError.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
        """
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="MyClass", is_abstract=False))

        writer = MarkdownWriter()

        # Test with neither parameter
        try:
            writer.write_packages_to_files([pkg])  # type: ignore
            assert False, "Expected ValueError for neither parameter"
        except ValueError as e:
            assert "must specify" in str(e).lower() or "either" in str(e).lower()

    def test_write_packages_invalid_base_dir(self) -> None:
        """Test that invalid base directory raises ValueError.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
        """
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="MyClass", is_abstract=False))

        writer = MarkdownWriter()

        # Test with empty string
        try:
            writer.write_packages_to_files([pkg], base_dir="")
            assert False, "Expected ValueError for empty base_dir"
        except ValueError as e:
            assert "base_dir" in str(e).lower()

    def test_write_packages_invalid_output_path(self) -> None:
        """Test that invalid output path raises ValueError.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
        """
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="MyClass", is_abstract=False))

        writer = MarkdownWriter()

        # Test with empty string
        try:
            writer.write_packages_to_files([pkg], output_path="")
            assert False, "Expected ValueError for empty output_path"
        except ValueError as e:
            assert "output_path" in str(e).lower()

    def test_write_deeply_nested_packages_to_files(self, tmp_path: Path) -> None:
        """Test writing deeply nested package structure.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
        """
        level1 = AutosarPackage(name="Level1")
        level2 = AutosarPackage(name="Level2")
        level3 = AutosarPackage(name="Level3")
        level3.add_class(AutosarClass(name="DeepClass", is_abstract=False))
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

    def test_sanitize_filename_normal_name(self) -> None:
        """Test sanitizing a normal class name.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
        """
        writer = MarkdownWriter()
        result = writer._sanitize_filename("NormalClass")
        assert result == "NormalClass"

    def test_sanitize_filename_invalid_chars(self) -> None:
        """Test sanitizing class name with invalid characters.

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
        """Test sanitizing class name with leading/trailing spaces and dots.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
        """
        writer = MarkdownWriter()
        result = writer._sanitize_filename("  .ClassName.  ")
        assert result == "ClassName"

    def test_sanitize_filename_empty_result(self) -> None:
        """Test sanitizing class name that becomes empty.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
        """
        writer = MarkdownWriter()
        result = writer._sanitize_filename("<<<")
        assert result == "UnnamedClass"

    def test_write_class_with_invalid_filename_chars(self, tmp_path: Path) -> None:
        """Test writing a class with invalid filename characters.

        Requirements:
            SWR_WRITER_00005: Directory-Based Class File Output
            SWR_WRITER_00006: Individual Class Markdown File Content
        """
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="<<atpVariation>>Class", is_abstract=False))

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
