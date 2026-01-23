# Software Test Cases

## autosar-pdf2txt Test Cases

This document contains all test cases extracted from the test suite of the autosar-pdf2txt package. Each test case maps to one or more software requirements from `requirements.md`.

## Maturity Levels

Each test case has a maturity level that indicates its status:

- **draft**: Newly created test case, under review, or not yet implemented
- **accept**: Accepted test case, implemented and passing
- **invalid**: Deprecated test case, superseded, or no longer applicable

All existing test cases in this document are currently at maturity level **accept**.

### 1. Model Tests

#### SWUT_MODEL_00001
**Title**: Test Initialization with Default Settings

**Maturity**: accept

**Description**: Verify that MarkdownWriter can be initialized without parameters.

**Precondition**: None

**Test Steps**:
1. Create a MarkdownWriter instance without parameters

**Expected Result**: Writer instance is created successfully

**Requirements Coverage**: SWR_WRITER_00001

---

#### SWUT_MODEL_00002
**Title**: Test Creating a Concrete AUTOSAR Class

**Maturity**: accept

**Description**: Verify that an AUTOSAR class can be created with name and abstract flag.

**Precondition**: None

**Test Steps**:
1. Create an AutosarClass with name="RunnableEntity" and is_abstract=False
2. Verify the name attribute is set to "RunnableEntity"
3. Verify the is_abstract attribute is set to False

**Expected Result**: Class is created with correct attributes

**Requirements Coverage**: SWR_MODEL_00001

---

#### SWUT_MODEL_00003
**Title**: Test Creating an Abstract AUTOSAR Class

**Maturity**: accept

**Description**: Verify that an abstract AUTOSAR class can be created.

**Precondition**: None

**Test Steps**:
1. Create an AutosarClass with name="InternalBehavior" and is_abstract=True
2. Verify the name attribute is set to "InternalBehavior"
3. Verify the is_abstract attribute is set to True

**Expected Result**: Abstract class is created with correct attributes

**Requirements Coverage**: SWR_MODEL_00001

---

#### SWUT_MODEL_00004
**Title**: Test Valid Class Name Validation

**Maturity**: accept

**Description**: Verify that a valid class name is accepted during initialization.

**Precondition**: None

**Test Steps**:
1. Create an AutosarClass with name="ValidClass"
2. Verify the name attribute is set to "ValidClass"

**Expected Result**: Class is created successfully

**Requirements Coverage**: SWR_MODEL_00002

---

#### SWUT_MODEL_00005
**Title**: Test Empty Class Name Raises ValueError

**Maturity**: accept

**Description**: Verify that empty class names are rejected with ValueError.

**Precondition**: None

**Test Steps**:
1. Attempt to create an AutosarClass with name=""
2. Verify that ValueError is raised with message "Class name cannot be empty"

**Expected Result**: ValueError is raised

**Requirements Coverage**: SWR_MODEL_00002

---

#### SWUT_MODEL_00006
**Title**: Test Whitespace-Only Class Name Raises ValueError

**Maturity**: accept

**Description**: Verify that whitespace-only class names are rejected with ValueError.

**Precondition**: None

**Test Steps**:
1. Attempt to create an AutosarClass with name="   "
2. Verify that ValueError is raised with message "Class name cannot be empty"

**Expected Result**: ValueError is raised

**Requirements Coverage**: SWR_MODEL_00002

---

#### SWUT_MODEL_00007
**Title**: Test String Representation of Concrete Class

**Maturity**: accept

**Description**: Verify that the string representation of a concrete class shows the class name.

**Precondition**: An AutosarClass instance exists

**Test Steps**:
1. Create an AutosarClass with name="MyClass" and is_abstract=False
2. Call str() on the class instance

**Expected Result**: String representation returns "MyClass"

**Requirements Coverage**: SWR_MODEL_00003

---

#### SWUT_MODEL_00008
**Title**: Test String Representation of Abstract Class

**Maturity**: accept

**Description**: Verify that the string representation of an abstract class includes "(abstract)" suffix.

**Precondition**: An AutosarClass instance exists

**Test Steps**:
1. Create an AutosarClass with name="AbstractClass" and is_abstract=True
2. Call str() on the class instance

**Expected Result**: String representation returns "AbstractClass (abstract)"

**Requirements Coverage**: SWR_MODEL_00003

---

#### SWUT_MODEL_00009
**Title**: Test Debug Representation of AUTOSAR Class

**Maturity**: accept

**Description**: Verify that the debug representation shows all attributes.

**Precondition**: An AutosarClass instance exists

**Test Steps**:
1. Create an AutosarClass with name="TestClass" and is_abstract=True
2. Call repr() on the class instance
3. Verify that "AutosarClass" is in the result
4. Verify that "name='TestClass'" is in the result
5. Verify that "is_abstract=True" is in the result

**Expected Result**: Debug representation contains all class attributes

**Requirements Coverage**: SWR_MODEL_00003

---

#### SWUT_MODEL_00010
**Title**: Test Creating Class with Empty Attributes Dictionary

**Maturity**: accept

**Description**: Verify that a class can be created with an empty attributes dictionary (default).

**Precondition**: None

**Test Steps**:
1. Create an AutosarClass with name="Component"
2. Verify the attributes dictionary is empty
3. Verify len(attributes) is 0

**Expected Result**: Class is created with empty attributes dict

**Requirements Coverage**: SWR_MODEL_00001

---

#### SWUT_MODEL_00011
**Title**: Test Creating Class with Attributes

**Maturity**: accept

**Description**: Verify that a class can be created with attributes.

**Precondition**: Two AutosarAttribute instances exist

**Test Steps**:
1. Create two AutosarAttribute instances (attr1: "dataReadPort", type="PPortPrototype", is_ref=True; attr2: "id", type="uint32", is_ref=False)
2. Create an AutosarClass with attributes={"dataReadPort": attr1, "id": attr2}
3. Verify the class has 2 attributes
4. Verify "dataReadPort" and "id" are in the attributes dict

**Expected Result**: Class is created with both attributes

**Requirements Coverage**: SWR_MODEL_00001

---

#### SWUT_MODEL_00012
**Title**: Test Debug Representation Shows Attributes Count

**Maturity**: accept

**Description**: Verify that __repr__ includes the attributes count.

**Precondition**: An AutosarClass instance with attributes exists

**Test Steps**:
1. Create an AutosarClass with name="Component" and multiple attributes
2. Call repr(cls)
3. Verify "attributes=2" is in the result (or actual count)

**Expected Result**: Debug representation shows attributes count

**Requirements Coverage**: SWR_MODEL_00003

---

#### SWUT_MODEL_00013
**Title**: Test Creating Class with Empty Bases List

**Maturity**: accept

**Description**: Verify that a class can be created with an empty bases list (default).

**Precondition**: None

**Test Steps**:
1. Create an AutosarClass with name="MyClass"
2. Verify the bases list is empty
3. Verify len(bases) is 0

**Expected Result**: Class is created with empty bases list

**Requirements Coverage**: SWR_MODEL_00001

---

#### SWUT_MODEL_00014
**Title**: Test Creating Class with Base Classes

**Maturity**: accept

**Description**: Verify that a class can be created with base classes for inheritance.

**Precondition**: None

**Test Steps**:
1. Create an AutosarClass with name="DerivedClass", bases=["BaseClass1", "BaseClass2"]
2. Verify the class has 2 bases
3. Verify "BaseClass1" and "BaseClass2" are in the bases list

**Expected Result**: Class is created with base classes

**Requirements Coverage**: SWR_MODEL_00001

---

#### SWUT_MODEL_00015
**Title**: Test Creating Class with Single Base Class

**Maturity**: accept

**Description**: Verify that a class can be created with a single base class.

**Precondition**: None

**Test Steps**:
1. Create an AutosarClass with name="DerivedClass", bases=["BaseClass"]
2. Verify the class has 1 base
3. Verify the base is "BaseClass"

**Expected Result**: Class is created with single base class

**Requirements Coverage**: SWR_MODEL_00001

---

#### SWUT_MODEL_00016
**Title**: Test Debug Representation Shows Bases Count

**Maturity**: accept

**Description**: Verify that __repr__ includes the bases count.

**Precondition**: An AutosarClass instance with bases exists

**Test Steps**:
1. Create an AutosarClass with name="DerivedClass", bases=["Base1", "Base2"]
2. Call repr(cls)
3. Verify "bases=2" is in the result

**Expected Result**: Debug representation shows bases count

**Requirements Coverage**: SWR_MODEL_00003

---

#### SWUT_MODEL_00017
**Title**: Test Creating Class with None Note (Default)

**Maturity**: accept

**Description**: Verify that a class can be created with None note (default).

**Precondition**: None

**Test Steps**:
1. Create an AutosarClass with name="MyClass"
2. Verify the note is None

**Expected Result**: Class is created with None note

**Requirements Coverage**: SWR_MODEL_00001

---

#### SWUT_MODEL_00018
**Title**: Test Creating Class with Note

**Maturity**: accept

**Description**: Verify that a class can be created with a note.

**Precondition**: None

**Test Steps**:
1. Create an AutosarClass with name="MyClass", note="This is a documentation note"
2. Verify the note is "This is a documentation note"

**Expected Result**: Class is created with note

**Requirements Coverage**: SWR_MODEL_00001

---

#### SWUT_MODEL_00019
**Title**: Test Creating Class with Empty String Note

**Maturity**: accept

**Description**: Verify that a class can be created with an empty string note.

**Precondition**: None

**Test Steps**:
1. Create an AutosarClass with name="MyClass", note=""
2. Verify the note is ""

**Expected Result**: Class is created with empty note

**Requirements Coverage**: SWR_MODEL_00001

---

#### SWUT_MODEL_00020
**Title**: Test Debug Representation Shows Note Presence

**Maturity**: accept

**Description**: Verify that __repr__ includes whether a note is present.

**Precondition**: An AutosarClass instance with note exists

**Test Steps**:
1. Create an AutosarClass with name="MyClass", note="Documentation"
2. Call repr(cls)
3. Verify "note=True" is in the result

**Expected Result**: Debug representation shows note presence

**Requirements Coverage**: SWR_MODEL_00003

---

#### SWUT_MODEL_00021
**Title**: Test Creating Class with All Fields Populated

**Maturity**: accept

**Description**: Verify that a class can be created with all fields populated.

**Precondition**: AutosarAttribute instances exist

**Test Steps**:
1. Create an AutosarAttribute with name="port", type="PPortPrototype", is_ref=True
2. Create an AutosarClass with name="CompleteClass", is_abstract=False, attributes={"port": attr}, bases=["Base1", "Base2"], note="Complete example"
3. Verify name is "CompleteClass"
4. Verify is_abstract is False
5. Verify len(attributes) is 1
6. Verify len(bases) is 2
7. Verify note is "Complete example"

**Expected Result**: Class is created with all fields correctly set

**Requirements Coverage**: SWR_MODEL_00001

---

#### SWUT_MODEL_00022
**Title**: Test Bases List Mutation

**Maturity**: accept

**Description**: Verify that the bases list can be mutated after class creation.

**Precondition**: An AutosarClass instance exists

**Test Steps**:
1. Create an AutosarClass with name="MyClass"
2. Append "BaseClass" to cls.bases
3. Verify len(bases) is 1
4. Verify "BaseClass" is in bases

**Expected Result**: Bases list can be mutated

**Requirements Coverage**: SWR_MODEL_00001

---

#### SWUT_MODEL_00023
**Title**: Test Note Reassignment

**Maturity**: accept

**Description**: Verify that the note can be reassigned after class creation.

**Precondition**: An AutosarClass instance exists

**Test Steps**:
1. Create an AutosarClass with name="MyClass"
2. Set cls.note = "Updated note"
3. Verify cls.note is "Updated note"

**Expected Result**: Note can be reassigned

**Requirements Coverage**: SWR_MODEL_00001

---

#### SWUT_MODEL_00071
**Title**: Test Default Parent Is None

**Maturity**: accept

**Description**: Verify that parent defaults to None.

**Precondition**: None

**Test Steps**:
1. Create an AutosarClass with name="MyClass", package="M2::Test", is_abstract=False
2. Verify cls.parent is None

**Expected Result**: Parent is None by default

**Requirements Coverage**: SWR_MODEL_00022

---

#### SWUT_MODEL_00072
**Title**: Test Creating Class with Parent

**Maturity**: accept

**Description**: Verify that a class can be created with a parent.

**Precondition**: A parent AutosarClass instance exists

**Test Steps**:
1. Create parent_cls with name="ParentClass", package="M2::Test", is_abstract=False
2. Create child_cls with name="ChildClass", package="M2::Test", is_abstract=False, parent=parent_cls
3. Verify child_cls.parent is parent_cls
4. Verify child_cls.parent.name is "ParentClass"

**Expected Result**: Class is created with parent reference

**Requirements Coverage**: SWR_MODEL_00022

---

#### SWUT_MODEL_00073
**Title**: Test Parent Reference Maintains Object

**Maturity**: accept

**Description**: Verify that parent maintains the actual object reference.

**Precondition**: Parent and child AutosarClass instances exist

