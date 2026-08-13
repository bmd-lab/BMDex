\# Literature Search



A simple BMDex tool for estimating how extensively candidate chemical compositions have appeared in the scientific literature.



The tool reads a list of chemical formulae, searches the Scopus API for each formula, and writes the number of matching publications to a CSV file.



It is intended as a \*\*researcher-facing screening tool\*\*, rather than as part of the BMDex electroneutral-composition generator or any canonical BMDex dataset.



\---



\## Purpose



When exploring large chemical composition spaces, it is often useful to distinguish between compositions that are already well represented in the literature and compositions that appear to have received little or no attention.



This tool provides a simple way to perform that screening.



For example, an input file containing:



```text

CaTiO3

BaTiO3

Bi2Se3

NaAuSe

```



can be searched automatically against Scopus to produce:



```csv

formula,papers

CaTiO3,12345

BaTiO3,23456

Bi2Se3,34567

NaAuSe,1

```



The publication count can then be used as one indicator when prioritising compositions for further investigation.



A low publication count does \*\*not\*\* establish that a material is novel. It only indicates that the particular search query returned few matching Scopus records.



\---



\## Directory contents



```text

literature\_search/

├── README.md

├── scopus\_search.py

└── check\_quota.py

```



\### `scopus\_search.py`



Main literature-search script.



It:



1\. reads chemical formulae from a text file;

2\. searches Scopus for each formula;

3\. obtains the number of matching records;

4\. writes the results to a CSV file;

5\. periodically reports the remaining Scopus API quota; and

6\. can resume an interrupted search without repeating completed formulae.



\### `check\_quota.py`



Small utility for checking whether the Scopus API connection is working and displaying the remaining API quota and reset time.



\---



\## Requirements



The search uses the Scopus API through

