# Software Test Cases

## autosar-pdf2txt Test Cases

This document contains all test cases extracted from the test suite of the autosar-pdf2txt package. Each test case maps to one or more software requirements from `requirements.md`.

### 1. Model Tests

#### SWUT_Model_00001
**Title**: Test Initialization with Default Settings

**Description**: Verify that MarkdownWriter can be initialized without parameters.

**Precondition**: None

**Test Steps**:
1. Create a MarkdownWriter instance without parameters

**Expected Result**: Writer instance is created successfully

**Requirements Coverage**: SWR_Writer_00001

---

#### SWUT_Model_00002
**Title**: Test Creating a Concrete AUTOSAR Class

**Description**: Verify that an AUTOSAR class can be created with name and abstract flag.

**Precondition**: None

**Test Steps**:
1. Create an AutosarClass with name="RunnableEntity" and is_abstract=False
2. Verify the name attribute is set to "RunnableEntity"
3. Verify the is_abstract attribute is set to False

**Expected Result**: Class is created with correct attributes

**Requirements Coverage**: SWR_Model_00001

---

#### SWUT_Model_00003
**Title**: Test Creating an Abstract AUTOSAR Class

**Description**: Verify that an abstract AUTOSAR class can be created.

**Precondition**: None

**Test Steps**:
1. Create an AutosarClass with name="InternalBehavior" and is_abstract=True
2. Verify the name attribute is set to "InternalBehavior"
3. Verify the is_abstract attribute is set to True

**Expected Result**: Abstract class is created with correct attributes

**Requirements Coverage**: SWR_Model_00001

---

#### SWUT_Model_00004
**Title**: Test Valid Class Name Validation

**Description**: Verify that a valid class name is accepted during initialization.

**Precondition**: None

**Test Steps**:
1. Create an AutosarClass with name="ValidClass"
2. Verify the name attribute is set to "ValidClass"

**Expected Result**: Class is created successfully

**Requirements Coverage**: SWR_Model_00002

---

#### SWUT_Model_00005
**Title**: Test Empty Class Name Raises ValueError

**Description**: Verify that empty class names are rejected with ValueError.

**Precondition**: None

**Test Steps**:
1. Attempt to create an AutosarClass with name=""
2. Verify that ValueError is raised with message "Class name cannot be empty"

**Expected Result**: ValueError is raised

**Requirements Coverage**: SWR_Model_00002

---

#### SWUT_Model_00006
**Title**: Test Whitespace-Only Class Name Raises ValueError

**Description**: Verify that whitespace-only class names are rejected with ValueError.

**Precondition**: None

**Test Steps**:
1. Attempt to create an AutosarClass with name="   "
2. Verify that ValueError is raised with message "Class name cannot be empty"

**Expected Result**: ValueError is raised

**Requirements Coverage**: SWR_Model_00002

---

#### SWUT_Model_00007
**Title**: Test String Representation of Concrete Class

**Description**: Verify that the string representation of a concrete class shows the class name.

**Precondition**: An AutosarClass instance exists

**Test Steps**:
1. Create an AutosarClass with name="MyClass" and is_abstract=False
2. Call str() on the class instance

**Expected Result**: String representation returns "MyClass"

**Requirements Coverage**: SWR_Model_00003

---

#### SWUT_Model_00008
**Title**: Test String Representation of Abstract Class

**Description**: Verify that the string representation of an abstract class includes "(abstract)" suffix.

**Precondition**: An AutosarClass instance exists

**Test Steps**:
1. Create an AutosarClass with name="AbstractClass" and is_abstract=True
2. Call str() on the class instance

**Expected Result**: String representation returns "AbstractClass (abstract)"

**Requirements Coverage**: SWR_Model_00003

---

#### SWUT_Model_00009
**Title**: Test Debug Representation of AUTOSAR Class

**Description**: Verify that the debug representation shows all attributes.

**Precondition**: An AutosarClass instance exists

**Test Steps**:
1. Create an AutosarClass with name="TestClass" and is_abstract=True
2. Call repr() on the class instance
3. Verify that "AutosarClass" is in the result
4. Verify that "name='TestClass'" is in the result
5. Verify that "is_abstract=True" is in the result