**Test Steps**:
1. Create parent with name="ParentClass", package="M2::Test", is_abstract=False
2. Create child with name="ChildClass", package="M2::Test", is_abstract=False, parent=parent
3. Verify child.parent is parent (same object)
4. Verify accessing parent attributes works (e.g., parent.name)

**Expected Result**: Parent reference is maintained correctly

**Requirements Coverage**: SWR_MODEL_00022

---

#### SWUT_MODEL_00074
**Title**: Test Debug Representation Shows Parent Name

**Maturity**: accept

**Description**: Verify that __repr__ includes parent name when parent is set.

**Precondition**: Parent and child AutosarClass instances exist

**Test Steps**:
1. Create parent with name="ParentClass", package="M2::Test", is_abstract=False
2. Create child with name="ChildClass", package="M2::Test", is_abstract=False, parent=parent
3. Call repr(child)
4. Verify "parent=ParentClass" is in the result

**Expected Result**: Debug representation includes parent name

**Requirements Coverage**: SWR_MODEL_00022

---

#### SWUT_MODEL_00075
**Title**: Test Debug Representation Shows Parent None When No Parent

**Maturity**: accept

**Description**: Verify that __repr__ shows parent=None when no parent.

**Precondition**: An AutosarClass instance without parent exists

**Test Steps**:
1. Create cls with name="MyClass", package="M2::Test", is_abstract=False
2. Call repr(cls)
3. Verify "parent=None" is in the result

**Expected Result**: Debug representation shows parent=None

**Requirements Coverage**: SWR_MODEL_00022

---

#### SWUT_MODEL_00076
**Title**: Test Parent Can Be Reassigned

**Maturity**: accept

**Description**: Verify that parent can be reassigned after class creation.

**Precondition**: Two potential parent AutosarClass instances exist

**Test Steps**:
1. Create parent1 with name="Parent1", package="M2::Test", is_abstract=False
2. Create parent2 with name="Parent2", package="M2::Test", is_abstract=False
3. Create child with name="ChildClass", package="M2::Test", is_abstract=False, parent=parent1
4. Verify child.parent is parent1
5. Set child.parent = parent2
6. Verify child.parent is parent2
7. Verify child.parent.name is "Parent2"

**Expected Result**: Parent can be reassigned

**Requirements Coverage**: SWR_MODEL_00022

---

#### SWUT_MODEL_00077
**Title**: Test Default Children Is Empty List

**Maturity**: accept

**Description**: Verify that children defaults to empty list.

**Precondition**: None

**Test Steps**:
1. Create an AutosarClass with name="MyClass", package="M2::Test", is_abstract=False
2. Verify cls.children is []
3. Verify len(cls.children) is 0

**Expected Result**: Children is empty list by default

**Requirements Coverage**: SWR_MODEL_00026

---

#### SWUT_MODEL_00078
**Title**: Test Creating Class with Children

**Maturity**: accept

**Description**: Verify that a class can be created with children.

**Precondition**: None

**Test Steps**:
1. Create an AutosarClass with name="ParentClass", package="M2::Test", is_abstract=False, children=["Child1", "Child2"]
2. Verify len(cls.children) is 2
3. Verify "Child1" is in cls.children
4. Verify "Child2" is in cls.children

**Expected Result**: Class is created with children list

**Requirements Coverage**: SWR_MODEL_00026

---

#### SWUT_MODEL_00079
**Title**: Test Children List Mutation

**Maturity**: accept

**Description**: Verify that the children list can be mutated after class creation.

**Precondition**: An AutosarClass instance exists

**Test Steps**:
1. Create an AutosarClass with name="ParentClass", package="M2::Test", is_abstract=False
2. Verify cls.children is []
3. Append "Child1" to cls.children
4. Append "Child2" to cls.children
5. Verify len(cls.children) is 2
6. Remove "Child1" from cls.children
7. Verify len(cls.children) is 1
8. Verify "Child2" is in cls.children

**Expected Result**: Children list can be mutated

**Requirements Coverage**: SWR_MODEL_00026

---

#### SWUT_MODEL_00080
**Title**: Test Debug Representation Shows Children Count

**Maturity**: accept

**Description**: Verify that __repr__ includes children count.

**Precondition**: An AutosarClass instance with children exists

**Test Steps**:
1. Create an AutosarClass with name="ParentClass", package="M2::Test", is_abstract=False, children=["Child1", "Child2", "Child3"]
2. Call repr(cls)
3. Verify "children=3" is in the result

**Expected Result**: Debug representation shows children count

**Requirements Coverage**: SWR_MODEL_00026

---

#### SWUT_MODEL_00081
**Title**: Test Debug Representation Shows Children Zero When No Children

**Maturity**: accept

**Description**: Verify that __repr__ shows children=0 when no children.

**Precondition**: An AutosarClass instance without children exists

**Test Steps**:
1. Create an AutosarClass with name="MyClass", package="M2::Test", is_abstract=False
2. Call repr(cls)
3. Verify "children=0" is in the result

**Expected Result**: Debug representation shows children=0

**Requirements Coverage**: SWR_MODEL_00026

---

#### SWUT_MODEL_00082
**Title**: Test Children Can Be Reassigned

**Maturity**: accept

**Description**: Verify that children can be reassigned after class creation.

**Precondition**: An AutosarClass instance exists

**Test Steps**:
1. Create an AutosarClass with name="ParentClass", package="M2::Test", is_abstract=False, children=["Child1", "Child2"]
2. Verify len(cls.children) is 2
3. Set cls.children = ["Child3", "Child4", "Child5"]
4. Verify len(cls.children) is 3
5. Verify "Child3" is in cls.children
6. Verify "Child1" is not in cls.children

**Expected Result**: Children can be reassigned

**Requirements Coverage**: SWR_MODEL_00026

---

### 2. Attribute Tests

#### SWUT_MODEL_00024
**Title**: Test Creating Reference Attribute

**Maturity**: accept

**Description**: Verify that a reference type attribute can be created.

**Precondition**: None

**Test Steps**:
1. Create an AutosarAttribute with name="dataReadPort", type="PPortPrototype", is_ref=True
2. Verify name is "dataReadPort"
3. Verify type is "PPortPrototype"
4. Verify is_ref is True

**Expected Result**: Reference attribute is created successfully

**Requirements Coverage**: SWR_MODEL_00010

---

#### SWUT_MODEL_00025
**Title**: Test Creating Non-Reference Attribute

**Maturity**: accept

**Description**: Verify that a non-reference type attribute can be created.

**Precondition**: None

**Test Steps**:
1. Create an AutosarAttribute with name="id", type="uint32", is_ref=False
2. Verify name is "id"
3. Verify type is "uint32"
4. Verify is_ref is False

**Expected Result**: Non-reference attribute is created successfully

**Requirements Coverage**: SWR_MODEL_00010

---

#### SWUT_MODEL_00026
**Title**: Test Valid Attribute Name Validation

**Maturity**: accept

**Description**: Verify that a valid attribute name is accepted during initialization.

**Precondition**: None

**Test Steps**:
1. Create an AutosarAttribute with name="validAttribute", type="string", is_ref=False
2. Verify the name attribute is set to "validAttribute"

**Expected Result**: Attribute is created successfully

**Requirements Coverage**: SWR_MODEL_00011

---

#### SWUT_MODEL_00027
**Title**: Test Empty Attribute Name Raises ValueError

**Maturity**: accept

**Description**: Verify that empty attribute names are rejected with ValueError.

**Precondition**: None

**Test Steps**:
1. Attempt to create an AutosarAttribute with name="", type="string", is_ref=False
2. Verify that ValueError is raised with message "Attribute name cannot be empty"

**Expected Result**: ValueError is raised

**Requirements Coverage**: SWR_MODEL_00011

---

#### SWUT_MODEL_00028
**Title**: Test Whitespace-Only Attribute Name Raises ValueError

**Maturity**: accept

**Description**: Verify that whitespace-only attribute names are rejected with ValueError.

**Precondition**: None

**Test Steps**:
1. Attempt to create an AutosarAttribute with name="   ", type="string", is_ref=False
2. Verify that ValueError is raised with message "Attribute name cannot be empty"

**Expected Result**: ValueError is raised

**Requirements Coverage**: SWR_MODEL_00011

---

#### SWUT_MODEL_00029
**Title**: Test Valid Attribute Type Validation

**Maturity**: accept

**Description**: Verify that a valid attribute type is accepted during initialization.

**Precondition**: None

**Test Steps**:
1. Create an AutosarAttribute with name="attr", type="ValidType", is_ref=False
2. Verify the type attribute is set to "ValidType"

**Expected Result**: Attribute is created successfully

**Requirements Coverage**: SWR_MODEL_00012

---

#### SWUT_MODEL_00030
**Title**: Test Empty Attribute Type Raises ValueError

**Maturity**: accept

**Description**: Verify that empty attribute types are rejected with ValueError.

**Precondition**: None

**Test Steps**:
1. Attempt to create an AutosarAttribute with name="attr", type="", is_ref=False
2. Verify that ValueError is raised with message "Attribute type cannot be empty"

**Expected Result**: ValueError is raised

**Requirements Coverage**: SWR_MODEL_00012

---

#### SWUT_MODEL_00031
**Title**: Test Whitespace-Only Attribute Type Raises ValueError

**Maturity**: accept

**Description**: Verify that whitespace-only attribute types are rejected with ValueError.

**Precondition**: None

**Test Steps**:
1. Attempt to create an AutosarAttribute with name="attr", type="   ", is_ref=False
2. Verify that ValueError is raised with message "Attribute type cannot be empty"

**Expected Result**: ValueError is raised

**Requirements Coverage**: SWR_MODEL_00012

---

#### SWUT_MODEL_00032
**Title**: Test String Representation of Reference Attribute

**Maturity**: accept

**Description**: Verify that the string representation of a reference attribute includes "(ref)" suffix.

**Precondition**: An AutosarAttribute instance exists

**Test Steps**:
1. Create an AutosarAttribute with name="port", type="PPortPrototype", is_ref=True
2. Call str(attr)
3. Verify the result is "port: PPortPrototype (ref)"

**Expected Result**: String representation includes "(ref)" suffix

**Requirements Coverage**: SWR_MODEL_00013

---

#### SWUT_MODEL_00033
**Title**: Test String Representation of Non-Reference Attribute

**Maturity**: accept

**Description**: Verify that the string representation of a non-reference attribute does not include "(ref)" suffix.

**Precondition**: An AutosarAttribute instance exists

**Test Steps**:
1. Create an AutosarAttribute with name="value", type="uint32", is_ref=False
2. Call str(attr)
3. Verify the result is "value: uint32"

**Expected Result**: String representation does not include "(ref)" suffix

**Requirements Coverage**: SWR_MODEL_00013

---

#### SWUT_MODEL_00034
**Title**: Test Debug Representation of AUTOSAR Attribute

**Maturity**: accept

**Description**: Verify that the debug representation shows all attributes.

**Precondition**: An AutosarAttribute instance exists

**Test Steps**:
1. Create an AutosarAttribute with name="testAttr", type="TestType", is_ref=True
2. Call repr(attr)
3. Verify "AutosarAttribute" is in the result
4. Verify "name='testAttr'" is in the result
5. Verify "type='TestType'" is in the result
6. Verify "is_ref=True" is in the result

**Expected Result**: Debug representation contains all attribute fields

**Requirements Coverage**: SWR_MODEL_00013

---

### 3. Package Tests (continued)

#### SWUT_MODEL_00035
**Title**: Test Creating an Empty Package

**Maturity**: accept

**Description**: Verify that an empty AUTOSAR package can be created.

**Precondition**: None

**Test Steps**:
1. Create an AutosarPackage with name="TestPackage"
2. Verify the name attribute is set to "TestPackage"
3. Verify the classes list is empty
4. Verify the subpackages list is empty

**Expected Result**: Empty package is created successfully

**Requirements Coverage**: SWR_MODEL_00004

---

#### SWUT_MODEL_00036
**Title**: Test Creating Package with Classes

**Maturity**: accept

**Description**: Verify that a package can be created with existing classes.

**Precondition**: Two AutosarClass instances exist

**Test Steps**:
1. Create two AutosarClass instances (Class1 concrete, Class2 abstract)
2. Create an AutosarPackage with classes=[cls1, cls2]
3. Verify the package has 2 classes
4. Verify the classes are in the correct order

**Expected Result**: Package is created with both classes

**Requirements Coverage**: SWR_MODEL_00004

---

#### SWUT_MODEL_00037
**Title**: Test Creating Package with Subpackages

**Maturity**: accept

**Description**: Verify that a package can be created with existing subpackages.

**Precondition**: An AutosarPackage instance exists

**Test Steps**:
1. Create a subpackage AutosarPackage with name="SubPackage"
2. Create a parent AutosarPackage with subpackages=[subpkg]
3. Verify the parent has 1 subpackage
4. Verify the subpackage name is "SubPackage"

**Expected Result**: Package is created with subpackage

**Requirements Coverage**: SWR_MODEL_00004

---

#### SWUT_MODEL_00038
**Title**: Test Valid Package Name Validation

