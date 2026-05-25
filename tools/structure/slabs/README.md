# Slab Utilities

This module contains reusable slab-generation utilities for computational materials workflows.

The utilities are intended to support:
- surface generation
- layered-material workflows
- exfoliation studies
- VASP slab preparation
- automated structure screening

## Design Philosophy

These utilities are intended to function as:
- generic reusable primitives
- independent of specific workflows or publications

Higher-level workflows such as MSS-Auto build upon these reusable tools.

## Typical Features

- slab construction
- vacuum insertion
- orientation handling
- structure export
- VASP compatibility

## Dependencies

Typical dependencies include:
- pymatgen
- numpy
