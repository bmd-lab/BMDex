# Structure Manipulation Philosophy

BMDex treats atomic structure handling as a core scientific topic rather than
as a standalone software bucket.

`pymatgen` is the lab's primary framework for structure manipulation and
materials representation, but the canonical concern here is structure
workflows, not the package name itself.

Preferred use cases include:
- structure transformations
- file parsing
- slab generation
- compositional reasoning tied to structure workflows
- workflow interoperability

General principles:
- prefer pymatgen-native representations where practical
- avoid unnecessary custom parsers
- preserve interoperability with VASP workflows
- favor reusable utilities over notebook-local code