**Expected Result**: Debug representation contains all class attributes

**Requirements Coverage**: SWR_Model_00003

---

#### SWUT_Model_00010
**Title**: Test Creating an Empty Package

**Description**: Verify that an empty AUTOSAR package can be created.

**Precondition**: None

**Test Steps**:
1. Create an AutosarPackage with name="TestPackage"
2. Verify the name attribute is set to "TestPackage"
3. Verify the classes list is empty
4. Verify the subpackages list is empty

**Expected Result**: Empty package is created successfully

**Requirements Coverage**: SWR_Model_00004

---

#### SWUT_Model_00011
**Title**: Test Creating Package with Classes

**Description**: Verify that a package can be created with existing classes.

**Precondition**: Two AutosarClass instances exist

**Test Steps**:
1. Create two AutosarClass instances (Class1 concrete, Class2 abstract)
2. Create an AutosarPackage with classes=[cls1, cls2]
3. Verify the package has 2 classes
4. Verify the classes are in the correct order

**Expected Result**: Package is created with both classes

**Requirements Coverage**: SWR_Model_00004

---

#### SWUT_Model_00012
**Title**: Test Creating Package with Subpackages

**Description**: Verify that a package can be created with existing subpackages.

**Precondition**: An AutosarPackage instance exists

**Test Steps**:
1. Create a subpackage AutosarPackage with name="SubPackage"
2. Create a parent AutosarPackage with subpackages=[subpkg]
3. Verify the parent has 1 subpackage
4. Verify the subpackage name is "SubPackage"

**Expected Result**: Package is created with subpackage

**Requirements Coverage**: SWR_Model_00004

---

#### SWUT_Model_00013
**Title**: Test Valid Package Name Validation

**Description**: Verify that a valid package name is accepted during initialization.

**Precondition**: None

**Test Steps**:
1. Create an AutosarPackage with name="ValidPackage"
2. Verify the name attribute is set to "ValidPackage"

**Expected Result**: Package is created successfully

**Requirements Coverage**: SWR_Model_00005

---

#### SWUT_Model_00014
**Title**: Test Empty Package Name Raises ValueError

**Description**: Verify that empty package names are rejected with ValueError.

**Precondition**: None

**Test Steps**:
1. Attempt to create an AutosarPackage with name=""
2. Verify that ValueError is raised with message "Package name cannot be empty"

**Expected Result**: ValueError is raised

**Requirements Coverage**: SWR_Model_00005

---

#### SWUT_Model_00015
**Title**: Test Whitespace-Only Package Name Raises ValueError

**Description**: Verify that whitespace-only package names are rejected with ValueError.

**Precondition**: None

**Test Steps**:
1. Attempt to create an AutosarPackage with name="   "
2. Verify that ValueError is raised with message "Package name cannot be empty"

**Expected Result**: ValueError is raised

**Requirements Coverage**: SWR_Model_00005

---

#### SWUT_Model_00016
**Title**: Test Adding Class to Package Successfully

**Description**: Verify that a class can be added to a package.

**Precondition**: An AutosarPackage instance exists

**Test Steps**:
1. Create an AutosarPackage with name="TestPackage"
2. Create an AutosarClass with name="NewClass"
3. Call pkg.add_class(cls)
4. Verify the package has 1 class
5. Verify the class is the one that was added

**Expected Result**: Class is added to the package

**Requirements Coverage**: SWR_Model_00006

---

#### SWUT_Model_00017
**Title**: Test Adding Duplicate Class Raises ValueError

**Description**: Verify that adding a class with a duplicate name raises ValueError.

**Precondition**: An AutosarPackage instance with one class exists

**Test Steps**:
1. Create an AutosarPackage with name="TestPackage"
2. Add first AutosarClass with name="DuplicateClass" (concrete)
3. Attempt to add second AutosarClass with same name="DuplicateClass" (abstract)
4. Verify that ValueError is raised with message "already exists"

