# 84 Representative Oxidation States

This dataset contains the 84 representative oxidation states proposed in:

> Ding, Y.; Kumagai, Y.; Oba, F.; Burton, L. A.
> *Data-Mining Element Charges in Inorganic Materials*.
> J. Phys. Chem. Lett. 2020, 11, 8264–8267.
> DOI: 10.1021/acs.jpclett.0c02072

The oxidation states were obtained by data-mining approximately:
- 169,800 ICSD entries
- 1,698,849 oxidation-state assignments

The goal was to identify a reduced oxidation-state set that:
- captures the majority of experimentally reported inorganic chemistry
- minimizes combinatorial explosion in materials discovery workflows
- preserves chemically plausible composition generation

The resulting 84 oxidation states recover:
- >90% of oxidation-state assignments observed in the ICSD.

## Scientific Motivation

The dataset is intended to support:
- electroneutral composition generation
- computational materials discovery
- heuristic chemical screening
- combinatorial reduction of candidate materials

The reduced oxidation-state set represents an intentional trade-off between:
- chemical completeness
- and computational tractability.

## Important Limitations

The dataset does not:
- enumerate all known oxidation states
- guarantee thermodynamic stability
- guarantee synthesizability
- replace detailed chemical validation

The oxidation states are intended as:
- representative
- probable
- and practically useful
for inorganic materials workflows.

## Repository Context

This dataset derives from the earlier:
- `electroneutral_match`
workflow developed within the BMD Lab.

Within BMDex, the dataset serves as:
- a reusable compositional reasoning resource
- a foundation for electroneutral composition generation
- a bridge between oxidation-state heuristics and computational materials workflows

## References

See:
- the associated publication
- the original `electroneutral_match` repository
- the ICSD-derived analysis described in the manuscript
