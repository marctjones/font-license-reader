#!/usr/bin/env python3
"""
Test script to demonstrate license verification
Shows what happens with non-canonical license text
"""

from fontmeta.license_texts import verify_license_text

# Test various license texts
test_cases = [
    {
        'name': 'Canonical OFL 1.1',
        'description': 'This Font Software is licensed under the SIL Open Font License, Version 1.1. This license is available with a FAQ at: http://scripts.sil.org/OFL',
        'url': 'http://scripts.sil.org/OFL'
    },
    {
        'name': 'Modified OFL (missing FAQ reference)',
        'description': 'This Font Software is licensed under the SIL Open Font License, Version 1.1',
        'url': 'http://scripts.sil.org/OFL'
    },
    {
        'name': 'OFL with wrong URL',
        'description': 'This Font Software is licensed under the SIL Open Font License, Version 1.1. This license is available with a FAQ at: http://scripts.sil.org/OFL',
        'url': 'http://example.com/license'
    },
    {
        'name': 'Canonical Apache 2.0',
        'description': 'Licensed under the Apache License, Version 2.0',
        'url': 'http://www.apache.org/licenses/LICENSE-2.0'
    },
    {
        'name': 'Unknown License',
        'description': 'This is my custom license',
        'url': None
    }
]

print("="*70)
print("LICENSE VERIFICATION TEST CASES")
print("="*70)

for test in test_cases:
    print(f"\n{'='*70}")
    print(f"Test: {test['name']}")
    print(f"{'='*70}")
    print(f"Description: \"{test['description']}\"")
    print(f"URL: {test['url']}")

    result = verify_license_text(test['description'], test['url'])

    print(f"\nResults:")
    if result['identified_license']:
        print(f"  Identified: {result['full_name']} ({result['identified_license']})")
        print(f"  Confidence: {result['confidence']*100:.0f}%")
        print(f"  OSI Approved: {'✓ Yes' if result['osi_approved'] else '✗ No'}")
        print(f"  Matches Canonical: {'✓ Yes' if result['matches_canonical'] else '✗ No'}")

        if result['warnings']:
            print(f"\n  Warnings:")
            for warning in result['warnings']:
                print(f"    ⚠️  {warning}")

        if result['recommendations']:
            print(f"\n  Recommendations:")
            for rec in result['recommendations']:
                print(f"    💡 {rec}")
    else:
        print(f"  ⚠️  License not recognized")

print(f"\n{'='*70}")
print("END OF TESTS")
print(f"{'='*70}\n")
