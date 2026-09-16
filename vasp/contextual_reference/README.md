# VASP Contextual Reference Knowledge

This directory contains curated BMDex reference knowledge for interpreting VASP
calculation observations.

BMDex provides contextual reference evidence. BMD Agent is responsible for
combining that reference context with observed calculation evidence and making
diagnostic assessments. BMD Compute remains the authority for executable
calculation methodology and VASP input generation in the core data-generation
pipeline.

Records in `records/` are structured JSON documents intended for deterministic
read-only retrieval by BMDex tools. They are not VASP calculation outputs, and
they should not encode remediation policies or BMD Compute runtime behavior.
