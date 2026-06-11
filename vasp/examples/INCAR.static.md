# Static Calculation INCAR Template

## Purpose

This template is intended for non-relaxing static calculations using a fixed geometry.

Typical use cases include:
- final energy calculations
- density of states calculations
- charge density generation
- post-relaxation analysis

## Key Settings

### Fixed Geometry

```text
IBRION = -1
NSW = 0
```

No ionic updates are performed.

### Electronic Convergence

```text
EDIFF = 1E-6
```

Tighter electronic convergence is used compared to relaxation workflows.

### Smearing

```text
ISMEAR = -5
```

Tetrahedron smearing is used as a conservative default for insulating systems.

Metallic systems may require different smearing settings.

## Notes

Static calculations should generally be performed on geometries that have already been properly relaxed.

For production workflows:
- k-point convergence
- ENCUT convergence
- smearing sensitivity
should be validated appropriately.
