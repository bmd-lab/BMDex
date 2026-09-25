# BMDex

BMDex is the BMD Lab repository for curated supporting scientific data,
reference evidence, and non-core scientific tools used in reproducible
computational materials research.

The repository is public. It contains material that is appropriate to share and
reuse, not private research storage or deployment configuration.

## Where BMDex Fits

BMDex complements the public `tutorials` repository and the other BMD tools:

- `tutorials` teaches public concepts, onboarding, and basic workflows.
- BMDex curates scientific datasets, contextual reference knowledge, validated
  evidence, reusable utilities, and publicly shareable infrastructure notes.
- BMD Compute owns methodology and implementation that determine how BMD
  generates VASP calculations.
- BMD Agent consumes BMDex producer interfaces and coordinates evidence without
  duplicating the authority of BMDex or BMD Compute.

BMDex is designed for graduate students and researchers in materials science.
Useful research actions should stay visible; repository mechanics and metadata
should remain supporting details.

## What Belongs Here

- curated scientific reference data with provenance and limitations;
- machine-readable domain context grounded in a concrete scientific use case;
- validated workflow evidence and reproducible examples;
- reusable non-core scientific tools and transformations;
- publicly shareable HPC operational guidance; and
- templates and supporting standards outside the BMD Compute VASP generation
  pipeline.

The following do not belong in BMDex:

- runtime calculation state, large generated outputs, or active project dumps;
- credentials, private keys, API tokens, or deployment-local configuration;
- private or unpublished research and collaborator material without explicit
  publication approval;
- personal or student records;
- licensed VASP `POTCAR` or PAW potential contents; and
- proprietary or licensed datasets without redistribution permission.

## Repository Layout

- `datasets/`: curated scientific datasets, including element-charge,
  element-abundance, and structure-prototype data.
- `tools/`: reusable composition, domain-context, structure, and literature
  utilities.
- `vasp/`: VASP supporting assets, examples, contextual references, and
  validation evidence. It does not contain licensed VASP source or potentials.
- `cluster/`: publicly shareable notes and scripts for externally managed HPC
  systems. Local policies and module names may change.
- `tests/`: contract and validation tests for the machine-facing producers and
  records.

## Python Setup

Run commands from the repository root. Python 3.10 or newer is required by the
current producer syntax; Python 3.12 is the routinely verified development
environment.

```bash
git clone https://github.com/bmd-lab/BMDex.git
cd BMDex
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

On Windows PowerShell, create and activate the environment with:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

`requirements.txt` declares the third-party libraries already used by the
researcher-facing scripts. It is intentionally not a lock file. Record exact
package versions when they are material to a scientific result.

The current Agent-facing producers and their tests use only the Python standard
library. A contributor working only on those interfaces can run the tests before
installing the scientific stack:

```bash
python -B -m unittest discover -s tests
```

Compile all Python sources as a lightweight syntax check:

```bash
python -B -m compileall -q tools vasp tests
```

Individual tools document runtime inputs, external services, and scientific
limitations in their nearest `README.md`. For example, Materials Project access
requires an API key configured outside the repository, and Scopus tools use the
user's external `pybliometrics` configuration.

## Producer Interfaces

BMD Agent consumes fixed JSON stdin/stdout interfaces from a repository
checkout. These commands are also useful for development and debugging. Run
them from the repository root and keep stdout machine-readable.

Composition context:

```bash
printf '{"formula":"MnCu5"}' | python -B -m tools.composition.context_producer
```

VASP domain context:

```bash
printf '{"query":{"code":"VASP","calculation_family":"hybrid_functional","functional":"HSE06","electronic_algorithm":"Damped","topic":"electronic_iteration_behavior"}}' | python -B -m tools.domain_context.query
```

These producers return curated contextual evidence. They do not inspect or
diagnose live calculations, change scientific data, or define BMD Compute
methodology. Their existing schemas, record IDs, versions, and query behavior
are compatibility contracts.

## Researcher Tools

Examples of researcher-facing commands include:

```bash
python tools/structure_transform/generate_all_slabs.py
python tools/structure_transform/make_supercell.py
python tools/composition/electroneutrality/generate_ternaries.py
python tools/structure_prototypes/abundance_rank.py
```

Cluster scripts are intended to run from a normal BMDex checkout on the cluster;
Codex is not required there. Review each script and the local cluster policy
before submission.

## Curation

Keep provenance, validation status, usage notes, and limitations in the nearest
relevant `README.md`. YAML, JSON, and CSV are appropriate when they are the
scientific data or an established producer record, not as automatic metadata
sidecars.

Do not introduce a broad metadata model, database, ontology, or vector store
without a concrete scientific use case. Keep runtime calculation state,
deployment configuration, and private research storage separate from curated
knowledge and data.

See `CONTRIBUTING.md` for the student contribution workflow and the material
that must never be committed.

## License and Sources

BMDex repository-owned source code and documentation are available under the
MIT License; see `LICENSE`. Third-party dependencies remain under their own
licenses. Source-derived factual datasets retain the attribution documented
beside each dataset, and the MIT License does not relicense the cited source
publications.

BMDex does not distribute or license VASP executables, VASP source code,
`POTCAR` files, or PAW potential contents. Repository examples use
`POTCAR.spec` files so users can generate potentials only in an appropriately
licensed environment.
