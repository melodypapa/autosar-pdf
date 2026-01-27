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
**Title**: Test Parsing Real AUTOSAR PDF and Verifying AUTOSAR, SwComponentType, and ARElement Classes

**Maturity**: accept

**Description**: Integration test that parses real AUTOSAR PDF files and verifies three classes:
1. The AUTOSAR class from GenericStructureTemplate PDF
2. The SwComponentType class from GenericStructureTemplate PDF (including attributes, attribute kinds, and note support)
3. The ARElement class and its subclasses from GenericStructureTemplate PDF

**Precondition**: examples/pdf/AUTOSAR_FO_TPS_GenericStructureTemplate.pdf exist

**Test Steps**:

**Part 1: Verify AUTOSAR class from GenericStructureTemplate PDF**
1. Parse the PDF file examples/pdf/AUTOSAR_FO_TPS_GenericStructureTemplate.pdf
2. Find the AUTOSAR class in the extracted packages (searching through M2 → AUTOSARTemplates → AutosarTopLevelStructure)
3. Verify the class name is "AUTOSAR"
4. Verify the class is not abstract (is_abstract=False)
5. Verify the class has one base class "ARObject" (bases=["ARObject"])
6. Verify the class has a note containing "AUTOSAR" or "Rootelement"
7. Verify the class is in the "AutosarTopLevelStructure" package under M2 → AUTOSARTemplates
8. Verify the note contains proper word spacing
9. Verify the source information is present (source is not None)
10. Verify the source pdf_file is "AUTOSAR_FO_TPS_GenericStructureTemplate.pdf"
11. Verify the source autosar_standard is "Foundation"
12. Verify the source standard_release is "R23-11"

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

**Part 3: Verify ARElement class and its subclasses from GenericStructureTemplate PDF**
1. Parse the PDF file examples/pdf/AUTOSAR_FO_TPS_GenericStructureTemplate.pdf
2. Find the ARElement class in the extracted packages
3. Verify the class name is "ARElement"
4. Verify the class is abstract (is_abstract=True)
5. Verify the subclasses list contains all expected subclasses (128 total)
6. Verify all expected subclasses are present: AclObjectSet, AclOperation, AclPermission, AclRole, AliasNameSet, ApplicabilityInfoSet, ApplicationPartition, AutosarDataType, BaseType, BlueprintMappingSet, BswEntryRelationshipSet, BswModuleDescription, BswModuleEntry, BuildActionManifest, CalibrationParameterValueSet, ClientIdDefinitionSet, ClientServerInterfaceToBswModuleEntryBlueprintMapping, Collection, CompuMethod, ConsistencyNeedsBlueprintSet, ConstantSpecification, ConstantSpecificationMappingSet, CpSoftwareCluster, CpSoftwareClusterBinaryManifestDescriptor, CpSoftwareClusterMappingSet, CpSoftwareClusterResourcePool, CryptoEllipticCurveProps, CryptoServiceCertificate, CryptoServiceKey, CryptoServicePrimitive, CryptoServiceQueue, CryptoSignatureScheme, DataConstr, DataExchangePoint, DataTransformationSet, DataTypeMappingSet, DdsCpConfig, DiagnosticCommonElement, DiagnosticConnection, DiagnosticContributionSet, DltContext, DltEcu, Documentation, E2EProfileCompatibilityProps, EcucDefinitionCollection, EcucDestinationUriDefSet, EcucModuleConfigurationValues, EcucModuleDef, EcucValueCollection, EndToEndProtectionSet, EthIpProps, EthTcpIpIcmpProps, EthTcpIpProps, EvaluatedVariantSet, FMFeature, FMFeatureMap, FMFeatureModel, FMFeatureSelectionSet, FirewallRule, FlatMap, GeneralPurposeConnection, HwCategory, HwElement, HwType, IEEE1722TpConnection, IPSecConfigProps, IPv6ExtHeaderFilterSet, IdsCommonElement, IdsDesign, Implementation, ImpositionTimeDefinitionGroup, InterpolationRoutineMappingSet, J1939ControllerApplication, KeywordSet, LifeCycleInfoSet, LifeCycleStateDefinitionGroup, LogAndTraceMessageCollectionSet, MacSecGlobalKayProps, MacSecParticipantSet, McFunction, McGroup, ModeDeclarationGroup, ModeDeclarationMappingSet, OsTaskProxy, PhysicalDimension, PhysicalDimensionMappingSet, PortInterface, PortInterfaceMappingSet, PortPrototypeBlueprint, PostBuildVariantCriterion, PostBuildVariantCriterionValueSet, PredefinedVariant, RapidPrototypingScenario, SdgDef, SignalServiceTranslationPropsSet, SomeipSdClientEventGroupTimingConfig, SomeipSdClientServiceInstanceConfig, SomeipSdServerEventGroupTimingConfig, SomeipSdServerServiceInstanceConfig, SwAddrMethod, SwAxisType, SwComponentMappingConstraints, SwComponentType, SwRecordLayout, SwSystemconst, SwSystemconstantValueSet, SwcBswMapping, System, SystemSignal, SystemSignalGroup, TDCpSoftwareClusterMappingSet, TcpOptionFilterSet, TimingExtension, TlsConnectionGroup, TlvDataIdDefinitionSet, TransformationPropsSet, Unit, UnitGroup, UploadablePackageElement, ViewMapSet
7. Verify no unexpected subclasses were extracted