**Expected Result**: ValueError is raised

**Requirements Coverage**: SWR_Model_00006

---

#### SWUT_Model_00018
**Title**: Test Adding Subpackage to Package Successfully

**Description**: Verify that a subpackage can be added to a package.

**Precondition**: Two AutosarPackage instances exist

**Test Steps**:
1. Create a parent AutosarPackage with name="ParentPackage"
2. Create a child AutosarPackage with name="ChildPackage"
3. Call parent.add_subpackage(child)
4. Verify the parent has 1 subpackage
5. Verify the subpackage is the one that was added

**Expected Result**: Subpackage is added to the parent package

**Requirements Coverage**: SWR_Model_00007

---

#### SWUT_Model_00019
**Title**: Test Adding Duplicate Subpackage Raises ValueError

**Description**: Verify that adding a subpackage with a duplicate name raises ValueError.

**Precondition**: An AutosarPackage instance exists

**Test Steps**:
1. Create an AutosarPackage with name="ParentPackage"
2. Add first subpackage with name="DuplicateSub"
3. Attempt to add second subpackage with same name="DuplicateSub"
4. Verify that ValueError is raised with message "already exists"

**Expected Result**: ValueError is raised

**Requirements Coverage**: SWR_Model_00007

---

#### SWUT_Model_00020
**Title**: Test Finding Existing Class by Name

**Description**: Verify that an existing class can be retrieved from a package.

**Precondition**: An AutosarPackage with a class exists

**Test Steps**:
1. Create an AutosarPackage with name="TestPackage"
2. Add an AutosarClass with name="TargetClass"
3. Call pkg.get_class("TargetClass")
4. Verify the result is not None
5. Verify the result's name is "TargetClass"

**Expected Result**: The correct class is returned

**Requirements Coverage**: SWR_Model_00008

---

#### SWUT_Model_00021
**Title**: Test Finding Non-Existent Class Returns None

**Description**: Verify that attempting to find a non-existent class returns None.

**Precondition**: An AutosarPackage instance exists

**Test Steps**:
1. Create an AutosarPackage with name="TestPackage"
2. Call pkg.get_class("NonExistent")
3. Verify the result is None

**Expected Result**: None is returned

**Requirements Coverage**: SWR_Model_00008

---

#### SWUT_Model_00022
**Title**: Test Finding Existing Subpackage by Name

**Description**: Verify that an existing subpackage can be retrieved from a package.

**Precondition**: An AutosarPackage with a subpackage exists

**Test Steps**:
1. Create an AutosarPackage with name="ParentPackage"
2. Add a subpackage with name="TargetSub"
3. Call pkg.get_subpackage("TargetSub")
4. Verify the result is not None
5. Verify the result's name is "TargetSub"

**Expected Result**: The correct subpackage is returned

**Requirements Coverage**: SWR_Model_00008

---

#### SWUT_Model_00023
**Title**: Test Finding Non-Existent Subpackage Returns None

**Description**: Verify that attempting to find a non-existent subpackage returns None.

**Precondition**: An AutosarPackage instance exists

**Test Steps**:
1. Create an AutosarPackage with name="ParentPackage"
2. Call pkg.get_subpackage("NonExistent")
3. Verify the result is None

**Expected Result**: None is returned

**Requirements Coverage**: SWR_Model_00008

---

#### SWUT_Model_00024
**Title**: Test Checking if Class Exists Returns True

**Description**: Verify that has_class returns True for existing classes.

**Precondition**: An AutosarPackage with a class exists

**Test Steps**:
1. Create an AutosarPackage with name="TestPackage"
2. Add an AutosarClass with name="ExistingClass"
3. Call pkg.has_class("ExistingClass")
4. Verify the result is True

**Expected Result**: True is returned

**Requirements Coverage**: SWR_Model_00008

---

#### SWUT_Model_00025
**Title**: Test Checking if Non-Existent Class Exists Returns False

**Description**: Verify that has_class returns False for non-existent classes.

**Precondition**: An AutosarPackage instance exists

