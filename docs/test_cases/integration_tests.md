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
7. Verify the attribute list contains: "consistencyNeeds", "port", "portGroup", "swcMapping", "swComponent", "unitGroup" (Note: CamelCase extraction fix now correctly extracts "consistencyNeeds" instead of truncating to "consistency")
8. Verify the attribute "swcMapping" has kind "ref" and is_ref is true
9. Verify attribute types match expected values: consistencyNeeds: ConsistencyNeeds, port: PortPrototype, portGroup: PortGroup, swcMapping: SwComponentMapping, swComponent: SwComponent, unitGroup: UnitGroup
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
- Attributes: ["consistencyNeeds", "port", "portGroup", "swcMapping", "swComponent", "unitGroup"]
- swcMapping.kind == "ref" and swcMapping.is_ref == True
- Attribute types: {consistencyNeeds: ConsistencyNeeds, port: PortPrototype, portGroup: PortGroup, swcMapping: SwComponentMapping, swComponent: SwComponent, unitGroup: UnitGroup}
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


#### SWIT_00008
**Title**: Test Pattern 5 - Multi-Line Literal Names with Different Suffixes

**Maturity**: accept

**Description**: Integration test that verifies the Pattern 5 scenario where two literals with the same base name but different suffixes (eventCombinationOnRetrieval and eventCombinationOnStorage) are parsed as separate literals, each with their own description and tags.

**Precondition**: examples/pdf/AUTOSAR_CP_TPS_DiagnosticExtractTemplate.pdf exists

**Test Steps**:
1. Parse the PDF file examples/pdf/AUTOSAR_CP_TPS_DiagnosticExtractTemplate.pdf
2. Find the DiagnosticEventCombinationBehaviorEnum enumeration in the extracted packages
3. Verify enumeration has exactly two literals
4. Verify both literal names are either "eventCombinationOnRetrieval" or "eventCombinationOnStorage"
5. Verify both literals have different names (one is OnRetrieval, one is OnStorage)
6. For each literal:
   - Verify description is not None
   - Verify index is not None
   - Verify tags attribute exists
   - Verify description contains expected content ("retrieval" or "storage")
7. Verify descriptions are clean (no tag patterns like "atp.EnumerationLiteralIndex")

**Expected Result**:
- DiagnosticEventCombinationBehaviorEnum enumeration found
- Exactly 2 literals present (separate literals with same base name, different suffixes)
- Literal names: eventCombinationOnRetrieval and eventCombinationOnStorage (order may vary)
- Both literals have proper structure (description, index, tags)
- Descriptions are clean of tag patterns
- Pattern 5 correctly handled (two separate literals with same base name, different suffixes)

**Requirements Coverage**: SWR_PARSER_00015, SWR_PARSER_00031

**Test Data**:
- PDF: examples/pdf/AUTOSAR_CP_TPS_DiagnosticExtractTemplate.pdf
- Enumeration: DiagnosticEventCombinationBehaviorEnum
- Expected result: 2 literals total
  - eventCombinationOnRetrieval (with description and tags, index=1)
  - eventCombinationOnStorage (with description and tags, index=0)
- Scenario: Two separate literals with same base name, different suffixes (Pattern 5)

**Test Implementation**:
- Test method: `test_diagnostic_event_combination_behavior_enum_swit_00008`
- Test file: `tests/integration/test_pdf_integration.py`
- Fixture: `diagnostic_extract_template_pdf` (session-scoped)

---

#### SWIT_00009
**Title**: Test Parsing BSWModuleDescriptionTemplate PDF and Verifying BswModuleDescription Class

**Maturity**: accept

**Description**: Integration test that parses the AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf PDF file and verifies the BswModuleDescription class with all its attributes, base classes, and attribute types.

**Precondition**: File examples/pdf/AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf exists

