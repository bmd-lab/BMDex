# KPOINTS Example Template

## Purpose

This example demonstrates a simple automatic k-point mesh for periodic bulk calculations.

## General Philosophy

K-point density should:
- scale appropriately with reciprocal lattice dimensions
- be validated for production calculations
- remain consistent across comparable calculations

The goal is to balance:
- numerical accuracy
- computational cost
- reproducibility

## Gamma vs Monkhorst-Pack

Gamma-centered meshes are often convenient for:
- large supercells
- low-symmetry systems
- general workflow consistency

Monkhorst-Pack meshes may be preferable for:
- highly symmetric primitive cells
- metallic systems
- carefully converged production calculations

## Convergence Expectations

Validated workflows should document:
- k-point convergence behavior
- rationale for chosen mesh density
- sensitivity of target properties

## Notes

This example is intentionally conservative and minimal.

Production calculations should not assume this mesh is universally sufficient.
