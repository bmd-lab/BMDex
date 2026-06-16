# Element Abundance Datasets

Curated private scientific assets for compositional reasoning, screening, and
prototype ranking.

The canonical dataset is:

```text
earth-abundance.yaml
```

Values are stored as:

```yaml
Element: abundance
```

where abundance is reported in:

```text
mg/kg
```

## Repository Role

This dataset supports:

* composition screening
* abundance-aware ranking
* structure-prototype prioritization
* materials discovery workflows
* future composition-based heuristics

Tools should read abundance information from this dataset rather than
maintaining independent abundance tables.

Current downstream users include:

* `tools/structure_prototypes/abundance_rank.py`
* abundance-aware structure prototype ranking workflows

## Dataset Structure

Example:

```yaml
O: 461000
Si: 282000
Al: 82300
Fe: 56300
```

## Source

The crustal abundance values are derived from:

> Haynes, W. M. (Ed.). *CRC Handbook of Chemistry and Physics*. CRC Press, 2016.

The original spreadsheet used in earlier workflows has been replaced by a
canonical YAML representation for improved readability, version control, and
interoperability within BMDex.

## Validation

The current YAML file should parse cleanly, use valid element symbols, and store
numeric abundance values. Treat edits as data changes: check parsing and inspect
any changed element values before using them in screening workflows.

## Limitations

* Values represent crustal abundance and are not universal abundance measures.
* Different scientific applications may require alternative abundance datasets,
  such as solar, cosmic, seawater, or bulk-Earth abundances.
* Screening results should not be interpreted as estimates of material cost,
  availability, or manufacturability.