**Maturity**: accept

**Description**: Verify that a valid package name is accepted during initialization.

**Precondition**: None

**Test Steps**:
1. Create an AutosarPackage with name="ValidPackage"
2. Verify the name attribute is set to "ValidPackage"

**Expected Result**: Package is created successfully

**Requirements Coverage**: SWR_MODEL_00005

---

#### SWUT_MODEL_00039
**Title**: Test Empty Package Name Raises ValueError

**Maturity**: accept

**Description**: Verify that empty package names are rejected with ValueError.

**Precondition**: None

**Test Steps**:
1. Attempt to create an AutosarPackage with name=""
2. Verify that ValueError is raised with message "Package name cannot be empty"

**Expected Result**: ValueError is raised

**Requirements Coverage**: SWR_MODEL_00005

---

#### SWUT_MODEL_00040
**Title**: Test Whitespace-Only Package Name Raises ValueError

**Maturity**: accept

**Description**: Verify that whitespace-only package names are rejected with ValueError.

**Precondition**: None

**Test Steps**:
1. Attempt to create an AutosarPackage with name="   "
2. Verify that ValueError is raised with message "Package name cannot be empty"

**Expected Result**: ValueError is raised

**Requirements Coverage**: SWR_MODEL_00005

---

#### SWUT_MODEL_00041
**Title**: Test Adding Class to Package Successfully

**Maturity**: accept

**Description**: Verify that a class can be added to a package.

**Precondition**: An AutosarPackage instance exists

**Test Steps**:
1. Create an AutosarPackage with name="TestPackage"
2. Create an AutosarClass with name="NewClass"
3. Call pkg.add_class(cls)
4. Verify the package has 1 class
5. Verify the class is the one that was added

**Expected Result**: Class is added to the package

**Requirements Coverage**: SWR_MODEL_00006

---

#### SWUT_MODEL_00042
**Title**: Test Adding Duplicate Class Raises ValueError

**Maturity**: accept

**Description**: Verify that adding a class with a duplicate name raises ValueError.

**Precondition**: An AutosarPackage instance with one class exists

**Test Steps**:
1. Create an AutosarPackage with name="TestPackage"
2. Add first AutosarClass with name="DuplicateClass" (concrete)
3. Attempt to add second AutosarClass with same name="DuplicateClass" (abstract)
4. Verify that ValueError is raised with message "already exists"

**Expected Result**: ValueError is raised

**Requirements Coverage**: SWR_MODEL_00006

---

#### SWUT_MODEL_00043
**Title**: Test Adding Subpackage to Package Successfully

**Maturity**: accept

**Description**: Verify that a subpackage can be added to a package.

**Precondition**: Two AutosarPackage instances exist

**Test Steps**:
1. Create a parent AutosarPackage with name="ParentPackage"
2. Create a child AutosarPackage with name="ChildPackage"
3. Call parent.add_subpackage(child)
4. Verify the parent has 1 subpackage
5. Verify the subpackage is the one that was added

**Expected Result**: Subpackage is added to the parent package

**Requirements Coverage**: SWR_MODEL_00007

---

#### SWUT_MODEL_00044
**Title**: Test Adding Duplicate Subpackage Raises ValueError

**Maturity**: accept

**Description**: Verify that adding a subpackage with a duplicate name raises ValueError.

**Precondition**: An AutosarPackage instance exists

**Test Steps**:
1. Create an AutosarPackage with name="ParentPackage"
2. Add first subpackage with name="DuplicateSub"
3. Attempt to add second subpackage with same name="DuplicateSub"
4. Verify that ValueError is raised with message "already exists"

**Expected Result**: ValueError is raised

**Requirements Coverage**: SWR_MODEL_00007

---

#### SWUT_MODEL_00045
**Title**: Test Finding Existing Class by Name

**Maturity**: accept

**Description**: Verify that an existing class can be retrieved from a package.

**Precondition**: An AutosarPackage with a class exists

**Test Steps**:
1. Create an AutosarPackage with name="TestPackage"
2. Add an AutosarClass with name="TargetClass"
3. Call pkg.get_class("TargetClass")
4. Verify the result is not None
5. Verify the result's name is "TargetClass"

**Expected Result**: The correct class is returned

**Requirements Coverage**: SWR_MODEL_00008

---

#### SWUT_MODEL_00046
**Title**: Test Finding Non-Existent Class Returns None

**Maturity**: accept

**Description**: Verify that attempting to find a non-existent class returns None.

**Precondition**: An AutosarPackage instance exists

**Test Steps**:
1. Create an AutosarPackage with name="TestPackage"
2. Call pkg.get_class("NonExistent")
3. Verify the result is None

**Expected Result**: None is returned

**Requirements Coverage**: SWR_MODEL_00008

---

#### SWUT_MODEL_00047
**Title**: Test Finding Existing Subpackage by Name

**Maturity**: accept

**Description**: Verify that an existing subpackage can be retrieved from a package.

**Precondition**: An AutosarPackage with a subpackage exists

**Test Steps**:
1. Create an AutosarPackage with name="ParentPackage"
2. Add a subpackage with name="TargetSub"
3. Call pkg.get_subpackage("TargetSub")
4. Verify the result is not None
5. Verify the result's name is "TargetSub"

**Expected Result**: The correct subpackage is returned

**Requirements Coverage**: SWR_MODEL_00008

---

#### SWUT_MODEL_00048
**Title**: Test Finding Non-Existent Subpackage Returns None

**Maturity**: accept

**Description**: Verify that attempting to find a non-existent subpackage returns None.

**Precondition**: An AutosarPackage instance exists

**Test Steps**:
1. Create an AutosarPackage with name="ParentPackage"
2. Call pkg.get_subpackage("NonExistent")
3. Verify the result is None

**Expected Result**: None is returned

**Requirements Coverage**: SWR_MODEL_00008

---

#### SWUT_MODEL_00049
**Title**: Test Checking if Class Exists Returns True

**Maturity**: accept

**Description**: Verify that has_class returns True for existing classes.

**Precondition**: An AutosarPackage with a class exists

**Test Steps**:
1. Create an AutosarPackage with name="TestPackage"
2. Add an AutosarClass with name="ExistingClass"
3. Call pkg.has_class("ExistingClass")
4. Verify the result is True

**Expected Result**: True is returned

**Requirements Coverage**: SWR_MODEL_00008

---

#### SWUT_MODEL_00050
**Title**: Test Checking if Non-Existent Class Exists Returns False

**Maturity**: accept

**Description**: Verify that has_class returns False for non-existent classes.

**Precondition**: An AutosarPackage instance exists

**Test Steps**:
1. Create an AutosarPackage with name="TestPackage"
2. Call pkg.has_class("NonExistent")
3. Verify the result is False

**Expected Result**: False is returned

**Requirements Coverage**: SWR_MODEL_00008

---

#### SWUT_MODEL_00051
**Title**: Test Checking if Subpackage Exists Returns True

**Maturity**: accept

**Description**: Verify that has_subpackage returns True for existing subpackages.

**Precondition**: An AutosarPackage with a subpackage exists

**Test Steps**:
1. Create an AutosarPackage with name="ParentPackage"
2. Add a subpackage with name="ExistingSub"
3. Call pkg.has_subpackage("ExistingSub")
4. Verify the result is True

**Expected Result**: True is returned

**Requirements Coverage**: SWR_MODEL_00008

---

#### SWUT_MODEL_00052
**Title**: Test Checking if Non-Existent Subpackage Exists Returns False

**Maturity**: accept

**Description**: Verify that has_subpackage returns False for non-existent subpackages.

**Precondition**: An AutosarPackage instance exists

**Test Steps**:
1. Create an AutosarPackage with name="ParentPackage"
2. Call pkg.has_subpackage("NonExistent")
3. Verify the result is False

**Expected Result**: False is returned

**Requirements Coverage**: SWR_MODEL_00008

---

#### SWUT_MODEL_00053
**Title**: Test String Representation of Package with Classes

**Maturity**: accept

**Description**: Verify that the string representation includes class count.

**Precondition**: An AutosarPackage with classes exists

**Test Steps**:
1. Create an AutosarPackage with name="TestPackage"
2. Add two classes (Class1 concrete, Class2 abstract)
3. Call str(pkg)
4. Verify "TestPackage" is in the result
5. Verify "2 classes" is in the result

**Expected Result**: String representation includes package name and class count

**Requirements Coverage**: SWR_MODEL_00009

---

#### SWUT_MODEL_00054
**Title**: Test String Representation of Package with Subpackages

**Maturity**: accept

**Description**: Verify that the string representation includes subpackage count.

**Precondition**: An AutosarPackage with subpackages exists

**Test Steps**:
1. Create an AutosarPackage with name="TestPackage"
2. Add two subpackages (Sub1, Sub2)
3. Call str(pkg)
4. Verify "TestPackage" is in the result
5. Verify "2 subpackages" is in the result

**Expected Result**: String representation includes package name and subpackage count

**Requirements Coverage**: SWR_MODEL_00009

---

#### SWUT_MODEL_00055
**Title**: Test String Representation of Package with Both Classes and Subpackages

**Maturity**: accept

**Description**: Verify that the string representation includes both class and subpackage counts.

**Precondition**: An AutosarPackage with classes and subpackages exists

**Test Steps**:
1. Create an AutosarPackage with name="TestPackage"
2. Add one class and one subpackage
3. Call str(pkg)
4. Verify "TestPackage" is in the result
5. Verify "1 classes" is in the result
6. Verify "1 subpackages" is in the result

**Expected Result**: String representation includes all counts

**Requirements Coverage**: SWR_MODEL_00009

---

#### SWUT_MODEL_00056
**Title**: Test String Representation of Empty Package

**Maturity**: accept

**Description**: Verify that the string representation of an empty package shows only the name.

**Precondition**: An empty AutosarPackage instance exists

**Test Steps**:
1. Create an AutosarPackage with name="EmptyPackage"
2. Call str(pkg)
3. Verify "EmptyPackage" is in the result

**Expected Result**: String representation shows only package name

**Requirements Coverage**: SWR_MODEL_00009

---

#### SWUT_MODEL_00057
**Title**: Test Debug Representation of AUTOSAR Package

**Maturity**: accept

**Description**: Verify that the debug representation shows all package attributes.

**Precondition**: An AutosarPackage with classes and subpackages exists

**Test Steps**:
1. Create an AutosarPackage with name="TestPackage"
2. Add one class and one subpackage
3. Call repr(pkg)
4. Verify "AutosarPackage" is in the result
5. Verify "name='TestPackage'" is in the result
6. Verify "classes=1" is in the result
7. Verify "subpackages=1" is in the result

**Expected Result**: Debug representation contains all package attributes

**Requirements Coverage**: SWR_MODEL_00009

---

#### SWUT_MODEL_00058
**Title**: Test Nested Package Structure

**Maturity**: accept

**Description**: Verify that nested package hierarchies can be created and navigated.

**Precondition**: Three AutosarPackage instances exist

**Test Steps**:
1. Create root package with name="Root"
2. Create child package with name="Child"
3. Create grandchild package with name="Grandchild"
4. Add child to root
5. Add grandchild to child
6. Verify root has 1 subpackage
7. Verify root.get_subpackage("Child") equals child
8. Verify child.get_subpackage("Grandchild") equals grandchild

**Expected Result**: Nested structure is created and can be navigated

**Requirements Coverage**: SWR_MODEL_00007, SWR_MODEL_00008

---

#### SWUT_MODEL_00061
**Title**: Test AbstractAutosarBase Abstract Base Class Properties

**Maturity**: accept

**Description**: Verify that the AbstractAutosarBase abstract base class provides common properties for all AUTOSAR types.

**Precondition**: None

**Test Steps**:
1. Create an AutosarClass with package="M2::SWR" (which inherits from AbstractAutosarBase)
2. Verify the name attribute is set correctly
3. Verify the package attribute is set correctly
4. Verify the note attribute is None by default
5. Verify the atp_type attribute (AutosarClass-specific) defaults to ATPType.NONE
6. Create an AutosarEnumeration with package="M2::ECUC" (which also inherits from AbstractAutosarBase)
7. Verify that enumeration also has the same base attributes (name, package, note)

**Expected Result**: All inherited properties from AbstractAutosarBase are correctly initialized in both AutosarClass and AutosarEnumeration. AutosarClass has additional atp_type attribute while AutosarEnumeration does not.

**Requirements Coverage**: SWR_MODEL_00018

---

#### SWUT_MODEL_00062
**Title**: Test AbstractAutosarBase Name Validation

**Maturity**: accept

**Description**: Verify that AbstractAutosarBase validates non-empty names.

**Precondition**: None

**Test Steps**:
1. Attempt to create an AutosarClass with name="" (empty string)
2. Verify ValueError is raised with message "Type name cannot be empty"
3. Attempt to create an AutosarClass with name="   " (whitespace only)
4. Verify ValueError is raised with message "Type name cannot be empty"

**Expected Result**: ValueError is raised for empty or whitespace-only names

**Requirements Coverage**: SWR_MODEL_00018

---

#### SWUT_MODEL_00063
**Title**: Test AutosarClass String Representation

