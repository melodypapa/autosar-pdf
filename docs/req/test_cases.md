# Test Cases: autosar-pdf2txt

## Test Statistics

- **Total Tests**: 109
- **Modules**: Models, Parser (3), Writer
- **Coverage Target**: 100% (models, parser), ≥95% (writer)

---

## Module 1: Models (autosar_models.py)

### Test Suite: TestAutosarClass

#### TC-MODEL-001: test_init_concrete_class
- **Description**: Test creating a concrete class
- **Precondition**: None
- **Test Steps**:
  1. Create AutosarClass with name="RunnableEntity" and is_abstract=False
  2. Verify cls.name equals "RunnableEntity"
  3. Verify cls.is_abstract equals False
- **Expected Result**: Class is created with correct name and abstract status

#### TC-MODEL-002: test_init_abstract_class
- **Description**: Test creating an abstract class
- **Precondition**: None
- **Test Steps**:
  1. Create AutosarClass with name="InternalBehavior" and is_abstract=True
  2. Verify cls.name equals "InternalBehavior"
  3. Verify cls.is_abstract equals True
- **Expected Result**: Class is created with correct name and abstract status

#### TC-MODEL-003: test_post_init_valid_name
- **Description**: Test valid name validation
- **Precondition**: None
- **Test Steps**:
  1. Create AutosarClass with name="ValidClass"
  2. Verify cls.name equals "ValidClass"
- **Expected Result**: Valid name is accepted

#### TC-MODEL-004: test_post_init_empty_name
- **Description**: Test empty name raises ValueError
- **Precondition**: None
- **Test Steps**:
  1. Attempt to create AutosarClass with name="" and is_abstract=False
- **Expected Result**: ValueError raised with message "Class name cannot be empty"

#### TC-MODEL-005: test_post_init_whitespace_name
- **Description**: Test whitespace-only name raises ValueError
- **Precondition**: None
- **Test Steps**:
  1. Attempt to create AutosarClass with name="   " and is_abstract=False
- **Expected Result**: ValueError raised with message "Class name cannot be empty"

#### TC-MODEL-006: test_str_concrete_class
- **Description**: Test string representation of concrete class
- **Precondition**: AutosarClass instance exists
- **Test Steps**:
  1. Create AutosarClass with name="MyClass" and is_abstract=False
  2. Call str(cls)
- **Expected Result**: Returns "MyClass"

#### TC-MODEL-007: test_str_abstract_class
- **Description**: Test string representation of abstract class
- **Precondition**: AutosarClass instance exists
- **Test Steps**:
  1. Create AutosarClass with name="AbstractClass" and is_abstract=True
  2. Call str(cls)
- **Expected Result**: Returns "AbstractClass (abstract)"

#### TC-MODEL-008: test_repr
- **Description**: Test __repr__ method
- **Precondition**: AutosarClass instance exists
- **Test Steps**:
  1. Create AutosarClass with name="TestClass" and is_abstract=True
  2. Call repr(cls)
  3. Verify result contains "AutosarClass", "name='TestClass'", and "is_abstract=True"
- **Expected Result**: repr() returns valid representation with all attributes

---

### Test Suite: TestAutosarPackage

#### TC-MODEL-009: test_init_empty_package
- **Description**: Test creating an empty package
- **Precondition**: None
- **Test Steps**:
  1. Create AutosarPackage with name="TestPackage"
  2. Verify pkg.name equals "TestPackage"
  3. Verify pkg.classes is empty
  4. Verify pkg.subpackages is empty
- **Expected Result**: Package created with correct name and empty collections

#### TC-MODEL-010: test_init_with_classes
- **Description**: Test creating a package with classes
- **Precondition**: Two AutosarClass instances created
- **Test Steps**:
  1. Create cls1 with name="Class1" and cls2 with name="Class2"
  2. Create AutosarPackage with name="TestPackage" and classes=[cls1, cls2]
  3. Verify len(pkg.classes) equals 2
  4. Verify pkg.classes[0].name equals "Class1"
  5. Verify pkg.classes[1].name equals "Class2"
- **Expected Result**: Package created with all classes in correct order

#### TC-MODEL-011: test_init_with_subpackages
- **Description**: Test creating a package with subpackages
- **Precondition**: One AutosarPackage (subpkg) instance created
- **Test Steps**:
  1. Create subpkg with name="SubPackage"
  2. Create AutosarPackage with name="TestPackage" and subpackages=[subpkg]
  3. Verify len(pkg.subpackages) equals 1
  4. Verify pkg.subpackages[0].name equals "SubPackage"
- **Expected Result**: Package created with subpackage

#### TC-MODEL-012: test_post_init_valid_name
- **Description**: Test valid name validation for package
- **Precondition**: None
- **Test Steps**:
  1. Create AutosarPackage with name="ValidPackage"
  2. Verify pkg.name equals "ValidPackage"
- **Expected Result**: Valid name is accepted

#### TC-MODEL-013: test_post_init_empty_name
- **Description**: Test empty package name raises ValueError
- **Precondition**: None
- **Test Steps**:
  1. Attempt to create AutosarPackage with name=""
- **Expected Result**: ValueError raised with message "Package name cannot be empty"

#### TC-MODEL-014: test_post_init_whitespace_name
- **Description**: Test whitespace-only package name raises ValueError
- **Precondition**: None
- **Test Steps**:
  1. Attempt to create AutosarPackage with name="   "
- **Expected Result**: ValueError raised with message "Package name cannot be empty"

#### TC-MODEL-015: test_add_class_success
- **Description**: Test successfully adding a class
- **Precondition**: AutosarPackage and AutosarClass instances exist
- **Test Steps**:
  1. Create AutosarPackage with name="TestPackage"
  2. Create AutosarClass with name="NewClass"
  3. Call pkg.add_class(cls)
  4. Verify len(pkg.classes) equals 1
  5. Verify pkg.classes[0] equals cls
- **Expected Result**: Class successfully added to package

#### TC-MODEL-016: test_add_class_duplicate
- **Description**: Test adding duplicate class raises ValueError
- **Precondition**: AutosarPackage instance with one class exists
- **Test Steps**:
  1. Create AutosarPackage with name="TestPackage"
  2. Create cls1 with name="DuplicateClass" and is_abstract=False
  3. Create cls2 with name="DuplicateClass" and is_abstract=True
  4. Add cls1 to package
  5. Attempt to add cls2 to package
