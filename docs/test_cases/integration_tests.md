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