**Maturity**: accept

**Description**: Verify that AutosarClass implements the abstract __str__() method with proper formatting including "(abstract)" suffix for abstract classes.

**Precondition**: None

**Test Steps**:
1. Create an AutosarClass with name="MyClass" and is_abstract=False
2. Verify str(cls) returns "MyClass"
3. Create an AutosarClass with name="AbstractClass" and is_abstract=True
4. Verify str(cls) returns "AbstractClass (abstract)"

**Expected Result**: String representation includes "(abstract)" suffix for abstract classes

**Requirements Coverage**: SWR_MODEL_00001, SWR_MODEL_00003, SWR_MODEL_00018

---

#### SWUT_MODEL_00064
**Title**: Test AutosarEnumeration Initialization

**Maturity**: accept

**Description**: Verify that an AUTOSAR enumeration can be created with proper initialization.

**Precondition**: None

**Test Steps**:
1. Create an AutosarEnumeration with name="MyEnum" and package="M2::ECUC"
2. Verify the name attribute is set to "MyEnum"
3. Verify the package attribute is set to "M2::ECUC"
4. Verify the note attribute is None by default
5. Verify the enumeration_literals attribute is an empty list
6. Verify that AutosarEnumeration inherits from AbstractAutosarBase

**Expected Result**: Enumeration is created with all attributes properly initialized

**Requirements Coverage**: SWR_MODEL_00018, SWR_MODEL_00019

---

#### SWUT_MODEL_00065
**Title**: Test AutosarEnumeration with Literals

**Maturity**: accept

**Description**: Verify that enumeration literals can be added to an AutosarEnumeration.

**Precondition**: AutosarEnumLiteral instances exist

**Test Steps**:
1. Create two AutosarEnumLiteral instances:
   - literal1 with name="VALUE1", index=0, description="First value"
   - literal2 with name="VALUE2", index=1, description="Second value"
2. Create an AutosarEnumeration with enumeration_literals=[literal1, literal2]
3. Verify len(enum.enumeration_literals) == 2
4. Verify enum.enumeration_literals[0].name == "VALUE1"
5. Verify enum.enumeration_literals[0].index == 0
6. Verify enum.enumeration_literals[1].name == "VALUE2"
7. Verify enum.enumeration_literals[1].index == 1

**Expected Result**: Enumeration literals are properly stored and accessible

**Requirements Coverage**: SWR_MODEL_00019

---

#### SWUT_MODEL_00066
**Title**: Test AutosarPackage add_type Method

**Maturity**: accept

**Description**: Verify that the add_type method can add both classes and enumerations to a package.

**Precondition**: AutosarClass and AutosarEnumeration instances exist

**Test Steps**:
1. Create an AutosarPackage with name="TestPackage"
2. Create an AutosarClass with name="MyClass"
3. Create an AutosarEnumeration with name="MyEnum"
4. Call pkg.add_type(cls)
5. Call pkg.add_type(enum)
6. Verify len(pkg.types) == 2
7. Verify pkg.types[0].name == "MyClass"
8. Verify pkg.types[1].name == "MyEnum"

**Expected Result**: Both class and enumeration are added to the package's types list

**Requirements Coverage**: SWR_MODEL_00020

---

#### SWUT_MODEL_00067
**Title**: Test AutosarPackage add_enumeration Method

**Maturity**: accept

**Description**: Verify that the add_enumeration method adds an enumeration to the package.

**Precondition**: AutosarEnumeration instance exists

**Test Steps**:
1. Create an AutosarPackage with name="TestPackage"
2. Create an AutosarEnumeration with name="MyEnum"
3. Call pkg.add_enumeration(enum)
4. Verify len(pkg.types) == 1
5. Verify pkg.types[0].name == "MyEnum"
6. Verify isinstance(pkg.types[0], AutosarEnumeration) is True

**Expected Result**: Enumeration is added to the package

**Requirements Coverage**: SWR_MODEL_00020

---

#### SWUT_MODEL_00068
**Title**: Test AutosarPackage get_enumeration Method

**Maturity**: accept

**Description**: Verify that the get_enumeration method retrieves enumerations by name.

**Precondition**: Package with both class and enumeration exists

**Test Steps**:
1. Create an AutosarPackage with name="TestPackage"
2. Add an AutosarClass with name="MyClass"
3. Add an AutosarEnumeration with name="MyEnum"
4. Call pkg.get_enumeration("MyEnum")
5. Verify the result is an AutosarEnumeration instance
6. Verify the result.name == "MyEnum"
7. Call pkg.get_enumeration("MyClass")
8. Verify the result is None (MyClass is not an enumeration)

**Expected Result**: get_enumeration returns only AutosarEnumeration instances

**Requirements Coverage**: SWR_MODEL_00020

---

#### SWUT_MODEL_00069
**Title**: Test AutosarPackage has_enumeration Method

**Maturity**: accept

**Description**: Verify that the has_enumeration method checks for enumeration existence.

**Precondition**: Package with both class and enumeration exists

**Test Steps**:
1. Create an AutosarPackage with name="TestPackage"
2. Add an AutosarClass with name="MyClass"
3. Add an AutosarEnumeration with name="MyEnum"
4. Call pkg.has_enumeration("MyEnum")
5. Verify the result is True
6. Call pkg.has_enumeration("MyClass")
7. Verify the result is False (MyClass is not an enumeration)
8. Call pkg.has_enumeration("NonExistent")
9. Verify the result is False

**Expected Result**: has_enumeration correctly identifies enumeration existence

**Requirements Coverage**: SWR_MODEL_00020

---

#### SWUT_MODEL_00070
**Title**: Test AutosarPackage Unified Type Management

**Maturity**: accept

**Description**: Verify that the unified types collection prevents duplicate names across classes and enumerations.

**Precondition**: AutosarClass and AutosarEnumeration instances exist

**Test Steps**:
1. Create an AutosarPackage with name="TestPackage"
2. Create an AutosarClass with name="MyType"
3. Create an AutosarEnumeration with name="MyType" (same name)
4. Add the class to the package
5. Attempt to add the enumeration to the package
6. Verify ValueError is raised with message "Type 'MyType' already exists in package 'TestPackage'"
7. Verify len(pkg.types) == 1 (only the class was added)

**Expected Result**: Duplicate type names are prevented across all types

**Requirements Coverage**: SWR_MODEL_00020

---

### 2. Writer Tests

#### SWUT_WRITER_00001
**Title**: Test Writing Single Empty Package

**Maturity**: accept

**Description**: Verify that a single empty package can be written to markdown.

**Precondition**: A MarkdownWriter instance and an empty AutosarPackage exist

**Test Steps**:
1. Create a MarkdownWriter instance
2. Create an empty AutosarPackage with name="TestPackage"
3. Call writer.write_packages([pkg])
4. Verify the output is "* TestPackage\n"

**Expected Result**: Markdown output contains the package name

**Requirements Coverage**: SWR_WRITER_00002, SWR_WRITER_00004

---

#### SWUT_WRITER_00002
**Title**: Test Writing Package with Single Class

**Maturity**: accept

**Description**: Verify that a package with one class can be written to markdown.

**Precondition**: A MarkdownWriter instance and an AutosarPackage with one class exist

**Test Steps**:
1. Create a MarkdownWriter instance
2. Create an AutosarPackage with name="TestPackage"
3. Add a concrete AutosarClass with name="MyClass"
4. Call writer.write_packages([pkg])
5. Verify the output is "* TestPackage\n  * MyClass\n"

**Expected Result**: Markdown output shows package with class indented correctly

**Requirements Coverage**: SWR_WRITER_00002, SWR_WRITER_00003

---

#### SWUT_WRITER_00003
**Title**: Test Writing Package with Abstract Class

**Maturity**: accept

**Description**: Verify that abstract classes are written with "(abstract)" suffix.

**Precondition**: A MarkdownWriter instance and an AutosarPackage with an abstract class exist

**Test Steps**:
1. Create a MarkdownWriter instance
2. Create an AutosarPackage with name="TestPackage"
3. Add an abstract AutosarClass with name="AbstractClass"
4. Call writer.write_packages([pkg])
5. Verify the output is "* TestPackage\n  * AbstractClass (abstract)\n"

**Expected Result**: Markdown output shows abstract class with suffix

**Requirements Coverage**: SWR_WRITER_00002, SWR_WRITER_00003

---

#### SWUT_WRITER_00004
**Title**: Test Writing Package with Multiple Classes

**Maturity**: accept

**Description**: Verify that multiple classes in a package are written correctly.

**Precondition**: A MarkdownWriter instance and an AutosarPackage with multiple classes exist

**Test Steps**:
1. Create a MarkdownWriter instance
2. Create an AutosarPackage with name="TestPackage"
3. Add three classes (Class1 concrete, Class2 abstract, Class3 concrete)
4. Call writer.write_packages([pkg])
5. Verify all three classes are in the output with correct indentation
6. Verify Class2 has "(abstract)" suffix

**Expected Result**: All classes are written in correct order with proper formatting

**Requirements Coverage**: SWR_WRITER_00002, SWR_WRITER_00003

---

#### SWUT_WRITER_00005
**Title**: Test Writing Nested Packages

**Maturity**: accept

**Description**: Verify that nested package structures are written with proper indentation.

**Precondition**: A MarkdownWriter instance and a nested package hierarchy exist

**Test Steps**:
1. Create a MarkdownWriter instance
2. Create root package with name="RootPackage"
3. Create child package with name="ChildPackage"
4. Add a class to child package
5. Add child to root
6. Call writer.write_packages([root])
7. Verify the output shows 3 levels of indentation (root, child, class)

**Expected Result**: Nested packages are written with correct indentation

**Requirements Coverage**: SWR_WRITER_00002

---

#### SWUT_WRITER_00006
**Title**: Test Writing Complex Nested Hierarchy

**Maturity**: accept

**Description**: Verify that deeply nested AUTOSAR hierarchies are written correctly.

**Precondition**: A MarkdownWriter instance and a complex 3-level package hierarchy exist

**Test Steps**:
1. Create a MarkdownWriter instance
2. Create AUTOSARTemplates → BswModuleTemplate → BswBehavior hierarchy
3. Add two classes to BswBehavior (BswInternalBehavior concrete, ExecutableEntity abstract)
4. Call writer.write_packages([root])
5. Verify the output shows correct 5-level hierarchy
6. Verify ExecutableEntity has "(abstract)" suffix

**Expected Result**: Complex hierarchy is written with correct indentation and formatting

**Requirements Coverage**: SWR_WRITER_00002, SWR_WRITER_00003

---

#### SWUT_WRITER_00007
**Title**: Test Writing Multiple Top-Level Packages

**Maturity**: accept

**Description**: Verify that multiple top-level packages can be written in one call.

**Precondition**: A MarkdownWriter instance and multiple AutosarPackage instances exist

**Test Steps**:
1. Create a MarkdownWriter instance
2. Create two packages: Package1 with Class1 (concrete), Package2 with Class2 (abstract)
3. Call writer.write_packages([pkg1, pkg2])
4. Verify both packages are in the output
5. Verify both classes are under their respective packages

**Expected Result**: All packages are written sequentially

**Requirements Coverage**: SWR_WRITER_00002, SWR_WRITER_00004

---

#### SWUT_WRITER_00008
**Title**: Test Writing Deeply Nested Hierarchy

**Maturity**: accept

**Description**: Verify that deeply nested package structures (3+ levels) are written correctly.

**Precondition**: A MarkdownWriter instance and a 3-level package hierarchy exist

**Test Steps**:
1. Create a MarkdownWriter instance
2. Create Level1 → Level2 → Level3 hierarchy
3. Add a class to Level3
4. Call writer.write_packages([level1])
5. Verify the output shows 4 levels of indentation

**Expected Result**: Deep nesting is written correctly

**Requirements Coverage**: SWR_WRITER_00002

---

#### SWUT_WRITER_00009
**Title**: Test Writing Empty Package List

**Maturity**: accept

**Description**: Verify that writing an empty list of packages produces empty output.

**Precondition**: A MarkdownWriter instance exists

**Test Steps**:
1. Create a MarkdownWriter instance
2. Call writer.write_packages([])
3. Verify the output is an empty string

**Expected Result**: No output is produced

**Requirements Coverage**: SWR_WRITER_00004

---

#### SWUT_WRITER_00010
**Title**: Test Writing Package with Both Classes and Subpackages

**Maturity**: accept

**Description**: Verify that packages with both direct classes and subpackages are written correctly.

**Precondition**: A MarkdownWriter instance and a package with classes and subpackages exist

**Test Steps**:
1. Create a MarkdownWriter instance
2. Create a parent package with one class and one subpackage
3. Add a class to the subpackage
4. Call writer.write_packages([pkg])
5. Verify the class under parent package appears
6. Verify the subpackage appears
7. Verify the class under subpackage appears with deeper indentation

**Expected Result**: All items are written with correct relative indentation

**Requirements Coverage**: SWR_WRITER_00002, SWR_WRITER_00003

---

#### SWUT_WRITER_00011
**Title**: Test Multiple Writes of Same Structure

**Maturity**: accept

