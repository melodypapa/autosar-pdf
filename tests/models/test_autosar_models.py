"""Tests for AutosarClass and AutosarPackage models.

Test coverage for autosar_models.py targeting 100%.
"""

import pytest

from autosar_pdf2txt.models import AutosarClass, AutosarPackage


class TestAutosarClass:
    """Tests for AutosarClass class."""

    def test_init_concrete_class(self) -> None:
        """Test creating a concrete class."""
        cls = AutosarClass(name="RunnableEntity", is_abstract=False)
        assert cls.name == "RunnableEntity"
        assert cls.is_abstract is False

    def test_init_abstract_class(self) -> None:
        """Test creating an abstract class."""
        cls = AutosarClass(name="InternalBehavior", is_abstract=True)
        assert cls.name == "InternalBehavior"
        assert cls.is_abstract is True

    def test_post_init_valid_name(self) -> None:
        """Test valid name validation."""
        cls = AutosarClass(name="ValidClass", is_abstract=False)
        assert cls.name == "ValidClass"

    def test_post_init_empty_name(self) -> None:
        """Test empty name raises ValueError."""
        with pytest.raises(ValueError, match="Class name cannot be empty"):
            AutosarClass(name="", is_abstract=False)

    def test_post_init_whitespace_name(self) -> None:
        """Test whitespace-only name raises ValueError."""
        with pytest.raises(ValueError, match="Class name cannot be empty"):
            AutosarClass(name="   ", is_abstract=False)

    def test_str_concrete_class(self) -> None:
        """Test string representation of concrete class."""
        cls = AutosarClass(name="MyClass", is_abstract=False)
        assert str(cls) == "MyClass"

    def test_str_abstract_class(self) -> None:
        """Test string representation of abstract class."""
        cls = AutosarClass(name="AbstractClass", is_abstract=True)
        assert str(cls) == "AbstractClass (abstract)"

    def test_repr(self) -> None:
        """Test __repr__ method."""
        cls = AutosarClass(name="TestClass", is_abstract=True)
        result = repr(cls)
        assert "AutosarClass" in result
        assert "name='TestClass'" in result
        assert "is_abstract=True" in result