**Expected Result**:

**Part 1: AUTOSAR class**
- Name: "AUTOSAR"
- Abstract: False
- Bases: ["ARObject"]
- Note contains "AUTOSAR" or "Rootelement" with proper word spacing
- Package hierarchy: M2 → AUTOSARTemplates → AutosarTopLevelStructure
- Source pdf_file: "AUTOSAR_FO_TPS_GenericStructureTemplate.pdf"
- Source autosar_standard: "Foundation"
- Source standard_release: "R23-11"
- Source page_number: 421

**Part 2: SwComponentType class**
- Name: "SwComponentType"
- Package: "M2::AUTOSARTemplates::SWComponentTemplate::Components"
- Note: "Base class for AUTOSAR software components."
- Bases: ["ARElement", "ARObject", "AtpBlueprint", "AtpBlueprintable", "AtpClassifier", "AtpType", "CollectableElement", "Identifiable", "MultilanguageReferrable", "PackageableElement", "Referrable"]
- Attributes: ["consistency", "port", "portGroup", "swcMapping", "swComponent", "unitGroup"]
- swcMapping.kind == "ref" and swcMapping.is_ref == True
- Attribute types: {consistency: ConsistencyNeeds, port: PortPrototype, portGroup: PortGroup, swcMapping: SwComponentMapping, swComponent: SwComponent, unitGroup: UnitGroup}
- All attributes have notes (single-line for SwComponentType)

**Part 3: ARElement class and subclasses**
- Name: "ARElement"
- Abstract: True
- Subclasses: 128 total
- All expected subclasses present: YES
- No unexpected subclasses: YES

**Requirements Coverage**: SWR_PARSER_00003, SWR_PARSER_00004, SWR_PARSER_00006, SWR_PARSER_00009, SWR_PARSER_00010, SWR_PARSER_00022, SWR_MODEL_00001, SWR_MODEL_00010, SWR_MODEL_00023, SWR_MODEL_00027

---

### 2. BSWModuleDescriptionTemplate PDF Integration Tests

#### SWIT_00002
**Title**: Test Parsing BSWModuleDescriptionTemplate PDF and Verifying AtomicSwComponentType Base Classes

**Maturity**: accept

**Description**: Integration test that parses the AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf PDF file and verifies that the AtomicSwComponentType class has correct base classes.

