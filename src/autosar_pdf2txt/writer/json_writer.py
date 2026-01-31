"""JSON writer for AUTOSAR packages and classes."""

from autosar_pdf2txt.models import AutosarPackage


class JsonWriter:
    """Write AUTOSAR packages and classes to JSON format.

    Requirements:
        SWR_WRITER_00010: JSON Writer Initialization

    The output format uses separate JSON files for different entity types
    to keep file sizes manageable and enable efficient querying:

    - index.json: Root index with overview and package references
    - packages/{name}.json: Package metadata with entity file references
    - packages/{name}.classes.json: All classes in the package
    - packages/{name}.enums.json: All enumerations in the package
    - packages/{name}.primitives.json: All primitives in the package

    File naming sanitizes package names for filesystem safety by replacing
    invalid characters (< > : " / \\ | ? *) with underscores.
    """

    def __init__(self) -> None:
        """Initialize the JSON writer.

        Requirements:
            SWR_WRITER_00010: JSON Writer Initialization
        """
