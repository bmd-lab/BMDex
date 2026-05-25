# Layered Material Screening Workflow

## Purpose

This workflow describes the MSS-Auto methodology for automated screening of potentially layered materials.

The workflow combines:
- crystallographic structure analysis
- automated structure manipulation
- slab-generation logic
- and conductivity effective mass analysis.

## Typical Workflow

1. Load bulk crystal structure
2. Standardize structure representation
3. Analyze crystallographic orientations
4. Generate candidate slabs
5. Insert vacuum regions
6. Evaluate anisotropy-related descriptors
7. Identify candidate layered materials

## Inputs

Typical inputs include:
- POSCAR structures
- CIF files
- crystallographic databases
- computed effective mass information

## Outputs

Typical outputs include:
- slab structures
- candidate exfoliation directions
- orientation metadata
- screening summaries

## Validation Considerations

Candidate materials should be checked for:
- physically meaningful slab geometries
- sufficient vacuum spacing
- realistic layer separation
- crystallographic consistency

Screening outputs should not automatically be interpreted as experimentally validated exfoliable materials.

## Notes

This workflow is intended to:
- accelerate screening
- reduce manual structure preparation
- support high-throughput computational workflows

Further:
- thermodynamic
- kinetic
- and experimental
validation may still be necessary.
