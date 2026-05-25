# VASP Input Standards

## Purpose

This document describes the standard conventions used for VASP calculations in the BMD Lab.

The goal is to maintain:
- reproducibility
- consistency across students
- transparent methodological assumptions
- maintainable workflows

## General Principles

- Prefer conservative and validated settings over aggressive optimization.
- Document all deviations from standard templates.
- Separate exploratory workflows from validated production workflows.
- Record pseudopotential functional explicitly.

## INCAR Standards

### Relaxation Calculations

Typical settings:
- ionic relaxation enabled
- conservative convergence thresholds
- stress tensor enabled when appropriate

### Static Calculations

Typical settings:
- fixed geometry
- tighter electronic convergence
- no ionic updates

## POTCAR Standards

- POTCAR files should never be committed to the repository.
- Use `POTCAR.spec` files instead.
- Functional must always be documented explicitly.

Current standard functional:
- PBE_64

## KPOINTS Standards

- k-point density should scale appropriately with cell size.
- Convergence testing should be documented for production calculations.

## Validation Expectations

Validated calculations should:
- converge electronically
- converge ionically where appropriate
- preserve expected physical behavior
- include basic sanity checks

## Documentation Expectations

Each validated workflow should document:
- scientific purpose
- assumptions
- expected outputs
- known limitations
- computational cost considerations