**Test Steps**:
1. Parse the PDF file examples/pdf/AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf using the PdfParser
2. Find the BswModuleDescription class in the extracted packages (searching through M2 → AUTOSARTemplates → BswModuleTemplate → BswOverview)
3. Verify the class name is "BswModuleDescription"
4. Verify the package name is "M2::AUTOSARTemplates::BswModuleTemplate::BswOverview"
5. Verify the note contains "Root element for the description of a single BSW module or BSW cluster. In case it describes a BSW module, the short name of this element equals the name of the BSW module."
6. Verify the tags contain "atp.recommendedPackage=BswModuleDescriptions"
7. Verify the base list contains all expected base classes (non-ATP interfaces): "ARElement", "ARObject", "CollectableElement", "Identifiable", "MultilanguageReferrable", "PackageableElement", "Referrable"
8. Verify the total number of base classes is 7
9. Verify the implements list contains all ATP interfaces: "AtpBlueprint", "AtpBlueprintable", "AtpClassifier", "AtpFeature", "AtpStructureElement"
10. Verify the total number of implements is 5
11. Verify the attribute list contains all expected attributes (with truncated names due to SWR_PARSER_00012): "bswModule", "expectedEntry", "implemented", "internalBehavior", "moduleId", "providedClient", "providedData", "providedMode", "releasedTrigger", "requiredClient", "requiredData", "requiredMode", "requiredTrigger"
12. Verify the total number of attributes is 13
13. Verify attribute types match expected values (using truncated attribute names)

**Expected Result**:

**BswModuleDescription from BSWModuleDescriptionTemplate PDF**
- Name: "BswModuleDescription"
- Package: "M2::AUTOSARTemplates::BswModuleTemplate::BswOverview"
- Note: Contains "Root element for the description of a single BSW module or BSW cluster. In case it describes a BSW module, the short name of this element equals the name of the BSW module."
- Tags: Contains "atp.recommendedPackage=BswModuleDescriptions"
- Bases (non-ATP interfaces): ["ARElement", "ARObject", "CollectableElement", "Identifiable", "MultilanguageReferrable", "PackageableElement", "Referrable"]
- Total base classes: 7
- Implements (ATP interfaces): ["AtpBlueprint", "AtpBlueprintable", "AtpClassifier", "AtpFeature", "AtpStructureElement"]
- Total implements: 5
- Attributes (with truncated names due to SWR_PARSER_00012): ["bswModule", "expectedEntry", "implemented", "internalBehavior", "moduleId", "providedClient", "providedData", "providedMode", "releasedTrigger", "requiredClient", "requiredData", "requiredMode", "requiredTrigger"]
- Total attributes: 13
- Attribute types verified: YES (using truncated attribute names)
  - bswModule: SwComponent
  - expectedEntry: BswModuleEntry
  - implemented: BswModuleEntry
  - providedClient: BswModuleClientServer
  - providedMode: ModeDeclarationGroup
  - requiredClient: BswModuleClientServer
  - requiredMode: ModeDeclarationGroup

**Requirements Coverage**: SWR_PARSER_00003, SWR_PARSER_00004, SWR_PARSER_00006, SWR_PARSER_00010, SWR_PARSER_00011, SWR_MODEL_00001

**Test Implementation**:
- Test method: `test_bsw_module_description_swit_00009`
- Test file: `tests/integration/test_pdf_integration.py`
- Fixture: `bsw_module_description_pdf` (session-scoped)


---

#### SWIT_00010
**Title**: Test J1939Cluster Hyphenated Attribute Name Continuation

**Maturity**: accept

**Description**: Integration test that verifies the hyphenated attribute name continuation pattern (re- + quest2Support = request2Support) in the J1939Cluster class from AUTOSAR_CP_TPS_DiagnosticExtractTemplate.pdf.

**Precondition**: File examples/pdf/AUTOSAR_CP_TPS_DiagnosticExtractTemplate.pdf exists

