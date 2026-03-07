"""
Basic tests for fontmeta CLI functionality.
"""

import pytest
from pathlib import Path
from fontmeta.cli import load_font, get_name_record, verify_license
from fontmeta.license_texts import verify_license_text


# Test fixtures - use fonts from the repo
ROBOTO_TTF = "fonts/roboto/Roboto-Regular.ttf"
INTER_WOFF2 = "fonts/inter/extras/woff-hinted/Inter-Regular.woff2"


class TestLoadFont:
    """Test font loading functionality."""

    def test_load_ttf(self):
        """Test loading a TTF file."""
        font = load_font(ROBOTO_TTF)
        assert font is not None
        assert 'name' in font

    def test_load_woff2(self):
        """Test loading a WOFF2 file."""
        font = load_font(INTER_WOFF2)
        assert font is not None
        assert 'name' in font

    def test_load_nonexistent_file(self):
        """Test error when file doesn't exist."""
        with pytest.raises(SystemExit) as exc_info:
            load_font("nonexistent.ttf")
        assert exc_info.value.code == 1


class TestGetNameRecord:
    """Test name table extraction."""

    def test_get_license_from_roboto(self):
        """Test extracting license text from Roboto (Apache)."""
        font = load_font(ROBOTO_TTF)
        license_text = get_name_record(font, 13)  # nameID 13 = License Description
        assert license_text is not None
        assert "Apache" in license_text

    def test_get_license_from_inter(self):
        """Test extracting license text from Inter (OFL)."""
        font = load_font(INTER_WOFF2)
        license_text = get_name_record(font, 13)
        assert license_text is not None
        assert "Open Font License" in license_text

    def test_get_missing_name_record(self):
        """Test getting non-existent name record returns None."""
        font = load_font(ROBOTO_TTF)
        result = get_name_record(font, 999)  # nameID 999 doesn't exist
        assert result is None


class TestVerifyLicense:
    """Test license verification."""

    def test_verify_roboto_has_license(self):
        """Test that Roboto has license metadata."""
        font = load_font(ROBOTO_TTF)
        result = verify_license(font)
        assert result is not None
        assert "type" in result
        assert result["found"] is True

    def test_verify_inter_has_license(self):
        """Test that Inter has license metadata."""
        font = load_font(INTER_WOFF2)
        result = verify_license(font)
        assert result is not None
        assert result["found"] is True


class TestLicenseTextVerification:
    """Test license text verification from license_texts.py."""

    def test_verify_ofl_license(self):
        """Test OFL license verification."""
        result = verify_license_text(
            "This Font Software is licensed under the SIL Open Font License, Version 1.1.",
            "http://scripts.sil.org/OFL"
        )
        assert result["identified_license"] == "OFL-1.1"
        assert result["osi_approved"] is True
        assert result["confidence"] > 0.8

    def test_verify_apache_license(self):
        """Test Apache license verification."""
        result = verify_license_text(
            "Licensed under the Apache License, Version 2.0",
            "http://www.apache.org/licenses/LICENSE-2.0"
        )
        assert result["identified_license"] == "Apache-2.0"
        assert result["osi_approved"] is True

    def test_verify_unknown_license(self):
        """Test unknown license returns None."""
        result = verify_license_text(
            "Some proprietary license",
            None
        )
        assert result["identified_license"] is None
