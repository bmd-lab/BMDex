# VASP Examples

Reusable VASP input examples and small runnable examples.

These files are starting points for calculation setup. They are not universal
production settings; convergence and scientific suitability still need to be
checked for each workflow.

Status:

- `INCAR.relax`: validated conservative structural relaxation starting point
- `INCAR.static`: validated fixed-geometry static-calculation starting point
- `KPOINTS.example`: minimal automatic mesh example for adaptation
- `POTCAR.spec.example`: repository-safe pseudopotential specification example

## Reusable Inputs

- `INCAR.relax`: conservative structural relaxation settings
- `INCAR.static`: fixed-geometry static calculation settings
- `KPOINTS.example`: simple automatic k-point mesh example
- `POTCAR.spec.example`: repository-safe pseudopotential specification example
- `si_bulk_relax/`: minimal runnable silicon bulk relaxation example

## `INCAR.relax`

Typical use cases include bulk relaxation, initial geometry optimization,
lattice optimization, and preparation for static calculations.

Important defaults:

```text
IBRION = 2
NSW = 100
ISIF = 3
EDIFF = 1E-5
EDIFFG = -0.02
ISMEAR = 0
SIGMA = 0.05
```

`ISIF = 3` relaxes both ionic positions and cell degrees of freedom. Modify
`ISIF` for fixed-volume calculations, surface calculations where vacuum should
be preserved, or selective relaxation workflows.

The convergence and smearing settings are conservative general-purpose
defaults. Metallic systems or property-sensitive workflows may need different
settings.

## `INCAR.static`

Typical use cases include final energy calculations, density of states,
charge-density generation, and post-relaxation analysis.

Important defaults:

```text
IBRION = -1
NSW = 0
EDIFF = 1E-6
ISMEAR = -5
```

Static calculations should generally be performed on properly relaxed
geometries. Production workflows should validate k-point density, `ENCUT`, and
smearing sensitivity.

## `KPOINTS.example`

This file demonstrates a simple automatic k-point mesh for periodic bulk
calculations.

K-point density should scale with reciprocal lattice dimensions and remain
consistent across comparable calculations. Gamma-centered meshes are convenient
for large supercells, low-symmetry systems, and general workflow consistency.
Monkhorst-Pack meshes may be preferable for highly symmetric primitive cells,
metallic systems, or carefully converged production calculations.

Do not assume the example mesh is universally sufficient.

## `POTCAR.spec.example`

`POTCAR.spec` files specify required pseudopotentials without storing licensed
`POTCAR` content in the repository.

Examples:

```text
Si
```

```text
Mg
O
```

Current group standard functional:

```text
PBE_64
```

The order of entries must match the species ordering in `POSCAR`. Actual
`POTCAR` files must never be committed to BMDex.
