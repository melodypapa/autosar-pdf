"""
测试 Parser 和 Model 的集成
"""

from autosar_pdf2txt.extractor.parser import extract_package_and_class_info


def test_extract_with_abstract_classes():
    """测试解析抽象类"""
    text = """
    Package M2::TestPackage
    Class AbstractClass abstract
    Class ConcreteClass
    Class AnotherAbstract abstract
    """

    packages = extract_package_and_class_info(text)

    assert len(packages) == 1
    pkg = packages[0]
    assert pkg.name == "TestPackage"
    assert pkg.total_classes == 3

    abstract_classes = [cls for cls in pkg.classes if cls.abstract]
    concrete_classes = [cls for cls in pkg.classes if not cls.abstract]

    assert len(abstract_classes) == 2
    assert len(concrete_classes) == 1

    assert abstract_classes[0].name == "AbstractClass"
    assert abstract_classes[1].name == "AnotherAbstract"
    assert concrete_classes[0].name == "ConcreteClass"


def test_extract_multiple_packages():
    """测试解析多个包"""
    text = """
    Package M2::PackageA
    Class ClassA1
    Class ClassA2 abstract

    Package M2::PackageB
    Class ClassB1
    Class ClassB2
    Class ClassB3 abstract
    """

    packages = extract_package_and_class_info(text)

    assert len(packages) == 2

    pkg_a = next((p for p in packages if p.name == "PackageA"), None)
    pkg_b = next((p for p in packages if p.name == "PackageB"), None)

    assert pkg_a is not None
    assert pkg_b is not None

    assert pkg_a.total_classes == 2
    assert pkg_a.total_abstract_classes == 1

    assert pkg_b.total_classes == 3
    assert pkg_b.total_abstract_classes == 1


def test_extract_empty_text():
    """测试解析空文本"""
    text = ""

    packages = extract_package_and_class_info(text)

    assert len(packages) == 0


def test_extract_no_classes():
    """测试只有包没有类"""
    text = """
    Package M2::EmptyPackage
    Package M2::AnotherEmptyPackage
    """

    packages = extract_package_and_class_info(text)

    assert len(packages) == 2
    assert all(pkg.total_classes == 0 for pkg in packages)


def test_case_insensitive_abstract():
    """测试 abstract 关键词不区分大小写"""
    text = """
    Package M2::TestPackage
    Class Class1 Abstract
    Class Class2 ABSTRACT
    Class Class3 abstract
    Class Class4 Abstract
    """

    packages = extract_package_and_class_info(text)

    assert len(packages) == 1
    pkg = packages[0]
    assert pkg.total_classes == 4
    assert pkg.total_abstract_classes == 4
