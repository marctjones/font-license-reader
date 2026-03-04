# Font License Metadata Reader

Python tool to extract and verify licensing metadata from font files (TTF, OTF, WOFF, WOFF2).

## Setup

1. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install fonttools brotli
```

## Usage

### Single Font Examination

```bash
# Show license information (default)
python fontmeta.py fonts/inter/Inter-Regular.woff2 --license

# Show all metadata
python fontmeta.py fonts/roboto/Roboto-Regular.ttf --all

# Show specific sections
python fontmeta.py font.woff2 --basic          # Basic info
python fontmeta.py font.woff2 --copyright      # Copyright
python fontmeta.py font.woff2 --embedding      # Embedding permissions
python fontmeta.py font.woff2 --vendor         # Designer/vendor info

# Show complete name table (all platforms/encodings)
python fontmeta.py font.woff2 --full

# Quick verification (returns exit code 0 if license found)
python fontmeta.py font.woff2 --verify

# Verify license against official OSI-approved versions
python fontmeta.py font.woff2 --verify-canonical

# JSON output for programmatic use
python fontmeta.py font.woff2 --format json
```

### Batch Processing

```bash
# Verify all fonts in a directory
./check_fonts.sh fonts/inter/ verify

# Get detailed text output for all fonts
./check_fonts.sh fonts/roboto/ text

# Export all metadata as JSON
./check_fonts.sh fonts/ json > all_fonts.json
```

## Command Line Options

| Option | Description |
|--------|-------------|
| `-b, --basic` | Show basic font information |
| `-c, --copyright` | Show copyright information |
| `-l, --license` | Show license information (default) |
| `-e, --embedding` | Show embedding permissions |
| `-v, --vendor` | Show vendor/designer information |
| `--full` | Show complete name table |
| `-a, --all` | Show all metadata |
| `--verify` | Quick verification (exit code based) |
| `--verify-canonical` | Verify license against OSI-approved canonical texts |
| `-f, --format` | Output format: `text` or `json` |

## What It Checks

### Name Table Entries
- **Copyright** (ID 0): Full copyright notice
- **License Description** (ID 13): License text (e.g., "SIL Open Font License 1.1")
- **License URL** (ID 14): URL to license (e.g., http://scripts.sil.org/OFL)
- **Designer/Vendor** (IDs 8-12): Creator information

### OS/2 Table
- **Embedding Permissions**: Whether font can be embedded in documents/apps

### License Detection
Automatically detects:
- SIL Open Font License (OFL)
- Apache License
- MIT License
- Creative Commons
- GPL

### Canonical License Verification (`--verify-canonical`)

The tool can verify that license metadata in font files matches **official OSI-approved license texts**:

**What it verifies:**
1. **License Description** - Checks if the text in nameID 13 matches canonical reference text
2. **License URL** - Verifies the URL in nameID 14 points to official license location
3. **OSI Approval** - Confirms the license is approved by the Open Source Initiative
4. **Exactness** - Detects modifications or deviations from standard license text

**Supported licenses:**
- **OFL-1.1**: SIL Open Font License 1.1
- **Apache-2.0**: Apache License 2.0
- **MIT**: MIT License

**Example output:**
```
OSI LICENSE VERIFICATION
------------------------------------------------------------------
Identified: SIL Open Font License 1.1 (OFL-1.1)
Confidence: 100%
OSI Approved: ✓ Yes
Matches Canonical: ✓ Yes

Canonical URL: https://scripts.sil.org/OFL

Recommendations:
  💡 Consider using canonical URL: https://scripts.sil.org/OFL
```

**Why this matters:**
- Font metadata often contains **shortened or modified** license references
- Web fonts (WOFF/WOFF2) may have license text stripped during conversion
- Ensures license information is **complete and accurate** for compliance
- Detects if license text differs from OSI-recognized versions

## Example Output

### Text Format (Standard)
```
======================================================================
Font: Inter-Regular.woff2
======================================================================

LICENSE INFORMATION
----------------------------------------------------------------------
  ✓ License Type: SIL Open Font License

  Full License Description (from font metadata):
  ------------------------------------------------------------------
  This Font Software is licensed under the SIL Open Font License,
  Version 1.1. This license is available with a FAQ at:
  http://scripts.sil.org/OFL
  ------------------------------------------------------------------
  Length: 144 characters

  License URL: http://scripts.sil.org/OFL