- **Expected Result**: ValueError raised with message "already exists"

#### TC-MODEL-017: test_add_subpackage_success
- **Description**: Test successfully adding a subpackage
- **Precondition**: AutosarPackage instances exist (parent and child)
- **Test Steps**:
  1. Create parent AutosarPackage with name="ParentPackage"
  2. Create child AutosarPackage with name="ChildPackage"
  3. Call parent.add_subpackage(child)
  4. Verify len(parent.subpackages) equals 1
  5. Verify parent.subpackages[0] equals child
- **Expected Result**: Subpackage successfully added

#### TC-MODEL-018: test_add_subpackage_duplicate
- **Description**: Test adding duplicate subpackage raises ValueError
- **Precondition**: AutosarPackage instances exist
- **Test Steps**:
  1. Create parent AutosarPackage with name="ParentPackage"
  2. Create subpkg1 with name="DuplicateSub"
  3. Create subpkg2 with name="DuplicateSub"
  4. Add subpkg1 to parent
  5. Attempt to add subpkg2 to parent
- **Expected Result**: ValueError raised with message "already exists"

#### TC-MODEL-019: test_get_class_found
- **Description**: Test finding an existing class
- **Precondition**: AutosarPackage with one class exists
- **Test Steps**:
  1. Create AutosarPackage with name="TestPackage"
  2. Create and add AutosarClass with name="TargetClass"
  3. Call pkg.get_class("TargetClass")
  4. Verify result is not None
  5. Verify result.name equals "TargetClass"
- **Expected Result**: Returns the correct class object

#### TC-MODEL-020: test_get_class_not_found
- **Description**: Test finding a non-existent class
- **Precondition**: AutosarPackage instance exists
- **Test Steps**:
  1. Create AutosarPackage with name="TestPackage"
  2. Call pkg.get_class("NonExistent")
- **Expected Result**: Returns None

#### TC-MODEL-021: test_get_subpackage_found
- **Description**: Test finding an existing subpackage
- **Precondition**: AutosarPackage with subpackage exists
- **Test Steps**:
  1. Create parent AutosarPackage with name="ParentPackage"
  2. Create and add subpkg with name="TargetSub"
  3. Call pkg.get_subpackage("TargetSub")
  4. Verify result is not None
  5. Verify result.name equals "TargetSub"
- **Expected Result**: Returns the correct subpackage object

#### TC-MODEL-022: test_get_subpackage_not_found
- **Description**: Test finding a non-existent subpackage
- **Precondition**: AutosarPackage instance exists
- **Test Steps**:
  1. Create AutosarPackage with name="ParentPackage"
  2. Call pkg.get_subpackage("NonExistent")
- **Expected Result**: Returns None

#### TC-MODEL-023: test_has_class_true
- **Description**: Test has_class returns True when class exists
- **Precondition**: AutosarPackage with class exists
- **Test Steps**:
  1. Create AutosarPackage with name="TestPackage"
  2. Create and add AutosarClass with name="ExistingClass"
  3. Call pkg.has_class("ExistingClass")
- **Expected Result**: Returns True

#### TC-MODEL-024: test_has_class_false
- **Description**: Test has_class returns False when class doesn't exist
- **Precondition**: AutosarPackage instance exists
- **Test Steps**:
  1. Create AutosarPackage with name="TestPackage"
  2. Call pkg.has_class("NonExistent")
- **Expected Result**: Returns False

#### TC-MODEL-025: test_has_subpackage_true
- **Description**: Test has_subpackage returns True when subpackage exists
- **Precondition**: AutosarPackage with subpackage exists
- **Test Steps**:
  1. Create parent AutosarPackage with name="ParentPackage"
  2. Create and add subpkg with name="ExistingSub"
  3. Call pkg.has_subpackage("ExistingSub")
- **Expected Result**: Returns True

#### TC-MODEL-026: test_has_subpackage_false
- **Description**: Test has_subpackage returns False when subpackage doesn't exist
- **Precondition**: AutosarPackage instance exists
- **Test Steps**:
  1. Create AutosarPackage with name="ParentPackage"
  2. Call pkg.has_subpackage("NonExistent")
- **Expected Result**: Returns False

#### TC-MODEL-027: test_str_package_with_classes_only
- **Description**: Test string representation of package with only classes
- **Precondition**: AutosarPackage with 2 classes exists
- **Test Steps**:
  1. Create AutosarPackage with name="TestPackage"
  2. Add Class1 (concrete) and Class2 (abstract)
  3. Call str(pkg)
  4. Verify result contains "TestPackage"
  5. Verify result contains "2 classes"
- **Expected Result**: String shows package name and class count

#### TC-MODEL-028: test_str_package_with_subpackages_only
- **Description**: Test string representation of package with only subpackages
- **Precondition**: AutosarPackage with 2 subpackages exists
- **Test Steps**:
  1. Create AutosarPackage with name="TestPackage"
  2. Add Sub1 and Sub2 subpackages
  3. Call str(pkg)
  4. Verify result contains "TestPackage"
  5. Verify result contains "2 subpackages"
- **Expected Result**: String shows package name and subpackage count

#### TC-MODEL-029: test_str_package_with_both
- **Description**: Test string representation of package with both classes and subpackages
- **Precondition**: AutosarPackage with class and subpackage exists
- **Test Steps**:
  1. Create AutosarPackage with name="TestPackage"
  2. Add one class and one subpackage
  3. Call str(pkg)
  4. Verify result contains "TestPackage"
  5. Verify result contains "1 classes"
  6. Verify result contains "1 subpackages"
- **Expected Result**: String shows package name with both counts

#### TC-MODEL-030: test_str_empty_package
- **Description**: Test string representation of empty package
- **Precondition**: Empty AutosarPackage exists
- **Test Steps**:
  1. Create AutosarPackage with name="EmptyPackage"
  2. Call str(pkg)
- **Expected Result**: String contains "EmptyPackage"

