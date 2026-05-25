# Silicon Bulk Relaxation

This example demonstrates a minimal bulk silicon structural relaxation workflow
using VASP.

Canonical metadata:
- `bmdex.yaml`

The example is intended to serve as:
- a canonical onboarding workflow
- a reference calculation
- a reference for future workflows
- a reference for file organization and submission conventions

## Scientific Context

System:
- crystalline silicon
- diamond cubic structure

Calculation type:
- structural relaxation

Typical goals:
- geometry optimization
- lattice relaxation
- workflow validation
- benchmarking and testing

## Included Files

| File | Purpose |
|---|---|
| POSCAR | Initial silicon crystal structure |
| INCAR | Relaxation parameters |
| KPOINTS | Brillouin-zone sampling |
| POTCAR.spec | Pseudopotential specification |
| submit.sbatch | Example SLURM submission script |

## Uses

- `method.vasp.input_standards`
- `template.vasp.incar_relax`
- `template.vasp.kpoints_example`
- `template.vasp.potcar_spec`
- `template.slurm.submit_vasp`

## Expected Workflow

1. Prepare VASP inputs
2. Generate POTCAR from `POTCAR.spec`
3. Submit calculation through SLURM
4. Monitor convergence
5. Verify successful relaxation
6. Inspect final structure and energy

## Expected Outputs

Typical outputs include:
- CONTCAR
- OUTCAR
- vasprun.xml
- final total energy
- relaxed lattice parameters

## Validation Checks

Successful calculations should:
- converge electronically
- converge ionically
- preserve expected silicon crystal symmetry
- produce physically reasonable Si-Si bond lengths

## Notes

This workflow intentionally prioritizes:
- clarity
- reproducibility
- conservative defaults
- maintainability

It is intended as a stable reference workflow rather than a highly optimized
production calculation.
