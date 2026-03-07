"""
fontmeta - Font License Metadata Reader

A Python tool to extract and verify licensing metadata from font files
(TTF, OTF, WOFF, WOFF2).
"""

__version__ = "1.0.0"

from .license_texts import verify_license_text

__all__ = ["verify_license_text"]