#### TC-MODEL-031: test_repr
- **Description**: Test __repr__ method for package
- **Precondition**: AutosarPackage with class and subpackage exists
- **Test Steps**:
  1. Create AutosarPackage with name="TestPackage"
  2. Add one class and one subpackage
  3. Call repr(pkg)
  4. Verify result contains "AutosarPackage", "name='TestPackage'", "classes=1", "subpackages=1"
- **Expected Result**: repr() returns valid representation with all attributes

#### TC-MODEL-032: test_nested_packages
- **Description**: Test nested package structure
- **Precondition**: None
- **Test Steps**:
  1. Create root AutosarPackage with name="Root"
  2. Create child AutosarPackage with name="Child"
  3. Create grandchild AutosarPackage with name="Grandchild"
  4. Add child to root
  5. Add grandchild to child
  6. Verify root.subpackages length is 1
  7. Verify root.get_subpackage("Child") equals child
  8. Verify child.get_subpackage("Grandchild") equals grandchild
- **Expected Result**: Three-level nesting works correctly

---

## Module 2: Parser - PDF Reader (pdf_reader.py)

### Test Suite: TestPDFReader

#### TC-PDFR-001: test_init_auto_backend_with_pdfplumber
- **Description**: Test auto-selecting pdfplumber backend
- **Precondition**: pdfplumber available, fitz and pypdf unavailable
- **Test Steps**:
  1. Patch HAS_PDFPLUMBER to True, HAS_FITZ to False, HAS_PYPDF to False
  2. Create PDFReader with backend="auto"
  3. Verify reader.backend equals "pdfplumber"
- **Expected Result**: pdfplumber backend is selected

#### TC-PDFR-002: test_init_auto_backend_with_fitz
- **Description**: Test auto-selecting fitz backend
- **Precondition**: fitz available, pdfplumber and pypdf unavailable
- **Test Steps**:
  1. Patch HAS_PDFPLUMBER to False, HAS_FITZ to True, HAS_PYPDF to False
  2. Create PDFReader with backend="auto"
  3. Verify reader.backend equals "fitz"
- **Expected Result**: fitz backend is selected

#### TC-PDFR-003: test_init_auto_backend_with_pypdf
- **Description**: Test auto-selecting pypdf backend
- **Precondition**: pypdf available, pdfplumber and fitz unavailable
- **Test Steps**:
  1. Patch HAS_PDFPLUMBER to False, HAS_FITZ to False, HAS_PYPDF to True
  2. Create PDFReader with backend="auto"
  3. Verify reader.backend equals "pypdf"
- **Expected Result**: pypdf backend is selected

#### TC-PDFR-004: test_init_auto_backend_no_backend_available
- **Description**: Test ValueError is raised when no backend is available
- **Precondition**: All backends unavailable
- **Test Steps**:
  1. Patch HAS_PDFPLUMBER to False, HAS_FITZ to False, HAS_PYPDF to False
  2. Attempt to create PDFReader with backend="auto"
- **Expected Result**: ValueError raised with message "No PDF backend available"

#### TC-PDFR-005: test_init_pdfplumber_backend_available
- **Description**: Test specifying pdfplumber backend (available)
- **Precondition**: pdfplumber available
- **Test Steps**:
  1. Patch HAS_PDFPLUMBER to True
  2. Create PDFReader with backend="pdfplumber"
  3. Verify reader.backend equals "pdfplumber"
- **Expected Result**: pdfplumber backend is selected

#### TC-PDFR-006: test_init_pdfplumber_backend_unavailable
- **Description**: Test specifying pdfplumber backend (unavailable)
- **Precondition**: pdfplumber unavailable
- **Test Steps**:
  1. Patch HAS_PDFPLUMBER to False
  2. Attempt to create PDFReader with backend="pdfplumber"
- **Expected Result**: ValueError raised with message "pdfplumber backend not available"

#### TC-PDFR-007: test_init_fitz_backend_available
- **Description**: Test specifying fitz backend (available)
- **Precondition**: fitz available
- **Test Steps**:
  1. Patch HAS_FITZ to True
  2. Create PDFReader with backend="fitz"
  3. Verify reader.backend equals "fitz"
- **Expected Result**: fitz backend is selected

#### TC-PDFR-008: test_init_fitz_backend_unavailable
- **Description**: Test specifying fitz backend (unavailable)
- **Precondition**: fitz unavailable
- **Test Steps**:
  1. Patch HAS_FITZ to False
  2. Attempt to create PDFReader with backend="fitz"
- **Expected Result**: ValueError raised with message "fitz backend not available"

#### TC-PDFR-009: test_init_pypdf_backend_available
- **Description**: Test specifying pypdf backend (available)
- **Precondition**: pypdf available
- **Test Steps**:
  1. Patch HAS_PYPDF to True
  2. Create PDFReader with backend="pypdf"
  3. Verify reader.backend equals "pypdf"
- **Expected Result**: pypdf backend is selected

#### TC-PDFR-010: test_init_pypdf_backend_unavailable
- **Description**: Test specifying pypdf backend (unavailable)
- **Precondition**: pypdf unavailable
- **Test Steps**:
  1. Patch HAS_PYPDF to False
  2. Attempt to create PDFReader with backend="pypdf"
- **Expected Result**: ValueError raised with message "pypdf backend not available"

#### TC-PDFR-011: test_read_text_with_pdfplumber
- **Description**: Test reading text with pdfplumber
- **Precondition**: pdfplumber backend available and mocked
- **Test Steps**:
  1. Patch HAS_PDFPLUMBER to True
  2. Create PDFReader with backend="pdfplumber"
  3. Mock pdfplumber.open to return mock PDF with page returning "Sample text from PDF"
  4. Call reader.read_text("test.pdf")
  5. Verify result contains "Sample text from PDF"
- **Expected Result**: Text extracted from PDF using pdfplumber

#### TC-PDFR-012: test_read_text_with_pdfplumber_error
- **Description**: Test pdfplumber read error
- **Precondition**: pdfplumber backend available
- **Test Steps**:
  1. Patch HAS_PDFPLUMBER to True
  2. Create PDFReader with backend="pdfplumber"
  3. Mock pdfplumber.open to raise Exception("Read error")
  4. Attempt to call reader.read_text("test.pdf")
- **Expected Result**: ValueError raised with message "Error reading PDF with pdfplumber"

