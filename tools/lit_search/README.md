# Literature Search

A simple BMDex tool for estimating how extensively candidate chemical
compositions have appeared in the scientific literature.

The tool reads a list of chemical formulae, searches the Scopus API for each
formula, and writes the number of matching publications to a CSV file.

It is a **researcher-facing screening tool**, not part of the BMDex
electroneutral-composition generator and not a canonical BMDex dataset.

## Scope

The literature-search workflow is deliberately narrow:

```text
formula list
    +
Scopus API
    |
    v
publication counts
```

It is useful for rapid screening of large composition spaces. It is not a
novelty detector, a full bibliographic analysis tool, a paper downloader, or a
replacement for a careful literature review.

A low publication count does **not** establish that a material is novel. It only
indicates that the particular Scopus query returned few matching records.

## Directory Contents

```text
tools/lit_search/
├── README.md
├── scopus_search.py
└── check_quota.py
```

### `scopus_search.py`

Main literature-search script. It:

1. reads chemical formulae from a text file;
2. searches Scopus for each formula;
3. obtains the number of matching records;
4. writes the results to a CSV file;
5. periodically reports the remaining Scopus API quota; and
6. can resume an interrupted search without repeating completed formulae.

### `check_quota.py`

Small utility for checking whether the Scopus API connection is working and
displaying the remaining API quota and reset time.

## Requirements

The search uses the Scopus API through
[`pybliometrics`](https://pybliometrics.readthedocs.io/).

Install it with:

```bash
pip install pybliometrics
```

A valid Elsevier/Scopus API key is required. Scopus credentials should be
configured through pybliometrics, not written into BMDex scripts or committed to
the repository.

Use the pybliometrics documentation for current setup instructions. API access,
quota, and rate limits are controlled by Elsevier and may change.

## Input

The input is a plain-text file containing one chemical formula per line:

```text
CaTiO3
BaTiO3
Bi2Se3
NaAuSe
CsInS2
```

Formulae may come from an electroneutral composition search, another BMDex
tool, an external materials database, a manually prepared list, or any other
composition-generation workflow.

This separation is intentional: **literature searching and composition
generation are independent operations.**

## Running A Search

Open `scopus_search.py` and edit the settings near the top of the file:

```python
INPUT_FILE = "formulae.txt"
OUTPUT_FILE = "scopus_counts.csv"

MAX_QUERIES = 20000
SLEEP_TIME = 0.1
```

Then run from the repository root:

```bash
python3 tools/lit_search/scopus_search.py
```

The script processes formulae sequentially and writes each result immediately,
so little progress should be lost if the search is interrupted.

## Checking API Access

Before a large search, check the Scopus API connection and current quota:

```bash
python3 tools/lit_search/check_quota.py
```

## Scopus Query

By default, each formula is searched using:

```text
TITLE-ABS-KEY("FORMULA")
```

For example:

```text
TITLE-ABS-KEY("CaTiO3")
```

This searches article titles, abstracts, and keywords. The quotation marks are
intentional: they request the compact formula as a phrase rather than treating
its components as independent search terms.

## Output

Results are written to a CSV file:

```csv
formula,papers
CaTiO3,12345
BaTiO3,23456
Bi2Se3,34567
NaAuSe,1
```

The first column contains the queried formula and the second contains the number
of Scopus records returned by the search.

## Restarting An Interrupted Search

If the output CSV already exists, `scopus_search.py` reads formulae that have
already completed and skips them. Rows marked `ERROR` are retried on the next
run.

For example, if `formulae.txt` contains 20,000 formulae but
`scopus_counts.csv` already contains results for 8,000 of them, restarting the
script continues with the remaining formulae rather than repeating the first
8,000 queries.

## Interpreting Publication Counts

The returned number should be treated as a **literature-search metric**, not as
a definitive count of papers about a particular crystalline material.

Chemical formula searches have several limitations:

- alternative chemical formula ordering;
- spaces or formatting within formulae;
- subscripts and other typographical representations;
- non-stoichiometric compositions;
- mineral or compound names used instead of formulae;
- formula strings that also occur in unrelated contexts; and
- papers not indexed by Scopus.

Consequently:

```text
papers = 0
```

means:

> No Scopus records were found using this particular query.

It does **not** mean:

> This composition has never been reported.

Likewise, a large count does not necessarily mean every returned paper concerns
the intended material.

## Relationship To Composition Generation

This tool deliberately does not generate electroneutral compositions.

A composition-generation workflow might produce:

```text
electroneutral composition generation
             |
             v
        formulae.txt
             |
             v
      scopus_search.py
             |
             v
     scopus_counts.csv
```

However, `scopus_search.py` only sees `formulae.txt`. It does not need to know
which oxidation states were considered, how charge neutrality was determined,
which elements were allowed, which BMDex generator produced the formulae, or
whether the formulae were generated by BMDex at all.

## Formula Ordering

Scopus searches text rather than chemical compositions. Consequently, `NaAuSe`
and an alternative ordering of the same composition are not guaranteed to
produce identical search results.

The literature-search tool does not silently reorder or modify input formulae.
**The formula written in the input file is the formula that is searched.**

If formula normalization or alternative formula representations are required,
generate them explicitly before running the literature search.

## Large Searches

For large candidate spaces:

1. check the API connection and quota first;
2. keep the input formula file unchanged while a search is running;
3. retain the partially completed CSV;
4. allow the restart mechanism to skip completed formulae; and
5. keep the raw search results before performing sorting or filtering.

Keeping raw results separate makes it easier to reproduce or reinterpret a
search later.

## Reproducibility

When publication counts are used in subsequent analysis, retain:

- the original input formula file;
- the raw output CSV;
- the date of the search;
- the query form used;
- the version of `scopus_search.py`; and
- the relevant pybliometrics version.

Literature databases change over time, so repeating the same search at a later
date may produce different counts.

