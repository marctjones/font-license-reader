# Project Vision

## Purpose

**fontmeta** ensures font licensing transparency and compliance by reading, verifying, and validating license metadata embedded directly in font files.

When fonts are distributed on the web or in applications, they often travel without their accompanying LICENSE.txt files. The only way to verify licensing in these scenarios is through embedded metadata. This tool exists to ensure that licensing information is present, accurate, and verifiable against official OSI-approved sources.

**Who it's for:**
- **Developers** building web applications with custom fonts
- **Designers** auditing font libraries for license compliance
- **Organizations** ensuring legal compliance across font usage
- **Font distributors** verifying metadata quality before publishing
- **Open source projects** checking fonts before inclusion

## Principles

1. **Read what's actually there** - Parse font binaries directly, don't assume external files exist
2. **Verify against authoritative sources** - Compare metadata to OSI canonical license texts
3. **Work at scale** - Support batch processing of entire font libraries
4. **Be format-agnostic** - Handle TTF, OTF, WOFF, WOFF2 uniformly
5. **Provide actionable output** - Both human-readable reports and machine-parseable JSON
6. **Fail clearly** - Exit codes and warnings that make compliance checking automated

## Goals

- [x] Read and display license metadata from all major font formats
- [x] Detect common open source licenses (OFL, Apache, MIT)
- [x] Verify licenses against OSI canonical texts
- [x] Support batch processing with shell scripts
- [x] Provide JSON output for programmatic use
- [ ] Support additional license types (BSD, GPL variants, CC licenses)
- [ ] Add license health scoring (completeness, accuracy, URL validity)
- [ ] Integrate with CI/CD pipelines (GitHub Actions, pre-commit hooks)
- [ ] Generate compliance reports for entire font collections
- [ ] Support font conversion workflows (ensure metadata preservation)
- [ ] Web service API for on-demand font license checking

## Success Metrics

**Success looks like:**
- Organizations confidently using fonts knowing licensing is verified
- Web font conversions that preserve licensing metadata
- Fewer fonts distributed without proper license attribution
- Industry adoption as a standard tool for font license auditing
- Contribution to font metadata quality standards
