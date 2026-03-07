#!/usr/bin/env python3
"""
fontmeta - Font Metadata Extraction Tool
Examine metadata from TTF, OTF, WOFF, and WOFF2 font files
"""

import argparse
import json
import sys
from pathlib import Path
from fontTools.ttLib import TTFont
try:
    from .license_texts import verify_license_text
    HAVE_LICENSE_VERIFICATION = True
except ImportError:
    HAVE_LICENSE_VERIFICATION = False


# Name table ID mappings
NAME_IDS = {
    0: "Copyright",
    1: "Font Family",
    2: "Font Subfamily",
    3: "Unique Font Identifier",
    4: "Full Font Name",
    5: "Version",
    6: "PostScript Name",
    7: "Trademark",
    8: "Manufacturer",
    9: "Designer",
    10: "Description",
    11: "Vendor URL",
    12: "Designer URL",
    13: "License Description",
    14: "License URL",
    15: "Reserved",
    16: "Typographic Family",
    17: "Typographic Subfamily",
    18: "Compatible Full",
    19: "Sample Text",
    20: "PostScript CID",
    21: "WWS Family Name",
    22: "WWS Subfamily Name",
    25: "Variations PostScript Name Prefix"
}


def load_font(font_path):
    """Load font file and return TTFont object"""
    path = Path(font_path)

    # Check if file exists
    if not path.exists():
        print(f"Error: Font file not found: {font_path}", file=sys.stderr)
        sys.exit(1)

    # Try to load the font
    try:
        return TTFont(str(font_path))
    except Exception as e:
        print(f"Error: Could not load font file: {font_path}", file=sys.stderr)
        print(f"Make sure it's a valid TTF, OTF, WOFF, or WOFF2 file.", file=sys.stderr)
        sys.exit(1)


def get_name_record(font, name_id, platform_id=3, encoding_id=1):
    """
    Get a specific name table record
    Default to Windows platform (3) with Unicode BMP (1)
    Falls back to Mac platform (1) if Windows not found
    """
    if 'name' not in font:
        return None

    name_table = font['name']

    # Try Windows platform first
    for record in name_table.names:
        if record.nameID == name_id and record.platformID == platform_id:
            return record.toUnicode()

    # Fallback to Mac platform
    for record in name_table.names:
        if record.nameID == name_id and record.platformID == 1:
            return record.toUnicode()

    return None


def get_all_name_records(font):
    """Extract all name table entries"""
    if 'name' not in font:
        return {}

    records = {}
    name_table = font['name']

    for record in name_table.names:
        name_id = record.nameID
        key = NAME_IDS.get(name_id, f"Unknown ({name_id})")

        try:
            value = record.toUnicode()

            # Store all platform/encoding variants
            if key not in records:
                records[key] = []

            records[key].append({
                'value': value,
                'platform': record.platformID,
                'encoding': record.encodingID,
                'language': record.langID
            })
        except:
            pass

    return records


def get_embedding_permissions(font):
    """Get embedding permissions from OS/2 table"""
    if 'OS/2' not in font:
        return "Unknown (no OS/2 table)"

    fs_type = font['OS/2'].fsType

    # Embedding flags
    if fs_type == 0:
        return "Installable (no restrictions)"
    elif fs_type & 0x0002:
        return "Restricted License (no embedding)"
    elif fs_type & 0x0004:
        return "Preview & Print (read-only)"
    elif fs_type & 0x0008:
        return "Editable (can modify and embed)"
    else:
        return f"Custom (0x{fs_type:04x})"


def verify_license(font):
    """Verify if OFL or other open source license is present"""
    license_desc = get_name_record(font, 13)
    license_url = get_name_record(font, 14)
    copyright_text = get_name_record(font, 0)

    result = {
        'found': False,
        'type': 'Unknown',
        'description': license_desc,
        'url': license_url,
        'copyright': copyright_text,
        'warnings': []
    }

    if not license_desc:
        result['warnings'].append("No license description (nameID 13) found")
    else:
        result['found'] = True
        # Check for common open licenses
        if 'Open Font License' in license_desc or 'OFL' in license_desc:
            result['type'] = 'SIL Open Font License'
        elif 'Apache' in license_desc:
            result['type'] = 'Apache License'
        elif 'MIT' in license_desc:
            result['type'] = 'MIT License'
        elif 'GPL' in license_desc:
            result['type'] = 'GPL'
        elif 'Creative Commons' in license_desc or 'CC' in license_desc:
            result['type'] = 'Creative Commons'

    if not license_url:
        result['warnings'].append("No license URL (nameID 14) found")

    if not copyright_text:
        result['warnings'].append("No copyright notice (nameID 0) found")

    return result


