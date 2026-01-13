"""
测试 Package 和 Class 模型
"""

from autosar_pdf2txt.extractor.models import Package, Class


def test_class_creation():
    """测试 Class 对象创建"""
    cls = Class(name="TestClass", abstract=False)
    assert cls.name == "TestClass"
    assert cls.abstract is False

    abstract_cls = Class(name="AbstractClass", abstract=True)
    assert abstract_cls.name == "AbstractClass"
    assert abstract_cls.abstract is True


def test_class_default_abstract():
    """测试 Class 对象的默认 abstract 值"""
    cls = Class(name="NonAbstractClass")
    assert cls.abstract is False


def test_package_creation():
    """测试 Package 对象创建"""
    classes = [Class("Class1"), Class("Class2", abstract=True)]
    pkg = Package(name="TestPackage", classes=classes)

    assert pkg.name == "TestPackage"
    assert len(pkg.classes) == 2
    assert pkg.classes[0].name == "Class1"
    assert pkg.classes[1].name == "Class2"
    assert pkg.classes[1].abstract is True


def test_package_total_classes():
    """测试 Package 的 total_classes 属性"""
    classes = [Class("Class1"), Class("Class2"), Class("Class3")]
    pkg = Package(name="TestPackage", classes=classes)

    assert pkg.total_classes == 3


def test_package_total_abstract_classes():
    """测试 Package 的 total_abstract_classes 属性"""
    classes = [
        Class("Class1", abstract=True),
        Class("Class2", abstract=False),
        Class("Class3", abstract=True),
    ]
    pkg = Package(name="TestPackage", classes=classes)

    assert pkg.total_abstract_classes == 2


def test_package_with_empty_classes():
    """测试空类列表的 Package"""
    pkg = Package(name="EmptyPackage", classes=[])
    assert pkg.total_classes == 0
    assert pkg.total_abstract_classes == 0


def test_class_equality():
    """测试 Class 对象相等性"""
    cls1 = Class(name="TestClass", abstract=False)
    cls2 = Class(name="TestClass", abstract=False)
    cls3 = Class(name="DifferentClass", abstract=False)

    assert cls1.name == cls2.name
    assert cls1.name != cls3.name


def test_package_equality():
    """测试 Package 对象相等性"""
    classes1 = [Class("Class1"), Class("Class2")]
    classes2 = [Class("Class1"), Class("Class2")]
    pkg1 = Package(name="TestPackage", classes=classes1)
    pkg2 = Package(name="TestPackage", classes=classes2)

    assert pkg1.name == pkg2.name
    assert pkg1.total_classes == pkg2.total_classes
