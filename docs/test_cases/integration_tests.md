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
**Title**: Test Parsing Real AUTOSAR PDF and Verifying AUTOSAR and SwComponentType Classes

**Maturity**: accept

**Description**: Integration test that parses real AUTOSAR PDF files and verifies two classes:
1. The AUTOSAR class from BSW Module Template PDF
2. The SwComponentType class from GenericStructureTemplate PDF (including attributes, attribute kinds, and note support)

**Precondition**: Files examples/pdf/AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf and examples/pdf/AUTOSAR_FO_TPS_GenericStructureTemplate.pdf exist

**Test Steps**:

**Part 1: Verify AUTOSAR class from BSW Module Template PDF**
1. Parse the PDF file examples/pdf/AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf
2. Find the first class in the extracted packages (searching through M2 → AUTOSARTemplates → AutosarTopLevelStructure)
3. Verify the class name is "AUTOSAR"
4. Verify the class is not abstract (is_abstract=False)
5. Verify the class has one base class "ARObject" (bases=["ARObject"])
6. Verify the class has a note containing "AUTOSAR" or "Rootelement"
7. Verify the class is in the "AutosarTopLevelStructure" package under M2 → AUTOSARTemplates
8. Verify the note contains proper word spacing

**Part 2: Verify SwComponentType class from GenericStructureTemplate PDF**
1. Parse the PDF file examples/pdf/AUTOSAR_FO_TPS_GenericStructureTemplate.pdf
2. Find the SwComponentType class in the extracted packages (searching through M2 → AUTOSARTemplates → SWComponentTemplate → Components)
3. Verify the class name is "SwComponentType"
4. Verify the package name is "M2::AUTOSARTemplates::SWComponentTemplate::Components"
5. Verify the note is "Base class for AUTOSAR software components."
6. Verify the base list contains: "ARElement", "ARObject", "AtpBlueprint", "AtpBlueprintable", "AtpClassifier", "AtpType", "CollectableElement", "Identifiable", "MultilanguageReferrable", "PackageableElement", "Referrable"
7. Verify the attribute list contains: "consistency", "port", "portGroup", "swcMapping", "swComponent", "unitGroup" (Note: Multi-line attributes have truncated names due to SWR_PARSER_00012 filtering)
8. Verify the attribute "swcMapping" has kind "ref" and is_ref is true
9. Verify attribute types match expected values: consistency: ConsistencyNeeds, port: PortPrototype, portGroup: PortGroup, swcMapping: SwComponentMapping, swComponent: SwComponent, unitGroup: UnitGroup
10. Verify attributes have notes (multi-line attribute note support is verified in SWIT_00006)

**Expected Result**:

**Part 1: AUTOSAR class**
- Name: "AUTOSAR"
- Abstract: False
- Bases: ["ARObject"]
- Note contains "AUTOSAR" or "Rootelement" with proper word spacing
- Package hierarchy: M2 → AUTOSARTemplates → AutosarTopLevelStructure

**Part 2: SwComponentType class**
- Name: "SwComponentType"
- Package: "M2::AUTOSARTemplates::SWComponentTemplate::Components"
- Note: "Base class for AUTOSAR software components."
- Bases: ["ARElement", "ARObject", "AtpBlueprint", "AtpBlueprintable", "AtpClassifier", "AtpType", "CollectableElement", "Identifiable", "MultilanguageReferrable", "PackageableElement", "Referrable"]
- Attributes: ["consistency", "port", "portGroup", "swcMapping", "swComponent", "unitGroup"]
- swcMapping.kind == "ref" and swcMapping.is_ref == True
- Attribute types: {consistency: ConsistencyNeeds, port: PortPrototype, portGroup: PortGroup, swcMapping: SwComponentMapping, swComponent: SwComponent, unitGroup: UnitGroup}
- All attributes have notes (single-line for SwComponentType)

**Requirements Coverage**: SWR_PARSER_00003, SWR_PARSER_00004, SWR_PARSER_00006, SWR_PARSER_00009, SWR_PARSER_00010, SWR_MODEL_00001, SWR_MODEL_00010, SWR_MODEL_00023

---

### 2. TimingExtensions PDF Integration Tests

#### SWIT_00002
**Title**: Test Parsing TimingExtensions PDF and Verifying Class List

**Maturity**: accept

**Description**: Integration test that parses the AUTOSAR_CP_TPS_TimingExtensions.pdf PDF file and verifies that all 148 expected AUTOSAR classes, enumerations, and primitives are correctly extracted.

**Precondition**: Files examples/pdf/AUTOSAR_CP_TPS_TimingExtensions.pdf and tests/integration/timing_extensions_class_list.txt exist

**Test Steps**:
1. Read the expected class list from tests/integration/timing_extensions_class_list.txt (excluding comments and empty lines)
2. Verify the class list file contains 148 expected entries
3. Parse the PDF file examples/pdf/AUTOSAR_CP_TPS_TimingExtensions.pdf using the PdfParser
4. Recursively collect all type names (classes, enumerations, and primitives) from the parsed document
5. Verify the total number of extracted types equals 148
6. Verify all expected class names from the file are present in the extracted types
7. Verify no unexpected additional types were extracted

**Expected Result**:
- Total extracted types: 148
- All expected classes present: YES
- No missing classes
- No extra classes

**Requirements Coverage**: SWR_PARSER_00003, SWR_PARSER_00004, SWR_PARSER_00006, SWR_MODEL_00001, SWR_MODEL_00023

