"""New tests for AUTOSAR standard and release extraction from PDF content.

Test coverage for SWR_PARSER_00022 enhancements.
"""


from autosar_pdf2txt.parser import PdfParser


class TestAutosarStandardAndReleaseExtraction:
    """Tests for extracting AUTOSAR standard and release from PDF content.

    Requirements:
        SWR_PARSER_00022: PDF Source Location Extraction
    """

    def test_extract_autosar_standard_foundation(self) -> None:
        """Test extracting AUTOSAR standard 'Foundation' from PDF content.

        Requirements:
            SWR_PARSER_00022: PDF Source Location Extraction
        """
        parser = PdfParser()
        text = """
Part of AUTOSAR Standard: Foundation
Part of Standard Release: R23-11

Class TestClass
Package M2::TestPackage
"""
        models = parser._parse_complete_text(text, "test.pdf")

        assert len(models) == 1
        assert models[0].sources is not None
        assert models[0].sources[0].autosar_standard == "Foundation"
        assert models[0].sources[0].standard_release == "R23-11"

    def test_extract_autosar_standard_classic_platform(self) -> None:
        """Test extracting AUTOSAR standard 'Classic Platform' from PDF content.

        Requirements:
            SWR_PARSER_00022: PDF Source Location Extraction
        """
        parser = PdfParser()
        text = """
Part of AUTOSAR Standard: Classic Platform
Part of Standard Release: R22-11

Class TestClass
Package M2::TestPackage
"""
        models = parser._parse_complete_text(text, "test.pdf")

        assert len(models) == 1
        assert models[0].sources is not None
        assert models[0].sources[0].autosar_standard == "Classic Platform"
        assert models[0].sources[0].standard_release == "R22-11"

    def test_extract_autosar_standard_adaptive_platform(self) -> None:
        """Test extracting AUTOSAR standard 'Adaptive Platform' from PDF content.

        Requirements:
            SWR_PARSER_00022: PDF Source Location Extraction
        """
        parser = PdfParser()
        text = """
Part of AUTOSAR Standard: Adaptive Platform
Part of Standard Release: R24-03

Class TestClass
Package M2::TestPackage
"""
        models = parser._parse_complete_text(text, "test.pdf")

        assert len(models) == 1
        assert models[0].sources is not None
        assert models[0].sources[0].autosar_standard == "Adaptive Platform"
        assert models[0].sources[0].standard_release == "R24-03"

    def test_extract_autosar_standard_methodology(self) -> None:
        """Test extracting AUTOSAR standard 'Methodology' from PDF content.

        Requirements:
            SWR_PARSER_00022: PDF Source Location Extraction
        """
        parser = PdfParser()
        text = """
Part of AUTOSAR Standard: Methodology
Part of Standard Release: R23-11

Class TestClass
Package M2::TestPackage
"""
        models = parser._parse_complete_text(text, "test.pdf")

        assert len(models) == 1
        assert models[0].sources is not None
        assert models[0].sources[0].autosar_standard == "Methodology"
        assert models[0].sources[0].standard_release == "R23-11"

    def test_missing_autosar_standard_and_release(self) -> None:
        """Test handling PDFs without AUTOSAR standard and release metadata.

        Requirements:
            SWR_PARSER_00022: PDF Source Location Extraction
        """
        parser = PdfParser()
        text = """
Class TestClass
Package M2::TestPackage
"""
        models = parser._parse_complete_text(text, "test.pdf")

        assert len(models) == 1
        assert models[0].sources is not None
        assert models[0].sources[0].autosar_standard is None
        assert models[0].sources[0].standard_release is None

    def test_apply_extracted_metadata_to_all_classes(self) -> None:
        """Test that extracted AUTOSAR standard and release are applied to all classes.

        Requirements:
            SWR_PARSER_00022: PDF Source Location Extraction
        """
        parser = PdfParser()
        text = """
Part of AUTOSAR Standard: Foundation
Part of Standard Release: R23-11

Class ClassA
Package M2::TestPackage
Note This is a note for ClassA

Attribute Type Mult. Kind Note
testAttr string 1 ATTR Test attribute
"""
        models = parser._parse_complete_text(text, "test.pdf")

        assert len(models) == 1
        assert models[0].sources is not None
        assert models[0].sources[0].autosar_standard == "Foundation"
        assert models[0].sources[0].standard_release == "R23-11"

    def test_extract_only_standard_without_release(self) -> None:
        """Test extracting AUTOSAR standard when release is not present.

        Requirements:
            SWR_PARSER_00022: PDF Source Location Extraction
        """
        parser = PdfParser()
        text = """
Part of AUTOSAR Standard: Foundation

Class TestClass
Package M2::TestPackage
"""
        models = parser._parse_complete_text(text, "test.pdf")

        assert len(models) == 1
        assert models[0].sources is not None
        assert models[0].sources[0].autosar_standard == "Foundation"
        assert models[0].sources[0].standard_release is None

    def test_extract_only_release_without_standard(self) -> None:
        """Test extracting AUTOSAR release when standard is not present.

        Requirements:
            SWR_PARSER_00022: PDF Source Location Extraction
        """
        parser = PdfParser()
        text = """
Part of Standard Release: R23-11

Class TestClass
Package M2::TestPackage
"""
        models = parser._parse_complete_text(text, "test.pdf")

        assert len(models) == 1
        assert models[0].sources is not None
        assert models[0].sources[0].autosar_standard is None
        assert models[0].sources[0].standard_release == "R23-11"