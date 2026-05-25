# pymatgen Usage Philosophy

BMDex uses pymatgen as the primary structure
manipulation and materials representation framework.

Preferred use cases include:
- structure transformations
- file parsing
- slab generation
- compositional reasoning
- workflow interoperability

General principles:
- prefer pymatgen-native representations
- avoid unnecessary custom parsers
- preserve interoperability with VASP workflows
- favor reusable utilities over notebook-local code