#### TC-PDFR-013: test_read_text_with_pypdf
- **Description**: Test reading text with pypdf
- **Precondition**: pypdf backend available, test PDF file exists
- **Test Steps**:
  1. Patch HAS_PYPDF to True
  2. Create PDFReader with backend="pypdf"
  3. Create test PDF file with dummy content
  4. Mock pypdf.PdfReader to return mock PDF with page returning "Sample text from pypdf"
  5. Call reader.read_text(test_pdf_path)
  6. Verify result contains "Sample text from pypdf"
- **Expected Result**: Text extracted from PDF using pypdf

#### TC-PDFR-014: test_read_text_with_pypdf_file_not_found
- **Description**: Test pypdf file not found
- **Precondition**: pypdf backend available
- **Test Steps**:
  1. Patch HAS_PYPDF to True
  2. Create PDFReader with backend="pypdf"
  3. Attempt to call reader.read_text("/nonexistent/file.pdf")
- **Expected Result**: FileNotFoundError raised

#### TC-PDFR-015: test_read_text_with_pypdf_error
- **Description**: Test pypdf read error
- **Precondition**: pypdf backend available
- **Test Steps**:
  1. Patch HAS_PYPDF to True
  2. Create PDFReader with backend="pypdf"
  3. Mock open() to raise Exception("Read error")
  4. Attempt to call reader.read_text(test_pdf_path)
- **Expected Result**: ValueError raised with message "Error reading PDF with pypdf"

#### TC-PDFR-016: test_read_text_with_fitz
- **Description**: Test reading text with fitz
- **Precondition**: fitz backend available and mocked
- **Test Steps**:
  1. Patch HAS_FITZ to True
  2. Mock fitz module with open() returning mock doc
  3. Reload pdf_reader module
  4. Create PDFReader with backend="fitz"
  5. Mock page.get_text to return "Sample text from fitz"
  6. Call reader._read_with_fitz("test.pdf")
  7. Verify result contains "Sample text from fitz"
  8. Reload pdf_reader module
- **Expected Result**: Text extracted from PDF using fitz

#### TC-PDFR-017: test_read_text_with_fitz_error
- **Description**: Test fitz read error
- **Precondition**: fitz backend available and mocked
- **Test Steps**:
  1. Patch HAS_FITZ to True
  2. Mock fitz module with open() raising Exception("Read error")
  3. Reload pdf_reader module
  4. Create PDFReader with backend="fitz"
  5. Attempt to call reader._read_with_fitz("test.pdf")
  6. Reload pdf_reader module
- **Expected Result**: ValueError raised with message "Error reading PDF with fitz"

#### TC-PDFR-018: test_read_text_dispatches_to_correct_backend
- **Description**: Test read_text dispatches to correct backend
- **Precondition**: PDFReader instance exists with backend set
- **Test Steps**:
  1. Create PDFReader with backend="auto"
  2. Manually set reader.backend to "pdfplumber"
  3. Mock reader._read_with_pdfplumber to return "pdfplumber text"
  4. Call reader.read_text("test.pdf")
  5. Verify result equals "pdfplumber text"
- **Expected Result**: Correct backend method is called

#### TC-PDFR-019: test_read_text_unknown_backend
- **Description**: Test read_text with unknown backend
- **Precondition**: PDFReader instance exists
- **Test Steps**:
  1. Create PDFReader with backend="auto"
  2. Manually set reader.backend to "unknown"
  3. Attempt to call reader.read_text("test.pdf")
- **Expected Result**: ValueError raised with message "Unknown backend"

---

### Test Suite: TestReadPDFFunctional

#### TC-PDFR-020: test_read_pdf_functional
- **Description**: Test functional interface
- **Precondition**: PDFReader class can be mocked
- **Test Steps**:
  1. Mock PDFReader class
  2. Mock read_text to return "extracted text"
  3. Call read_pdf("test.pdf", backend="pdfplumber")
  4. Verify result equals "extracted text"
  5. Verify PDFReader called with backend="pdfplumber"
  6. Verify read_text called with "test.pdf"
- **Expected Result**: Functional interface correctly delegates to PDFReader

---

## Module 3: Parser - Hierarchy Parser (hierarchy_parser.py)

### Test Suite: TestHierarchyParserInit

#### TC-HP-001: test_init
- **Description**: Test initialization
- **Precondition**: None
- **Test Steps**:
  1. Create HierarchyParser with text="* Package\n    * Class"
  2. Verify parser.text equals input text
  3. Verify parser.lines equals ["* Package", "    * Class"]
- **Expected Result**: Parser initialized with correct text and lines

---

### Test Suite: TestParseLine

#### TC-HP-002: test_parse_line_valid_hierarchy
- **Description**: Test parsing valid hierarchy line
- **Precondition**: HierarchyParser instance exists
- **Test Steps**:
  1. Create HierarchyParser with "* Package"
  2. Call parser._parse_line("* Package")
  3. Verify level equals 0, name equals "Package", is_abstract equals False
- **Expected Result**: Correct level, name, and abstract status returned

#### TC-HP-003: test_parse_line_with_leading_spaces
- **Description**: Test parsing line with leading spaces
- **Precondition**: HierarchyParser instance exists
- **Test Steps**:
  1. Create HierarchyParser with "* Package"
  2. Call parser._parse_line("  * SubPackage")
  3. Verify level equals 2, name equals "SubPackage"
- **Expected Result**: Leading spaces correctly counted as level

#### TC-HP-004: test_parse_line_with_abstract
- **Description**: Test parsing line with abstract marker
- **Precondition**: HierarchyParser instance exists
- **Test Steps**:
  1. Create HierarchyParser with "* Package"
  2. Call parser._parse_line("* ClassName (abstract)")
  3. Verify name equals "ClassName", is_abstract equals True
- **Expected Result**: Abstract marker detected and removed from name

#### TC-HP-005: test_parse_line_abstract_with_spaces
- **Description**: Test parsing abstract marker with spaces before it
- **Precondition**: HierarchyParser instance exists
- **Test Steps**:
  1. Create HierarchyParser with "* Package"
  2. Call parser._parse_line("    * ClassName (abstract)")
  3. Verify level equals 4, name equals "ClassName", is_abstract equals True