This test is critical for detecting a multi-page parsing bug where the base class "SwComponentType" gets corrupted to "SwComponentTypeClass AtomicSwComponentType (abstract)" when the class definition spans multiple pages.

**Precondition**: File examples/pdf/AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf exists

**Test Steps**:
1. Parse the PDF file examples/pdf/AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf using the PdfParser
2. Find the AtomicSwComponentType class in the extracted packages (searching through M2 → AUTOSARTemplates → SWComponentTemplate → Components)
3. Verify the class name is "AtomicSwComponentType"
4. Verify the package name is "M2::AUTOSARTemplates::SWComponentTemplate::Components"
5. Verify the base list contains all expected base classes: "ARElement", "ARObject", "AtpBlueprint", "AtpBlueprintable", "AtpClassifier", "AtpType", "CollectableElement", "Identifiable", "MultilanguageReferrable", "PackageableElement", "Referrable", "SwComponentType"
6. Verify SwComponentType is in the base list (indicating AtomicSwComponentType inherits from SwComponentType)
7. **CRITICAL CHECK**: Verify the last base class is exactly "SwComponentType", not "SwComponentTypeClass AtomicSwComponentType (abstract)"
8. Verify the total number of base classes is 12

**Expected Result**:

**AtomicSwComponentType from BSWModuleDescriptionTemplate PDF**
- Name: "AtomicSwComponentType"
- Package: "M2::AUTOSARTemplates::SWComponentTemplate::Components"
- Bases: ["ARElement", "ARObject", "AtpBlueprint", "AtpBlueprintable", "AtpClassifier", "AtpType", "CollectableElement", "Identifiable", "MultilanguageReferrable", "PackageableElement", "Referrable", "SwComponentType"]
- Total base classes: 12
- Last base class: "SwComponentType" (not corrupted)
- SwComponentType is in base list: YES

**Requirements Coverage**: SWR_PARSER_00003, SWR_PARSER_00004, SWR_PARSER_00006, SWR_MODEL_00001

---

### 3. TimingExtensions PDF Integration Tests

#### SWIT_00003
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

**TimingExtensions class list**
- Total extracted types: 148
- All expected classes present: YES
- No missing classes
- No extra classes

**Requirements Coverage**: SWR_PARSER_00003, SWR_PARSER_00004, SWR_PARSER_00006, SWR_MODEL_00001, SWR_MODEL_00023, SWR_MODEL_00010

---

### 4. Enumeration Immutability Tests

#### SWIT_00004
**Title**: Verify DiagnosticDebounceBehaviorEnum from GenericStructureTemplate PDF

**Maturity**: accept

**Description**: Verify that the DiagnosticDebounceBehaviorEnum enumeration is correctly parsed from the AUTOSAR_FO_TPS_GenericStructureTemplate.pdf with multi-line literal descriptions and that its enumeration_literals list is immutable (frozen) after creation.

**Precondition**: File examples/pdf/AUTOSAR_FO_TPS_GenericStructureTemplate.pdf exists

**Test Steps**:
1. Parse the PDF file examples/pdf/AUTOSAR_FO_TPS_GenericStructureTemplate.pdf using the PdfParser
2. Navigate to M2::AUTOSARTemplates::DiagnosticExtract::Dem::DiagnosticDebouncingAlgorithm package
3. Retrieve DiagnosticDebounceBehaviorEnum
4. Verify enumeration name is "DiagnosticDebounceBehaviorEnum"
5. Verify package is "M2::AUTOSARTemplates::DiagnosticExtract::Dem::DiagnosticDebouncingAlgorithm"
6. Verify enumeration_literals is a tuple (immutable type, not list)
7. Attempt to modify enumeration_literals to verify immutability (should raise TypeError)
8. Verify .append() method is not available on enumeration_literals
9. Verify literal count is 2 (freeze and reset)
10. Verify expected literals exist: freeze, reset
11. Verify freeze literal has full multi-line description
12. Verify reset literal has full multi-line description

