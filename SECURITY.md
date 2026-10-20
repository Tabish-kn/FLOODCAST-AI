# Security & Privacy Policy

FloodCast AI is committed to ensuring the security of its geospatial intelligence platform, safeguarding the privacy of citizen observers who submit community waterlogging reports, and maintaining responsible disclosure practices.

## Supported Versions

Security updates are applied to active development branches and designated release versions:

| Version | Supported          | Status                                 |
| ------- | ------------------ | -------------------------------------- |
| 1.0.x   | :white_check_mark: | Current stable prototype               |
| < 1.0.0 | :x:                | Deprecated early experimental releases |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

If you discover a security vulnerability, credential leak, or privacy flaw in FloodCast AI:

1. **Email the Maintainers**: Send a detailed advisory to `[CONFIGURE_SECURITY_CONTACT: security@floodcast.ai or contact the repository owner privately via GitHub Security Advisories]`.
2. **Include Reproduction Details**:
   - Component affected (Backend FastAPI, Database, Frontend React, or ML pipeline)
   - Step-by-step reproduction instructions or proof-of-concept
   - Impact assessment (e.g., unauthorized data access, arbitrary code execution, denial of service)
   - Proposed remediation if available
3. **Response Timeline**: Maintainers aim to acknowledge receipt within 48 hours and provide an initial assessment and mitigation plan within 7 business days.
4. **Coordinated Disclosure**: We ask that you respect a 90-day embargo before any public disclosure to allow reasonable time for patching and distribution.

## Secrets & Credentials Policy

- **Zero-Secret Commitment**: Never commit production passwords, API tokens, JWT secret keys, cloud access keys, or database credentials to version control.
- **Environment Configuration**: Always use environment variables or secret managers. A template is provided in [.env.example](file:///.env.example).
- **Pre-commit Checks**: Contributors are encouraged to use automated secret scanning tools (e.g., `git-secrets`, `trufflehog`) prior to pushing branches.

## Geospatial Privacy & Citizen Protection

Community waterlogging reports contribute crucial ground-truth validation, but contributor privacy must remain protected:

1. **Location Obfuscation / Spatial Fuzzing**:
   - The platform intentionally fuzzes precise residential geographic coordinates (~100m - 200m grid centroid snapping) on public map feeds when reporting from residential areas to prevent de-anonymization.
2. **Metadata & EXIF Sanitization**:
   - Any future image upload capability must strip EXIF metadata (GPS tags, camera serial numbers, timestamps, and device make/model) on server ingestion prior to persisting files to disk or cloud storage.
3. **Consent & Anonymity**:
   - Contributor names, emails, and device identifiers are never published publicly. Community submissions support optional anonymous reporting.
4. **Safety Disclaimers**:
   - Observers are explicitly warned: **Never enter floodwaters, swift currents, or storm drains to submit a report or take a photograph.**

## Third-Party Data Compliance

FloodCast AI respects terms of service for external services:
- Rate limits on public APIs (e.g., Open-Meteo, OpenStreetMap Nominatim/Overpass, Copernicus Data Space) must be respected with local caching and exponential backoff.
- Commercial reuse of geospatial products must respect upstream licensing constraints.
