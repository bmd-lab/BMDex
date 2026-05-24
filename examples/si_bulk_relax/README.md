# Silicon Bulk Relaxation Example

This example demonstrates a minimal bulk silicon structural relaxation workflow using VASP.

The purpose of this example is to provide:
- a validated reference calculation
- a canonical file structure
- a minimal reproducible workflow
- an onboarding example for new group members

## Scientific Context

System:
- bulk crystalline silicon
- diamond cubic structure

Calculation type:
- structural relaxation

Typical goals:
- lattice optimization
- energy minimization
- workflow validation
- benchmarking and testing

## Included Files

| File | Purpose |
|---|---|
| POSCAR | Initial silicon structure |
| INCAR | Relaxation settings |
| KPOINTS | k-point sampling |
| POTCAR.spec | Pseudopotential specification |
| submit.sbatch | Example SLURM submission script |

## Expected Workflow

1. Prepare input files
2. Submit calculation to cluster
3. Monitor convergence
4. Verify successful relaxation
5. Inspect final structure and energy

## Expected Outputs

Typical outputs include:
- relaxed structure
- final total energy
- OUTCAR
- vasprun.xml
- CONTCAR

## Validation Checks

Successful calculations should:
- converge electronically
- converge ionically
- produce reasonable Si-Si bond lengths
- preserve expected crystal symmetry

## Notes

This example is intentionally minimal and conservative.

It should function as a stable reference workflow and onboarding example rather than a highly optimized production workflow.
