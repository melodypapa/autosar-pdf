"""Integration tests for AUTOSAR PDF parsing.

These tests use real AUTOSAR PDF files to verify end-to-end functionality.

Performance optimization: Tests use session-scoped fixtures defined in conftest.py
to cache parsed PDF data. Each PDF is parsed only once per test session, with
results shared across all tests that need them.
"""

import os
from typing import Optional

import pytest

from autosar_pdf2txt.models import AutosarClass, AutosarDoc, AutosarEnumeration


# Import helper functions from conftest
from tests.integration.conftest import (
    find_class_by_name,
)


def find_enumeration_by_name(doc: AutosarDoc, name: str) -> Optional[AutosarEnumeration]:
    """Find an enumeration by name in the document.

    Args:
        doc: The AutosarDoc to search.
        name: The enumeration name to find.

    Returns:
        The AutosarEnumeration if found, None otherwise.
    """
    for pkg in doc.packages:
        enum = pkg.get_enumeration(name)
        if enum:
            return enum
    return None


class TestPdfIntegration:
    """Integration tests using real AUTOSAR PDF files.

    These tests require actual PDF files to be present in the examples/pdf directory.
    Tests are skipped if files are not available (for CI/CD environments).
    """

    def test_parse_real_autosar_pdf_and_verify_autosar_and_sw_component_type(
        self, generic_structure_template_pdf: AutosarDoc, generic_structure_sw_component_type: AutosarClass
    ) -> None:
        """Test Parsing Real AUTOSAR PDF and Verifying AUTOSAR, SwComponentType, and ARElement Classes.

        Test Case ID: SWIT_00001

        Requirements:
            SWR_PARSER_00001: PDF Parser Initialization
            SWR_PARSER_00003: PDF File Parsing
            SWR_PARSER_00004: Class Definition Pattern Recognition
            SWR_PARSER_00005: Class Definition Data Model
            SWR_PARSER_00006: Package Hierarchy Building
            SWR_PARSER_00010: Attribute Extraction from PDF
            SWR_PARSER_00021: Multi-Line Attribute Parsing for AutosarClass
            SWR_MODEL_00027: AUTOSAR Source Location Representation
            SWR_PARSER_00022: PDF Source Location Extraction

        This test verifies three classes from the GenericStructureTemplate PDF:
        1. The AUTOSAR class (root metamodel class)
        2. The SwComponentType class (including attributes, attribute kinds, and note support)
        3. The ARElement class and its subclasses (inheritance hierarchy)

        Args:
            generic_structure_template_pdf: Parsed GenericStructureTemplate PDF data.
            generic_structure_sw_component_type: Cached SwComponentType class.

        This test is divided into three parts:
        - Part 1: Verify AUTOSAR class
        - Part 2: Verify SwComponentType class
        - Part 3: Verify ARElement class and subclasses
        """
        # ========== Verify AUTOSAR class from GenericStructureTemplate PDF ==========
        packages = generic_structure_template_pdf.packages

        # Verify we got some packages
        assert len(packages) > 0, "Should extract at least one package from PDF"

        # Find the AUTOSAR class explicitly
        first_package, autosar_class = find_class_by_name(packages, "AUTOSAR")

        assert autosar_class is not None, "Should find AUTOSAR class in the PDF"
        assert first_package is not None, "Should find the package containing the AUTOSAR class"

        # Verify the AUTOSAR class details
        assert autosar_class.name == "AUTOSAR", f"Expected class name 'AUTOSAR', got '{autosar_class.name}'"
        assert autosar_class.is_abstract is False, "AUTOSAR class should not be abstract"
        assert first_package.name == "AutosarTopLevelStructure", f"Expected package 'AutosarTopLevelStructure', got '{first_package.name}'"

        # Verify bases - should have one base class
        assert len(autosar_class.bases) == 1, f"Expected 1 base class, got {len(autosar_class.bases)}"
        assert "ARObject" in autosar_class.bases, f"Expected 'ARObject' in bases, got {autosar_class.bases}"

        # Verify note - should have a note
        assert autosar_class.note is not None, "AUTOSAR class should have a note"
        assert len(autosar_class.note) > 0, "Note should not be empty"
        assert "AUTOSAR" in autosar_class.note or "Rootelement" in autosar_class.note, \
            f"Note should contain AUTOSAR or Rootelement, got: '{autosar_class.note}'"

        # Verify source information
        assert autosar_class.sources is not None, "AUTOSAR class should have source information"
        assert autosar_class.sources[0].pdf_file == "AUTOSAR_FO_TPS_GenericStructureTemplate.pdf", \
            f"Expected pdf_file 'AUTOSAR_FO_TPS_GenericStructureTemplate.pdf', got '{autosar_class.sources[0].pdf_file}'"
        assert autosar_class.sources[0].autosar_standard == "Foundation", \
            f"Expected autosar_standard 'Foundation', got '{autosar_class.sources[0].autosar_standard}'"
        assert autosar_class.sources[0].standard_release == "R23-11", \
            f"Expected standard_release 'R23-11', got '{autosar_class.sources[0].standard_release}'"
        # SWR_PARSER_00030: Verify page number is tracked correctly
        assert autosar_class.sources[0].page_number == 421, \
            f"Expected page_number 421, got {autosar_class.sources[0].page_number}"

        # Print AUTOSAR class information for verification
        print("\n=== AUTOSAR class verified ===")
        print(f"  Name: {autosar_class.name}")
        print(f"  Abstract: {autosar_class.is_abstract}")
        print(f"  Bases: {autosar_class.bases}")
        print(f"  Note: {autosar_class.note}")
        print(f"  Package: {first_package.name}")
        print(f"  Source: {autosar_class.sources[0]}")

        # ========== Verify SwComponentType class from GenericStructureTemplate PDF ==========
        sw_component_type = generic_structure_sw_component_type

        # Verify class name
        assert sw_component_type.name == "SwComponentType", \
            f"Expected class name 'SwComponentType', got '{sw_component_type.name}'"

        # Verify package name is M2::AUTOSARTemplates::SWComponentTemplate::Components
        expected_package = "M2::AUTOSARTemplates::SWComponentTemplate::Components"
        assert sw_component_type.package == expected_package, \
            f"Expected package '{expected_package}', got '{sw_component_type.package}'"

        # Verify note
        assert sw_component_type.note is not None, "SwComponentType should have a note"
        assert len(sw_component_type.note) > 0, "Note should not be empty"
        assert sw_component_type.note == "Base class for AUTOSAR software components.", \
            f"Expected note 'Base class for AUTOSAR software components.', got '{sw_component_type.note}'"

        # Verify base list - split into regular bases and Atp interfaces
        # Regular bases (non-Atp)
        expected_bases = [
            "ARElement", "ARObject", "CollectableElement", "Identifiable",
            "MultilanguageReferrable", "PackageableElement", "Referrable"
        ]
        assert len(sw_component_type.bases) == len(expected_bases), \
            f"Expected {len(expected_bases)} base classes, got {len(sw_component_type.bases)}"
        for base in expected_bases:
            assert base in sw_component_type.bases, \
                f"Expected '{base}' in bases, got {sw_component_type.bases}"

        # Atp interfaces (bases starting with "Atp")
        expected_implements = ["AtpBlueprint", "AtpBlueprintable", "AtpClassifier", "AtpType"]
        assert len(sw_component_type.implements) == len(expected_implements), \
            f"Expected {len(expected_implements)} interfaces, got {len(sw_component_type.implements)}"
        for interface in expected_implements:
            assert interface in sw_component_type.implements, \
                f"Expected '{interface}' in implements, got {sw_component_type.implements}"

        # Verify attribute list
        # Note: Multi-line attributes have truncated names due to SWR_PARSER_00012 filtering
        expected_attributes = [
            "consistency", "port", "portGroup", "swcMapping", "swComponent", "unitGroup"
        ]
        assert len(sw_component_type.attributes) == len(expected_attributes), \
            f"Expected {len(expected_attributes)} attributes, got {len(sw_component_type.attributes)}"
        for attr_name in expected_attributes:
            assert attr_name in sw_component_type.attributes, \
                f"Expected attribute '{attr_name}' not found. Got: {list(sw_component_type.attributes.keys())}"

        # Verify swcMapping attribute kind is "ref" and is_ref is true
        swc_mapping = sw_component_type.attributes.get("swcMapping")
        assert swc_mapping is not None, "swcMapping attribute should exist"
        assert swc_mapping.kind.value == "ref", \
            f"Expected swcMapping kind to be 'ref', got '{swc_mapping.kind.value}'"
        assert swc_mapping.is_ref is True, \
            f"Expected swcMapping is_ref to be True, got {swc_mapping.is_ref}"

        # Verify attribute types match expected values
        expected_types = {
            "consistency": "ConsistencyNeeds",
            "port": "PortPrototype",
            "portGroup": "PortGroup",
            "swcMapping": "SwComponentMapping",
            "swComponent": "SwComponent",
            "unitGroup": "UnitGroup"
        }
        for attr_name, expected_type in expected_types.items():
            attr = sw_component_type.attributes.get(attr_name)
            assert attr is not None, f"Attribute '{attr_name}' should exist"
            assert attr.type == expected_type, \
                f"Expected attribute '{attr_name}' to have type '{expected_type}', got '{attr.type}'"

        # Verify attribute notes exist
        attrs_with_notes = [name for name, attr in sw_component_type.attributes.items() if attr.note]
        assert len(attrs_with_notes) > 0, "At least one attribute should have a note"

        # Print SwComponentType class information for verification
        print("\n=== SwComponentType class verified ===")
        print(f"  Name: {sw_component_type.name}")
        print(f"  Package: {sw_component_type.package}")
        print(f"  Abstract: {sw_component_type.is_abstract}")
        print(f"  Bases ({len(sw_component_type.bases)}): {', '.join(sw_component_type.bases)}")
        print(f"  Implements ({len(sw_component_type.implements)}): {', '.join(sw_component_type.implements)}")
        print(f"  Note: {sw_component_type.note}")
        print(f"  Attributes ({len(sw_component_type.attributes)}):")
        for attr_name, attr in sw_component_type.attributes.items():
            print(f"    - {attr_name}: {attr.type} (ref: {attr.is_ref}, kind: {attr.kind.value})")

    def test_parse_real_autosar_pdf_and_verify_arelement_and_subclasses(
        self, generic_structure_arelement: AutosarClass
    ) -> None:
        """Test parsing real AUTOSAR PDF files and verify ARElement class and its subclasses.

        SWIT_00001 Part 3: Verify ARElement class and its subclasses from GenericStructureTemplate PDF

        Requirements:
            SWR_PARSER_00003: PDF File Parsing
            SWR_PARSER_00004: Class Definition Pattern Recognition
            SWR_PARSER_00006: Package Hierarchy Building
            SWR_MODEL_00001: AUTOSAR Class Representation
            SWR_MODEL_00023: AUTOSAR Document Model

        Args:
            generic_structure_arelement: Cached ARElement class from GenericStructureTemplate PDF.
        """
        # ========== Verify ARElement class from GenericStructureTemplate PDF ==========
        arelement = generic_structure_arelement

        # Verify class name
        assert arelement.name == "ARElement", \
            f"Expected class name 'ARElement', got '{arelement.name}'"

        # Verify the class is abstract
        assert arelement.is_abstract is True, "ARElement class should be abstract"

        # Verify the subclasses list contains all expected subclasses (121 total)
        expected_subclasses = [
            "AclObjectSet", "AclOperation", "AclPermission", "AclRole", "AliasNameSet",
            "ApplicabilityInfoSet", "ApplicationPartition", "AutosarDataType", "BaseType",
            "BlueprintMappingSet", "BswEntryRelationshipSet", "BswModuleDescription",
            "BswModuleEntry", "BuildActionManifest", "CalibrationParameterValueSet",
            "ClientIdDefinitionSet", "ClientServerInterfaceToBswModuleEntryBlueprintMapping",
            "Collection", "CompuMethod", "ConsistencyNeedsBlueprintSet", "ConstantSpecification",
            "ConstantSpecificationMappingSet", "CpSoftwareCluster", "CpSoftwareClusterBinaryManifestDescriptor",
            "CpSoftwareClusterMappingSet", "CpSoftwareClusterResourcePool", "CryptoEllipticCurveProps",
            "CryptoServiceCertificate", "CryptoServiceKey", "CryptoServicePrimitive",
            "CryptoServiceQueue", "CryptoSignatureScheme", "DataConstr", "DataExchangePoint",
            "DataTransformationSet", "DataTypeMappingSet", "DdsCpConfig", "DiagnosticCommonElement",
            "DiagnosticConnection", "DiagnosticContributionSet", "DltContext", "DltEcu",
            "Documentation", "E2EProfileCompatibilityProps", "EcucDefinitionCollection",
            "EcucDestinationUriDefSet", "EcucModuleConfigurationValues", "EcucModuleDef",
            "EcucValueCollection", "EndToEndProtectionSet", "EthIpProps", "EthTcpIpIcmpProps",
            "EthTcpIpProps", "EvaluatedVariantSet", "FMFeature", "FMFeatureMap", "FMFeatureModel",
            "FMFeatureSelectionSet", "FirewallRule", "FlatMap", "GeneralPurposeConnection",
            "HwCategory", "HwElement", "HwType", "IEEE1722TpConnection", "IPSecConfigProps",
            "IPv6ExtHeaderFilterSet", "IdsCommonElement", "IdsDesign", "Implementation",
            "ImpositionTimeDefinitionGroup", "InterpolationRoutineMappingSet",
            "J1939ControllerApplication", "KeywordSet", "LifeCycleInfoSet",
            "LifeCycleStateDefinitionGroup", "LogAndTraceMessageCollectionSet",
            "MacSecGlobalKayProps", "MacSecParticipantSet", "McFunction", "McGroup",
            "ModeDeclarationGroup", "ModeDeclarationMappingSet", "OsTaskProxy", "PhysicalDimension",
            "PhysicalDimensionMappingSet", "PortInterface", "PortInterfaceMappingSet",
            "PortPrototypeBlueprint", "PostBuildVariantCriterion", "PostBuildVariantCriterionValueSet",
            "PredefinedVariant", "RapidPrototypingScenario", "SdgDef", "SignalServiceTranslationPropsSet",
            "SomeipSdClientEventGroup", "SomeipSdClientServiceInstanceConfig",
            "SomeipSdServerEventGroupTimingConfig", "SomeipSdServerServiceInstanceConfig",
            "SwAddrMethod", "SwAxisType", "SwComponentMappingConstraints", "SwComponentType",
            "SwRecordLayout", "SwSystemconst", "SwSystemconstantValueSet", "SwcBswMapping",
            "System", "SystemSignal", "SystemSignalGroup", "TDCpSoftwareClusterMappingSet",
            "TcpOptionFilterSet", "TimingConfig", "TimingExtension", "TlsConnectionGroup",
            "TlvDataIdDefinitionSet", "TransformationPropsSet", "Unit", "UnitGroup",
            "UploadablePackageElement", "ViewMapSet"
        ]

        # Verify expected count of subclasses
        expected_count = 121
        assert len(arelement.subclasses) == expected_count, \
            f"Expected {expected_count} subclasses, got {len(arelement.subclasses)}"

        # Verify all expected subclasses are present
        actual_subclasses = arelement.subclasses
        for expected_subclass in expected_subclasses:
            assert expected_subclass in actual_subclasses, \
                f"Expected subclass '{expected_subclass}' not found in ARElement.subclasses"

        # Verify no unexpected subclasses were extracted
        unexpected_subclasses = set(actual_subclasses) - set(expected_subclasses)
        assert not unexpected_subclasses, \
            f"Found unexpected subclasses: {sorted(unexpected_subclasses)}"

        # Print ARElement class information for verification
        print("\n=== ARElement class verified ===")
        print(f"  Name: {arelement.name}")
        print(f"  Abstract: {arelement.is_abstract}")
        print(f"  Subclasses ({len(arelement.subclasses)}):")
        print("    All expected subclasses present: YES")
        print("    No unexpected subclasses: YES")
        print(f"  Sample subclasses: {sorted(arelement.subclasses)[:10]}...")

    def test_parse_timing_extensions_pdf_and_verify_class_list(
        self, timing_extensions_pdf: AutosarDoc
    ) -> None:
        """Test parsing TimingExtensions PDF and verify complete class list.

        SWIT_00002: Test Parsing TimingExtensions PDF and Verifying Class List

        Requirements:
            SWR_PARSER_00003: PDF File Parsing
            SWR_PARSER_00004: Class Definition Pattern Recognition
            SWR_PARSER_00006: Package Hierarchy Building
            SWR_MODEL_00001: AUTOSAR Class Representation
            SWR_MODEL_00023: AUTOSAR Document Model

        Args:
            timing_extensions_pdf: Cached parsed TimingExtensions PDF data (AutosarDoc).
        """
        # Read expected class list from file
        class_list_file = "tests/integration/timing_extensions_class_list.txt"

        if not os.path.exists(class_list_file):
            pytest.skip(f"Class list file not found: {class_list_file}")

        expected_classes = set()
        with open(class_list_file, 'r') as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if line and not line.startswith('#'):
                    expected_classes.add(line)

        # Verify expected count from file header
        expected_count = 148
        assert len(expected_classes) == expected_count, \
            f"Expected {expected_count} classes in file, found {len(expected_classes)}"

        # Extract all class names from parsed PDF
        extracted_classes = set()
        packages = timing_extensions_pdf.packages

        # Collect all classes, enumerations, and primitives recursively
        def collect_types(pkg) -> set:
            """Recursively collect all type names from a package."""
            types = set()
            for typ in pkg.types:
                types.add(typ.name)
            for subpkg in pkg.subpackages:
                types.update(collect_types(subpkg))
            return types

        for pkg in packages:
            extracted_classes.update(collect_types(pkg))

        # Verify total number of classes
        actual_count = len(extracted_classes)
        assert actual_count == expected_count, \
            f"Expected {expected_count} classes, but found {actual_count}"

        # Verify all expected classes are present
        missing_classes = expected_classes - extracted_classes
        assert not missing_classes, \
            f"Missing {len(missing_classes)} classes: {sorted(missing_classes)}"

        # Verify no extra classes were extracted
        extra_classes = extracted_classes - expected_classes
        assert not extra_classes, \
            f"Found {len(extra_classes)} unexpected classes: {sorted(extra_classes)}"

        # Print summary for verification
        print("\n=== TimingExtensions PDF verification ===")
        print(f"  Expected classes: {expected_count}")
        print(f"  Extracted classes: {actual_count}")
        print("  All expected classes found: YES")
        print(f"  Sample classes: {sorted(list(extracted_classes))[:10]}...")

    def test_parse_bsw_module_description_pdf_and_verify_atomic_sw_component_type_bases(
        self, bsw_module_description_atomic_sw_component_type: AutosarClass
    ) -> None:
        """Test parsing BSWModuleDescriptionTemplate PDF and verify AtomicSwComponentType base classes.

        SWIT_00002 Part 2: Verify AtomicSwComponentType base classes from AUTOSAR_CP_TPS_BSWModuleDescriptionTemplate PDF

        This test detects the bug where "SwComponentTypeClass AtomicSwComponentType (abstract)"
        is incorrectly parsed as a base class instead of just "SwComponentType".

        Requirements:
            SWR_PARSER_00003: PDF File Parsing
            SWR_PARSER_00004: Class Definition Pattern Recognition
            SWR_PARSER_00006: Package Hierarchy Building
            SWR_MODEL_00001: AUTOSAR Class Representation

        Args:
            bsw_module_description_atomic_sw_component_type: Cached AtomicSwComponentType class from BSWModuleDescriptionTemplate PDF.
        """
        # ========== Verify AtomicSwComponentType class from BSWModuleDescriptionTemplate PDF ==========
        atomic_sw_component_type = bsw_module_description_atomic_sw_component_type

        # Verify class name
        assert atomic_sw_component_type.name == "AtomicSwComponentType", \
            f"Expected class name 'AtomicSwComponentType', got '{atomic_sw_component_type.name}'"

        # Verify package name is M2::AUTOSARTemplates::SWComponentTemplate::Components
        expected_package = "M2::AUTOSARTemplates::SWComponentTemplate::Components"
        assert atomic_sw_component_type.package == expected_package, \
            f"Expected package '{expected_package}', got '{atomic_sw_component_type.package}'"

        # Verify base list contains all expected base classes
        # Regular bases (non-Atp) including SwComponentType
        expected_bases = [
            "ARElement", "ARObject", "CollectableElement", "Identifiable",
            "MultilanguageReferrable", "PackageableElement", "Referrable", "SwComponentType"
        ]
        assert len(atomic_sw_component_type.bases) == len(expected_bases), \
            f"Expected {len(expected_bases)} base classes, got {len(atomic_sw_component_type.bases)}"

        # This is the critical check - verify each expected base is in the list
        for base in expected_bases:
            assert base in atomic_sw_component_type.bases, \
                f"Expected '{base}' in bases, got {atomic_sw_component_type.bases}"

        # Verify Atp interfaces are in implements field
        expected_implements = ["AtpBlueprint", "AtpBlueprintable", "AtpClassifier", "AtpType"]
        assert len(atomic_sw_component_type.implements) == len(expected_implements), \
            f"Expected {len(expected_implements)} interfaces, got {len(atomic_sw_component_type.implements)}"
        for interface in expected_implements:
            assert interface in atomic_sw_component_type.implements, \
                f"Expected '{interface}' in implements, got {atomic_sw_component_type.implements}"

        # Verify SwComponentType is in the base list (indicating AtomicSwComponentType inherits from SwComponentType)
        assert "SwComponentType" in atomic_sw_component_type.bases, \
            f"Expected 'SwComponentType' in bases, got {atomic_sw_component_type.bases}"

        # CRITICAL: Verify the LAST base class is exactly "SwComponentType", not a corrupted string
        # This catches the bug where it becomes "SwComponentTypeClass AtomicSwComponentType (abstract)"
        assert atomic_sw_component_type.bases[-1] == "SwComponentType", \
            f"Expected last base to be 'SwComponentType', got '{atomic_sw_component_type.bases[-1]}'"

        # Print AtomicSwComponentType class information for verification
        print("\n=== AtomicSwComponentType class verified ===")
        print(f"  Name: {atomic_sw_component_type.name}")
        print(f"  Package: {atomic_sw_component_type.package}")
        print(f"  Abstract: {atomic_sw_component_type.is_abstract}")
        print(f"  Bases ({len(atomic_sw_component_type.bases)}): {', '.join(atomic_sw_component_type.bases)}")
        print(f"  Implements ({len(atomic_sw_component_type.implements)}): {', '.join(atomic_sw_component_type.implements)}")
        print(f"  Last base: {atomic_sw_component_type.bases[-1]}")
        print("  SwComponentType in bases: YES")
        print("  Base corruption check: PASSED")

    def test_parse_timing_extensions_pdf_and_verify_atomic_sw_component_type_bases(
        self, timing_extensions_atomic_sw_component_type: AutosarClass
    ) -> None:
        """Test parsing TimingExtensions PDF and verify AtomicSwComponentType base classes.

        SWIT_00002 Part 2: Verify AtomicSwComponentType base classes from AUTOSAR_CP_TPS_TimingExtensions PDF

        Requirements:
            SWR_PARSER_00003: PDF File Parsing
            SWR_PARSER_00004: Class Definition Pattern Recognition
            SWR_PARSER_00006: Package Hierarchy Building
            SWR_MODEL_00001: AUTOSAR Class Representation
            SWR_MODEL_00010: AUTOSAR Attribute Representation

        Args:
            timing_extensions_atomic_sw_component_type: Cached AtomicSwComponentType class from TimingExtensions PDF.
        """
        # ========== Verify AtomicSwComponentType class from TimingExtensions PDF ==========
        atomic_sw_component_type = timing_extensions_atomic_sw_component_type

        # Verify class name
        assert atomic_sw_component_type.name == "AtomicSwComponentType", \
            f"Expected class name 'AtomicSwComponentType', got '{atomic_sw_component_type.name}'"

        # Verify package name is M2::AUTOSARTemplates::SWComponentTemplate::Components
        expected_package = "M2::AUTOSARTemplates::SWComponentTemplate::Components"
        assert atomic_sw_component_type.package == expected_package, \
            f"Expected package '{expected_package}', got '{atomic_sw_component_type.package}'"

        # Verify base list contains all expected base classes
        # Regular bases (non-Atp) including SwComponentType
        expected_bases = [
            "ARElement", "ARObject", "CollectableElement", "Identifiable",
            "MultilanguageReferrable", "PackageableElement", "Referrable", "SwComponentType"
        ]
        assert len(atomic_sw_component_type.bases) == len(expected_bases), \
            f"Expected {len(expected_bases)} base classes, got {len(atomic_sw_component_type.bases)}"
        for base in expected_bases:
            assert base in atomic_sw_component_type.bases, \
                f"Expected '{base}' in bases, got {atomic_sw_component_type.bases}"

        # Verify Atp interfaces are in implements field
        expected_implements = ["AtpBlueprint", "AtpBlueprintable", "AtpClassifier", "AtpType"]
        assert len(atomic_sw_component_type.implements) == len(expected_implements), \
            f"Expected {len(expected_implements)} interfaces, got {len(atomic_sw_component_type.implements)}"
        for interface in expected_implements:
            assert interface in atomic_sw_component_type.implements, \
                f"Expected '{interface}' in implements, got {atomic_sw_component_type.implements}"

        # Verify SwComponentType is in the base list (indicating AtomicSwComponentType inherits from SwComponentType)
        assert "SwComponentType" in atomic_sw_component_type.bases, \
            f"Expected 'SwComponentType' in bases, got {atomic_sw_component_type.bases}"

        # Print AtomicSwComponentType class information for verification
        print("\n=== AtomicSwComponentType class verified ===")
        print(f"  Name: {atomic_sw_component_type.name}")
        print(f"  Package: {atomic_sw_component_type.package}")
        print(f"  Abstract: {atomic_sw_component_type.is_abstract}")
        print(f"  Bases ({len(atomic_sw_component_type.bases)}): {', '.join(sorted(atomic_sw_component_type.bases))}")
        print(f"  Implements ({len(atomic_sw_component_type.implements)}): {', '.join(sorted(atomic_sw_component_type.implements))}")
        print("  SwComponentType in bases: YES")

    def test_parse_real_autosar_pdf_and_verify_diagnostic_debounce_enum(
        self, generic_structure_diagnostic_debounce_enum: AutosarEnumeration
    ) -> None:
        """Test parsing real AUTOSAR PDF and verify DiagnosticDebounceBehaviorEnum.

        SWIT_00004: Verify DiagnosticDebounceBehaviorEnum from GenericStructureTemplate PDF

        Requirements:
            SWR_PARSER_00003: PDF File Parsing
            SWR_PARSER_00013: Enumeration Pattern Recognition
            SWR_PARSER_00014: Enumeration Literal Extraction
            SWR_PARSER_00015: Enumeration Literal Extraction from PDF
            SWR_MODEL_00019: AUTOSAR Enumeration Type Representation

        Args:
            generic_structure_diagnostic_debounce_enum: Cached DiagnosticDebounceBehaviorEnum.
        """
        enum = generic_structure_diagnostic_debounce_enum

        # Verify enumeration name
        assert enum.name == "DiagnosticDebounceBehaviorEnum", \
            f"Expected name 'DiagnosticDebounceBehaviorEnum', got '{enum.name}'"

        # Verify package
        expected_package = "M2::AUTOSARTemplates::DiagnosticExtract::Dem::DiagnosticDebouncingAlgorithm"
        assert enum.package == expected_package, \
            f"Expected package '{expected_package}', got '{enum.package}'"

        # Verify enumeration_literals is a tuple (immutable)
        assert isinstance(enum.enumeration_literals, tuple), \
            f"enumeration_literals should be tuple for immutability, got {type(enum.enumeration_literals)}"

        # SWIT_00004 Step 9: Verify literal count is 2 (freeze and reset)
        assert len(enum.enumeration_literals) == 2, \
            f"Expected 2 literals (freeze and reset), got {len(enum.enumeration_literals)}. Actual literals: {[lit.name for lit in enum.enumeration_literals]}"

        # Verify immutability - attempt to modify should raise TypeError
        with pytest.raises(TypeError):
            enum.enumeration_literals[0] = enum.enumeration_literals[0]

        # Verify .append() is not available
        assert not hasattr(enum.enumeration_literals, "append") or \
               not callable(getattr(enum.enumeration_literals, "append", None)), \
               "enumeration_literals should not have append method"

        # SWIT_00004 Step 10: Verify expected literals exist: freeze, reset
        literal_names = [lit.name for lit in enum.enumeration_literals]
        expected_literals = ["freeze", "reset"]
        for expected in expected_literals:
            assert expected in literal_names, \
                f"Expected literal '{expected}' not found. Got: {literal_names}"

        # Verify only expected literals exist
        assert len(literal_names) == 2, \
            f"Expected exactly 2 literals (freeze, reset), but got {len(literal_names)}: {literal_names}"

        # SWIT_00004 Step 11: Verify freeze literal has full multi-line description
        freeze_literal = next((lit for lit in enum.enumeration_literals
                             if lit.name == "freeze"), None)
        assert freeze_literal is not None, "freeze literal must exist"
        assert freeze_literal.description is not None, \
            "freeze literal should have a description"
        assert "event debounce counter will be frozen" in freeze_literal.description.lower(), \
            f"freeze literal description should mention 'event debounce counter will be frozen'. Got: {freeze_literal.description}"

        # SWIT_00004 Step 12: Verify reset literal has full multi-line description
        reset_literal = next((lit for lit in enum.enumeration_literals
                            if lit.name == "reset"), None)
        assert reset_literal is not None, "reset literal must exist"
        assert reset_literal.description is not None, \
            "reset literal should have a description"
        assert "event debounce counter will be reset" in reset_literal.description.lower(), \
            f"reset literal description should mention 'event debounce counter will be reset'. Got: {reset_literal.description}"

        # Print enumeration information for verification
        print("\n=== DiagnosticDebounceBehaviorEnum verified ===")
        print(f"  Name: {enum.name}")
        print(f"  Package: {enum.package}")
        print(f"  Literals ({len(enum.enumeration_literals)}):")
        for lit in enum.enumeration_literals:
            desc_preview = lit.description[:100] + "..." if lit.description and len(lit.description) > 100 else lit.description
            print(f"    - {lit.name}: {desc_preview}")
        print("  Immutability: VERIFIED (tuple type)")
        print("  Multi-line description parsing: VERIFIED")

    def test_enumeration_literal_tags_extraction_from_real_pdf_swit_00005(
        self, diagnostic_extract_template_pdf: AutosarDoc
    ) -> None:
        """Test Enumeration Literal Tags Extraction from Real PDF (enum1.jpg scenario).

        Test Case ID: SWIT_00005

        Requirements:
            SWR_PARSER_00015: Enumeration Literal Extraction from PDF
            SWR_PARSER_00031: Enumeration Literal Tags Extraction

        This test verifies that tags are correctly extracted from enumeration literal
        descriptions using DiagnosticTypeOfDtcSupportedEnum from enum1.jpg example.

        Tags tested:
        - atp.EnumerationLiteralIndex: The index value of the literal
        - xml.name: The XML name for the literal

        Args:
            diagnostic_extract_template_pdf: Cached parsed DiagnosticExtractTemplate PDF data (AutosarDoc).
        """
        # Find DiagnosticTypeOfDtcSupportedEnum enumeration (from enum1.jpg)
        enum = find_enumeration_by_name(
            diagnostic_extract_template_pdf,
            "DiagnosticTypeOfDtcSupportedEnum"
        )
        if enum is None:
            pytest.skip("DiagnosticTypeOfDtcSupportedEnum not found in PDF - may not exist or be in different location")

        # SWIT_00005 Step 1: Verify enumeration has literals
        assert len(enum.enumeration_literals) > 0, "Enumeration must have literals"

        # SWIT_00005 Step 2: Verify tags are extracted for literals
        literals_with_tags = [lit for lit in enum.enumeration_literals if lit.tags]
        assert len(literals_with_tags) > 0, "At least one literal should have tags"

        # SWIT_00005 Step 3: Verify expected tags are present
        for literal in enum.enumeration_literals:
            # Check that tags dictionary exists
            assert hasattr(literal, 'tags'), "Literal must have tags attribute"
            assert isinstance(literal.tags, dict), "Tags must be a dictionary"

            # If tags are present, verify they are structured correctly
            if literal.tags:
                print(f"\n=== Literal: {literal.name} ===")
                print(f"  Description: {literal.description}")
                print(f"  Index: {literal.index}")
                print(f"  Tags: {literal.tags}")

                # Verify atp.EnumerationLiteralIndex tag
                if "atp.EnumerationLiteralIndex" in literal.tags:
                    assert literal.tags["atp.EnumerationLiteralIndex"].isdigit(), \
                        "atp.EnumerationLiteralIndex value must be numeric string"
                    # Verify index field matches tag value
                    assert literal.index == int(literal.tags["atp.EnumerationLiteralIndex"]), \
                        f"Index field ({literal.index}) must match atp.EnumerationLiteralIndex tag ({literal.tags['atp.EnumerationLiteralIndex']})"

                # Verify xml.name tag if present
                if "xml.name" in literal.tags:
                    assert literal.tags["xml.name"], "xml.name value must not be empty"

                # Verify tags are removed from description
                if literal.description:
                    assert "atp.EnumerationLiteralIndex" not in literal.description, \
                        "Tags should be removed from description"
                    assert "xml.name" not in literal.description, \
                        "Tags should be removed from description"

        print("\n=== Enumeration Literal Tags Extraction verified ===")
        print(f"  Total literals: {len(enum.enumeration_literals)}")
        print(f"  Literals with tags: {len(literals_with_tags)}")
        print("  Tags extraction: VERIFIED")
        print("  Description cleaning: VERIFIED")

    def test_multipage_enumeration_literal_list_from_real_pdf_swit_00006(
        self, diagnostic_extract_template_pdf: AutosarDoc
    ) -> None:
        """Test Multi-page Enumeration Literal List from Real PDF.

        Test Case ID: SWIT_00006

        Requirements:
            SWR_PARSER_00015: Enumeration Literal Extraction from PDF
            SWR_PARSER_00032: Multi-page Enumeration Literal List Support
            SWR_MODEL_00014: AUTOSAR Enumeration Type Representation
            SWR_MODEL_00027: AUTOSAR Source Location Representation

        This test verifies that enumeration literal lists spanning multiple pages
        are parsed correctly using DiagnosticExtractTemplate.pdf (from enum2.jpg example).

        Args:
            diagnostic_extract_template_pdf: Cached parsed DiagnosticExtractTemplate PDF data (AutosarDoc).
        """
        # Find ByteOrderEnum enumeration (from enum2.jpg - spans multiple pages)
        enum = find_enumeration_by_name(
            diagnostic_extract_template_pdf,
            "ByteOrderEnum"
        )
        if enum is None:
            pytest.skip("ByteOrderEnum not found in PDF - may not exist or be in different location")

        # SWIT_00006 Step 1: Verify enumeration has literals
        assert len(enum.enumeration_literals) > 0, "Enumeration must have literals"

        # SWIT_00006 Step 2: Verify expected literals are present
        literal_names = [lit.name for lit in enum.enumeration_literals]
        expected_literals = ["mostSignificantByteFirst", "mostSignificantByteLast", "opaque"]
        for expected in expected_literals:
            assert expected in literal_names, f"Expected literal '{expected}' not found. Found: {literal_names}"

        # SWIT_00006 Step 3: Verify each literal has proper structure
        for literal in enum.enumeration_literals:
            assert literal.name, "Literal name must not be empty"
            assert hasattr(literal, 'description'), "Literal must have description attribute"
            assert hasattr(literal, 'index'), "Literal must have index attribute"
            assert hasattr(literal, 'tags'), "Literal must have tags attribute"

            # If description exists, verify it's clean (no tag patterns)
            if literal.description:
                assert "atp.EnumerationLiteralIndex" not in literal.description, \
                    f"Tags should be removed from description for literal '{literal.name}'"

            # Print literal details for verification
            print(f"\n=== Literal: {literal.name} ===")
            print(f"  Description: {literal.description}")
            print(f"  Index: {literal.index}")
            print(f"  Tags: {literal.tags}")

        # SWIT_00006 Step 4: Verify source location tracking
        assert enum.sources, "Enumeration should have source location"
        assert len(enum.sources) > 0, "Enumeration should have at least one source"
        source = enum.sources[0]
        assert source.pdf_file, "Source PDF file must be specified"
        assert source.page_number, "Source page number must be specified"

        print("\n=== Multi-page Enumeration Literal List verified ===")
        print(f"  Name: {enum.name}")
        print(f"  Package: {enum.package}")
        print(f"  Total literals: {len(enum.enumeration_literals)}")
        print(f"  Source: {source.pdf_file}, Page {source.page_number}")
        print("  Multi-page parsing: VERIFIED")
        print("  Literal structure: VERIFIED")

    def test_diagnostic_event_combination_reporting_behavior_enum_swit_00007(
        self, diagnostic_extract_template_pdf: AutosarDoc
    ) -> None:
        """Test DiagnosticEventCombinationReportingBehaviorEnum enum3.png scenario.

        Test Case ID: SWIT_00007

        Requirements:
            SWR_PARSER_00015: Enumeration Literal Extraction from PDF
            SWR_PARSER_00031: Enumeration Literal Tags Extraction

        This test verifies the enum3.png scenario where three literal names
        (reportingIn, ChronlogicalOrder, and OldestFirst) are stacked vertically
        in one cell, sharing the same description and tags.

        The parser recognizes this and creates one combined literal:
        - reportingInChronlogicalOrderOldestFirst with the full description and tags

        Args:
            diagnostic_extract_template_pdf: Cached parsed DiagnosticExtractTemplate PDF data (AutosarDoc).
        """
        # Find DiagnosticEventCombinationReportingBehaviorEnum enumeration
        enum = find_enumeration_by_name(
            diagnostic_extract_template_pdf,
            "DiagnosticEventCombinationReportingBehaviorEnum"
        )
        if enum is None:
            pytest.skip("DiagnosticEventCombinationReportingBehaviorEnum not found in PDF")

        # Step 1: Verify enumeration has exactly one literal
        assert len(enum.enumeration_literals) == 1, \
            f"Expected 1 literal, found {len(enum.enumeration_literals)}"

        # Step 2: Verify the literal
        literal = enum.enumeration_literals[0]
        assert literal.name == "reportingInChronlogicalOrderOldestFirst", \
            f"Expected literal name 'reportingInChronlogicalOrderOldestFirst', got '{literal.name}'"

        # Step 3: Verify literal has proper structure
        assert literal.description is not None, "Literal must have description"
        assert literal.index is not None, "Literal must have index"
        assert literal.tags is not None, "Literal must have tags attribute"

        # Step 4: Verify literal description contains expected content
        assert "chronological" in literal.description.lower(), \
            f"Literal description should contain 'chronological': {literal.description}"

        # Step 5: Verify literal tags are present
        assert "atp.EnumerationLiteralIndex" in literal.tags, \
            "Literal should have atp.EnumerationLiteralIndex tag"

        # Step 6: Verify description is clean (no tag patterns)
        assert "atp.EnumerationLiteralIndex" not in literal.description, \
            f"Tags should be removed from literal description: {literal.description}"

        # Print literal details for verification
        print("\n=== DiagnosticEventCombinationReportingBehaviorEnum ===")
        print(f"  Name: {enum.name}")
        print(f"  Package: {enum.package}")
        print(f"  Total literals: {len(enum.enumeration_literals)}")
        print(f"\n=== Literal: {literal.name} ===")
        print(f"  Description: {literal.description}")
        print(f"  Index: {literal.index}")
        print(f"  Tags: {literal.tags}")

        if enum.sources:
            source = enum.sources[0]
            print(f"\n  Source: {source.pdf_file}, Page {source.page_number}")

        print("\n=== enum3.png scenario verified ===")
        print("  Three literal names stacked in one cell")
        print("  Combined literal name: reportingInChronlogicalOrderOldestFirst")
        print("  Description and tags: VERIFIED")
