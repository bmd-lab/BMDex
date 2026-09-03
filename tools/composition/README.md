# Composition Tools

Private BMD Lab computational assets for formula generation, oxidation-state
reasoning, and chemically constrained candidate screening.

Current entries include:

- `electroneutrality/` charge-balance-based composition generation utilities
  - `generate_binary_oxides.py`
  - `generate_ternaries.py`
- `context_producer.py` read-only JSON composition-context evidence producer

## Composition Context Producer

`context_producer.py` is the first narrow BMDex-owned machine-readable producer
for local composition context. It reads one JSON object from stdin and writes
one compact JSON evidence fragment to stdout:

```bash
printf '{"formula":"MnCu5"}' | python -B -m tools.composition.context_producer
```

The `-B` flag prevents Python bytecode cache writes during no-mutation use.

For scientific evidence, the producer reads only:

- `datasets/element_abundances/earth-abundance.yaml`
- `datasets/element_charges/oxidation_states_84.yaml`

For repository provenance, it also runs fixed local Git commands. It performs
no network access, credential lookup, external API call, cluster operation, or
scientific-data write.

It reports element-level crustal abundance records in `mg/kg` and
representative oxidation-state entries. These records are contextual evidence
only. They do not establish compound viability, sustainability, oxidation
states, charge balance, stability, existence, or synthesizability.