- **Expected Result**: Both indentation and abstract marker correctly parsed

#### TC-HP-006: test_parse_line_no_asterisk
- **Description**: Test parsing line without asterisk
- **Precondition**: HierarchyParser instance exists
- **Test Steps**:
  1. Create HierarchyParser with "* Package"
  2. Call parser._parse_line("Just text")
  3. Verify level equals -1, name equals ""
- **Expected Result**: Invalid line returns -1 level and empty name

#### TC-HP-007: test_parse_line_empty_content_after_asterisk
- **Description**: Test parsing line with empty content after asterisk
- **Precondition**: HierarchyParser instance exists
- **Test Steps**:
  1. Create HierarchyParser with "* Package"
  2. Call parser._parse_line("*     ")
  3. Verify level equals 0, name equals ""
- **Expected Result**: Level detected but name is empty

#### TC-HP-008: test_parse_line_empty_line
- **Description**: Test parsing empty line
- **Precondition**: HierarchyParser instance exists
- **Test Steps**:
  1. Create HierarchyParser with ""
  2. Call parser._parse_line("")
  3. Verify level equals -1
- **Expected Result**: Empty line returns -1 level

---

### Test Suite: TestIsPackageLine

#### TC-HP-009: test_is_package_line_with_children
- **Description**: Test line with children is identified as package
- **Precondition**: Parsed lines available
- **Test Steps**:
  1. Create HierarchyParser with ""
  2. Create lines list with [(0, "Package", False), (2, "Class", False)]
  3. Call parser._is_package_line(lines, 0)
- **Expected Result**: Returns True (line has child with greater level)

#### TC-HP-010: test_is_package_line_last_line
- **Description**: Test last line is not identified as package
- **Precondition**: Parsed lines available
- **Test Steps**:
  1. Create HierarchyParser with ""
  2. Create lines list with [(0, "Class", False)]
  3. Call parser._is_package_line(lines, 0)
- **Expected Result**: Returns False (no children)

#### TC-HP-011: test_is_package_line_no_children
- **Description**: Test line without children is not identified as package
- **Precondition**: Parsed lines available
- **Test Steps**:
  1. Create HierarchyParser with ""
  2. Create lines list with [(0, "Package", False), (0, "Sibling", False)]
  3. Call parser._is_package_line(lines, 0)
- **Expected Result**: Returns False (next line has same/sibling level)

---

### Test Suite: TestParseHierarchy

#### TC-HP-012: test_parse_empty_text
- **Description**: Test parsing empty text
- **Precondition**: HierarchyParser with empty text
- **Test Steps**:
  1. Create HierarchyParser with ""
  2. Call parser._parse_hierarchy()
- **Expected Result**: Returns empty list

#### TC-HP-013: test_parse_no_valid_lines
- **Description**: Test parsing text with no valid lines
- **Precondition**: HierarchyParser with non-hierarchy text
- **Test Steps**:
  1. Create HierarchyParser with "Just random text\nWithout asterisks"
  2. Call parser._parse_hierarchy()
- **Expected Result**: Returns empty list

#### TC-HP-014: test_parse_single_package
- **Description**: Test parsing single package
- **Precondition**: HierarchyParser with package text
- **Test Steps**:
  1. Create HierarchyParser with "* Package"
  2. Call parser.parse()
  3. Verify result length equals 1
  4. Verify result[0].name equals "Package"
- **Expected Result**: Returns list with one package

#### TC-HP-015: test_parse_package_with_class
- **Description**: Test parsing package with class
- **Precondition**: HierarchyParser with package and class text
- **Test Steps**:
  1. Create HierarchyParser with "* Package\n    * Class"
  2. Call parser._parse_hierarchy()
  3. Verify result length equals 1
  4. Verify result[0].name equals "Package"
  5. Verify result[0].classes length equals 1
  6. Verify result[0].classes[0].name equals "Class"
- **Expected Result**: Package contains one class

#### TC-HP-016: test_parse_nested_packages
- **Description**: Test parsing nested packages
- **Precondition**: HierarchyParser with nested structure
- **Test Steps**:
  1. Create HierarchyParser with "* RootPackage\n  * SubPackage\n      * Class"
  2. Call parser._parse_hierarchy()
  3. Verify result[0].name equals "RootPackage"
  4. Verify result[0].subpackages length equals 1
  5. Verify result[0].subpackages[0].name equals "SubPackage"
  6. Verify result[0].subpackages[0].classes length equals 1
- **Expected Result**: Three-level nesting correctly parsed

#### TC-HP-017: test_parse_multiple_top_level_packages
- **Description**: Test parsing multiple top-level packages
- **Precondition**: HierarchyParser with multiple packages
- **Test Steps**:
  1. Create HierarchyParser with "* Package1\n    * Class1\n* Package2\n    * Class2"
  2. Call parser._parse_hierarchy()
  3. Verify result length equals 2
  4. Verify result[0].name equals "Package1"
  5. Verify result[1].name equals "Package2"
- **Expected Result**: Returns two top-level packages

#### TC-HP-018: test_parse_abstract_class
- **Description**: Test parsing abstract class
- **Precondition**: HierarchyParser with abstract class
- **Test Steps**:
  1. Create HierarchyParser with "* Package\n    * ConcreteClass\n    * AbstractClass (abstract)"
  2. Call parser._parse_hierarchy()
  3. Verify result[0].classes length equals 2
  4. Verify result[0].classes[0].is_abstract equals False
  5. Verify result[0].classes[1].is_abstract equals True
- **Expected Result**: Abstract class correctly marked

#### TC-HP-019: test_parse_duplicate_detection
- **Description**: Test duplicate detection
- **Precondition**: HierarchyParser with duplicate class names
- **Test Steps**:
  1. Create HierarchyParser with "* Package\n    * MyClass\n    * MyClass"
  2. Call parser._parse_hierarchy()
  3. Verify result[0].classes length equals 1
  4. Verify result[0].classes[0].name equals "MyClass"
- **Expected Result**: Only first class added, duplicate skipped