\[`pybliometrics`](https://pybliometrics.readthedocs.io/).



Install it with:



```bash

pip install pybliometrics

```



A valid Elsevier/Scopus API key is also required.



See the pybliometrics documentation for current instructions on obtaining and configuring API access.



API keys should \*\*not\*\* be stored directly in the BMDex repository.



\---



\## Input



The input is a plain-text file containing one chemical formula per line.



For example:



```text

CaTiO3

BaTiO3

Bi2Se3

NaAuSe

CsInS2

```



The formulae do not need to originate from any particular BMDex workflow.



For example, they may come from:



\* an electroneutral composition search;

\* an external materials database;

\* another BMDex tool;

\* a manually prepared list; or

\* any other composition-generation workflow.



This separation is intentional: \*\*literature searching and composition generation are independent operations.\*\*



\---



\## Running a search



Open `scopus\_search.py` and edit the settings near the top of the file:



```python

INPUT\_FILE = "formulae.txt"

OUTPUT\_FILE = "scopus\_counts.csv"



MAX\_QUERIES = 20000

SLEEP\_TIME = 0.1

```



Then run:



```bash

python scopus\_search.py

```



The script processes the formulae sequentially and writes each result to the output file as soon as the query has completed.



\---



\## Scopus query



By default, each formula is searched using:



```text

TITLE-ABS-KEY("FORMULA")

```



For example:



```text

TITLE-ABS-KEY("CaTiO3")

```



This asks Scopus to search for the formula in article titles, abstracts, and keywords.



The quotation marks are intentional. They request the compact chemical formula as a phrase rather than treating its components as independent search terms.



\---



\## Output



Results are written to a CSV file:



```csv

formula,papers

CaTiO3,12345

BaTiO3,23456

Bi2Se3,34567

NaAuSe,1

```



The first column contains the queried formula and the second contains the number of Scopus records returned by the search.



The output can be sorted or analysed using standard spreadsheet, command-line, Python, or BMDex tools.



\---



\## Restarting an interrupted search



Large composition spaces may require thousands of Scopus queries.



`scopus\_search.py` is therefore designed to be restartable.



If the output CSV already exists, the script reads the formulae that have already been completed and skips them.



For example, if:



```text

formulae.txt

```



contains 20,000 formulae but:



```text

scopus\_counts.csv

```



already contains results for 8,000 of them, restarting the script continues with the remaining formulae rather than repeating the first 8,000 queries.



Results are written immediately after each successful query, so little progress should be lost if the search is interrupted.



\---



\## API quota



Scopus limits the number of API requests that can be made within a given period.



During a long search, `scopus\_search.py` periodically reports the remaining quota.



The separate utility:



```bash

python check\_quota.py

```



can also be used to check the API connection and current quota before starting a large search.



The exact quota and rate limits are controlled by Elsevier and may change. Consult the current Scopus and pybliometrics documentation rather than assuming that historical limits remain valid.



\---



\## Interpreting publication counts



The returned number should be treated as a \*\*literature-search metric\*\*, not as a definitive count of papers about a particular crystalline material.



Chemical formula searches have several limitations.



For example:



```text

CaSe

```



may appear in contexts unrelated to a specific calcium selenide material, while some papers describing calcium selenide may use alternative notation or terminology and therefore not contain the exact string `CaSe`.



Other complications include:



\* alternative chemical formula ordering;

\* spaces or formatting within formulae;

\* subscripts and other typographical representations;

\* non-stoichiometric compositions;

\* mineral or compound names used instead of formulae;

\* formula strings that also occur in unrelated contexts; and

\* papers not indexed by Scopus.



Consequently:



```text

papers = 0

```



should be interpreted as:



> No Scopus records were found using this particular query.



It should \*\*not\*\* be interpreted as:



> This composition has never been reported.



Likewise, a large count does not necessarily mean that every returned paper concerns the intended material.



\---



\## Relationship to electroneutral composition generation



This tool deliberately does not generate electroneutral compositions.



A composition-generation workflow might produce:



```text

electroneutral composition generation

&#x20;             |

&#x20;             v

&#x20;        formulae.txt

&#x20;             |

&#x20;             v

&#x20;      scopus\_search.py

&#x20;             |

&#x20;             v

&#x20;     scopus\_counts.csv

```



However, `scopus\_search.py` only sees `formulae.txt`.



It does not need to know:



\* which oxidation states were considered;

\* how charge neutrality was determined;

\* which elements were allowed;

\* how many elements were combined;

\* which BMDex generator produced the formulae; or

\* whether the formulae were generated by BMDex at all.



This keeps the literature-search tool independent, transparent, and reusable.



\---



\## Formula ordering



Scopus searches text rather than chemical compositions.



Consequently:



```text

NaAuSe

```



and an alternative ordering of the same composition are not guaranteed to produce identical search results.



The literature-search tool therefore does not silently reorder or modify input formulae.



\*\*The formula written in the input file is the formula that is searched.\*\*



If formula normalization or alternative formula representations are required, they should be generated explicitly before running the literature search.



This behaviour is intentional so that the search procedure remains transparent.



\---



\## Large searches



For large candidate spaces, it is recommended to:



1\. check the API connection and quota first;

2\. keep the input formula file unchanged while a search is running;

3\. retain the partially completed CSV;

4\. allow the restart mechanism to skip completed formulae; and

5\. keep the raw search results before performing sorting or filtering.



For example:



```text

formulae.txt

&#x20;     |

&#x20;     v

scopus\_search.py

&#x20;     |

&#x20;     v

scopus\_counts.csv

&#x20;     |

&#x20;     v

sorting / filtering / analysis

```



Keeping the raw results separate makes it easier to reproduce or reinterpret a search later.



\---



\## Example workflow



Suppose another BMDex tool generates:



```text

candidate\_formulae.txt

```



containing:



```text

CsInS2

NaAuSe

FeSiS3

KFeTe2

RbCrSe2

```



Set:



```python

INPUT\_FILE = "candidate\_formulae.txt"

OUTPUT\_FILE = "scopus\_counts.csv"

```



and run:



```bash

python scopus\_search.py

```



The resulting file might contain:



```csv

formula,papers

CsInS2,6

NaAuSe,1

FeSiS3,0

KFeTe2,0

RbCrSe2,0

```



These results can then be sorted to identify candidates with little apparent literature coverage.



\---



\## Scope



This tool currently uses \*\*Scopus\*\* as its literature source.



Its purpose is deliberately narrow:



```text

formula list

&#x20;    +

Scopus API

&#x20;    |

&#x20;    v

publication counts

```



It is not intended to perform full bibliographic analysis, establish material novelty, download papers, or replace a careful literature review.



Its role is rapid screening of large composition spaces.



\---



\## Reproducibility



When publication counts are used in subsequent analysis, it is good practice to retain:



\* the original input formula file;

\* the raw output CSV;

\* the date of the search;

\* the query form used;

\* the version of `scopus\_search.py`; and

\* the relevant pybliometrics version.



Literature databases change over time, so repeating the same search at a later date may produce different counts.



\---



\## Summary



The BMDex literature-search tool is intentionally simple:



```text

formulae.txt

&#x20;    |

&#x20;    v

scopus\_search.py

&#x20;    |

&#x20;    v

scopus\_counts.csv

```



It accepts arbitrary chemical formulae, queries Scopus, records publication counts, respects API limitations, and can resume interrupted searches.



Composition generation remains outside the tool.



This separation allows the same literature-search workflow to be used with electroneutral BMDex compositions, other BMDex tools, external datasets, or manually selected candidate materials.

