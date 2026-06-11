# Relaxation INCAR Template

## Purpose

This template is intended for standard structural relaxation calculations in VASP.

Typical use cases include:
- bulk relaxation
- initial geometry optimization
- lattice optimization
- preparation for static calculations

The template prioritizes:
- stability
- reproducibility
- conservative convergence behavior
over aggressive optimization.

## Key Settings

### Ionic Relaxation

```text
IBRION = 2
NSW = 100
```

Conjugate-gradient ionic relaxation is used as a conservative default.

### Cell Relaxation

```text
ISIF = 3
```

Both ionic positions and cell degrees of freedom are relaxed.

Modify `ISIF` when:
- fixed-volume calculations are required
- surface calculations should preserve vacuum geometry
- selective relaxation is needed

### Convergence Criteria

```text
EDIFF = 1E-5
EDIFFG = -0.02
```

These values are intended as general-purpose defaults.

Production calculations may require tighter convergence depending on:
- energy sensitivity
- force sensitivity
- target properties

### Smearing

```text
ISMEAR = 0
SIGMA = 0.05
```

Gaussian smearing is used as a conservative default for general workflows.

Metallic systems may require alternative smearing schemes.

## Notes

This template should be treated as a stable starting point rather than a universally optimal configuration.

Deviations from the template should be documented explicitly in validated workflows.