**Test Steps**:
1. Create an AutosarPackage with name="TestPackage"
2. Call pkg.has_class("NonExistent")
3. Verify the result is False

**Expected Result**: False is returned

**Requirements Coverage**: SWR_Model_00008

---

#### SWUT_Model_00026
**Title**: Test Checking if Subpackage Exists Returns True

**Description**: Verify that has_subpackage returns True for existing subpackages.

**Precondition**: An AutosarPackage with a subpackage exists

**Test Steps**:
1. Create an AutosarPackage with name="ParentPackage"
2. Add a subpackage with name="ExistingSub"
3. Call pkg.has_subpackage("ExistingSub")
4. Verify the result is True

**Expected Result**: True is returned

**Requirements Coverage**: SWR_Model_00008

---

#### SWUT_Model_00027
**Title**: Test Checking if Non-Existent Subpackage Exists Returns False

**Description**: Verify that has_subpackage returns False for non-existent subpackages.

**Precondition**: An AutosarPackage instance exists

**Test Steps**:
1. Create an AutosarPackage with name="ParentPackage"
2. Call pkg.has_subpackage("NonExistent")
3. Verify the result is False

**Expected Result**: False is returned

**Requirements Coverage**: SWR_Model_00008

---

#### SWUT_Model_00028
**Title**: Test String Representation of Package with Classes

**Description**: Verify that the string representation includes class count.

**Precondition**: An AutosarPackage with classes exists

**Test Steps**:
1. Create an AutosarPackage with name="TestPackage"
2. Add two classes (Class1 concrete, Class2 abstract)
3. Call str(pkg)
4. Verify "TestPackage" is in the result
5. Verify "2 classes" is in the result

**Expected Result**: String representation includes package name and class count

**Requirements Coverage**: SWR_Model_00009

---

#### SWUT_Model_00029
**Title**: Test String Representation of Package with Subpackages

**Description**: Verify that the string representation includes subpackage count.

**Precondition**: An AutosarPackage with subpackages exists

**Test Steps**:
1. Create an AutosarPackage with name="TestPackage"
2. Add two subpackages (Sub1, Sub2)
3. Call str(pkg)
4. Verify "TestPackage" is in the result
5. Verify "2 subpackages" is in the result

**Expected Result**: String representation includes package name and subpackage count

**Requirements Coverage**: SWR_Model_00009

---

#### SWUT_Model_00030
**Title**: Test String Representation of Package with Both Classes and Subpackages

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

**Requirements Coverage**: SWR_Model_00009

---

#### SWUT_Model_00031
**Title**: Test String Representation of Empty Package

**Description**: Verify that the string representation of an empty package shows only the name.

**Precondition**: An empty AutosarPackage instance exists

**Test Steps**:
1. Create an AutosarPackage with name="EmptyPackage"
2. Call str(pkg)
3. Verify "EmptyPackage" is in the result

**Expected Result**: String representation shows only package name

**Requirements Coverage**: SWR_Model_00009

---

#### SWUT_Model_00032
**Title**: Test Debug Representation of AUTOSAR Package

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

**Requirements Coverage**: SWR_Model_00009

---

#### SWUT_Model_00033
**Title**: Test Nested Package Structure

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

**Requirements Coverage**: SWR_Model_00007, SWR_Model_00008

---

### 2. Writer Tests

#### SWUT_Writer_00001
**Title**: Test Writing Single Empty Package

**Description**: Verify that a single empty package can be written to markdown.

**Precondition**: A MarkdownWriter instance and an empty AutosarPackage exist

**Test Steps**:
1. Create a MarkdownWriter instance
2. Create an empty AutosarPackage with name="TestPackage"
3. Call writer.write_packages([pkg])
4. Verify the output is "* TestPackage\n"

**Expected Result**: Markdown output contains the package name

**Requirements Coverage**: SWR_Writer_00002, SWR_Writer_00004

---

#### SWUT_Writer_00002
**Title**: Test Writing Package with Single Class

**Description**: Verify that a package with one class can be written to markdown.

**Precondition**: A MarkdownWriter instance and an AutosarPackage with one class exist