def format_text_output(font_path, font, args):
    """Format output as human-readable text"""
    print(f"\n{'='*70}")
    print(f"Font: {Path(font_path).name}")
    print(f"{'='*70}\n")

    if args.basic or args.all:
        print("BASIC INFO")
        print("-" * 70)
        family = get_name_record(font, 1) or "Unknown"
        subfamily = get_name_record(font, 2) or "Unknown"
        version = get_name_record(font, 5) or "Unknown"
        manufacturer = get_name_record(font, 8) or "Unknown"

        print(f"  Font Family:    {family}")
        print(f"  Subfamily:      {subfamily}")
        print(f"  Version:        {version}")
        print(f"  Manufacturer:   {manufacturer}")
        print()

    if args.copyright or args.all:
        print("COPYRIGHT")
        print("-" * 70)
        copyright_text = get_name_record(font, 0)
        if copyright_text:
            print(f"  {copyright_text}")
        else:
            print("  ⚠️  No copyright information found")
        print()

    if args.license or args.all or args.verify_canonical:
        print("LICENSE INFORMATION")
        print("-" * 70)
        license_info = verify_license(font)

        if license_info['found']:
            print(f"  ✓ License Type: {license_info['type']}")
        else:
            print(f"  ✗ License Type: {license_info['type']}")

        if license_info['description']:
            print(f"\n  Full License Description (from font metadata):")
            print(f"  {'-' * 66}")
            # Show complete license text without truncation
            desc = license_info['description']
            print(f"  {desc}")
            print(f"  {'-' * 66}")
            print(f"  Length: {len(desc)} characters")

        if license_info['url']:
            print(f"\n  License URL: {license_info['url']}")

        # Verify against canonical license texts
        if args.verify_canonical and HAVE_LICENSE_VERIFICATION:
            print(f"\n  OSI LICENSE VERIFICATION")
            print(f"  {'-' * 66}")
            verification = verify_license_text(
                license_info['description'],
                license_info['url']
            )

            if verification['identified_license']:
                print(f"  Identified: {verification['full_name']} ({verification['identified_license']})")
                print(f"  Confidence: {verification['confidence']*100:.0f}%")
                print(f"  OSI Approved: {'✓ Yes' if verification['osi_approved'] else '✗ No'}")
                print(f"  Matches Canonical: {'✓ Yes' if verification['matches_canonical'] else '✗ No'}")

                if not verification['matches_canonical']:
                    print(f"\n  Expected canonical text:")
                    print(f"  \"{verification['canonical_reference']}\"")

                if verification['canonical_url']:
                    print(f"\n  Canonical URL: {verification['canonical_url']}")

                if verification['warnings']:
                    print(f"\n  Verification Warnings:")
                    for warning in verification['warnings']:
                        print(f"    ⚠️  {warning}")

                if verification['recommendations']:
                    print(f"\n  Recommendations:")
                    for rec in verification['recommendations']:
                        print(f"    💡 {rec}")
            else:
                print(f"  ⚠️  License not recognized or cannot be verified")

        elif args.verify_canonical and not HAVE_LICENSE_VERIFICATION:
            print(f"\n  ⚠️  License verification not available (license_texts.py not found)")

        if license_info['warnings']:
            print(f"\n  Metadata Warnings:")
            for warning in license_info['warnings']:
                print(f"    ⚠️  {warning}")
        print()

    if args.embedding or args.all:
        print("EMBEDDING PERMISSIONS")
        print("-" * 70)
        perms = get_embedding_permissions(font)
        print(f"  {perms}")
        print()

    if args.vendor or args.all:
        print("VENDOR INFORMATION")
        print("-" * 70)
        vendor_url = get_name_record(font, 11)
        designer = get_name_record(font, 9)
        designer_url = get_name_record(font, 12)

        if designer:
            print(f"  Designer:       {designer}")
        if designer_url:
            print(f"  Designer URL:   {designer_url}")
        if vendor_url:
            print(f"  Vendor URL:     {vendor_url}")
        print()

    if args.full:
        print("FULL NAME TABLE")
        print("-" * 70)
        all_records = get_all_name_records(font)
        for name, entries in sorted(all_records.items()):
            print(f"\n  {name}:")
            for entry in entries:
                plat = f"P{entry['platform']}/E{entry['encoding']}/L{entry['language']}"
                value = entry['value'][:80] + "..." if len(entry['value']) > 80 else entry['value']
                print(f"    [{plat}] {value}")
        print()