#### TC-HP-020: test_parse_complex_hierarchy
- **Description**: Test parsing complex hierarchy
- **Precondition**: HierarchyParser with multi-level nested structure
- **Test Steps**:
  1. Create HierarchyParser with AUTOSAR template hierarchy
  2. Call parser._parse_hierarchy()
  3. Verify root package name equals "AUTOSARTemplates"
  4. Verify root has 2 subpackages
  5. Verify BswModuleTemplate subpackage structure
  6. Verify BswBehavior contains 3 classes including abstract ones
- **Expected Result**: Complex multi-level hierarchy correctly parsed

#### TC-HP-021: test_parse_with_blank_lines
- **Description**: Test parsing with blank lines
- **Precondition**: HierarchyParser with blank lines in hierarchy
- **Test Steps**:
  1. Create HierarchyParser with "* Package\n\n    * Class\n\n    * AnotherClass"
  2. Call parser._parse_hierarchy()
  3. Verify result length equals 1
  4. Verify result[0].classes length equals 2
- **Expected Result**: Blank lines ignored, classes parsed correctly

---

### Test Suite: TestParse

#### TC-HP-022: test_parse_method
- **Description**: Test parse method
- **Precondition**: HierarchyParser with simple hierarchy
- **Test Steps**:
  1. Create HierarchyParser with "* Package\n    * Class"
  2. Call parser.parse()
  3. Verify result length equals 1
- **Expected Result**: Returns parsed packages

---

### Test Suite: TestFunctionalInterface

#### TC-HP-023: test_parse_hierarchy_function
- **Description**: Test parse_hierarchy function
- **Precondition**: None
- **Test Steps**:
  1. Call parse_hierarchy with "* Package\n    * Class1\n    * Class2 (abstract)"
  2. Verify result length equals 1
  3. Verify result[0].name equals "Package"
  4. Verify result[0].classes length equals 2
  5. Verify result[0].classes[1].is_abstract equals True
- **Expected Result**: Functional interface correctly parses hierarchy

---

## Module 4: Parser - Autosar Parser (autosar_parser.py)

### Test Suite: TestAutosarParser

#### TC-AP-001: test_init_default_backend
- **Description**: Test initialization with default backend
- **Precondition**: PDFReader can be mocked
- **Test Steps**:
  1. Mock PDFReader class
  2. Create AutosarParser()
  3. Verify parser.pdf_reader is not None
- **Expected Result**: Parser initialized with PDFReader

#### TC-AP-002: test_init_custom_backend
- **Description**: Test initialization with custom backend
- **Precondition**: PDFReader can be mocked
- **Test Steps**:
  1. Mock PDFReader class
  2. Create AutosarParser(pdf_backend="pdfplumber")
  3. Verify parser.pdf_reader is not None
- **Expected Result**: Parser initialized with custom backend

#### TC-AP-003: test_parse_pdf_success
- **Description**: Test successful PDF parsing
- **Precondition**: AutosarParser instance exists with mocked reader
- **Test Steps**:
  1. Create AutosarParser
  2. Mock pdf_reader.read_text to return hierarchy text
  3. Call parser.parse_pdf("test.pdf")
  4. Verify result length equals 1
  5. Verify result[0].name equals "TestPackage"
  6. Verify result[0].classes[0].name equals "TestClass"
  7. Verify read_text called with "test.pdf"
- **Expected Result**: Returns parsed packages from PDF text

#### TC-AP-004: test_parse_pdf_with_nested_structure
- **Description**: Test parsing PDF with nested structure
- **Precondition**: AutosarParser instance exists with mocked reader
- **Test Steps**:
  1. Create AutosarParser
  2. Mock pdf_reader.read_text to return nested hierarchy text
  3. Call parser.parse_pdf("test.pdf")
  4. Verify root package structure
  5. Verify subpackage exists
  6. Verify subpackage contains concrete and abstract classes
- **Expected Result**: Nested structure correctly parsed

#### TC-AP-005: test_parse_pdf_empty_result
- **Description**: Test parsing PDF with no hierarchy
- **Precondition**: AutosarParser instance exists with mocked reader
- **Test Steps**:
  1. Create AutosarParser
  2. Mock pdf_reader.read_text to return "No hierarchy here\nJust plain text"
  3. Call parser.parse_pdf("test.pdf")
  4. Verify result length equals 0
- **Expected Result**: Returns empty list when no hierarchy found

#### TC-AP-006: test_parse_pdf_to_text
- **Description**: Test parse_pdf_to_text method
- **Precondition**: AutosarParser instance exists with mocked reader
- **Test Steps**:
  1. Create AutosarParser
  2. Mock pdf_reader.read_text to return "Extracted text from PDF"
  3. Call parser.parse_pdf_to_text("test.pdf")
  4. Verify result equals "Extracted text from PDF"
  5. Verify read_text called with "test.pdf"
- **Expected Result**: Returns raw text from PDF

---

### Test Suite: TestFunctionalInterface

#### TC-AP-007: test_parse_autosar_pdf
- **Description**: Test parse_autosar_pdf function
- **Precondition**: AutosarParser can be mocked
- **Test Steps**:
  1. Mock AutosarParser class
  2. Mock parse_pdf to return [AutosarPackage(name="TestPackage")]
  3. Call parse_autosar_pdf("test.pdf", pdf_backend="pdfplumber")
  4. Verify packages equals mock_packages
  5. Verify AutosarParser called with pdf_backend="pdfplumber"
  6. Verify parse_pdf called with "test.pdf"
- **Expected Result**: Functional interface correctly delegates to AutosarParser

#### TC-AP-008: test_extract_pdf_text
- **Description**: Test extract_pdf_text function
- **Precondition**: PDFReader can be mocked
- **Test Steps**:
  1. Mock PDFReader class
  2. Mock read_text to return "PDF text content"
  3. Call extract_pdf_text("test.pdf", pdf_backend="fitz")
  4. Verify result equals "PDF text content"
  5. Verify PDFReader called with backend="fitz"
  6. Verify read_text called with "test.pdf"
- **Expected Result**: Functional interface extracts PDF text correctly

#### TC-AP-009: test_extract_pdf_text_default_backend
- **Description**: Test extract_pdf_text with default backend
- **Precondition**: PDFReader can be mocked
- **Test Steps**:
  1. Mock PDFReader class
  2. Mock read_text to return "PDF text"
  3. Call extract_pdf_text("test.pdf")
  4. Verify result equals "PDF text"
  5. Verify PDFReader called with backend="auto"
