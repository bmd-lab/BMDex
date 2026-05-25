# POTCAR.spec Template

## Purpose

`POTCAR.spec` files specify the pseudopotentials required for a calculation without storing actual POTCAR data in the repository.

This preserves:
- reproducibility
- pseudopotential transparency
- compliance with VASP licensing restrictions

## Example

```text
Si
```

or:

```text
Mg
O
```

## Functional Consistency

The pseudopotential functional should always be documented explicitly.

Current group standard:
- PBE_64

Mixing incompatible pseudopotential families within workflows should be avoided unless explicitly justified.

## Repository Policy

Actual POTCAR files must never be committed to the repository.

Only specifications and documented conventions should be stored.