**Description**: Verify that multiple writes of the same structure produce identical output.

**Precondition**: A MarkdownWriter instance and a package exist

**Test Steps**:
1. Create a MarkdownWriter instance
2. Create a package with one class
3. Call writer.write_packages([pkg]) - first write
4. Call writer.write_packages([pkg]) - second write
5. Verify both outputs are identical

**Expected Result**: Output is identical both times (no writer-level deduplication)

**Requirements Coverage**: SWR_WRITER_00002, SWR_WRITER_00003

---

#### SWUT_WRITER_00012
**Title**: Test Model-Level Duplicate Prevention

**Maturity**: accept

**Description**: Verify that duplicate classes are prevented at the model level.

**Precondition**: An AutosarPackage instance exists

**Test Steps**:
1. Create an AutosarPackage with name="TestPackage"
2. Add an AutosarClass with name="MyClass"
3. Attempt to add another AutosarClass with the same name "MyClass"
4. Verify that ValueError is raised with message "already exists"
5. Verify only one class exists in the package
6. Write the package to markdown
7. Verify only one class appears in the output

**Expected Result**: Duplicate is prevented at model level before writing

**Requirements Coverage**: SWR_MODEL_00006, SWR_WRITER_00002, SWR_WRITER_00003

---

#### SWUT_WRITER_00013
**Title**: Test Writing Multiple Packages with Same Name Different Content

**Maturity**: accept

**Description**: Verify that packages with the same name but different content are both written.

**Precondition**: A MarkdownWriter instance and two packages with same name exist

**Test Steps**:
1. Create a MarkdownWriter instance
2. Create pkg1 with name="TestPackage" and Class1
3. Create pkg2 with name="TestPackage" and Class2
4. Call writer.write_packages([pkg1, pkg2])
5. Verify both "* TestPackage" appear in the output
6. Verify both Class1 and Class2 appear

**Expected Result**: Both packages are written (no writer-level deduplication)

**Requirements Coverage**: SWR_WRITER_00002, SWR_WRITER_00004

---

### 3. CLI Tests

#### SWUT_CLI_00001
**Title**: Test CLI Main Entry Point

**Maturity**: accept

**Description**: Verify that the main() function is callable and returns int type.

**Precondition**: None

**Test Steps**:
1. Import the main function from autosar_cli
2. Verify that main is callable
3. Verify that main.__annotations__["return"] is int

**Expected Result**: main() is a valid entry point function

**Requirements Coverage**: SWR_CLI_00001

---

#### SWUT_CLI_00002
**Title**: Test CLI Handles Non-Existent Paths

**Maturity**: accept

**Description**: Verify that CLI returns error code when given a non-existent path.

**Precondition**: None

**Test Steps**:
1. Mock sys.argv with ["autosar-extract", "nonexistent.pdf"]
2. Mock Path to return exists() = False
3. Call main()
4. Verify return code is 1
5. Verify logging.error was called

**Expected Result**: CLI exits with error code 1 and logs error message

**Requirements Coverage**: SWR_CLI_00006, SWR_CLI_00009

---

#### SWUT_CLI_00003
**Title**: Test CLI Warns About Non-PDF Files

**Maturity**: accept

**Description**: Verify that CLI warns about non-PDF files and skips them.

**Precondition**: A non-PDF file exists

**Test Steps**:
1. Mock sys.argv with ["autosar-extract", "test.txt"]
2. Mock Path to return a .txt file
3. Mock PdfParser and MarkdownWriter
4. Call main()
5. Verify return code is 1 (no valid PDFs)
6. Verify logging.warning was called

**Expected Result**: CLI warns about non-PDF file and returns error

**Requirements Coverage**: SWR_CLI_00006, SWR_CLI_00008

---

#### SWUT_CLI_00004
**Title**: Test CLI Verbose Mode Enables DEBUG Logging

**Maturity**: accept

**Description**: Verify that verbose mode configures logging to DEBUG level.

**Precondition**: None

**Test Steps**:
1. Mock sys.argv with ["autosar-extract", "test.pdf", "-v"]
2. Mock Path to return a valid PDF file
3. Mock PdfParser, MarkdownWriter, and logging
4. Call main()
5. Verify logging.basicConfig was called with level=DEBUG

**Expected Result**: Logging is configured at DEBUG level

**Requirements Coverage**: SWR_CLI_00005, SWR_CLI_00008

---

#### SWUT_CLI_00005
**Title**: Test CLI Output File Option

**Maturity**: accept

**Description**: Verify that CLI can write output to a specified file.

**Precondition**: None

**Test Steps**:
1. Mock sys.argv with ["autosar-extract", "test.pdf", "-o", "output.md"]
2. Mock Path to return a valid PDF file and output file path
3. Mock PdfParser and MarkdownWriter
4. Call main()
5. Verify output_path.write_text was called once

**Expected Result**: Output is written to specified file

**Requirements Coverage**: SWR_CLI_00004

---

#### SWUT_CLI_00006
**Title**: Test CLI Default Logging is INFO Level

**Maturity**: accept

**Description**: Verify that CLI uses INFO level logging by default (without verbose flag).

**Precondition**: None

**Test Steps**:
1. Mock sys.argv with ["autosar-extract", "test.pdf"] (no -v flag)
2. Mock Path to return a valid PDF file
3. Mock PdfParser, MarkdownWriter, and logging
4. Call main()
5. Verify logging.basicConfig was called with level=INFO

**Expected Result**: Logging is configured at INFO level

**Requirements Coverage**: SWR_CLI_00008

---

#### SWUT_CLI_00007
**Title**: Test CLI Error Handling Without Verbose Mode

**Maturity**: accept

**Description**: Verify that exceptions are caught and logged without traceback in normal mode.

**Precondition**: None

**Test Steps**:
1. Mock sys.argv with ["autosar-extract", "test.pdf"]
2. Mock Path to return a valid PDF file
3. Mock PdfParser to raise Exception("Parse error")
4. Mock logging.error and logging.exception
5. Call main()
6. Verify return code is 1
7. Verify logging.error was called
8. Verify logging.exception was NOT called

**Expected Result**: Error is logged without traceback

**Requirements Coverage**: SWR_CLI_00009

---

#### SWUT_CLI_00008
**Title**: Test CLI Verbose Mode Shows Exception Traceback

**Maturity**: accept

**Description**: Verify that verbose mode includes exception traceback in error output.

**Precondition**: None

**Test Steps**:
1. Mock sys.argv with ["autosar-extract", "test.pdf", "-v"]
2. Mock Path to return a valid PDF file
3. Mock PdfParser to raise Exception("Parse error")
4. Mock logging.error and logging.exception
5. Call main()
6. Verify return code is 1
7. Verify logging.error was called
8. Verify logging.exception WAS called

**Expected Result**: Full exception traceback is logged

**Requirements Coverage**: SWR_CLI_00005, SWR_CLI_00009

---

#### SWUT_CLI_00009
**Title**: Test CLI Success Exit Code

**Maturity**: accept

**Description**: Verify that CLI returns 0 on successful execution.

**Precondition**: None

**Test Steps**:
1. Mock sys.argv with ["autosar-extract", "test.pdf"]
2. Mock Path to return a valid PDF file
3. Mock PdfParser to return a package
4. Mock MarkdownWriter to return markdown
5. Call main()
6. Verify return code is 0

**Expected Result**: CLI exits with success code 0

**Requirements Coverage**: SWR_CLI_00009

---

#### SWUT_CLI_00010
**Title**: Test CLI Supports Directory Input

**Maturity**: accept

**Description**: Verify that CLI accepts directory paths as input for PDF discovery.

**Precondition**: None

**Test Steps**:
1. Document that CLI supports directory input (integration test)
2. Verify that CLI should:
   - Accept directory paths as input arguments
   - Discover all PDF files using glob("*.pdf")
   - Sort PDF files alphabetically
   - Process all discovered PDF files

**Expected Result**: CLI can process directories containing PDF files

**Requirements Coverage**: SWR_CLI_00003

---

### 4. Parser Tests

#### SWUT_PARSER_00001
**Title**: Test Parser Initialization

**Maturity**: accept

**Description**: Verify that the PDF parser can be initialized successfully.

**Precondition**: pdfplumber is installed

**Test Steps**:
1. Create a PdfParser instance
2. Verify the parser is not None

**Expected Result**: Parser instance is created successfully

**Requirements Coverage**: SWR_PARSER_00001

---

#### SWUT_PARSER_00002
**Title**: Test Extracting Class with Base Classes

**Maturity**: accept

**Description**: Verify that base classes are extracted from class definitions.

**Precondition**: None

**Test Steps**:
1. Create a PdfParser instance
2. Parse text with "Class RunnableEntity", "Package M2::AUTOSAR::BswModule", "Base InternalBehavior"
3. Verify one class definition is extracted
4. Verify the class name is "RunnableEntity"
5. Verify base_classes is ["InternalBehavior"]

**Expected Result**: Base classes are extracted correctly

**Requirements Coverage**: SWR_PARSER_00004

---

#### SWUT_PARSER_00003
**Title**: Test Extracting Class with Multiple Base Classes

**Maturity**: accept

**Description**: Verify that multiple base classes are extracted and split correctly.

**Precondition**: None

**Test Steps**:
1. Create a PdfParser instance
2. Parse text with "Class DerivedClass", "Base BaseClass1, BaseClass2, BaseClass3"
3. Verify base_classes is ["BaseClass1", "BaseClass2", "BaseClass3"]

**Expected Result**: Multiple base classes are extracted and split by comma

**Requirements Coverage**: SWR_PARSER_00004

---

#### SWUT_PARSER_00004
**Title**: Test Extracting Class with Note

**Maturity**: accept

**Description**: Verify that notes are extracted from class definitions.

**Precondition**: None

**Test Steps**:
1. Create a PdfParser instance
2. Parse text with "Class BswInternalBehavior", "Package M2::AUTOSAR::BswModule", "Note Implementation for basic software internal behavior"
3. Verify the class name is "BswInternalBehavior"
4. Verify note is "Implementation for basic software internal behavior"

**Expected Result**: Note is extracted correctly

**Requirements Coverage**: SWR_PARSER_00004

---

#### SWUT_PARSER_00005
**Title**: Test Extracting Class with Base and Note

**Maturity**: accept

**Description**: Verify that both base classes and notes are extracted together.

**Precondition**: None

**Test Steps**:
1. Create a PdfParser instance
2. Parse text with class definition including both "Base InternalBehavior" and "Note Implementation for basic software entities"
3. Verify base_classes is ["InternalBehavior"]
4. Verify note contains "Implementation for basic software entities"

**Expected Result**: Both base classes and note are extracted correctly

**Requirements Coverage**: SWR_PARSER_00004

---

#### SWUT_PARSER_00006
**Title**: Test Extracting Class Without Base or Note

**Maturity**: accept

**Description**: Verify that classes without bases or notes are extracted with default values.

**Precondition**: None

**Test Steps**:
1. Create a PdfParser instance
2. Parse text with "Class SimpleClass", "Package M2::AUTOSAR" (no Base or Note lines)
3. Verify the class name is "SimpleClass"
4. Verify base_classes is []
5. Verify note is None

**Expected Result**: Class is extracted with empty bases and None note

**Requirements Coverage**: SWR_PARSER_00004

---

#### SWUT_PARSER_00050
**Title**: Test Extracting Class with Multi-Line Note

**Maturity**: accept

**Description**: Verify that notes spanning multiple lines are captured completely until encountering another known pattern (Base, Subclasses, Tags:, Attribute, etc.).

**Precondition**: None

**Test Steps**:
1. Create a PdfParser instance
2. Parse text with "Class BswImplementation", "Package M2::AUTOSARTemplates::BswModuleTemplate::BswImplementation"
3. Parse multi-line note spanning 3 lines:
   - Line 1: "Note Contains the implementation specific information in addition to the generic specification (BswModule"
   - Line 2: "Description and BswBehavior). It is possible to have several different BswImplementations referring to"
   - Line 3: "the same BswBehavior."
4. Parse "Base ARElement" line after the note (termination pattern)
5. Verify the class name is "BswImplementation"
6. Verify the note contains the complete multi-line text:
   - "Contains the implementation specific information in addition to the generic specification (BswModule Description and BswBehavior)"
   - "It is possible to have several different BswImplementations referring to the same BswBehavior"
7. Verify the note word count is at least 20 words

**Expected Result**: Multi-line note is captured completely, not truncated at line breaks. Note contains all phrases from multiple lines.

**Requirements Coverage**: SWR_PARSER_00004

---

#### SWUT_PARSER_00007
**Title**: Test Extracting Abstract Class

**Maturity**: accept

**Description**: Verify that abstract classes are extracted with the is_abstract flag.

**Precondition**: None

**Test Steps**:
1. Create a PdfParser instance
2. Parse text with "Class InternalBehavior (abstract)", "Package M2::AUTOSAR"
3. Verify the class name is "InternalBehavior"
4. Verify is_abstract is True

**Expected Result**: Abstract class is extracted correctly

**Requirements Coverage**: SWR_PARSER_00004

---

