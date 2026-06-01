# Silicon Bulk Relaxation Example

This example is a minimal VASP structural relaxation for diamond-cubic silicon.
It is intended as a small, readable reference calculation for onboarding,
workflow checks, and comparison against future VASP examples.

The runnable inputs and metadata are kept in this directory so new students
can inspect the full example in one place.

## Included Files

| File | Purpose |
|---|---|
| `POSCAR` | Initial silicon structure |
| `INCAR` | Relaxation settings |
| `KPOINTS` | Brillouin-zone sampling |
| `POTCAR.spec` | Pseudopotential specification |
| `submit.sbatch` | Example SLURM submission script |
| `bmdex.yaml` | Structured metadata for curation |

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
