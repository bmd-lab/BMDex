---
record_id: vasp.validation.si_hse06_band_structure_powerslurm_2026_08_21
record_type: computational_validation_evidence
title: Crystalline Si HSE06 band structure PowerSLURM validation evidence
benchmark_system: crystalline Si
formula: Si
evidence_status: powerslurm_validation_established
methodology_status: evidence_item_only
validated_on_powerslurm: established
formal_human_scientific_review: not_recorded
adopted_bmd_standard: false
deprecated: false
execution_date: "2026-08-21"
workflow_identity:
  requested_workflow:
    - PBE Geometry Optimisation
    - HSE06 Static Energy
    - HSE06 Band Structure
  final_stage: HSE06 Band Structure
  final_stage_path: "/bmd-db/guest/flows/vasp_run_custom_workflow-20260821-094759/stage_03"
producer_provenance:
  system: BMD Compute
  base_commit: "05eacdb8e56b089f7c98bdd968561fceb2bbcd19"
  submission_checkout_state: dirty
  dirty_diff_preserved: false
  submission_json: "/bmd-db/guest/flows/vasp_run_custom_workflow-20260821-094759/submission.json"
  flow_root: "/bmd-db/guest/flows/vasp_run_custom_workflow-20260821-094759"
powerslurm_job:
  job_id: "20893681"
  state: COMPLETED
  exit: "0:0"
  elapsed: "02:48:37"
  start: "2026-08-21T12:14:10"
  end: "2026-08-21T15:02:47"
  partition: leeburton-pool
  account: power-leeburton-users_v2
  requested_resources:
    nodes: 1
    tasks: 24
    memory_gb: 128
    walltime_h: 72
environment:
  VASP_CMD: "mpirun -n $SLURM_NTASKS vasp_std"
  PMG_VASP_PSP_DIR: "/bmd-db/potcars"
  python: "3.12.13"
  atomate2: "0.1.5"
  jobflow: "0.1.19"
  custodian: "2025.12.14"
  pymatgen_runtime_version: unavailable
  vasp_version: not_recorded
jobflow_uuids:
  stage_01: "64210872-5626-40c7-a7eb-79f7e49272ba"
  stage_02: "328290de-b493-4d39-a4c7-238eb9055720"
  stage_03: "48f52369-d3b9-40b5-9a9f-a87bae6d007f"
stage_directory_observation:
  observed_present:
    - stage_01
    - stage_02
    - stage_03
  inference_from_presence: no_additional_inference
observed_final_artifacts:
  - CONTCAR
  - OUTCAR
  - vasprun.xml
  - KPOINTS
  - DOSCAR
pymatgen_parse_observation:
  source: BMD Agent independent parse of final-stage VASP artifacts
  bmd_agent_observer: not_recorded
  formula: Si
  final_energy_ev: -12.575253
  energy_per_atom_ev: -6.287627
  electronic_convergence: true
  band_gap_ev: 1.1913
  band_path_kpoints: 310
  bands: 24
human_ui_corroboration:
  source: BMD Compute Results UI
  durable_machine_artifact: false
  observation: matching numerical values and Band Structure available
review_and_adoption:
  human_scientific_reviewer: not_recorded
  human_scientific_review_date: not_recorded
  scientific_review_status: not_recorded
  adoption_authority: not_recorded
  adoption_date: not_recorded
  adoption_status: not_adopted
limitations:
  - The BMD Compute checkout was dirty and the exact dirty paths/content/diff were not preserved.
  - This evidence covers one crystalline-Si validation run, not arbitrary materials.
  - Requested resources are execution context, not convergence recommendations.
  - Large VASP artifacts are referenced by path and are not copied into Git.
  - Pymatgen runtime version was not successfully recorded.
  - Formal human scientific review is not yet recorded.
  - This is not an adopted BMD methodology or standard.
---

# Crystalline Si HSE06 Band Structure PowerSLURM Validation Evidence

This record preserves evidence from one real computational validation
experiment: a crystalline-Si BMD Compute workflow that ran through TAU
PowerSLURM and produced an independently parseable HSE06 band structure.

This is an evidence item. It is not the definitive BMD HSE06 band-structure
methodology specification, and it does not record adoption as a BMD standard.

## What This Evidence Supports

This evidence supports the following limited claim:

> BMD Compute's PBE Geometry Optimisation -> HSE06 Static Energy -> HSE06 Band
> Structure pathway executed end-to-end through BMD Compute / atomate2 / VASP
> on TAU PowerSLURM for crystalline Si, completed successfully, established
> electronic convergence of the final-stage VASP output through independently
> reconstructed evidence, and produced a band structure independently parseable
> with pymatgen.

For this Si benchmark, PowerSLURM validation is recorded as established.

## What This Evidence Does Not Establish

This record does not establish:

- adopted BMD standard status;
- universal validation of HSE06 band-structure methodology;
- convergence validation for arbitrary materials;
- experimental validation;
- literature validation;
- formal human scientific review;
- that the requested resources are recommended resources for future runs.

Future BMD methodology may cite this record as supporting evidence, but should
also record the deliberate methodology choices, scope, convergence expectations,
review status, and adoption decision separately.

