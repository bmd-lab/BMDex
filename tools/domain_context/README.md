# Domain Context Tools

This directory contains read-only producers for curated BMDex contextual
reference knowledge.

The current producer queries local BMDex JSON records and writes JSON-safe
contextual reference evidence:

```bash
printf '{"query":{"code":"VASP","calculation_family":"hybrid_functional","functional":"HSE06","electronic_algorithm":"Damped","topic":"electronic_iteration_behavior"}}' | python -B -m tools.domain_context.query
```

BMDex provides reference context. BMD Agent performs evidence synthesis and
diagnosis. BMD Compute owns executable calculation methodology for the core
VASP data-generation pipeline.