**Expected Result**:

**DiagnosticDebounceBehaviorEnum verification**
- Enumeration name: "DiagnosticDebounceBehaviorEnum"
- Package: "M2::AUTOSARTemplates::DiagnosticExtract::Dem::DiagnosticDebouncingAlgorithm"
- enumeration_literals type: tuple (immutable)
- Literal count: 2
- Expected literals: freeze, reset
- Multi-line description parsing: VERIFIED
- freeze literal description: Full multi-line description with "event debounce counter will be frozen..."
- reset literal description: Full multi-line description with "event debounce counter will be reset..."
- Immutability verified: Cannot modify tuple, no .append() method

**Requirements Coverage**: SWR_PARSER_00003, SWR_PARSER_00013, SWR_PARSER_00014, SWR_PARSER_00015, SWR_MODEL_00019

**Test Data**:
- PDF: examples/pdf/AUTOSAR_FO_TPS_GenericStructureTemplate.pdf
- Enumeration: DiagnosticDebounceBehaviorEnum
- Expected literals: freeze, reset (2 literals total with multi-line descriptions)

---

#### SWIT_00005
**Title**: Test Enumeration Literal Tags Extraction from Real PDF

**Maturity**: accept

**Description**: Integration test that verifies enumeration literal tags (atp.EnumerationLiteralIndex, xml.name) are extracted correctly from real AUTOSAR PDF files using DiagnosticExtractTemplate.pdf.

**Precondition**: examples/pdf/AUTOSAR_CP_TPS_DiagnosticExtractTemplate.pdf exists

**Test Steps**:
1. Parse the PDF file examples/pdf/AUTOSAR_CP_TPS_DiagnosticExtractTemplate.pdf
2. Find the DiagnosticTypeOfDtcSupportedEnum enumeration in the extracted packages
3. Verify enumeration has literals
4. Verify at least one literal has tags
5. For each literal with tags:
   - Verify tags attribute exists and is a dictionary
   - Verify atp.EnumerationLiteralIndex tag exists (if present)
   - Verify atp.EnumerationLiteralIndex value is numeric string
   - Verify index field matches atp.EnumerationLiteralIndex tag value
   - Verify xml.name tag exists (if present)
   - Verify xml.name value is not empty
   - Verify tags are removed from description (no tag patterns in description text)
6. Verify total count of literals with tags

**Expected Result**:
- DiagnosticTypeOfDtcSupportedEnum enumeration found
- Multiple literals have tags extracted
- All tags are structured correctly (key-value pairs)
- Index field matches atp.EnumerationLiteralIndex tag value
- xml.name tags are present for relevant literals
- Descriptions are clean of all tag patterns
- Tags extraction works correctly on real AUTOSAR PDF

**Requirements Coverage**: SWR_PARSER_00031, SWR_MODEL_00014

**Test Data**:
- PDF: examples/pdf/AUTOSAR_CP_TPS_DiagnosticExtractTemplate.pdf
- Enumeration: DiagnosticTypeOfDtcSupportedEnum
- Expected: Multiple literals with tags (atp.EnumerationLiteralIndex, xml.name)

---

#### SWIT_00006
**Title**: Test Multi-page Enumeration Literal List from Real PDF

**Maturity**: accept

**Description**: Integration test that verifies enumeration literal lists spanning multiple pages are parsed correctly using DiagnosticExtractTemplate.pdf (from enum2.jpg example).

**Precondition**: examples/pdf/AUTOSAR_CP_TPS_DiagnosticExtractTemplate.pdf exists

**Test Steps**:
1. Parse the PDF file examples/pdf/AUTOSAR_CP_TPS_DiagnosticExtractTemplate.pdf
2. Find the ByteOrderEnum enumeration in the extracted packages
3. Verify enumeration has literals
4. Verify expected literals are present:
   - mostSignificantByteFirst
   - mostSignificantByteLast
   - opaque