#### SWUT_PARSER_00008
**Title**: Test Extracting Class with Subclasses

**Maturity**: accept

**Description**: Verify that subclasses are extracted from class definitions.

**Precondition**: None

**Test Steps**:
1. Create a PdfParser instance
2. Parse text with "Class BaseClass", "Subclasses DerivedClass1, DerivedClass2"
3. Verify subclasses is ["DerivedClass1", "DerivedClass2"]

**Expected Result**: Subclasses are extracted correctly

**Requirements Coverage**: SWR_PARSER_00004

---

#### SWUT_PARSER_00009
**Title**: Test Extracting Multiple Classes

**Maturity**: accept

**Description**: Verify that multiple class definitions are extracted from a single text.

**Precondition**: None

**Test Steps**:
1. Create a PdfParser instance
2. Parse text with two class definitions (InternalBehavior abstract with note, BswInternalBehavior with base and note)
3. Verify two class definitions are extracted
4. Verify first class: name="InternalBehavior", is_abstract=True, has note
5. Verify second class: name="BswInternalBehavior", base_classes=["InternalBehavior"], has note

**Expected Result**: All classes are extracted with correct properties

**Requirements Coverage**: SWR_PARSER_00003, SWR_PARSER_00004

---

#### SWUT_PARSER_00010
**Title**: Test Building Package Hierarchy with Bases and Notes

**Maturity**: accept

**Description**: Verify that package hierarchy is built with bases and notes transferred to AutosarClass.

**Precondition**: Two ClassDefinition instances exist

**Test Steps**:
1. Create ClassDefinition for InternalBehavior (abstract, with note="Base behavior class")
2. Create ClassDefinition for BswInternalBehavior (bases=["InternalBehavior"], note="BSW specific behavior")
3. Call parser._build_package_hierarchy()
4. Verify top-level package exists
5. Verify InternalBehavior class: is_abstract=True, bases=[], note="Base behavior class"
6. Verify BswInternalBehavior class: bases=["InternalBehavior"], note="BSW specific behavior"

**Expected Result**: Package hierarchy is built with bases and notes transferred correctly

**Requirements Coverage**: SWR_PARSER_00006

---

#### SWUT_PARSER_00011
**Title**: Test Parsing Real AUTOSAR PDF and Verifying First Class

**Maturity**: accept

**Description**: Integration test that parses a real AUTOSAR PDF and verifies the first extracted class.

**Precondition**: File examples/pdf/AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf exists

**Test Steps**:
1. Create a PdfParser instance
2. Parse the PDF file examples/pdf/AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf
3. Find the first class in the extracted packages (searching through M2 → AUTOSARTemplates → AutosarTopLevelStructure)
4. Verify the class name is "AUTOSAR"
5. Verify the class is not abstract
6. Verify the class has one base class "ARObject"
7. Verify the class has a note containing "AUTOSAR" or "Rootelement"
8. Verify the class is in the "AutosarTopLevelStructure" package under M2 → AUTOSARTemplates
9. Verify the note contains proper word spacing (e.g., "Root element" not "Rootelement")

**Expected Result**: First class is extracted with correct name="AUTOSAR", bases=["ARObject"], and valid note with proper word spacing, located in package hierarchy M2 → AUTOSARTemplates → AutosarTopLevelStructure

**Requirements Coverage**: SWR_PARSER_00003, SWR_PARSER_00004, SWR_PARSER_00006, SWR_PARSER_00009

---

#### SWUT_PARSER_00012
**Title**: Test Extracting Class with Attributes

**Maturity**: accept

**Description**: Verify that class attributes are extracted from PDF text and converted to AutosarAttribute objects.

**Precondition**: None

**Test Steps**:
1. Create a PdfParser instance
2. Parse text with class definition including attribute section
3. Verify attributes are extracted correctly
4. Verify attribute names, types, and reference flags are correct

**Expected Result**: Attributes are extracted with correct name, type, and is_ref flag

**Requirements Coverage**: SWR_PARSER_00004, SWR_PARSER_00010, SWR_MODEL_00010

---

#### SWUT_PARSER_00013
**Title**: Test Extracting Class with Reference Attributes

**Maturity**: accept

**Description**: Verify that reference type attributes are correctly identified based on their type names.

**Precondition**: None

**Test Steps**:
1. Create a PdfParser instance
2. Parse text with class containing reference-type attributes (e.g., PPortPrototype, ModeDeclarationGroup)
3. Verify is_ref flag is set to True for reference types
4. Verify is_ref flag is set to False for non-reference types

**Expected Result**: Reference types are correctly identified by checking for patterns like Prototype, Ref, Dependency, Group, etc.

**Requirements Coverage**: SWR_PARSER_00004, SWR_PARSER_00010

---

#### SWUT_PARSER_00014
**Title**: Test Building Packages with Attributes

**Maturity**: accept

**Description**: Verify that attributes are transferred from ClassDefinition to AutosarClass objects during package hierarchy building.

**Precondition**: None

**Test Steps**:
1. Create a PdfParser instance
2. Create ClassDefinition with attributes
3. Build package hierarchy
4. Verify AutosarClass contains the attributes

**Expected Result**: Attributes are correctly transferred to AutosarClass objects

**Requirements Coverage**: SWR_PARSER_00006, SWR_PARSER_00010, SWR_MODEL_00001

---

#### SWUT_PARSER_00020
**Title**: Test Extracting Class with ATP Variation

**Maturity**: accept

**Description**: Verify that the parser correctly recognizes and extracts the <<atpVariation>> ATP marker from class definitions.

**Precondition**: None

**Test Steps**:
1. Create a PdfParser instance
2. Parse text containing a class definition with <<atpVariation>> marker (e.g., "Class MyClass <<atpVariation>>")
3. Verify that the class is extracted
4. Verify that the atp_type is set to ATP_VARIATION

**Expected Result**: Class with <<atpVariation>> marker is extracted with correct ATP type

**Requirements Coverage**: SWR_PARSER_00004

---

#### SWUT_PARSER_00021
**Title**: Test Extracting Class with ATP Mixed String

**Maturity**: accept

**Description**: Verify that the parser correctly recognizes and extracts the <<atpMixedString>> ATP marker from class definitions.

**Precondition**: None

**Test Steps**:
1. Create a PdfParser instance
2. Parse text containing a class definition with <<atpMixedString>> marker (e.g., "Class MyClass <<atpMixedString>>")
3. Verify that the class is extracted
4. Verify that the atp_type is set to ATP_MIXED_STRING

**Expected Result**: Class with <<atpMixedString>> marker is extracted with correct ATP type

**Requirements Coverage**: SWR_PARSER_00004

---

#### SWUT_PARSER_00022
**Title**: Test Extracting Class with ATP Mixed

**Maturity**: accept

**Description**: Verify that the parser correctly recognizes and extracts the <<atpMixed>> ATP marker from class definitions.

**Precondition**: None

**Test Steps**:
1. Create a PdfParser instance
2. Parse text containing a class definition with <<atpMixed>> marker (e.g., "Class MyClass <<atpMixed>>")
3. Verify that the class is extracted
4. Verify that the atp_type is set to ATP_MIXED

**Expected Result**: Class with <<atpMixed>> marker is extracted with correct ATP type

**Requirements Coverage**: SWR_PARSER_00004

---

#### SWUT_PARSER_00023
**Title**: Test Extracting Class with Both ATP Patterns Raises Error

**Maturity**: accept

**Description**: Verify that attempting to parse a class with multiple ATP markers raises a ValueError.

**Precondition**: None

**Test Steps**:
1. Create a PdfParser instance
2. Parse text containing a class definition with two ATP markers (e.g., "Class MyClass <<atpVariation>> <<atpMixedString>>")
3. Verify that a ValueError is raised with message "cannot have multiple ATP markers"

**Expected Result**: ValueError is raised when class has multiple ATP markers

**Requirements Coverage**: SWR_PARSER_00004

---

#### SWUT_PARSER_00024
**Title**: Test Extracting Class with ATP Patterns in Reverse Order Raises Error

**Maturity**: accept

**Description**: Verify that attempting to parse a class with multiple ATP markers in reverse order raises a ValueError.

**Precondition**: None

**Test Steps**:
1. Create a PdfParser instance
2. Parse text containing a class definition with two ATP markers in reverse order (e.g., "Class MyClass <<atpMixedString>> <<atpVariation>>")
3. Verify that a ValueError is raised with message "cannot have multiple ATP markers"

**Expected Result**: ValueError is raised when class has multiple ATP markers in any order

**Requirements Coverage**: SWR_PARSER_00004

---

#### SWUT_PARSER_00025
**Title**: Test Extracting Class with ATP Mixed and Variation Raises Error

**Maturity**: accept

**Description**: Verify that attempting to parse a class with <<atpMixed>> and <<atpVariation>> markers raises a ValueError.

**Precondition**: None

**Test Steps**:
1. Create a PdfParser instance
2. Parse text containing a class definition with <<atpMixed>> and <<atpVariation>> markers
3. Verify that a ValueError is raised

**Expected Result**: ValueError is raised when class has both <<atpMixed>> and <<atpVariation>> markers

**Requirements Coverage**: SWR_PARSER_00004

---

#### SWUT_PARSER_00026
**Title**: Test Extracting Class with ATP Mixed String and Mixed Raises Error

**Maturity**: accept

**Description**: Verify that attempting to parse a class with <<atpMixedString>> and <<atpMixed>> markers raises a ValueError.

**Precondition**: None

**Test Steps**:
1. Create a PdfParser instance
2. Parse text containing a class definition with <<atpMixedString>> and <<atpMixed>> markers
3. Verify that a ValueError is raised

**Expected Result**: ValueError is raised when class has both <<atpMixedString>> and <<atpMixed>> markers

**Requirements Coverage**: SWR_PARSER_00004

---

#### SWUT_PARSER_00027
**Title**: Test Extracting Class with All Three ATP Patterns Raises Error

**Maturity**: accept

**Description**: Verify that attempting to parse a class with all three ATP markers raises a ValueError.

**Precondition**: None

**Test Steps**:
1. Create a PdfParser instance
2. Parse text containing a class definition with all three ATP markers
3. Verify that a ValueError is raised

**Expected Result**: ValueError is raised when class has all three ATP markers

**Requirements Coverage**: SWR_PARSER_00004

---

#### SWUT_PARSER_00028
**Title**: Test Extracting Class with ATP and Abstract

**Maturity**: accept

**Description**: Verify that a class can have both an ATP marker and be marked as abstract.

**Precondition**: None

**Test Steps**:
1. Create a PdfParser instance
2. Parse text containing an abstract class definition with ATP marker (e.g., "Class MyClass (abstract) <<atpVariation>>")
3. Verify that the class is extracted
4. Verify that the class is marked as abstract
5. Verify that the atp_type is set correctly

**Expected Result**: Abstract class with ATP marker is extracted with both properties set correctly

**Requirements Coverage**: SWR_PARSER_00004

---

#### SWUT_PARSER_00029
**Title**: Test Extracting Class without ATP Patterns

**Maturity**: accept

**Description**: Verify that classes without ATP markers are parsed correctly with ATP type set to NONE.

**Precondition**: None

**Test Steps**:
1. Create a PdfParser instance
2. Parse text containing a class definition without ATP markers
3. Verify that the class is extracted
4. Verify that the atp_type is set to ATPType.NONE

**Expected Result**: Class without ATP markers is extracted with atp_type=NONE

**Requirements Coverage**: SWR_PARSER_00004

---

#### SWUT_PARSER_00030
**Title**: Test Extracting Class with Malformed ATP Pattern

**Maturity**: accept

**Description**: Verify that malformed ATP patterns are ignored and do not prevent class parsing.

**Precondition**: None

**Test Steps**:
1. Create a PdfParser instance
2. Parse text containing a class definition with malformed ATP pattern (e.g., "Class MyClass <<atpMixedString")
3. Verify that the class is extracted
4. Verify that the atp_type is set to ATPType.NONE (malformed pattern ignored)

**Expected Result**: Class is extracted with malformed ATP pattern ignored

**Requirements Coverage**: SWR_PARSER_00004

---

#### SWUT_PARSER_00031
**Title**: Test Building Packages with ATP Flags

**Maturity**: accept

**Description**: Verify that ATP flags are correctly transferred from ClassDefinition to AutosarClass during package hierarchy building.

**Precondition**: None

**Test Steps**:
1. Create ClassDefinition instances with various ATP types
2. Call parser._build_package_hierarchy()
3. Verify that AutosarClass instances have correct ATP types

**Expected Result**: ATP flags are correctly transferred to AutosarClass objects

**Requirements Coverage**: SWR_PARSER_00006

---

#### SWUT_PARSER_00032
**Title**: Test Extracting Class with Attributes

**Maturity**: accept

**Description**: Verify that class attributes are extracted from PDF text and converted to AutosarAttribute objects.

**Precondition**: None

**Test Steps**:
1. Create a PdfParser instance
2. Parse text with class definition including attribute section
3. Verify attributes are extracted correctly
4. Verify attribute names, types, multiplicities, kinds, and reference flags are correct

