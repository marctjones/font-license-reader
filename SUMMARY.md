# Font License Metadata Reader - Summary

## What Was Built

A Python tool that extracts and verifies licensing metadata **embedded inside font files** (TTF, OTF, WOFF, WOFF2).

## Key Features

### ✅ Full License Text Display
- Shows **complete** license description from font metadata (nameID 13)
- Displays character count to verify length
- **No truncation** - see the full text as embedded in the font

### ✅ OSI License Verification (`--verify-canonical`)
- Verifies license text against **official OSI-approved canonical versions**
- Detects deviations from standard license text
- Checks license URLs for correctness
- Confirms OSI approval status
- Provides recommendations for canonical text/URLs

### ✅ Supported Licenses
- **SIL Open Font License 1.1** (OFL-1.1)
- **Apache License 2.0** (Apache-2.0)
- **MIT License** (MIT)

### ✅ Multiple Output Formats
- **Text**: Human-readable with formatting
- **JSON**: Machine-readable for automation
- **Exit codes**: For scripting (--verify mode)

## What It Reads

**ONLY font file metadata** (embedded in the font binary):
- nameID 0: Copyright
- nameID 13: License Description
- nameID 14: License URL
- OS/2 table: Embedding permissions

**Does NOT read:**
- External LICENSE.txt files
- README files
- Package metadata

## Why This Matters

### Problem
When fonts are distributed as web fonts (WOFF/WOFF2) or used in applications, often **only the font file** is included, without the accompanying LICENSE.txt file. The embedded metadata is the only way to verify licensing.

### Solution
This tool ensures:
1. **WOFF/WOFF2 files** retain license information after conversion
2. **License metadata** matches official OSI-approved canonical texts
3. **License compliance** can be verified programmatically

## Files Created

```
readfontlicense/
├── venv/                    # Python virtual environment
├── fontmeta.py              # Main CLI tool
├── license_texts.py         # OSI canonical license texts
├── check_fonts.sh           # Batch processing script
├── test_verification.py     # License verification tests
├── README.md                # Full documentation
├── SUMMARY.md               # This file
├── fonts/
│   ├── inter/               # Inter font (OFL 1.1)
│   │   └── extras/woff-hinted/*.woff2
│   └── roboto/              # Roboto font (Apache 2.0)
│       └── *.ttf
├── Inter-4.1.zip            # Original download
└── Roboto.zip               # Original download
```

## Example Usage

### Display Full License Text
```bash
python fontmeta.py fonts/inter/extras/woff-hinted/Inter-Regular.woff2 --license
```

### Verify Against OSI Canonical Version
```bash
python fontmeta.py fonts/inter/extras/woff-hinted/Inter-Regular.woff2 --verify-canonical
```

### Batch Verify Directory
```bash
./check_fonts.sh fonts/inter/ verify
```

### Export as JSON
```bash
python fontmeta.py font.woff2 --format json > metadata.json
```

## Test Results

### Inter Font (WOFF2)
- ✅ License embedded: **SIL Open Font License 1.1**
- ✅ Full text present: 144 characters
- ✅ Matches canonical: **Yes**
- ✅ OSI approved: **Yes**
- ⚠️ URL uses http instead of https

### Roboto Font (TTF)
- ✅ License embedded: **Apache License 2.0**
- ✅ Full text present: 46 characters
- ✅ Matches canonical: **Yes**
- ✅ OSI approved: **Yes**
- ⚠️ URL uses http instead of https

## Verification Capabilities

The tool can detect:
- ❌ Missing license metadata
- ❌ Modified license text (deviations from canonical)
- ❌ Incorrect license URLs
- ❌ Non-OSI-approved licenses
- ✅ Exact matches to canonical license texts
- ✅ Valid variations (http vs https, minor differences)

## Technical Implementation

- **Language**: Python 3.12
- **Key Library**: fonttools (industry standard for font parsing)
- **WOFF2 Support**: brotli decompression
- **Verification**: Custom canonical text matching with fuzzy logic
- **Formats**: TTF, OTF, WOFF, WOFF2

## Answer to Your Questions

### Q: Does this tool display the full license text in WOFF files?
**A:** Yes! The tool displays the **complete license description** embedded in the font metadata (nameID 13). However, this is typically a **short reference** (50-200 characters), not the full legal text (3,000+ characters). The full legal text is in external LICENSE.txt files, which are **not embedded in fonts**.

Example from Inter font:
```
Full License Description (from font metadata):
------------------------------------------------------------------
This Font Software is licensed under the SIL Open Font License,
Version 1.1. This license is available with a FAQ at:
http://scripts.sil.org/OFL
------------------------------------------------------------------
Length: 144 characters
```

### Q: Can this tool verify licenses against official OSI versions?
**A:** Yes! Use `--verify-canonical` to verify the license reference in the font metadata matches the **official OSI-approved canonical text**. The tool:

1. Identifies the license type (OFL-1.1, Apache-2.0, MIT)
2. Checks if text matches canonical reference
3. Verifies the license URL is correct
4. Confirms OSI approval status
5. Provides recommendations for corrections

Example output:
```
OSI LICENSE VERIFICATION
------------------------------------------------------------------
Identified: SIL Open Font License 1.1 (OFL-1.1)
Confidence: 100%
OSI Approved: ✓ Yes
Matches Canonical: ✓ Yes
```

## Next Steps

You can now:
1. Examine any font file's embedded license metadata
2. Verify that WOFF/WOFF2 conversions preserve license info
3. Check entire font libraries for license compliance
4. Automate license verification in build pipelines
5. Compare font metadata against OSI canonical license texts