5. For each literal:
   - Verify literal name is not empty
   - Verify description attribute exists
   - Verify index attribute exists
   - Verify tags attribute exists
   - If description exists, verify it's clean (no tag patterns)
6. Verify source location tracking:
   - Verify enumeration has source information
   - Verify source pdf_file is specified
   - Verify source page_number is specified
7. Verify all literals are extracted (none missing due to page boundaries)

**Expected Result**:
- ByteOrderEnum enumeration found
- All 3 expected literals are present (mostSignificantByteFirst, mostSignificantByteLast, opaque)
- All literals have proper structure (name, description, index, tags)
- Descriptions are clean of tag patterns
- Source location is tracked correctly
- Multi-page parsing works correctly on real AUTOSAR PDF
- No literals are lost due to page boundaries

**Requirements Coverage**: SWR_PARSER_00032, SWR_MODEL_00014, SWR_MODEL_00027

**Test Data**:
- PDF: examples/pdf/AUTOSAR_CP_TPS_DiagnosticExtractTemplate.pdf
- Enumeration: ByteOrderEnum
- Expected literals: mostSignificantByteFirst, mostSignificantByteLast, opaque (3 literals total)
- Multi-page scenario: Enumeration literal list spans multiple pages


#### SWIT_00007
**Title**: Test enum3.png Scenario - Multiple Literal Names Stacked in Single Table Cell

**Maturity**: accept

**Description**: Integration test that verifies the enum3.png scenario where three literal names (reportingIn, ChronlogicalOrder, and OldestFirst) are stacked vertically in one table cell, sharing the same description and tags. The parser recognizes this and creates one combined literal with the name formed by concatenating all three literal names.

**Precondition**: examples/pdf/AUTOSAR_CP_TPS_DiagnosticExtractTemplate.pdf exists

**Test Steps**:
1. Parse the PDF file examples/pdf/AUTOSAR_CP_TPS_DiagnosticExtractTemplate.pdf
2. Find the DiagnosticEventCombinationReportingBehaviorEnum enumeration in the extracted packages
3. Verify enumeration has exactly one literal
4. Verify literal name is "reportingInChronlogicalOrderOldestFirst"
5. Verify literal has proper structure:
   - Verify description is not None
   - Verify index is not None
   - Verify tags attribute exists
6. Verify literal description contains expected content (e.g., "chronological")
7. Verify literal tags are present (atp.EnumerationLiteralIndex)
8. Verify description is clean (no tag patterns like "atp.EnumerationLiteralIndex")
9. Verify source location tracking if available

**Expected Result**:
- DiagnosticEventCombinationReportingBehaviorEnum enumeration found
- Exactly 1 literal present (combined from three stacked names)
- Literal name: reportingInChronlogicalOrderOldestFirst (with full description and tags)
- Literal has description containing "chronological"
- Literal has index attribute
- Literal has tags (atp.EnumerationLiteralIndex)
- Description is clean of tag patterns
- enum3.png scenario correctly handled (three literal names stacked in same cell, combined into one literal)

**Requirements Coverage**: SWR_PARSER_00015, SWR_PARSER_00031

**Test Data**:
- PDF: examples/pdf/AUTOSAR_CP_TPS_DiagnosticExtractTemplate.pdf
- Enumeration: DiagnosticEventCombinationReportingBehaviorEnum
- Source literal names (enum3.png): reportingIn, ChronlogicalOrder, OldestFirst
- Expected result: 1 literal total
  - reportingInChronlogicalOrderOldestFirst (with description and tags)
- Scenario: Three literal names stacked vertically in same table cell, sharing description and tags

**Test Implementation**:
- Test method: `test_diagnostic_event_combination_reporting_behavior_enum_swit_00007`
- Test file: `tests/integration/test_pdf_integration.py`
- Fixture: `diagnostic_extract_template_pdf` (session-scoped)
