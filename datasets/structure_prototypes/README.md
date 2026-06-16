# Materials Project Unique Structure Prototypes 2025

This dataset contains a Materials Project-derived collection of inorganic crystal structure prototypes grouped by anonymous stoichiometry labels.

The dataset was developed as part of the Master's thesis:

> **The Unique Structure Prototypes of All Materials**
> Tel Aviv University, 2025

## Scientific Overview

Crystal structure provides a compact, composition-independent basis for understanding materials behavior and accelerating materials discovery.

This dataset was generated using an automated and reproducible workflow that identifies structure prototypes directly from atomic geometries rather than relying on database metadata.

By analyzing **23,160 experimentally observed thermodynamic ground-state inorganic materials** from the Materials Project, a geometric matching workflow was used to identify unique structural frameworks.

## Included Files

* `sorted-structures/` — stoichiometry-grouped CIF files and prototype summaries
* `all-prototypes-unfiltered.txt` — complete unfiltered prototype summary

Current dataset status:

* experimental external-source import under BMD Lab curation
* useful for structure-prototype exploration, but not yet a fully audited public
  release

Current dataset counts:

* source materials analyzed: 23,160
* anonymous stoichiometry prototype groups: 174
* CIF files: 5,557
* filtered unique entries: 699
* unfiltered entries: 2,410

## Dataset Structure

Each stoichiometry-group directory contains:

* CIF files belonging to that stoichiometry class
* `unique_structures.txt` summarizing the identified structure prototypes

Each prototype entry contains:

* Materials Project filename
* chemical formula
* prototype occurrence count
* space group information
* lattice/orientation matrix
* atomic fractional coordinates

### Example Entry

```text
Filename: mp-614603.cif  CaO  appeared: 122 times
Space Group: Fm-3m no. 225

Atoms Locations:
Ca [0. 0. 0.]
O  [0.5 0.5 0.5]
```

## Repository Role

This dataset is a canonical BMDex scientific dataset.

Reusable code for:

* prototype matching
* framework comparison
* prototype filtering
* abundance-aware ranking
* structure screening

should live under `tools/` and operate on this dataset rather than embedding duplicate prototype data.

The current reusable prototype utilities live under:

```text
tools/structure_prototypes/
```

## Provenance

Source repository:

* `https://github.com/bmd-lab/structure-prototypes.git`
* source commit: `3072b2e7b5dab54ed7a434d453838d8ce864d61a`

Original scientific work:

* *The Unique Structure Prototypes of All Materials*
* Tel Aviv University, 2025

Source structures:

* Materials Project thermodynamic ground-state inorganic materials

Method summary:

* structures are grouped by anonymous stoichiometry labels
* unique frameworks are identified using pymatgen structure matching
* prototype summaries record representative CIF filename, formula, occurrence
  count, space group, lattice information, and fractional coordinates

Primary dependency:

* pymatgen

## Limitations

* The dataset inherits the assumptions and coverage limitations of the Materials Project source structures.
* Structure matching depends on the geometric matching methodology used during dataset generation.
* Structure-matching tolerances should be reviewed before using the dataset as
  evidence for a specific scientific claim.
* Redistribution and licensing considerations should be reviewed before use outside the private BMD Lab repository.
