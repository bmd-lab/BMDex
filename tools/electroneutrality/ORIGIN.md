# Origin and Provenance

This module derives from the earlier:

- `electroneutral_match`
repository developed within the BMD Lab:
https://github.com/bmd-lab/electroneutral_match

The original project implemented electroneutral composition generation using a curated set of representative oxidation states.

The methodology and oxidation-state selection were published in:

> Ding, Y.; Kumagai, Y.; Oba, F.; Burton, L. A.
> *Data-Mining Element Charges in Inorganic Materials*.
> J. Phys. Chem. Lett. 2020, 11, 8264–8267.
> DOI: 10.1021/acs.jpclett.0c02072

The original workflow explored:
- oxidation-state assignment statistics in the ICSD
- reduced representative oxidation-state sets
- combinatorial composition generation
- electroneutrality-constrained materials discovery

## Migration into BMDex

BMDex reorganizes the original project into:
- curated oxidation-state datasets
- reusable compositional reasoning tools
- documented workflows
- maintainable repository structure
- future pymatgen interoperability

The goal is to preserve:
- scientific provenance
- institutional knowledge
- reproducibility
- and long-term maintainability.

## Notes

The oxidation-state dataset included in BMDex reflects the representative 84 oxidation states proposed in the associated publication and is intentionally reduced relative to exhaustive oxidation-state references.