**Test Steps**:
1. Parse the PDF file examples/pdf/AUTOSAR_CP_TPS_DiagnosticExtractTemplate.pdf using the PdfParser
2. Find the J1939Cluster class in the extracted packages
3. Verify the class name is "J1939Cluster"
4. Verify the package name is "M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Can::CanTopology"
5. Verify the attribute "request2Support" exists (NOT "re-")
6. Verify the incorrect attribute name "re-" does NOT exist
7. Verify the request2Support attribute type is "Boolean"
8. Verify the request2Support attribute multiplicity is "0..1"
9. Verify the request2Support attribute kind is "attr"
10. Verify the request2Support note mentions "Request2" or "RQST2"
11. Verify other expected attributes exist: "networkId", "usesAddress"

**Expected Result**:

**J1939Cluster from DiagnosticExtractTemplate PDF**
- Name: "J1939Cluster"
- Package: "M2::AUTOSARTemplates::SystemTemplate::Fibex::Fibex4Can::CanTopology"
- Hyphenated attribute continuation: VERIFIED
  - Attribute "request2Support" correctly extracted (NOT "re-")
  - Hyphenated word break (re- + quest2Support) handled correctly
- Attributes: ["networkId", "request2Support", "usesAddress"]
- Total attributes: 3
- request2Support details:
  - Type: "Boolean"
  - Multiplicity: "0..1"
  - Kind: "attr"
  - Note: Contains "Request2" or "RQST2"

**Requirements Coverage**: SWR_PARSER_00010, SWR_PARSER_00012

**Test Implementation**:
- Test method: `test_j1939_cluster_hyphenated_attribute_name_continuation_swit_00010`
- Test file: `tests/integration/test_pdf_integration.py`
- Fixture: `diagnostic_extract_j1939_cluster` (session-scoped)

**Notes**:
- This test validates the fix for hyphenated attribute name continuation
- The PDF has the attribute name split across two lines with a hyphen:
  - Line 1: "re- Boolean 0..1 attr Enables support for the Request2 PGN (RQST2)."
  - Line 2: "quest2Support"
- The parser correctly concatenates these to form "request2Support"
- Test screenshot reference: examples/pdf/Screenshot 2026-02-08 at 12.15.48.png

---

#### SWIT_00011
**Title**: Test Referrable Class CamelCase Attribute Name Extraction

**Maturity**: accept

**Description**: Integration test that verifies the Referrable class from AUTOSAR_FO_TPS_GenericStructureTemplate.pdf has correct attributes, specifically testing the camelCase attribute name extraction fix for "shortNameFragment".

**Precondition**: File examples/pdf/AUTOSAR_FO_TPS_GenericStructureTemplate.pdf exists

**Test Steps**:
1. Parse the PDF file examples/pdf/AUTOSAR_FO_TPS_GenericStructureTemplate.pdf using the PdfParser
2. Navigate to M2::AUTOSARTemplates::GenericStructure::GeneralTemplateClasses::Identifiable package
3. Retrieve Referrable class
4. Verify class name is "Referrable"
5. Verify class is abstract
6. Verify base classes include "ARObject"
7. Verify total attribute count is 2
8. Verify first attribute "shortName" exists with:
   - Type: "Identifier"
   - Multiplicity: "1"
   - Kind: "attr"
9. Verify second attribute "shortNameFragment" exists with:
   - Type: "ShortNameFragment"
   - Multiplicity: "*"
   - Kind: "aggr"
10. Verify both attributes have notes

**Expected Result**:

**Referrable from GenericStructureTemplate PDF**
- Name: "Referrable"
- Package: "M2::AUTOSARTemplates::GenericStructure::GeneralTemplateClasses::Identifiable"
- Abstract: True
- Base classes: ["ARObject"]
- Total attributes: 2
- Attributes:
  - shortName (Identifier, 1, attr)
  - shortNameFragment (ShortNameFragment, *, aggr)
- CamelCase attribute extraction: VERIFIED
  - "shortNameFragment" correctly extracted from "shortName ShortNameFragment * aggr"
  - First attribute "shortName" preserved (not overwritten)

**Requirements Coverage**: SWR_PARSER_00003, SWR_PARSER_00004, SWR_PARSER_00010, SWR_PARSER_00012, SWR_MODEL_00001

