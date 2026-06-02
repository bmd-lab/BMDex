# Repository Access Model

BMDex is intended to be accessed in stages as students become more comfortable
with the group's computational environment.

## Access Path

1. Public tutorials
2. Private GitHub repository and website
3. Console, SSH, and cluster-side repository checkout
4. Codex-assisted curation for users comfortable with terminal workflows

The public tutorials repository remains the broad pedagogical entry point.
BMDex is the private operational layer: standards, templates, runnable tools,
datasets, examples, and institutional workflow knowledge.

## Audience Assumptions

Most students onboarding into BMDex are materials scientists. They may learn
Python, VASP, pymatgen, SLURM, and computational materials science before they
are comfortable with Git, Codex, metadata schemas, or repository governance.

BMDex should therefore expose the simplest useful researcher workflow first:

- find a relevant example, template, or tool
- copy it into a calculation or screening folder when appropriate
- edit clear user settings
- run it on the cluster
- inspect scientific outputs
- ask for review before treating results as production data

Git, metadata sidecars, validation scripts, and Codex-assisted curation are
important for repository maintainability, but they should not be prerequisites
for running an existing BMDex tool.

## Intended Execution Model

Codex should usually operate on a laptop or workstation checkout of BMDex.
Cluster execution should happen from a normal git checkout on the cluster.

Preferred workflow:

1. Curate or edit BMDex locally.
2. Commit and push changes.
3. Pull BMDex on the cluster.
4. Run or copy tools from the cluster-side checkout inside the real VASP,
   SLURM, pymatgen, and filesystem environment.

Do not assume Codex is installed on the cluster. The cluster should only need:

- git access to BMDex
- the local scientific software stack
- the BMDex tools, templates, and standards pulled from version control

## Student-Facing Access Levels

### Public Tutorials

Use the tutorials repository for conceptual onboarding, first exposure to VASP,
SLURM, pymatgen, and basic cluster practice.

### Private GitHub Website

Use the private GitHub repository or website as the first BMDex entry point for
students. This should expose curated standards and runnable examples without
requiring students to immediately modify the repository.

Student-facing pages should avoid assuming prior Git or metadata knowledge.
They should provide direct commands, expected files, and clear next actions.

### Cluster Checkout

Once students can use SSH and the terminal, they should clone or pull BMDex on
the cluster and run tools from that checkout.

Cluster-side usage should look like normal research computing:

```bash
git pull
python3 tools/hpc/vasp_status.py --root my-screening-run
cp slurm/templates/submit_vasp.sbatch my-calc/submit.sbatch
```

### Codex-Assisted Curation

Codex is appropriate when users are ready to work at the console and understand
the repository workflow. It should help curate, standardize, review, and extend
BMDex. It should not be required for a student to run an existing tool.

For most new students, Codex should be introduced after they can already use
the terminal, navigate files, run Python scripts, and submit cluster jobs.

## Design Implications

BMDex should:

- keep tools directly runnable from a cluster checkout
- avoid requiring package installation for simple operational scripts
- keep templates copyable into calculation folders
- document cluster assumptions separately from laptop editing assumptions
- preserve public tutorials as pedagogy and BMDex as operational knowledge
- keep metadata helpful to maintainers without making it the first thing a
  student must understand

Tools may be importable where useful, but the primary researcher interface
should remain shallow, visible, and practical.