- **Expected Result**: Default backend="auto" is used

---

### Test Suite: TestIntegration

#### TC-AP-010: test_full_workflow
- **Description**: Test complete workflow
- **Precondition**: AutosarParser instance exists
- **Test Steps**:
  1. Create test hierarchy text with AUTOSAR template structure
  2. Create AutosarParser
  3. Mock pdf_reader.read_text to return hierarchy text
  4. Call parser.parse_pdf("test.pdf")
  5. Verify complete package hierarchy parsed correctly
  6. Verify all levels and classes present
- **Expected Result**: Full workflow from PDF to packages works correctly

---

## Module 5: Writer - Markdown Writer (markdown_writer.py)

### Test Suite: TestMarkdownWriter

#### TC-MDW-001: test_init_default
- **Description**: Test initialization with default settings
- **Precondition**: None
- **Test Steps**:
  1. Create MarkdownWriter()
  2. Verify writer.deduplicate equals True
  3. Verify writer._seen_packages equals empty set
  4. Verify writer._seen_classes equals empty set
- **Expected Result**: Writer initialized with deduplication enabled

#### TC-MDW-002: test_init_no_deduplication
- **Description**: Test initialization with deduplication disabled
- **Precondition**: None
- **Test Steps**:
  1. Create MarkdownWriter(deduplicate=False)
  2. Verify writer.deduplicate equals False
- **Expected Result**: Writer initialized with deduplication disabled

#### TC-MDW-003: test_write_single_empty_package
- **Description**: Test writing a single empty package
- **Precondition**: AutosarPackage instance exists
- **Test Steps**:
  1. Create AutosarPackage with name="TestPackage"
  2. Create MarkdownWriter()
  3. Call writer.write_packages([pkg])
  4. Verify result equals "* TestPackage\n"
- **Expected Result**: Package name written with asterisk

#### TC-MDW-004: test_write_package_with_class
- **Description**: Test writing a package with a class
- **Precondition**: AutosarPackage with class exists
- **Test Steps**:
  1. Create AutosarPackage with name="TestPackage"
  2. Add AutosarClass with name="MyClass"
  3. Create MarkdownWriter()
  4. Call writer.write_packages([pkg])
  5. Verify result equals "* TestPackage\n    * MyClass\n"
- **Expected Result**: Package and class written with proper indentation

#### TC-MDW-005: test_write_package_with_abstract_class
- **Description**: Test writing a package with an abstract class
- **Precondition**: AutosarPackage with abstract class exists
- **Test Steps**:
  1. Create AutosarPackage with name="TestPackage"
  2. Add abstract AutosarClass with name="AbstractClass"
  3. Create MarkdownWriter()
  4. Call writer.write_packages([pkg])
  5. Verify result equals "* TestPackage\n    * AbstractClass (abstract)\n"
- **Expected Result**: Abstract class marked with "(abstract)" suffix

#### TC-MDW-006: test_write_package_with_multiple_classes
- **Description**: Test writing a package with multiple classes
- **Precondition**: AutosarPackage with 3 classes exists
- **Test Steps**:
  1. Create AutosarPackage with name="TestPackage"
  2. Add Class1 (concrete), Class2 (abstract), Class3 (concrete)
  3. Create MarkdownWriter()
  4. Call writer.write_packages([pkg])
  5. Verify all three classes appear in output
  6. Verify Class2 marked as abstract
- **Expected Result**: All classes written in correct order with proper markers

#### TC-MDW-007: test_write_nested_packages
- **Description**: Test writing nested packages
- **Precondition**: Two-level package hierarchy exists
- **Test Steps**:
  1. Create root AutosarPackage with name="RootPackage"
  2. Create child AutosarPackage with name="ChildPackage"
  3. Add class to child
  4. Add child to root
  5. Create MarkdownWriter()
  6. Call writer.write_packages([root])
  7. Verify output has proper indentation for both levels
- **Expected Result**: Nested packages with correct indentation (2 spaces per level)

#### TC-MDW-008: test_write_complex_hierarchy
- **Description**: Test writing complex nested hierarchy
- **Precondition**: Multi-level AUTOSAR template hierarchy exists
- **Test Steps**:
  1. Create AUTOSARTemplates package
  2. Create BswModuleTemplate subpackage
  3. Create BswBehavior sub-subpackage
  4. Add BswInternalBehavior and ExecutableEntity (abstract) classes
  5. Create MarkdownWriter()
  6. Call writer.write_packages([root])
  7. Verify complete hierarchy with proper indentation
- **Expected Result**: Four-level hierarchy correctly formatted

#### TC-MDW-009: test_write_multiple_top_level_packages
- **Description**: Test writing multiple top-level packages
- **Precondition**: Two separate packages exist
- **Test Steps**:
  1. Create pkg1 with class Class1
  2. Create pkg2 with abstract class Class2
  3. Create MarkdownWriter()
  4. Call writer.write_packages([pkg1, pkg2])
  5. Verify both packages appear at same level
- **Expected Result**: Multiple top-level packages written sequentially

#### TC-MDW-010: test_write_deeply_nested_hierarchy
- **Description**: Test writing deeply nested package structure
- **Precondition**: Three-level package hierarchy exists
- **Test Steps**:
  1. Create Level1 package
  2. Create Level2 package under Level1
  3. Create Level3 package under Level2
  4. Add DeepClass to Level3
  5. Create MarkdownWriter()
  6. Call writer.write_packages([level1])
  7. Verify four levels of indentation
- **Expected Result**: Deep nesting with increasing indentation (0, 2, 4, 6 spaces)

#### TC-MDW-011: test_deduplicate_classes_across_calls
- **Description**: Test that duplicate classes across multiple write calls are skipped
- **Precondition**: AutosarPackage with class exists, MarkdownWriter with deduplication
- **Test Steps**:
  1. Create AutosarPackage with MyClass
  2. Create MarkdownWriter(deduplicate=True)
  3. Call writer.write_packages([pkg]) - first time
  4. Verify output contains package and class
  5. Call writer.write_packages([pkg]) - second time
  6. Verify second output is empty
- **Expected Result**: Second write returns empty due to deduplication

