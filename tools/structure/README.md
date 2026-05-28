# Structure Tools

Structure-focused computational utilities, reference data integrations, and
supporting documentation for crystallographic workflows in BMDex.

This section groups reusable structure infrastructure in one place, including:

- `orientations/` crystallographic orientation utilities
- `poscar/` small VASP structure-file cleanup utilities
- `comparison/` structure and framework comparison utilities
- `primitive_cells/` primitive-cell generation from VASP structures
- `slabs/` slab-generation utilities
- `supercells/` supercell-generation utilities
- `mss_auto/` layered-material structure screening and slab workflow tooling

These entries are organized together because they support the same class of
structure manipulation, analysis, and workflow preparation tasks.

The preferred tool style is a practical, standalone script with a clear
user-settings block. Tools should be easy for researchers to run directly or
copy into calculation folders while remaining pymatgen-native and maintainable.

Structure prototype reference data lives under:

- `datasets/structure_prototypes/`
