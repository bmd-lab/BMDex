# Silicon Bulk Relaxation Example

This example is a minimal VASP structural relaxation for diamond-cubic silicon.
It is intended as a small, readable reference calculation for onboarding,
workflow checks, and comparison against future VASP examples.

The canonical runnable inputs and metadata live in:
- `examples/vasp/si_bulk_relax/`

## Workflow Type

Bulk structural relaxation:
- optimize ionic positions and lattice degrees of freedom
- use conservative relaxation settings
- generate a relaxed structure suitable for basic sanity checks or follow-on
  static calculations

## Expected Outputs

A successful run should produce standard VASP relaxation outputs, including:
- `CONTCAR`
- `OUTCAR`
- `vasprun.xml`
- final total energy
- relaxed lattice parameters

## Validation Expectations

After completion, check that the calculation:
- converged electronically
- converged ionically
- preserved the expected silicon crystal symmetry
- produced physically reasonable Si-Si bond lengths