#### TC-MDW-012: test_deduplicate_classes_same_path
- **Description**: Test that duplicate classes in the same hierarchy path are skipped
- **Precondition**: Two packages with same structure exist
- **Test Steps**:
  1. Create pkg with MyClass and OtherClass
  2. Create MarkdownWriter(deduplicate=True)
  3. Call writer.write_packages([pkg]) - first write
  4. Verify output contains both classes
  5. Create pkg2 with same classes
  6. Call writer.write_packages([pkg2]) - second write
  7. Verify second output is empty
- **Expected Result**: Duplicate path skipped in second write

#### TC-MDW-013: test_deduplicate_subpackages_across_calls
- **Description**: Test that duplicate subpackages across multiple write calls are skipped
- **Precondition**: Nested package structure exists
- **Test Steps**:
  1. Create parent package with child subpackage containing class
  2. Create MarkdownWriter(deduplicate=True)
  3. Call writer.write_packages([parent]) - first time
  4. Verify output contains both packages
  5. Call writer.write_packages([parent]) - second time
  6. Verify second output is empty
- **Expected Result**: Entire hierarchy skipped on second write

#### TC-MDW-014: test_no_deduplicate_mode
- **Description**: Test that deduplication can be disabled
- **Precondition**: Two packages with same name exist
- **Test Steps**:
  1. Create pkg1 with MyClass
  2. Create pkg2 with OtherClass
  3. Create MarkdownWriter(deduplicate=False)
  4. Call writer.write_packages([pkg1, pkg2])
  5. Verify both packages written
  6. Verify both classes written
- **Expected Result**: Duplicate packages allowed when deduplication disabled

#### TC-MDW-015: test_write_empty_package_list
- **Description**: Test writing an empty package list
- **Precondition**: MarkdownWriter instance exists
- **Test Steps**:
  1. Create MarkdownWriter()
  2. Call writer.write_packages([])
- **Expected Result**: Returns empty string

#### TC-MDW-016: test_write_package_with_both_classes_and_subpackages
- **Description**: Test writing package with both classes and subpackages
- **Precondition**: Package with class and subpackage exists
- **Test Steps**:
  1. Create parent package with DirectClass
  2. Create child subpackage with ChildClass (abstract)
  3. Add child to parent
  4. Create MarkdownWriter()
  5. Call writer.write_packages([pkg])
  6. Verify DirectClass at level+2 indentation
  7. Verify ChildPackage at level+1 indentation
  8. Verify ChildClass at level+3 indentation
- **Expected Result**: Mixed classes and subpackages with correct indentation

#### TC-MDW-017: test_multiple_calls_with_deduplication
- **Description**: Test that deduplication persists across multiple calls
- **Precondition**: Package with class exists
- **Test Steps**:
  1. Create AutosarPackage with MyClass
  2. Create MarkdownWriter(deduplicate=True)
  3. Call writer.write_packages([pkg]) - first call
  4. Verify output contains package and class
  5. Call writer.write_packages([pkg]) - second call
  6. Verify second output is empty
- **Expected Result**: Deduplication state persists across calls

#### TC-MDW-018: test_nested_duplicate_tracking
- **Description**: Test duplicate tracking works across nested structures
- **Precondition**: Root package with two subpackages containing same class name
- **Test Steps**:
  1. Create pkg1 with CommonClass
  2. Create pkg2 with CommonClass
  3. Create root package
  4. Add pkg1 and pkg2 to root
  5. Create MarkdownWriter(deduplicate=True)
  6. Call writer.write_packages([root])
  7. Verify both CommonClass instances written (different paths)
  8. Verify count of "* CommonClass" equals 2
- **Expected Result**: Same class name allowed in different package paths

---

### Test Suite: TestFunctionalInterface

#### TC-MDW-019: test_write_markdown_function
- **Description**: Test write_markdown function
- **Precondition**: AutosarPackage with class exists
- **Test Steps**:
  1. Create AutosarPackage with name="TestPackage"
  2. Add AutosarClass with name="MyClass"
  3. Call write_markdown([pkg])
  4. Verify result equals "* TestPackage\n    * MyClass\n"
- **Expected Result**: Functional interface produces correct output

#### TC-MDW-020: test_write_markdown_with_deduplicate_false
- **Description**: Test write_markdown with deduplication disabled
- **Precondition**: Two packages with same name exist
- **Test Steps**:
  1. Create pkg1 with MyClass
  2. Create pkg2 with OtherClass
  3. Call write_markdown([pkg1, pkg2], deduplicate=False)
  4. Verify count of "* TestPackage" equals 2
  5. Verify MyClass present
  6. Verify OtherClass present
- **Expected Result**: Both packages written without deduplication

#### TC-MDW-021: test_write_markdown_with_deduplicate_true
- **Description**: Test write_markdown with deduplication enabled
- **Precondition**: Two packages with same name exist
- **Test Steps**:
  1. Create pkg1 with MyClass
  2. Create pkg2 with OtherClass
  3. Call write_markdown([pkg1, pkg2], deduplicate=True)
  4. Verify result equals "* TestPackage\n    * MyClass\n"
  5. Verify only first package and class written
- **Expected Result**: Deduplication prevents duplicate packages

#### TC-MDW-022: test_write_markdown_empty_list
- **Description**: Test write_markdown with empty package list
- **Precondition**: None
- **Test Steps**:
  1. Call write_markdown([])
- **Expected Result**: Returns empty string

---

## Test Summary by Module

| Module | Test Cases | Coverage Target |
|--------|-----------|-----------------|
| Models | 32 | 100% |
| Parser - PDF Reader | 20 | 100% |
| Parser - Hierarchy Parser | 23 | 100% |
| Parser - Autosar Parser | 10 | 100% |
| Writer - Markdown Writer | 22 | ≥95% |
| **Total** | **107** | **99%** |

---

## Test Execution Commands

```bash
# Run all tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ -v --cov=src/autosar_pdf2txt --cov-report=term-missing

# Run specific module tests
pytest tests/models/ -v
pytest tests/parser/ -v
pytest tests/writer/ -v

# Run specific test class
pytest tests/models/test_autosar_models.py::TestAutosarClass -v

# Run specific test case
pytest tests/models/test_autosar_models.py::TestAutosarClass::test_init_concrete_class -v
```