## Evidence Provenance

Producer provenance:

- BMD Compute base commit:
  `05eacdb8e56b089f7c98bdd968561fceb2bbcd19`
- submission checkout state: `dirty`
- submission JSON:
  `/bmd-db/guest/flows/vasp_run_custom_workflow-20260821-094759/submission.json`
- flow root:
  `/bmd-db/guest/flows/vasp_run_custom_workflow-20260821-094759`

Important reproducibility limitation: the checkout was dirty and the exact
dirty paths, content, and diff were not preserved. This limits reconstruction
of the precise producer state even though the base commit is recorded.

## Workflow

Requested workflow:

1. PBE Geometry Optimisation
2. HSE06 Static Energy
3. HSE06 Band Structure

Jobflow UUIDs:

- stage 01: `64210872-5626-40c7-a7eb-79f7e49272ba`
- stage 02: `328290de-b493-4d39-a4c7-238eb9055720`
- stage 03: `48f52369-d3b9-40b5-9a9f-a87bae6d007f`

Stage directory observation:

- all producer-declared stage directories were observed present:
  `stage_01`, `stage_02`, and `stage_03`.

No additional inference is made from their presence.

Final stage path:

```text
/bmd-db/guest/flows/vasp_run_custom_workflow-20260821-094759/stage_03
```

## PowerSLURM Observation

Scheduler observation:

- job ID: `20893681`
- state: `COMPLETED`
- exit: `0:0`
- elapsed: `02:48:37`
- start: `2026-08-21T12:14:10`
- end: `2026-08-21T15:02:47`
- partition: `leeburton-pool`
- account: `power-leeburton-users_v2`

Requested resources:

- nodes: 1
- tasks: 24
- memory: 128 GB
- walltime: 72 h

These resources are execution context for this validation run. They are not a
convergence recommendation or general resource policy.

## Execution Environment

Recorded environment:

- `VASP_CMD=mpirun -n $SLURM_NTASKS vasp_std`
- `PMG_VASP_PSP_DIR=/bmd-db/potcars`
- Python 3.12.13
- atomate2 0.1.5
- jobflow 0.1.19
- custodian 2025.12.14
- pymatgen runtime version: unavailable / not successfully recorded
- VASP version: not recorded

## Artifact Observation

Observed final-stage artifacts:

- `CONTCAR`
- `OUTCAR`
- `vasprun.xml`
- `KPOINTS`
- `DOSCAR`

Large VASP artifacts are intentionally not copied into Git. This record
preserves their external location and parsed summary, not their full contents.

## Pymatgen-Derived Observation

BMD Agent independently parsed the actual final-stage VASP artifacts with
pymatgen and recovered:

- formula: `Si`
- final energy: `-12.575253 eV`
- energy per atom: `-6.287627 eV/atom`
- electronic convergence: `true`
- band gap: `1.1913 eV`
- band-path k-points: `310`
- bands: `24`

These values establish that the final HSE06 band-structure output was
independently parseable and internally available for downstream inspection.

The BMD Agent version or commit responsible for the successful `inspect-run`
evidence reconstruction is not recorded in the available evidence and is not
inferred from unrelated current repository state.

## Human/UI Observation

BMD Compute's Results UI also displayed matching numerical values and
reported Band Structure available.

BMD Compute does not currently persist that parsed UI result summary as a
durable producer artifact, so this is recorded as human-observed UI
corroboration rather than a durable machine comparison.

## Human Scientific Review And Adoption

Formal human scientific review is not yet recorded.

Adoption as a BMD methodology or group standard is not recorded.

No reviewer, approver, PI adoption decision, review date, or adoption date is
invented here.

## Related Documentation Drift Observations

BMDwiki is explanatory and student-contributed documentation. It is not
authoritative over BMD Compute or BMDex. The older
`Calculating-Band-Structure-in-VASP.md` tutorial differs from current BMD
Compute practice and this operational evidence in several places.

High-signal drift candidates:

- wiki `ENCUT = 520 eV` versus current BMD Compute HSE static/band floor of
  `620 eV`;
- wiki `SIGMA = 0.03` versus current BMD Compute HSE band value of `0.01`;
- both use line density `40`;
- BMD Compute additionally uses reciprocal density `64`;
- the wiki describes a manual HSE/zero-weight path workflow, while BMD Compute
  uses atomate2 HSEBS machinery;
- the wiki, current BMDex operational guidance, and this evidence record
  contain historical/current POTCAR path differences, including
  `/bmd-db/lee/potcars` in BMDex guidance and `/bmd-db/potcars` in this run.

These are documentation/history drift observations. They are not treated here
as competing methodology claims, and this record does not update BMDwiki.

## Open Follow-Up Items

- Preserve or regenerate a clean BMD Compute provenance snapshot for future
  validation runs.
- Record the VASP version and pymatgen runtime version in future validation
  evidence.
- Preserve a durable parsed result summary from BMD Compute when available.
- Complete human scientific review if this evidence will support a future BMD
  HSE06 band-structure methodology.
- Decide separately whether any HSE06 settings from the implementation should
  become deliberate BMD methodology choices.
