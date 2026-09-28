# Domain Context Tools

This directory contains read-only producers for curated BMDex contextual
reference knowledge.

The current producer queries local BMDex JSON records and writes JSON-safe
contextual reference evidence:

```bash
printf '{"query":{"code":"VASP","calculation_family":"hybrid_functional","functional":"HSE06","electronic_algorithm":"Damped","topic":"electronic_iteration_behavior"}}' | python -B -m tools.domain_context.query
```

## Record Contract

Records live in `vasp/contextual_reference/records/`. Every record is validated
before any query is answered, and one invalid record makes the query return a
structured `record_validation_error` or `record_store_error` instead of
results. A record must have:

- `schema_version` equal to a supported record schema version (currently `1`);
- an `id` identical to its filename without `.json`, unique across records
  (case-insensitively);
- `status` of `active`, `deprecated`, or `retired`; queries return only
  `active` records;
- non-empty string `id`, `title`, `status`, `contextual_statement`, and
  `diagnostic_relevance`;
- non-empty lists of non-empty strings for `topics` and `limitations`;
- at least one source, each with non-empty text fields and an absolute
  `https://` URL;
- `record_provenance.record_version` as a positive integer;
- if present, `applicability.relevant_observed_patterns` as a non-empty list of
  identifiers from the observed-pattern vocabulary (below); and
- no top-level fields other than the required fields and the optional
  `shorthand_correction`.

Records must be strict JSON: `NaN` and `Infinity` are rejected. Increasing
`record_version` when a record's scientific content changes is still a review
responsibility; the producer does not detect unversioned edits.

## Query Fields

`code` and its alias `domain` take one string and must not disagree.
`calculation_family`, `functional`, `electronic_algorithm`, `topic`, and
`observed_patterns` take a string or a list of strings. `input_tags` takes an
object mapping VASP tag names to scalar values, for example
`{"LHFCALC": ".TRUE."}`. `null` and empty lists mean "not specified". Other
malformed values return an `invalid_query` error rather than an empty result.

## Observed-Pattern Vocabulary

BMDex owns the identifiers used for run observations:
`vasp/contextual_reference/observed_patterns.json` defines each identifier and
its limitations. Records may list only these identifiers in
`applicability.relevant_observed_patterns`, and queries may send only these
identifiers as `observed_patterns`. Identifiers are compared exactly. An
unknown identifier in a query returns `invalid_query`; in a record it is a
`record_validation_error`. A malformed vocabulary file is a
`record_store_error`.

A consumer reports an identifier only when its observation meets that
identifier's definition. The identifiers name observations; they are not
diagnoses.

## Matching

A record matches when the query's `code` agrees and at least one of
`calculation_family`, `functional`, `topic`, `observed_patterns`, or
`input_tags` overlaps the record. Observed patterns are additional evidence,
not a requirement: a record can match on calculation and input fields alone.
Each match reports `matched_fields` and `matched_observed_patterns`, the
record's patterns that the query supplied. An empty
`matched_observed_patterns` means run observations did not contribute to that
match, so consumers must not describe the match as supported by trajectory
evidence.

BMDex provides reference context. BMD Agent performs evidence synthesis and
diagnosis. BMD Compute owns executable calculation methodology for the core
VASP data-generation pipeline.