**Test Implementation**:
- Test method: `test_parse_real_autosar_pdf_and_verify_referrable_attributes`
- Test file: `tests/integration/test_pdf_integration.py`
- Fixture: `generic_structure_referrable` (session-scoped)

**Notes**:
- This test validates the fix for camelCase attribute name extraction (SWUT_PARSER_00102)
- The PDF has the attribute "shortNameFragment" where the PDF text extraction splits the camelCase name:
  - Expected attribute name: "shortNameFragment"
  - Extracted as: "shortName ShortNameFragment * aggr"
- Before the fix: Only 1 attribute "shortName" (type: "ShortNameFragment") was captured
- After the fix: Both "shortName" and "shortNameFragment" are correctly extracted
- The fix detects when the second word starts with the capitalized version of the first word
  and combines them to form the camelCase attribute name


---

#### SWIT_00012
**Title**: Test BswModuleDescription Class CamelCase Attribute Name and Type Split Across Lines

**Maturity**: accept

**Description**: Integration test that verifies the BswModuleDescription class from AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf correctly handles camelCase attribute names and types that are split across PDF lines. This test validates the look-ahead fragment detection and merging fix for attributes like "bswModuleDocumentation" where the PDF text extraction splits both the name and type across lines.

**Precondition**: File examples/pdf/AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf exists

**Test Steps**:
1. Parse the PDF file examples/pdf/AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate.pdf using the PdfParser
2. Navigate to M2::AUTOSARTemplates::BswModuleTemplate::BswOverview package
3. Retrieve BswModuleDescription class
4. Verify class name is "BswModuleDescription"
5. Verify the class is NOT abstract
6. Verify the attribute "bswModuleDocumentation" exists with:
   - Type: "SwComponentDocumentation"
   - Multiplicity: "0..1"
   - Kind: "aggr"
7. Verify the attribute note contains "documentation" (case-insensitive)
8. Verify NO attribute named "bswModule" exists (this would indicate incorrect parsing)
9. Verify NO attribute named "SwComponent" exists (this would indicate incorrect type parsing)

**Expected Result**:

**BswModuleDescription from BSWModuleDescriptionTemplate PDF**
- Name: "BswModuleDescription"
- Package: "M2::AUTOSARTemplates::BswModuleTemplate::BswOverview"
- Abstract: False
- Attributes includes "bswModuleDocumentation" (SwComponentDocumentation, 0..1, aggr)
- NO attribute "bswModule" (fragment would indicate incomplete parsing)
- NO attribute "SwComponent" (incomplete type would indicate incorrect parsing)
- Attribute note contains "documentation"

**CamelCase fragment merging: VERIFIED**
- PDF text extraction splits the attribute across lines:
  - Line 37: "bswModule SwComponent 0..1 aggr This adds documentation..."
  - Line 38: "Documentation Documentation"
- Before the fix: Created attribute "bswModule" with type "SwComponent" (both incomplete)
- After the fix: Creates attribute "bswModuleDocumentation" with type "SwComponentDocumentation"
- The fix detects when BOTH name and type are short fragments and looks ahead to the next line
- When the next line contains continuation words, it merges them with both fragments

**Requirements Coverage**: SWR_PARSER_00003, SWR_PARSER_00004, SWR_PARSER_00010, SWR_PARSER_00012, SWR_MODEL_00001

**Test Implementation**:
- Test method: `test_parse_bsw_module_description_pdf_and_verify_camelcase_fragment_attributes`
- Test file: `tests/integration/test_pdf_integration.py`
- Fixture: `bsw_module_description_pdf` (session-scoped)

**Notes**:
- This test validates the fix for camelCase attribute name and type split across lines (SWUT_PARSER_00102)
- The fix handles the specific case where PDF text extraction splits compound camelCase words at line boundaries
- Key scenarios tested:
  1. Both attribute name and type are fragments (short, incomplete)
  2. Continuation line contains two words (one for name, one for type)
  3. Orphaned look-ahead fragments are properly finalized when no continuation exists
  4. Previous pending attributes are finalized before returning look-ahead markers
