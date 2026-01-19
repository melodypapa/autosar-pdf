# Integration Test Cases

## autosar-pdf2txt Integration Tests

This document contains integration test cases for the autosar-pdf2txt package. Integration tests verify that multiple components work together correctly.

## Maturity Levels

Each test case has a maturity level that indicates its status:

- **draft**: Newly created test case, under review, or not yet implemented
- **accept**: Accepted test case, implemented and passing
- **invalid**: Deprecated test case, superseded, or no longer applicable

All existing integration test cases in this document are currently at maturity level **accept**.

---

## Integration Test Scenarios

### 1. PDF Parser Integration Tests

#### SWIT_00001
**Title**: Test Parsing Real AUTOSAR PDF and Verifying First Class

**Maturity**: accept

**Description**: Integration test that parses a real AUTOSAR PDF file and verifies the first extracted class has correct structure including name, abstract flag, base classes, and note with proper word spacing.

**Precondition**: File examples/pdf/AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf exists

**Test Steps**:
1. Create a PdfParser instance
2. Parse the PDF file examples/pdf/AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf
3. Find the first class in the extracted packages (searching through M2 → AUTOSARTemplates → AutosarTopLevelStructure)
4. Verify the class name is "AUTOSAR"
5. Verify the class is not abstract (is_abstract=False)
6. Verify the class has one base class "ARObject" (bases=["ARObject"])
7. Verify the class has a note containing "AUTOSAR" or "Rootelement"
8. Verify the class is in the "AutosarTopLevelStructure" package under M2 → AUTOSARTemplates
9. Verify the note contains proper word spacing (e.g., "Root element" not "Rootelement", "AUTOSAR description" not "AUTOSARdescription")

**Expected Result**: First class is extracted successfully with:
- Name: "AUTOSAR"
- Abstract: False
- Bases: ["ARObject"]
- Note contains "AUTOSAR" or "Rootelement" with proper word spacing
- Package hierarchy: M2 → AUTOSARTemplates → AutosarTopLevelStructure

**Requirements Coverage**: SWR_PARSER_00003, SWR_PARSER_00004, SWR_PARSER_00006, SWR_PARSER_00009, SWR_MODEL_00001

---

#### SWIT_00002
**Title**: Test Parsing Real AUTOSAR PDF Extracts Multiple Classes

**Maturity**: accept

**Description**: Verify that the parser can extract all classes from a large real AUTOSAR PDF file, confirming comprehensive parsing functionality.

**Precondition**: File examples/pdf/AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf exists

**Test Steps**:
1. Create a PdfParser instance
2. Parse the PDF file examples/pdf/AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf
3. Count total classes by iterating through all packages and subpackages
4. Verify that more than 10 classes are extracted (should be 240 in actual PDF)
5. Print total classes and packages extracted

**Expected Result**: Parser successfully extracts many classes (240 classes from 14 packages), demonstrating comprehensive parsing of the entire AUTOSAR template document

**Requirements Coverage**: SWR_PARSER_00003, SWR_PARSER_00006

---

#### SWIT_00003
**Title**: Test Parsing Real AUTOSAR PDF Has Bases and Notes

**Maturity**: accept

**Description**: Verify that classes with base classes and notes are correctly parsed and transferred from real AUTOSAR PDF to the AutosarClass model.

**Precondition**: File examples/pdf/AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf exists

**Test Steps**:
1. Create a PdfParser instance
2. Parse the PDF file examples/pdf/AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf
3. Iterate through all packages and subpackages to find classes with bases
4. Iterate through all packages and subpackages to find classes with notes
5. Verify that multiple classes have base classes (expected: 231)
6. Verify that multiple classes have notes (expected: 240 - all classes)
7. Print counts and examples of classes with bases and notes

**Expected Result**: Parser correctly extracts:
- Many classes with base classes (231 out of 240 classes)
- All classes have notes (240 out of 240 classes)
- Example class shows: Name="AUTOSAR", Bases=["ARObject"], Note contains description

**Requirements Coverage**: SWR_PARSER_00004, SWR_MODEL_00001

---

## Additional Integration Test Scenarios

Future integration tests should cover:
- End-to-end PDF parsing and markdown generation
- CLI functionality with various input combinations
- Error handling across module boundaries
- Performance testing with large PDFs
- Writer output verification with real data

---

#### SWIT_00004
**Title**: Test Parsing ECU Configuration PDF and Verifying Fibex Package Structure and ImplementationDataType Attributes

**Maturity**: accept

**Description**: Integration test that parses an ECU Configuration PDF and verifies:
1. The correct hierarchical package structure, particularly the nested Fibex package hierarchy under M2
2. The ImplementationDataType class has correct attributes (not broken fragments from multi-line PDF table formatting)

**Precondition**: File examples/pdf/AUTOSAR_CP_TPS_ECUConfiguration.pdf exists

**Test Steps**:
1. Create a PdfParser instance
2. Parse the PDF file examples/pdf/AUTOSAR_CP_TPS_ECUConfiguration.pdf
3. Verify there is exactly 1 top-level package (M2)
4. Find AUTOSARTemplates subpackage under M2
5. Find SystemTemplate subpackage under AUTOSARTemplates
6. Find Fibex subpackage under SystemTemplate
7. Find FibexCore subpackage under Fibex
8. Find CoreCommunication subpackage under FibexCore
9. Verify CoreCommunication contains classes
10. Verify specific Fibex classes exist: Frame, NPdu, Pdu, PduTriggering, UserDefinedPdu
11. Verify that Fibex, SystemTemplate, FibexCore, and AUTOSARTemplates are NOT top-level packages
12. Find CommonStructure subpackage under AUTOSARTemplates
13. Find ImplementationDataTypes subpackage under CommonStructure
14. Find ImplementationDataType class in ImplementationDataTypes
15. Verify ImplementationDataType attributes are correct:
    - Should have exactly 5 attributes
    - Should have `dynamicArray: String` attribute
    - Should have `isStructWithOptionalElement: Boolean` attribute
    - Should have `subElement: ImplementationData` attribute
    - Should have `symbolProps: SymbolProps` attribute
    - Should have `typeEmitter: NameToken` attribute
    - Should NOT have broken fragment attributes like:
      - `SizeProfile: data` (continuation fragment)
      - `isStructWith: Boolean` (partial name)
      - `Element: If` (continuation fragment)
      - `ImplementationDataType: has` (continuation fragment)
      - `intention: to` (continuation fragment)

**Expected Result**:
1. Package hierarchy is correctly structured as:
   - M2 (top-level)
     └─ AUTOSARTemplates
        ├─ SystemTemplate
        │  └─ Fibex
        │     └─ FibexCore
        │        └─ CoreCommunication (contains Frame, NPdu, Pdu, PduTriggering, UserDefinedPdu)
        └─ CommonStructure
           └─ ImplementationDataTypes
              └─ ImplementationDataType (with correct attributes)

2. ImplementationDataType has exactly 5 attributes:
   - `dynamicArray: String`
   - `isStructWithOptionalElement: Boolean`
   - `subElement: ImplementationData`
   - `symbolProps: SymbolProps`
   - `typeEmitter: NameToken`

3. Broken attribute fragments are filtered out and not present

**Requirements Coverage**: SWR_PARSER_00003, SWR_PARSER_00004, SWR_PARSER_00006, SWR_PARSER_00009, SWR_PARSER_00010, SWR_PARSER_00011, SWR_PARSER_00012, SWR_MODEL_00004