**Test Steps**:
1. Create a MarkdownWriter instance
2. Create an AutosarPackage with name="TestPackage"
3. Add a concrete AutosarClass with name="MyClass"
4. Call writer.write_packages([pkg])
5. Verify the output is "* TestPackage\n  * MyClass\n"

**Expected Result**: Markdown output shows package with class indented correctly

**Requirements Coverage**: SWR_Writer_00002, SWR_Writer_00003

---

#### SWUT_Writer_00003
**Title**: Test Writing Package with Abstract Class

**Description**: Verify that abstract classes are written with "(abstract)" suffix.

**Precondition**: A MarkdownWriter instance and an AutosarPackage with an abstract class exist

**Test Steps**:
1. Create a MarkdownWriter instance
2. Create an AutosarPackage with name="TestPackage"
3. Add an abstract AutosarClass with name="AbstractClass"
4. Call writer.write_packages([pkg])
5. Verify the output is "* TestPackage\n  * AbstractClass (abstract)\n"

**Expected Result**: Markdown output shows abstract class with suffix

**Requirements Coverage**: SWR_Writer_00002, SWR_Writer_00003

---

#### SWUT_Writer_00004
**Title**: Test Writing Package with Multiple Classes

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

**Requirements Coverage**: SWR_Writer_00002, SWR_Writer_00003

---

#### SWUT_Writer_00005
**Title**: Test Writing Nested Packages

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

**Requirements Coverage**: SWR_Writer_00002

---

#### SWUT_Writer_00006
**Title**: Test Writing Complex Nested Hierarchy

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

**Requirements Coverage**: SWR_Writer_00002, SWR_Writer_00003

---

#### SWUT_Writer_00007
**Title**: Test Writing Multiple Top-Level Packages

**Description**: Verify that multiple top-level packages can be written in one call.

**Precondition**: A MarkdownWriter instance and multiple AutosarPackage instances exist

**Test Steps**:
1. Create a MarkdownWriter instance
2. Create two packages: Package1 with Class1 (concrete), Package2 with Class2 (abstract)
3. Call writer.write_packages([pkg1, pkg2])
4. Verify both packages are in the output
5. Verify both classes are under their respective packages

**Expected Result**: All packages are written sequentially

**Requirements Coverage**: SWR_Writer_00002, SWR_Writer_00004

---

#### SWUT_Writer_00008
**Title**: Test Writing Deeply Nested Hierarchy

**Description**: Verify that deeply nested package structures (3+ levels) are written correctly.

**Precondition**: A MarkdownWriter instance and a 3-level package hierarchy exist

**Test Steps**:
1. Create a MarkdownWriter instance
2. Create Level1 → Level2 → Level3 hierarchy
3. Add a class to Level3
4. Call writer.write_packages([level1])
5. Verify the output shows 4 levels of indentation

**Expected Result**: Deep nesting is written correctly

**Requirements Coverage**: SWR_Writer_00002

---

#### SWUT_Writer_00009
**Title**: Test Writing Empty Package List

**Description**: Verify that writing an empty list of packages produces empty output.

**Precondition**: A MarkdownWriter instance exists

**Test Steps**:
1. Create a MarkdownWriter instance
2. Call writer.write_packages([])
3. Verify the output is an empty string

**Expected Result**: No output is produced

**Requirements Coverage**: SWR_Writer_00004

---

#### SWUT_Writer_00010
**Title**: Test Writing Package with Both Classes and Subpackages

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

**Requirements Coverage**: SWR_Writer_00002, SWR_Writer_00003

---

#### SWUT_Writer_00011
**Title**: Test Multiple Writes of Same Structure

**Description**: Verify that multiple writes of the same structure produce identical output.

**Precondition**: A MarkdownWriter instance and a package exist

**Test Steps**:
1. Create a MarkdownWriter instance
2. Create a package with one class
3. Call writer.write_packages([pkg]) - first write
4. Call writer.write_packages([pkg]) - second write
5. Verify both outputs are identical

**Expected Result**: Output is identical both times (no writer-level deduplication)

