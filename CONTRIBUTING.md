# Contributing to BMDex

BMDex is maintained for materials-science researchers. Contributions should be
focused, scientifically clear, and easy for another student to review and
reuse.

## Basic Workflow

1. Clone BMDex and create a Python environment as described in `README.md`.
2. Create a focused branch from the current `main` branch.
3. Make one coherent change and update the nearest relevant documentation.
4. Run the full test suite and any checks relevant to the changed tool or data.
5. Commit and push the branch.
6. Open a pull request that explains the scientific purpose, provenance, tests,
   and limitations of the change.

Keep generated calculation output and active project files outside the
repository. Preserve existing schemas and producer contracts unless changing
them is the explicit purpose of the contribution and the change includes
contract tests.

## Scientific Knowledge and Data

For new or changed scientific knowledge, data, or evidence:

- provide a clear source, citation, and description of how the material was
  obtained or transformed;
- distinguish original BMD work from externally sourced material;
- record units, assumptions, validation status, and important limitations near
  the data;
- prefer machine-readable factual data with explicit source attribution when
  that form serves a concrete workflow;
- do not copy substantial copyrighted prose or tables merely because they are
  academically useful; and
- confirm redistribution permission before adding externally sourced datasets.

Source attribution remains necessary even when factual values are represented
under the repository's data structures. The repository license does not
relicense a cited publication or other third-party material.

## Never Commit

- credentials, API keys, access tokens, or passwords;
- private SSH keys or other private key material;
- `POTCAR` files or licensed VASP potential contents;
- proprietary or licensed raw datasets without redistribution permission;
- private or unpublished research and collaborator material unless publication
  is explicitly approved;
- personal, student, or participant records; or
- deployment-local secrets or configuration.

`.gitignore` is only a guardrail. Review staged files before every commit. If a
credential is committed, report it immediately so it can be revoked and the
exposure handled; deleting it in a later commit is not sufficient.
