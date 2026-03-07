"""
Official license texts for verification
Sources: OSI (opensource.org) and SIL (scripts.sil.org)
"""

# SIL Open Font License 1.1 - Official reference text
# Source: https://scripts.sil.org/OFL
OFL_1_1_REFERENCE = """This Font Software is licensed under the SIL Open Font License, Version 1.1. This license is available with a FAQ at: http://scripts.sil.org/OFL"""

OFL_1_1_REFERENCE_VARIANTS = [
    "This Font Software is licensed under the SIL Open Font License, Version 1.1. This license is available with a FAQ at: http://scripts.sil.org/OFL",
    "This Font Software is licensed under the SIL Open Font License, Version 1.1. This license is available with a FAQ at: https://scripts.sil.org/OFL",
    "Licensed under the SIL Open Font License, Version 1.1",
    "SIL Open Font License, Version 1.1",
]

OFL_1_1_FULL_TEXT_EXCERPT = """SIL OPEN FONT LICENSE Version 1.1 - 26 February 2007

PREAMBLE
The goals of the Open Font License (OFL) are to stimulate worldwide
development of collaborative font projects"""

# Apache License 2.0 - Official reference text
# Source: https://www.apache.org/licenses/LICENSE-2.0
APACHE_2_0_REFERENCE = """Licensed under the Apache License, Version 2.0"""

APACHE_2_0_REFERENCE_VARIANTS = [
    "Licensed under the Apache License, Version 2.0",
    "Apache License, Version 2.0",
    "Apache License 2.0",
]

APACHE_2_0_FULL_TEXT_EXCERPT = """Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/"""

# MIT License - Common reference texts
MIT_REFERENCE_VARIANTS = [
    "Licensed under the MIT License",
    "MIT License",
    "Permission is hereby granted, free of charge",
]

MIT_FULL_TEXT_EXCERPT = """Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files"""

# Ubuntu Font License
UBUNTU_FONT_LICENSE_REFERENCE = "Ubuntu Font Licence Version 1.0"

# License verification rules
KNOWN_LICENSES = {
    'OFL-1.1': {
        'full_name': 'SIL Open Font License 1.1',
        'reference_variants': OFL_1_1_REFERENCE_VARIANTS,
        'canonical_reference': OFL_1_1_REFERENCE,
        'full_text_excerpt': OFL_1_1_FULL_TEXT_EXCERPT,
        'url_variants': [
            'http://scripts.sil.org/OFL',
            'https://scripts.sil.org/OFL',
            'http://scripts.sil.org/ofl',
            'https://opensource.org/licenses/OFL-1.1',
        ],
        'canonical_url': 'https://scripts.sil.org/OFL',
        'osi_approved': True,
    },
    'Apache-2.0': {
        'full_name': 'Apache License 2.0',
        'reference_variants': APACHE_2_0_REFERENCE_VARIANTS,
        'canonical_reference': APACHE_2_0_REFERENCE,
        'full_text_excerpt': APACHE_2_0_FULL_TEXT_EXCERPT,
        'url_variants': [
            'http://www.apache.org/licenses/LICENSE-2.0',
            'https://www.apache.org/licenses/LICENSE-2.0',
            'http://apache.org/licenses/LICENSE-2.0',
            'https://opensource.org/licenses/Apache-2.0',
        ],
        'canonical_url': 'https://www.apache.org/licenses/LICENSE-2.0',
        'osi_approved': True,
    },
    'MIT': {
        'full_name': 'MIT License',
        'reference_variants': MIT_REFERENCE_VARIANTS,
        'canonical_reference': MIT_REFERENCE_VARIANTS[0],
        'full_text_excerpt': MIT_FULL_TEXT_EXCERPT,
        'url_variants': [
            'https://opensource.org/licenses/MIT',
            'http://opensource.org/licenses/MIT',
        ],
        'canonical_url': 'https://opensource.org/licenses/MIT',
        'osi_approved': True,
    },
}


def normalize_text(text):
    """Normalize text for comparison (whitespace, case, punctuation)"""
    if not text:
        return ""
    # Remove extra whitespace, normalize case
    return ' '.join(text.lower().split())


def identify_license(description, url=None):
    """
    Identify which known license this is
    Returns: (license_id, confidence, warnings)
    """
    if not description:
        return (None, 0.0, ["No license description found"])

    desc_norm = normalize_text(description)
    url_norm = normalize_text(url) if url else ""

    best_match = None
    best_confidence = 0.0
    warnings = []

    for license_id, license_data in KNOWN_LICENSES.items():
        confidence = 0.0

        # Check description variants
        for variant in license_data['reference_variants']:
            if normalize_text(variant) in desc_norm:
                confidence = max(confidence, 0.8)
                break

        # Check URL variants
        if url_norm:
            for url_variant in license_data['url_variants']:
                if normalize_text(url_variant) in url_norm:
                    confidence = max(confidence, 0.9)
                    break

        # Exact match bonus
        if desc_norm == normalize_text(license_data['canonical_reference']):
            confidence = 1.0

        if confidence > best_confidence:
            best_confidence = confidence
            best_match = license_id

    if best_match:
        license_data = KNOWN_LICENSES[best_match]

        # Check for issues
        canonical_ref_norm = normalize_text(license_data['canonical_reference'])
        if desc_norm != canonical_ref_norm:
            warnings.append(
                f"License description differs from canonical text for {license_data['full_name']}"
            )

        if url and url_norm not in [normalize_text(u) for u in license_data['url_variants']]:
            warnings.append(
                f"License URL differs from known variants. Expected: {license_data['canonical_url']}"
            )

    return (best_match, best_confidence, warnings)


def verify_license_text(description, url=None):
    """
    Verify license description and URL against known good versions
    Returns: dict with verification results
    """
    license_id, confidence, warnings = identify_license(description, url)

    result = {
        'identified_license': license_id,
        'confidence': confidence,
        'osi_approved': False,
        'matches_canonical': False,
        'warnings': warnings,
        'recommendations': []
    }

    if license_id:
        license_data = KNOWN_LICENSES[license_id]
        result['full_name'] = license_data['full_name']
        result['osi_approved'] = license_data['osi_approved']
        result['canonical_reference'] = license_data['canonical_reference']
        result['canonical_url'] = license_data['canonical_url']

        # Check if it matches canonical
        if normalize_text(description) == normalize_text(license_data['canonical_reference']):
            result['matches_canonical'] = True
        else:
            result['recommendations'].append(
                f"Consider using canonical text: \"{license_data['canonical_reference']}\""
            )

        if url and normalize_text(url) != normalize_text(license_data['canonical_url']):
            result['recommendations'].append(
                f"Consider using canonical URL: {license_data['canonical_url']}"
            )

    return result