```

### Text Format (With Canonical Verification)
```
======================================================================
Font: Inter-Regular.woff2
======================================================================

LICENSE INFORMATION
----------------------------------------------------------------------
  ✓ License Type: SIL Open Font License

  Full License Description (from font metadata):
  ------------------------------------------------------------------
  This Font Software is licensed under the SIL Open Font License,
  Version 1.1. This license is available with a FAQ at:
  http://scripts.sil.org/OFL
  ------------------------------------------------------------------
  Length: 144 characters

  License URL: http://scripts.sil.org/OFL

  OSI LICENSE VERIFICATION
  ------------------------------------------------------------------
  Identified: SIL Open Font License 1.1 (OFL-1.1)
  Confidence: 100%
  OSI Approved: ✓ Yes
  Matches Canonical: ✓ Yes

  Canonical URL: https://scripts.sil.org/OFL

  Recommendations:
    💡 Consider using canonical URL: https://scripts.sil.org/OFL
```

### JSON Format
```json
{
  "file": "Roboto-Regular.ttf",
  "basic": {
    "family": "Roboto",
    "version": "Version 2.138",
    "manufacturer": "Google"
  },
  "license": {
    "type": "Apache License",
    "found": true,
    "description": "Licensed under the Apache License, Version 2.0",
    "url": "http://www.apache.org/licenses/LICENSE-2.0",
    "warnings": []
  },
  "copyright": "Copyright 2011 Google Inc. All Rights Reserved.",
  "embedding": "Installable (no restrictions)"
}
```

## Fonts Included

This repository includes sample fonts for testing:

### Inter (SIL OFL)
- **License**: SIL Open Font License 1.1
- **Source**: https://github.com/rsms/inter
- **Designer**: Rasmus Andersson
- **Formats**: TTC, TTF, WOFF2

### Roboto (Apache)
- **License**: Apache License 2.0
- **Source**: https://github.com/google/roboto
- **Designer**: Christian Robertson (Google)
- **Formats**: TTF

## Use Cases

1. **License Compliance**: Verify that fonts include proper licensing metadata
2. **Font Auditing**: Check if WOFF/WOFF2 web fonts retain license information
3. **Font Selection**: Review font metadata before using in projects
4. **Batch Processing**: Audit entire font libraries for licensing compliance

## Important: What This Tool Reads

**This tool ONLY reads metadata embedded INSIDE font files** (TTF, OTF, WOFF, WOFF2). It does **NOT** read external LICENSE.txt files that may be distributed alongside fonts.

### What's in Font Metadata vs. LICENSE Files

**Font Metadata (nameID 13):**
- Short license reference (typically 50-200 characters)
- Example: "This Font Software is licensed under the SIL Open Font License, Version 1.1"
- **Embedded in the font file binary**
- Preserved when fonts are converted to web formats (WOFF/WOFF2)

**External LICENSE.txt Files:**
- Full license text (3,000+ characters for OFL, 11,000+ for Apache)
- Complete legal terms and conditions
- **Separate file in font distribution packages**
- **NOT embedded in font files**

### Why Font Metadata Matters

When you use fonts on the web or in applications, often **only the font file is distributed**, without the accompanying LICENSE.txt file. The embedded metadata is the only way to verify licensing in these scenarios.

This tool helps ensure that:
1. **Web fonts** (WOFF/WOFF2) retain licensing information after conversion
2. **Font metadata** correctly references the license type and URL
3. **License references** match official OSI-approved canonical texts

## Technical Notes

- Uses `fonttools` library for parsing font tables
- Supports all major font formats (TTF, OTF, WOFF, WOFF2)
- WOFF2 requires `brotli` for decompression
- Reads OpenType name table (IDs 0-25)
- Checks OS/2 table for embedding permissions
- Falls back to Mac platform if Windows platform records not found
- Verifies license metadata against OSI canonical texts

## Dependencies

- Python 3.8+
- fonttools 4.61.1+
- brotli 1.2.0+ (for WOFF2 support)