**Expected Result**: Attributes are extracted with correct name, type, multiplicity, kind (attr/aggr), and is_ref flag

**Requirements Coverage**: SWR_PARSER_00004, SWR_PARSER_00010, SWR_MODEL_00010

---

#### SWUT_PARSER_00033
**Title**: Test Extracting Class with Reference Attribute

**Maturity**: accept

**Description**: Verify that reference type attributes are correctly identified based on their type names.

**Precondition**: None

**Test Steps**:
1. Create a PdfParser instance
2. Parse text with class containing reference-type attributes (e.g., PPortPrototype, ModeDeclarationGroup)
3. Verify is_ref flag is set to True for reference types
4. Verify is_ref flag is set to False for non-reference types

**Expected Result**: Reference types are correctly identified by checking for patterns like Prototype, Ref, Dependency, Group, etc.

**Requirements Coverage**: SWR_PARSER_00004, SWR_PARSER_00010

---

#### SWUT_PARSER_00051
**Title**: Test Extracting Class with REF Kind Attributes

**Maturity**: accept

**Description**: Verify that attributes with "ref" in the Kind column are extracted and assigned the AttributeKind.REF enum value.

**Precondition**: None

**Test Steps**:
1. Create a PdfParser instance
2. Parse text with class containing attributes that have "ref" specified in the Kind column
3. Verify that attributes with kind="ref" have AttributeKind.REF
4. Verify that attributes with kind="attr" have AttributeKind.ATTR
5. Verify that attribute multiplicity is correctly extracted
6. Verify that attribute notes are correctly extracted

**Expected Result**: Attributes are extracted with correct kind values:
- "behavior" attribute has kind=AttributeKind.REF
- "arRelease" attribute has kind=AttributeKind.ATTR
- "preconfigured" attribute has kind=AttributeKind.REF

**Requirements Coverage**: SWR_PARSER_00004, SWR_PARSER_00010, SWR_MODEL_00010

---

#### SWUT_PARSER_00052
**Title**: Test Extracting Class with Tags in Note

**Maturity**: accept

**Description**: Verify that the Tags field is included in the class note when present in PDF class definitions.

**Precondition**: None

**Test Steps**:
1. Create a PdfParser instance
2. Parse text with class definition containing Note and Tags fields
3. Verify that the Tags field is included in the note
4. Verify that the note contains both the description and Tags information

**Expected Result**: The note contains both the description text and the Tags field (e.g., "Tags: atp.recommendedPackage=BswImplementations")

**Requirements Coverage**: SWR_PARSER_00004

---

#### SWUT_PARSER_00053
**Title**: Test Extracting Class with Multi-Line Attribute Notes

**Maturity**: accept

**Description**: Verify that attribute notes spanning multiple lines in the PDF are captured completely, ensuring that the full attribute description is preserved.

**Precondition**: None

**Test Steps**:
1. Create a PdfParser instance
2. Parse text with class definition containing attribute with multi-line note
3. Verify that the attribute note contains text from all lines
4. Verify specific phrases from different lines are present in the note
5. Verify note length is sufficient to confirm multi-line capture

**Expected Result**: Attribute notes are extracted with complete text from multiple lines:
- Note contains "Version of the AUTOSAR Release"
- Note contains "The numbering contains three"
- Note contains "AUTOSAR"
- Note length > 100 characters
- Note word count > 15 words

**Requirements Coverage**: SWR_PARSER_00004, SWR_PARSER_00010, SWR_MODEL_00010

---

#### SWUT_PARSER_00056
**Title**: Test Missing Base Class Logging During Parent Resolution

**Maturity**: accept

**Description**: Verify that warnings are logged when a class references base classes that cannot be located in the model during parent resolution.

**Precondition**: None

**Test Steps**:
1. Create a PdfParser instance
2. Create ClassDefinition with a base class that doesn't exist in the model (e.g., "NonExistentBase")
3. Call parser._build_package_hierarchy() to build the package hierarchy
4. Verify that the class is created successfully with parent set to None
5. Verify that warning messages are logged for the missing base class
6. Verify warning message contains the class name, package name, and missing base class name

**Expected Result**:
- Class is created with parent=None and bases=["NonExistentBase"]
- Warning is logged with message: "Class 'DerivedClass' in package 'Derived' has base classes that could not be located in the model: ['NonExistentBase']. Parent resolution may be incomplete."
- Warning is logged for ancestry traversal: "Class 'NonExistentBase' referenced in base classes could not be located in the model during ancestry traversal. Ancestry analysis may be incomplete."
- Each unique missing class is logged only once during ancestry traversal (deduplication)

**Requirements Coverage**: SWR_PARSER_00017, SWR_PARSER_00020

---

#### SWUT_PARSER_00034
**Title**: Test Building Packages with Attributes

**Maturity**: accept

**Description**: Verify that attributes are transferred from ClassDefinition to AutosarClass objects during package hierarchy building.

**Precondition**: None

**Test Steps**:
1. Create ClassDefinition instances with attributes
2. Call parser._build_package_hierarchy()
3. Verify that AutosarClass instances have attributes dictionaries
4. Verify that attributes are AutosarAttribute objects with correct properties

**Expected Result**: Attributes are correctly transferred from ClassDefinition to AutosarClass

**Requirements Coverage**: SWR_PARSER_00006

---

#### SWUT_PARSER_00035
**Title**: Test Metadata Filtering in Attribute Extraction

**Maturity**: accept

**Description**: Verify that metadata and formatting information from PDF class tables are filtered out during attribute extraction to ensure only valid AUTOSAR class attributes are extracted.

**Precondition**: None

**Test Steps**:
1. Create a PdfParser instance
2. Parse text containing attribute section with metadata lines like "Stereotypes: : atpSplitable;", "287 : of", "Specification : of", "AUTOSAR : CP"
3. Verify that these metadata lines are NOT parsed as attributes
4. Verify that only valid attributes are extracted

**Expected Result**: Metadata lines are filtered out and not incorrectly parsed as attributes

**Requirements Coverage**: SWR_PARSER_00004, SWR_PARSER_00010, SWR_PARSER_00011

---

#### SWUT_PARSER_00036
**Title**: Test Multi-Line Attribute Handling

**Maturity**: accept

**Description**: Verify that broken attribute fragments from multi-line PDF table formatting are filtered out to prevent incorrect parsing of partial attributes, while valid attributes with proper type information are preserved.

**Precondition**: None

**Test Steps**:
1. Create a PdfParser instance
2. Parse text containing attribute section with mixed content:
   - Valid attribute with proper type: "dynamicArray String * aggr"
   - Broken fragments: "SizeProfile data", "Element If", "ImplementationDataType has", "intention to", "isStructWith Boolean"
3. Verify that attributes with proper type information (e.g., "dynamicArray" with type "String") are kept
4. Verify that broken fragments without proper types are filtered out
5. Verify that only valid attributes remain

**Expected Result**: Attributes with proper type information (starting with uppercase) are preserved; broken attribute fragments from multi-line formatting are filtered out

**Requirements Coverage**: SWR_PARSER_00004, SWR_PARSER_00010, SWR_PARSER_00012

---

#### SWUT_PARSER_00037
**Title**: Test Recognition of Primitive Class Definition Pattern

**Maturity**: accept

**Description**: Verify that the parser correctly recognizes class definitions that use the "Primitive" prefix.

**Precondition**: None

**Test Steps**:
1. Create a PdfParser instance
2. Parse text containing a "Primitive <classname>" definition followed by a package path (e.g., "Primitive Limit" followed by "Package M2::AUTOSARTemplates::...")
3. Verify that the primitive class is recognized as a valid class definition
4. Verify that the primitive class name is extracted correctly (e.g., "Limit" from "Primitive Limit")
5. Verify that the primitive class is marked as non-abstract
6. Verify that any attributes following the primitive definition belong to the primitive class

**Expected Result**: Primitive class definitions are correctly recognized and parsed; attributes are assigned to the correct class

**Requirements Coverage**: SWR_PARSER_00004, SWR_PARSER_00013

---

#### SWUT_PARSER_00038
**Title**: Test Recognition of Enumeration Class Definition Pattern

**Maturity**: accept

**Description**: Verify that the parser correctly recognizes class definitions that use the "Enumeration" prefix.

**Precondition**: None

**Test Steps**:
1. Create a PdfParser instance
2. Parse text containing an "Enumeration <classname>" definition followed by a package path (e.g., "Enumeration IntervalTypeEnum" followed by "Package M2::AUTOSARTemplates::...")
3. Verify that the enumeration class is recognized as a valid class definition
4. Verify that the enumeration class name is extracted correctly (e.g., "IntervalTypeEnum" from "Enumeration IntervalTypeEnum")
5. Verify that the enumeration class is marked as non-abstract
6. Verify that any attributes following the enumeration definition belong to the enumeration class

**Expected Result**: Enumeration class definitions are correctly recognized and parsed; attributes are assigned to the correct class

**Requirements Coverage**: SWR_PARSER_00004, SWR_PARSER_00013

---

#### SWUT_PARSER_00039
**Title**: Test Prevention of Attribute Bleed Between Class Definitions

**Maturity**: accept

**Description**: Verify that when different class definition patterns (Class, Primitive, Enumeration) appear sequentially, each class receives only its own attributes and not attributes from subsequent classes.

**Precondition**: None

**Test Steps**:
1. Create a PdfParser instance
2. Parse text containing multiple class definitions using different patterns:
   - "Class ImplementationDataType" with attributes
   - "Primitive Limit" with attributes
   - "Enumeration IntervalTypeEnum" with literals
3. Verify that each class is recognized as a separate class definition
4. Verify that ImplementationDataType has only its own attributes
5. Verify that Limit has only its own attributes
6. Verify that IntervalTypeEnum has its own literals
7. Verify that attributes are not "bleeding" from one class to another

**Expected Result**: Each class receives only its own attributes; no attribute bleed occurs between classes with different definition patterns

**Requirements Coverage**: SWR_PARSER_00004, SWR_PARSER_00010, SWR_PARSER_00013

---

#### SWUT_PARSER_00047
**Title**: Test Package Path Validation

**Maturity**: accept

**Description**: Verify that the package path validation function correctly identifies valid and invalid package paths, filtering out paths with spaces, special characters, PDF artifacts, or invalid naming conventions.

**Precondition**: None

**Test Steps**:
1. Create a PdfParser instance
2. Test valid package paths:
   - "M2::AUTOSAR::DataTypes" (valid nested path)
   - "AUTOSAR::Templates" (valid simple path)
   - "M2::MSR" (valid path)
   - "Some_Package" (valid with underscore)
   - "_PrivatePackage" (valid starting with underscore)
3. Verify all valid paths return True
4. Test invalid package paths with spaces:
   - "live in various packages which do not have a common" (contains spaces)
   - "Package With Spaces" (contains spaces)
5. Verify paths with spaces return False
6. Test invalid package paths with special characters:
   - "can coexist in the context of a ReferenceBase.(cid:99)()" (contains parentheses and PDF artifact)
   - "Package.With.Dots" (contains dots)
   - "Package(With)Parens" (contains parentheses)
7. Verify paths with special characters return False
8. Test invalid package paths with lowercase start:
   - "lowercase::Package" (starts with lowercase)
   - "anotherPackage" (starts with lowercase)
9. Verify paths starting with lowercase return False
10. Test invalid package paths with empty parts:
    - "AUTOSAR::" (empty part after ::)
    - "::AUTOSAR" (empty part before ::)
11. Verify paths with empty parts return False

**Expected Result**:
- Valid package paths return True:
  - "M2::AUTOSAR::DataTypes" → True
  - "AUTOSAR::Templates" → True
  - "M2::MSR" → True
  - "Some_Package" → True
  - "_PrivatePackage" → True

- Invalid package paths return False:
  - Paths with spaces → False
  - Paths with special characters → False
  - Paths starting with lowercase → False
  - Paths with empty parts → False

**Requirements Coverage**: SWR_PARSER_00006

---

#### SWUT_PARSER_00048
**Title**: Test Extracting Class with Multi-Line Base Classes

**Maturity**: accept

**Description**: Verify that base classes spanning multiple lines in the PDF are correctly extracted and combined, including handling word splitting across line boundaries.

**Precondition**: None

**Test Steps**:
1. Create a PdfParser instance
2. Parse text with:
   - "Class CanTpConfig"
   - "Package M2::AUTOSARTemplates::SystemTemplate::TransportProtocols"
   - "Base ARObject,CollectableElement,FibexElement,Identifiable,MultilanguageReferrable,Packageable"
   - "Element,Referrable,TpConfig" (continuation line)
   - "Note This is a test class."
3. Verify base_classes contains all 8 expected base classes:
   - "ARObject"
   - "CollectableElement"
   - "FibexElement"
   - "Identifiable"
   - "MultilanguageReferrable"
   - "PackageableElement" (combined from "Packageable" + "Element")
   - "Referrable"
   - "TpConfig"
4. Verify "PackageableElement" is correctly formed by combining the split word
5. Verify "TpConfig" is in the list (critical for parent resolution)