def format_json_output(font_path, font, args):
    """Format output as JSON"""
    data = {
        'file': str(Path(font_path).name),
        'path': str(font_path)
    }

    # Basic info
    data['basic'] = {
        'family': get_name_record(font, 1),
        'subfamily': get_name_record(font, 2),
        'full_name': get_name_record(font, 4),
        'version': get_name_record(font, 5),
        'postscript_name': get_name_record(font, 6),
        'manufacturer': get_name_record(font, 8),
        'designer': get_name_record(font, 9)
    }

    # License
    license_info = verify_license(font)
    data['license'] = {
        'type': license_info['type'],
        'found': license_info['found'],
        'description': license_info['description'],
        'url': license_info['url'],
        'warnings': license_info['warnings']
    }

    # Copyright
    data['copyright'] = get_name_record(font, 0)

    # Embedding
    data['embedding'] = get_embedding_permissions(font)

    # Vendor
    data['vendor'] = {
        'url': get_name_record(font, 11),
        'designer_url': get_name_record(font, 12)
    }

    if args.full:
        data['name_table'] = get_all_name_records(font)

    print(json.dumps(data, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(
        description='Extract and examine font metadata from TTF/OTF/WOFF/WOFF2 files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s font.woff2 --license          Show license information
  %(prog)s font.ttf --all                Show all metadata
  %(prog)s font.woff2 --verify           Verify OFL license
  %(prog)s font.ttf --format json        Output as JSON
  %(prog)s font.woff2 --full             Show complete name table
        """
    )

    parser.add_argument('font', help='Path to font file (TTF, OTF, WOFF, WOFF2)')

    # Output format
    parser.add_argument('-f', '--format', choices=['text', 'json'],
                       default='text', help='Output format (default: text)')

    # What to show (text mode)
    parser.add_argument('-b', '--basic', action='store_true',
                       help='Show basic font information')
    parser.add_argument('-c', '--copyright', action='store_true',
                       help='Show copyright information')
    parser.add_argument('-l', '--license', action='store_true',
                       help='Show license information')
    parser.add_argument('-e', '--embedding', action='store_true',
                       help='Show embedding permissions')
    parser.add_argument('-v', '--vendor', action='store_true',
                       help='Show vendor/designer information')
    parser.add_argument('--full', action='store_true',
                       help='Show complete name table with all platforms/encodings')
    parser.add_argument('-a', '--all', action='store_true',
                       help='Show all metadata (equivalent to -b -c -l -e -v)')

    # Quick verification
    parser.add_argument('--verify', action='store_true',
                       help='Quick license verification (returns exit code)')
    parser.add_argument('--verify-canonical', action='store_true',
                       help='Verify license text against official OSI-approved versions')

    args = parser.parse_args()

    # Load font (error handling is in load_font function)
    font_path = Path(args.font)
    font = load_font(font_path)

    # Verify mode
    if args.verify:
        license_info = verify_license(font)
        if license_info['found'] and not license_info['warnings']:
            print(f"✓ {font_path.name}: {license_info['type']}")
            sys.exit(0)
        else:
            print(f"✗ {font_path.name}: License issues found")
            for warning in license_info['warnings']:
                print(f"  ⚠️  {warning}")
            sys.exit(1)

    # If no specific flags, default to showing license
    if not any([args.basic, args.copyright, args.license, args.embedding,
                args.vendor, args.full, args.all, args.verify_canonical]):
        args.license = True

    # Output
    if args.format == 'json':
        format_json_output(font_path, font, args)
    else:
        format_text_output(font_path, font, args)


if __name__ == '__main__':
    main()