**Requirements Coverage**: SWR_Writer_00002, SWR_Writer_00003

---

#### SWUT_Writer_00012
**Title**: Test Model-Level Duplicate Prevention

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

**Requirements Coverage**: SWR_Model_00006, SWR_Writer_00002, SWR_Writer_00003

---

#### SWUT_Writer_00013
**Title**: Test Writing Multiple Packages with Same Name Different Content

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

**Requirements Coverage**: SWR_Writer_00002, SWR_Writer_00004

---

### 3. CLI Tests

#### SWUT_Cli_00001
**Title**: Test CLI Main Entry Point

**Description**: Verify that the main() function is callable and returns int type.

**Precondition**: None

**Test Steps**:
1. Import the main function from autosar_cli
2. Verify that main is callable
3. Verify that main.__annotations__["return"] is int

**Expected Result**: main() is a valid entry point function

**Requirements Coverage**: SWR_Cli_00001

---

#### SWUT_Cli_00002
**Title**: Test CLI Handles Non-Existent Paths

**Description**: Verify that CLI returns error code when given a non-existent path.

**Precondition**: None

**Test Steps**:
1. Mock sys.argv with ["autosar-extract", "nonexistent.pdf"]
2. Mock Path to return exists() = False
3. Call main()
4. Verify return code is 1
5. Verify logging.error was called

**Expected Result**: CLI exits with error code 1 and logs error message

**Requirements Coverage**: SWR_Cli_00006, SWR_Cli_00009

---

#### SWUT_Cli_00003
**Title**: Test CLI Warns About Non-PDF Files

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

**Requirements Coverage**: SWR_Cli_00006, SWR_Cli_00008

---

#### SWUT_Cli_00004
**Title**: Test CLI Verbose Mode Enables DEBUG Logging

**Description**: Verify that verbose mode configures logging to DEBUG level.

**Precondition**: None

**Test Steps**:
1. Mock sys.argv with ["autosar-extract", "test.pdf", "-v"]
2. Mock Path to return a valid PDF file
3. Mock PdfParser, MarkdownWriter, and logging
4. Call main()
5. Verify logging.basicConfig was called with level=DEBUG

**Expected Result**: Logging is configured at DEBUG level

**Requirements Coverage**: SWR_Cli_00005, SWR_Cli_00008

---

#### SWUT_Cli_00005
**Title**: Test CLI Output File Option

**Description**: Verify that CLI can write output to a specified file.

**Precondition**: None

**Test Steps**:
1. Mock sys.argv with ["autosar-extract", "test.pdf", "-o", "output.md"]
2. Mock Path to return a valid PDF file and output file path
3. Mock PdfParser and MarkdownWriter
4. Call main()
5. Verify output_path.write_text was called once

**Expected Result**: Output is written to specified file

**Requirements Coverage**: SWR_Cli_00004

---

#### SWUT_Cli_00006
**Title**: Test CLI Default Logging is INFO Level

**Description**: Verify that CLI uses INFO level logging by default (without verbose flag).

**Precondition**: None

**Test Steps**:
1. Mock sys.argv with ["autosar-extract", "test.pdf"] (no -v flag)
2. Mock Path to return a valid PDF file
3. Mock PdfParser, MarkdownWriter, and logging
4. Call main()
5. Verify logging.basicConfig was called with level=INFO

**Expected Result**: Logging is configured at INFO level

**Requirements Coverage**: SWR_Cli_00008

---

#### SWUT_Cli_00007
**Title**: Test CLI Error Handling Without Verbose Mode

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

**Requirements Coverage**: SWR_Cli_00009

---

#### SWUT_Cli_00008
**Title**: Test CLI Verbose Mode Shows Exception Traceback

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

**Requirements Coverage**: SWR_Cli_00005, SWR_Cli_00009

---

#### SWUT_Cli_00009
**Title**: Test CLI Success Exit Code

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

**Requirements Coverage**: SWR_Cli_00009

---

#### SWUT_Cli_00010
**Title**: Test CLI Supports Directory Input

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

**Requirements Coverage**: SWR_Cli_00003