**Expected Result**:
- All base classes from both lines are extracted
- Words split across lines are correctly combined ("Packageable" + "Element" = "PackageableElement")
- The complete base class list contains 8 classes
- TpConfig is included in the base class list

**Requirements Coverage**: SWR_PARSER_00004, SWR_PARSER_00021

---

### 7. Extract Tables CLI Tests

#### SWUT_CLI_00013
**Title**: Test AUTOSAR Table Detection with Class and Package Fields

**Maturity**: accept

**Description**: Verify that a table containing both Class and Package fields is correctly identified as AUTOSAR-related.

**Precondition**: None

**Test Steps**:
1. Create a table with header: ["Class", "Package", "Attribute", "Type"]
2. Add a data row: ["TestClass", "TestPackage", "testAttr", "string"]
3. Call is_autosar_table(table)
4. Verify the result is True

**Expected Result**: Table is identified as AUTOSAR-related

**Requirements Coverage**: SWR_CLI_00013

---

#### SWUT_CLI_00014
**Title**: Test AUTOSAR Table Detection Case Insensitive

**Maturity**: accept

**Description**: Verify that table detection is case-insensitive for Class and Package fields.

**Precondition**: None

**Test Steps**:
1. Create a table with header: ["CLASS", "PACKAGE", "Attribute", "Type"]
2. Add a data row: ["TestClass", "TestPackage", "testAttr", "string"]
3. Call is_autosar_table(table)
4. Verify the result is True

**Expected Result**: Table is identified as AUTOSAR-related regardless of case

**Requirements Coverage**: SWR_CLI_00013

---

#### SWUT_CLI_00015
**Title**: Test AUTOSAR Table Detection with Mixed Case

**Maturity**: accept

**Description**: Verify that table detection works with mixed case in header fields.

**Precondition**: None

**Test Steps**:
1. Create a table with header: ["Class", "PaCKaGe", "Attribute", "Type"]
2. Add a data row: ["TestClass", "TestPackage", "testAttr", "string"]
3. Call is_autosar_table(table)
4. Verify the result is True

**Expected Result**: Table is identified as AUTOSAR-related with mixed case

**Requirements Coverage**: SWR_CLI_00013

---

#### SWUT_CLI_00016
**Title**: Test Table with Only Class Field Not AUTOSAR

**Maturity**: accept

**Description**: Verify that a table with only Class field (missing Package) is not identified as AUTOSAR-related.

**Precondition**: None

**Test Steps**:
1. Create a table with header: ["Class", "Attribute", "Type"]
2. Add a data row: ["TestClass", "testAttr", "string"]
3. Call is_autosar_table(table)
4. Verify the result is False

**Expected Result**: Table is not identified as AUTOSAR-related

**Requirements Coverage**: SWR_CLI_00013

---

#### SWUT_CLI_00017
**Title**: Test Table with Only Package Field Not AUTOSAR

**Maturity**: accept

**Description**: Verify that a table with only Package field (missing Class) is not identified as AUTOSAR-related.

**Precondition**: None

**Test Steps**:
1. Create a table with header: ["Package", "Attribute", "Type"]
2. Add a data row: ["TestPackage", "testAttr", "string"]
3. Call is_autosar_table(table)
4. Verify the result is False

**Expected Result**: Table is not identified as AUTOSAR-related

**Requirements Coverage**: SWR_CLI_00013

---

#### SWUT_CLI_00018
**Title**: Test Table with Neither Class nor Package Not AUTOSAR

**Maturity**: accept

**Description**: Verify that a table without Class or Package fields is not identified as AUTOSAR-related.

**Precondition**: None

**Test Steps**:
1. Create a table with header: ["Attribute", "Type", "Mult"]
2. Add a data row: ["testAttr", "string", "0..1"]
3. Call is_autosar_table(table)
4. Verify the result is False

**Expected Result**: Table is not identified as AUTOSAR-related

**Requirements Coverage**: SWR_CLI_00013

---

#### SWUT_CLI_00019
**Title**: Test Empty Table Returns False

**Maturity**: accept

**Description**: Verify that an empty table returns False for AUTOSAR detection.

**Precondition**: None

**Test Steps**:
1. Create an empty table: []
2. Call is_autosar_table(table)
3. Verify the result is False

**Expected Result**: Empty table returns False

**Requirements Coverage**: SWR_CLI_00013

---

#### SWUT_CLI_00020
**Title**: Test Table with None in Header

**Maturity**: accept

**Description**: Verify that a table with None values in header is handled correctly.

**Precondition**: None

**Test Steps**:
1. Create a table with header: ["Class", None, "Package", "Type"]
2. Add a data row: ["TestClass", None, "TestPackage", "string"]
3. Call is_autosar_table(table)
4. Verify the result is True

**Expected Result**: Table is identified as AUTOSAR-related despite None values

**Requirements Coverage**: SWR_CLI_00013

---

#### SWUT_CLI_00021
**Title**: Test Table with Whitespace in Header

**Maturity**: accept

**Description**: Verify that a table with whitespace in header fields is handled correctly.

**Precondition**: None

**Test Steps**:
1. Create a table with header: [" Class ", " Package ", "Attribute", "Type"]
2. Add a data row: ["TestClass", "TestPackage", "testAttr", "string"]
3. Call is_autosar_table(table)
4. Verify the result is True

**Expected Result**: Table is identified as AUTOSAR-related after stripping whitespace

**Requirements Coverage**: SWR_CLI_00013

---

#### SWUT_CLI_00022
**Title**: Test Extracting Only AUTOSAR Tables from PDF

**Maturity**: accept

**Description**: Verify that only AUTOSAR-related tables are extracted from a PDF file.

**Precondition**: A PDF file with mixed tables exists

**Test Steps**:
1. Create a mock PDF with two tables on one page:
   - Table 1: AUTOSAR table with Class and Package fields
   - Table 2: Non-AUTOSAR table without Package field
2. Call extract_tables_from_pdf(pdf_path, output_dir)
3. Verify only 1 table image is saved (AUTOSAR table only)
4. Verify the non-AUTOSAR table is skipped

**Expected Result**: Only AUTOSAR tables are extracted and saved

**Requirements Coverage**: SWR_CLI_00013

---

#### SWUT_CLI_00023
**Title**: Test Extracting PDF with No AUTOSAR Tables

**Maturity**: accept

**Description**: Verify that an empty list is returned when no AUTOSAR tables are found.

**Precondition**: A PDF file with non-AUTOSAR tables exists

**Test Steps**:
1. Create a mock PDF with only non-AUTOSAR tables
2. Call extract_tables_from_pdf(pdf_path, output_dir)
3. Verify the result is an empty list
4. Verify no images are saved

**Expected Result**: Empty list is returned

**Requirements Coverage**: SWR_CLI_00013

---

#### SWUT_CLI_00024
**Title**: Test Extracting Tables from Multiple Pages

**Maturity**: accept

**Description**: Verify that AUTOSAR tables are extracted from multiple pages of a PDF.

**Precondition**: A PDF file with AUTOSAR tables on multiple pages exists

**Test Steps**:
1. Create a mock PDF with AUTOSAR tables on 2 pages
2. Call extract_tables_from_pdf(pdf_path, output_dir)
3. Verify 2 table images are saved (one from each page)
4. Verify both tables are AUTOSAR-related

**Expected Result**: All AUTOSAR tables from all pages are extracted

**Requirements Coverage**: SWR_CLI_00013

---

#### SWUT_CLI_00025
**Title**: Test Extract Tables CLI Entry Point

**Maturity**: accept

**Description**: Verify that the main function exists and returns an integer exit code.

**Precondition**: None

**Test Steps**:
1. Verify main function is callable
2. Verify main function has return type annotation of int

**Expected Result**: main function exists and returns int

**Requirements Coverage**: SWR_CLI_00013

---

#### SWUT_CLI_00026
**Title**: Test CLI Handles Non-Existent Paths

**Maturity**: accept

**Description**: Verify that CLI returns error when path does not exist.

**Precondition**: None

**Test Steps**:
1. Run CLI with non-existent PDF path: "nonexistent.pdf"
2. Verify exit code is 1 (error)
3. Verify error message is logged

**Expected Result**: CLI returns error exit code

**Requirements Coverage**: SWR_CLI_00013

---

#### SWUT_CLI_00027
**Title**: Test CLI Warns About Non-PDF Files

**Maturity**: accept

**Description**: Verify that CLI warns about non-PDF files and skips them.

**Precondition**: A non-PDF file exists

**Test Steps**:
1. Run CLI with non-PDF file: "test.txt"
2. Verify warning is logged
3. Verify file is skipped

**Expected Result**: Warning is logged and non-PDF files are skipped

**Requirements Coverage**: SWR_CLI_00013

---

#### SWUT_CLI_00028
**Title**: Test CLI Verbose Mode

**Maturity**: accept

**Description**: Verify that verbose mode enables detailed debug logging.

**Precondition**: None

**Test Steps**:
1. Run CLI with "-v" flag: "test.pdf -o output -v"
2. Verify logging is configured at DEBUG level
3. Verify detailed debug information is available

**Expected Result**: Verbose mode enables DEBUG level logging

**Requirements Coverage**: SWR_CLI_00013

---

#### SWUT_CLI_00029
**Title**: Test CLI Logging Configuration

**Maturity**: accept

**Description**: Verify that CLI logging is configured correctly in normal mode.

**Precondition**: None

**Test Steps**:
1. Run CLI without "-v" flag: "test.pdf -o output"
2. Verify logging is configured at INFO level
3. Verify logging format is correct

**Expected Result**: Logging is configured at INFO level in normal mode

**Requirements Coverage**: SWR_CLI_00013

---

#### SWUT_CLI_00030
**Title**: Test CLI Creates Output Directory

**Maturity**: accept

**Description**: Verify that CLI creates output directory if it doesn't exist.

**Precondition**: Output directory does not exist

**Test Steps**:
1. Run CLI with output directory: "test.pdf -o new_output_dir"
2. Verify output directory is created
3. Verify directory creation uses parents=True, exist_ok=True

**Expected Result**: Output directory is created successfully

**Requirements Coverage**: SWR_CLI_00013

---

#### SWUT_CLI_00031
**Title**: Test CLI Directory Input Support

**Maturity**: accept

**Description**: Verify that CLI supports directory input for PDF discovery.

**Precondition**: A directory with PDF files exists

**Test Steps**:
1. Run CLI with directory path: "test_dir -o output"
2. Verify glob("*.pdf") is called to find PDF files
3. Verify all PDF files in directory are processed

**Expected Result**: All PDF files in directory are discovered and processed

**Requirements Coverage**: SWR_CLI_00013

---

#### SWUT_CLI_00032
**Title**: Test CLI Error Handling

**Maturity**: accept

**Description**: Verify that CLI handles exceptions gracefully.

**Precondition**: None

**Test Steps**:
1. Mock extract_tables_from_pdf to raise an exception
2. Run CLI: "test.pdf -o output"
3. Verify exit code is 1 (error)
4. Verify error message is logged
5. Verify exception traceback is NOT logged in non-verbose mode

**Expected Result**: Error is handled gracefully without traceback in normal mode

**Requirements Coverage**: SWR_CLI_00013

---

#### SWUT_CLI_00033
**Title**: Test CLI Verbose Mode Exception Traceback

**Maturity**: accept

**Description**: Verify that CLI shows exception traceback in verbose mode.

**Precondition**: None

**Test Steps**:
1. Mock extract_tables_from_pdf to raise an exception
2. Run CLI with "-v" flag: "test.pdf -o output -v"
3. Verify exit code is 1 (error)
4. Verify error message is logged
5. Verify exception traceback IS logged in verbose mode

**Expected Result**: Exception traceback is logged in verbose mode

**Requirements Coverage**: SWR_CLI_00013

---

#### SWUT_CLI_00034
**Title**: Test CLI Success Exit Code

**Maturity**: accept

**Description**: Verify that CLI returns success exit code on successful extraction.

**Precondition**: A valid PDF file exists

**Test Steps**:
1. Mock extract_tables_from_pdf to return list of table paths
2. Run CLI: "test.pdf -o output"
3. Verify exit code is 0 (success)

**Expected Result**: CLI returns success exit code

**Requirements Coverage**: SWR_CLI_00013

---

#### SWUT_CLI_00035
**Title**: Test CLI Empty Directory Warning

**Maturity**: accept

**Description**: Verify that CLI warns about empty directories.

**Precondition**: An empty directory exists

**Test Steps**:
1. Run CLI with empty directory: "empty_dir -o output"
2. Verify warning is logged about no PDF files found
3. Verify exit code is 1 (error)

**Expected Result**: Warning is logged and CLI returns error

**Requirements Coverage**: SWR_CLI_00013

---

#### SWUT_CLI_00036
**Title**: Test CLI PDFMiner Warning Suppression

**Maturity**: accept

**Description**: Verify that CLI suppresses pdfminer warnings.

**Precondition**: None

**Test Steps**:
1. Run CLI: "test.pdf -o output"
2. Verify logging.getLogger("pdfminer") is called
3. Verify setLevel is called to suppress warnings

**Expected Result**: PDFMiner warnings are suppressed

**Requirements Coverage**: SWR_CLI_00013

