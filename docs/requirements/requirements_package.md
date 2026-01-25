# Package Requirements

This document contains all software requirements for the autosar-pdf2txt Python package configuration.

## Maturity Levels

Each requirement has a maturity level that indicates its status:

- **draft**: Newly created requirement, under review, or not yet implemented
- **accept**: Accepted requirement, implemented in the codebase
- **invalid**: Deprecated requirement, superseded, or no longer applicable

---

### SWR_PACKAGE_00001
**Title**: Package API Export

**Maturity**: accept

**Description**: The system shall export the following public API from the root package:
- `AttributeKind` (Enum)
- `AutosarAttribute` (Dataclass)
- `AutosarClass` (Dataclass)
- `AutosarDoc` (Dataclass)
- `AutosarEnumLiteral` (Dataclass)
- `AutosarEnumeration` (Dataclass)
- `AutosarPackage` (Dataclass)
- `AutosarPrimitive` (Dataclass)
- `PdfParser` (Class)
- `MarkdownWriter` (Class)
- `__version__` (String)

---

### SWR_PACKAGE_00002
**Title**: Python Version Support

**Maturity**: accept

**Description**: The system shall support Python versions 3.7 through 3.11.

---

### SWR_PACKAGE_00003
**Title**: Package Metadata

**Maturity**: accept

**Description**: The system shall include appropriate package metadata including:
- Package name: autosar-pdf2txt
- Version information
- Author and contact information
- Description and long description
- Project URL
- License classification (MIT)