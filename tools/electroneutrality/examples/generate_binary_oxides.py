#! /usr/bin/env python3

"""
Generate electroneutral binary oxides using the
84 representative oxidation states.

Examples:
    MgO
    TiO2
    Fe2O3
"""

from collections import Counter
from functools import reduce
from math import gcd


OXIDATION_STATES = {
    "Li": [1],
    "Na": [1],
    "K": [1],
    "Mg": [2],
    "Ca": [2],
    "Sr": [2],
    "Ba": [2],
    "Al": [3],
    "Sc": [3],
    "Y": [3],
    "Ti": [4],
    "Zr": [4],
    "Hf": [4],
    "V": [5],
    "Nb": [5],
    "Ta": [5],
    "Cr": [3],
    "Mn": [2],
    "Fe": [2, 3],
    "Co": [2],
    "Ni": [2],
    "Cu": [1, 2],
    "Zn": [2],
    "Ga": [3],
    "Ge": [4],
    "Sn": [2, 4],
    "Pb": [2],
    "Bi": [3],
    "O": [-2],
}


def reduce_formula(counts):

    values = list(counts.values())
    divisor = reduce(gcd, values)

    return {k: v // divisor for k, v in counts.items()}


def format_formula(counts):

    formula = ""

    for element in sorted(counts.keys()):

        formula += element

        if counts[element] > 1:
            formula += str(counts[element])

    return formula


def neutral_formula(cation, cation_charge):

    oxygen_charge = -2

    total_positive = abs(cation_charge)
    total_negative = abs(oxygen_charge)

    lcm = total_positive * total_negative // gcd(
        total_positive,
        total_negative
    )

    n_cation = lcm // total_positive
    n_oxygen = lcm // total_negative

    counts = {
        cation: n_cation,
        "O": n_oxygen
    }

    reduced = reduce_formula(counts)

    return format_formula(reduced)


def generate_binary_oxides():

    formulas = set()

    for element, charges in OXIDATION_STATES.items():

        if element == "O":
            continue

        for charge in charges:

            if charge > 0:

                formula = neutral_formula(element, charge)

                formulas.add(formula)

    return sorted(formulas)


if __name__ == "__main__":

    print("Electroneutral binary oxides:\n")

    for formula in generate_binary_oxides():
        print(formula)
