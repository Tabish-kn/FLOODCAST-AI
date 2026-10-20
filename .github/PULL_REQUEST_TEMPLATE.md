# Pull Request Submission

## Summary

<!-- Provide a concise description of the changes introduced by this pull request. -->

## Motivation

<!-- Why is this change necessary? What problem or user story does it address? -->

## Implementation Details

<!-- Detail the technical architecture, algorithms, or API changes implemented. -->

## Related Issue

<!-- Closes #123, Fixes #456, or Relates to #789 -->

## Testing Performed

<!-- Detail the exact automated tests and manual verification performed.
Distinguish verified, tested results from assumptions or simulated behavior. -->
- [ ] Backend test suite: `pytest tests/ -v` (Result: ____)
- [ ] Frontend build verification: `npm run build` (Result: ____)
- [ ] Manual endpoint or UI verification: (Detail steps)

## Screenshots or Visuals (if applicable)

<!-- Attach before/after screenshots or UI previews for dashboard modifications. -->

## Data & ML Changes

<!-- Answer if applicable:
- Did this change modify training datasets, features, or model hyperparameters?
- How was feature leakage prevented? (Spatial / Event holdouts)
- Measured evaluation impact (PR-AUC, Brier score, Calibration error): -->

## Documentation Changes

- [ ] Updated `README.md` (if public interfaces or setup changed)
- [ ] Updated `ARCHITECTURE.md` (if technical design changed)
- [ ] Updated `CHANGELOG.md` under `[Unreleased]`

## Privacy & Security Considerations

- [ ] No API keys, credentials, or secrets committed.
- [ ] Geospatial coordinates adhere to privacy/fuzzing guidelines.
- [ ] Uploaded media strips EXIF and identifying metadata.

## Contributor Checklist

- [ ] My code follows the repository style standards (PEP 8, ESLint).
- [ ] I have commented my code, particularly in complex geospatial or mathematical logic.
- [ ] New code is covered by automated unit/integration tests.
- [ ] I have verified that all links and documentation render correctly.