class TestAutosarPackage:
    """Tests for AutosarPackage class."""

    def test_init_empty_package(self) -> None:
        """Test creating an empty package."""
        pkg = AutosarPackage(name="TestPackage")
        assert pkg.name == "TestPackage"
        assert len(pkg.classes) == 0
        assert len(pkg.subpackages) == 0

    def test_init_with_classes(self) -> None:
        """Test creating a package with classes."""
        cls1 = AutosarClass(name="Class1", is_abstract=False)
        cls2 = AutosarClass(name="Class2", is_abstract=True)
        pkg = AutosarPackage(name="TestPackage", classes=[cls1, cls2])
        assert len(pkg.classes) == 2
        assert pkg.classes[0].name == "Class1"
        assert pkg.classes[1].name == "Class2"

    def test_init_with_subpackages(self) -> None:
        """Test creating a package with subpackages."""
        subpkg = AutosarPackage(name="SubPackage")
        pkg = AutosarPackage(name="TestPackage", subpackages=[subpkg])
        assert len(pkg.subpackages) == 1
        assert pkg.subpackages[0].name == "SubPackage"

    def test_post_init_valid_name(self) -> None:
        """Test valid name validation."""
        pkg = AutosarPackage(name="ValidPackage")
        assert pkg.name == "ValidPackage"

    def test_post_init_empty_name(self) -> None:
        """Test empty name raises ValueError."""
        with pytest.raises(ValueError, match="Package name cannot be empty"):
            AutosarPackage(name="")

    def test_post_init_whitespace_name(self) -> None:
        """Test whitespace-only name raises ValueError."""
        with pytest.raises(ValueError, match="Package name cannot be empty"):
            AutosarPackage(name="   ")

    def test_add_class_success(self) -> None:
        """Test successfully adding a class."""
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(name="NewClass", is_abstract=False)
        pkg.add_class(cls)
        assert len(pkg.classes) == 1
        assert pkg.classes[0] == cls

    def test_add_class_duplicate(self) -> None:
        """Test adding duplicate class raises ValueError."""
        pkg = AutosarPackage(name="TestPackage")
        cls1 = AutosarClass(name="DuplicateClass", is_abstract=False)
        cls2 = AutosarClass(name="DuplicateClass", is_abstract=True)
        pkg.add_class(cls1)
        with pytest.raises(ValueError, match="already exists"):
            pkg.add_class(cls2)

    def test_add_subpackage_success(self) -> None:
        """Test successfully adding a subpackage."""
        pkg = AutosarPackage(name="ParentPackage")
        subpkg = AutosarPackage(name="ChildPackage")
        pkg.add_subpackage(subpkg)
        assert len(pkg.subpackages) == 1
        assert pkg.subpackages[0] == subpkg

    def test_add_subpackage_duplicate(self) -> None:
        """Test adding duplicate subpackage raises ValueError."""
        pkg = AutosarPackage(name="ParentPackage")
        subpkg1 = AutosarPackage(name="DuplicateSub")
        subpkg2 = AutosarPackage(name="DuplicateSub")
        pkg.add_subpackage(subpkg1)
        with pytest.raises(ValueError, match="already exists"):
            pkg.add_subpackage(subpkg2)

    def test_get_class_found(self) -> None:
        """Test finding an existing class."""
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(name="TargetClass", is_abstract=False)
        pkg.add_class(cls)
        result = pkg.get_class("TargetClass")
        assert result is not None
        assert result.name == "TargetClass"

    def test_get_class_not_found(self) -> None:
        """Test finding a non-existent class."""
        pkg = AutosarPackage(name="TestPackage")
        result = pkg.get_class("NonExistent")
        assert result is None

    def test_get_subpackage_found(self) -> None:
        """Test finding an existing subpackage."""
        pkg = AutosarPackage(name="ParentPackage")
        subpkg = AutosarPackage(name="TargetSub")
        pkg.add_subpackage(subpkg)
        result = pkg.get_subpackage("TargetSub")
        assert result is not None
        assert result.name == "TargetSub"

    def test_get_subpackage_not_found(self) -> None:
        """Test finding a non-existent subpackage."""
        pkg = AutosarPackage(name="ParentPackage")
        result = pkg.get_subpackage("NonExistent")
        assert result is None

    def test_has_class_true(self) -> None:
        """Test has_class returns True when class exists."""
        pkg = AutosarPackage(name="TestPackage")
        cls = AutosarClass(name="ExistingClass", is_abstract=False)
        pkg.add_class(cls)
        assert pkg.has_class("ExistingClass") is True

    def test_has_class_false(self) -> None:
        """Test has_class returns False when class doesn't exist."""
        pkg = AutosarPackage(name="TestPackage")
        assert pkg.has_class("NonExistent") is False

    def test_has_subpackage_true(self) -> None:
        """Test has_subpackage returns True when subpackage exists."""
        pkg = AutosarPackage(name="ParentPackage")
        subpkg = AutosarPackage(name="ExistingSub")
        pkg.add_subpackage(subpkg)
        assert pkg.has_subpackage("ExistingSub") is True

    def test_has_subpackage_false(self) -> None:
        """Test has_subpackage returns False when subpackage doesn't exist."""
        pkg = AutosarPackage(name="ParentPackage")
        assert pkg.has_subpackage("NonExistent") is False

    def test_str_package_with_classes_only(self) -> None:
        """Test string representation of package with only classes."""
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="Class1", is_abstract=False))
        pkg.add_class(AutosarClass(name="Class2", is_abstract=True))
        result = str(pkg)
        assert "TestPackage" in result
        assert "2 classes" in result

    def test_str_package_with_subpackages_only(self) -> None:
        """Test string representation of package with only subpackages."""
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_subpackage(AutosarPackage(name="Sub1"))
        pkg.add_subpackage(AutosarPackage(name="Sub2"))
        result = str(pkg)
        assert "TestPackage" in result
        assert "2 subpackages" in result

    def test_str_package_with_both(self) -> None:
        """Test string representation of package with both classes and subpackages."""
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="Class1", is_abstract=False))
        pkg.add_subpackage(AutosarPackage(name="Sub1"))
        result = str(pkg)
        assert "TestPackage" in result
        assert "1 classes" in result
        assert "1 subpackages" in result

    def test_str_empty_package(self) -> None:
        """Test string representation of empty package."""
        pkg = AutosarPackage(name="EmptyPackage")
        result = str(pkg)
        assert "EmptyPackage" in result

    def test_repr(self) -> None:
        """Test __repr__ method."""
        pkg = AutosarPackage(name="TestPackage")
        pkg.add_class(AutosarClass(name="Class1", is_abstract=False))
        pkg.add_subpackage(AutosarPackage(name="Sub1"))
        result = repr(pkg)
        assert "AutosarPackage" in result
        assert "name='TestPackage'" in result
        assert "classes=1" in result
        assert "subpackages=1" in result

    def test_nested_packages(self) -> None:
        """Test nested package structure."""
        root = AutosarPackage(name="Root")
        child = AutosarPackage(name="Child")
        grandchild = AutosarPackage(name="Grandchild")

        root.add_subpackage(child)
        child.add_subpackage(grandchild)

        assert len(root.subpackages) == 1
        assert root.get_subpackage("Child") == child
        assert child.get_subpackage("Grandchild") == grandchild
