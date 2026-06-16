# Silicon Bulk Relaxation Example

This example is a minimal VASP structural relaxation for diamond-cubic silicon.
It is intended as a small, readable reference calculation for onboarding,
workflow checks, and comparison against future VASP examples.

The runnable inputs are kept in this directory so new students can inspect the
full example in one place.

## Included Files

| File | Purpose |
|---|---|
| `POSCAR` | Initial silicon structure |
| `INCAR` | Relaxation settings |
| `KPOINTS` | Brillouin-zone sampling |
| `POTCAR.spec` | Pseudopotential specification |
| `submit.sh` | Example SLURM submission script |

## Workflow Type

Bulk structural relaxation:
- optimize ionic positions and lattice degrees of freedom
- use conservative relaxation settings
- generate a relaxed structure suitable for basic sanity checks or follow-on
  static calculations

## Operational Context

This example is written for the current BMD Lab VASP-on-SLURM workflow. The
submission script records the cluster partition, account, module, and launch
conventions used when the example was curated. Those details may need updating
when university-managed cluster policy changes.

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

## Limitations

- This is an onboarding and workflow-check example, not a universal silicon
  convergence study.
- The committed `POTCAR.spec` records pseudopotential requirements, but the
  actual licensed `POTCAR` must be generated in the appropriate computational
  environment.
