#! /usr/bin/env python3

"""
Generate electroneutral ternary compositions using
the representative oxidation-state dataset.

Examples:
    LiFeO2
    SrTiO3
    BaZrO3
"""

from itertools import combinations
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


def reduce_numbers(numbers):

    divisor = reduce(gcd, numbers)

    return [x // divisor for x in numbers]


def format_formula(elements, counts):

    formula = ""

    for element, count in zip(elements, counts):

        formula += element

        if count > 1:
            formula += str(count)

    return formula


def solve_stoichiometry(charges):

    q1, q2, q3 = charges

    limit = 12

    for a in range(1, limit):
        for b in range(1, limit):
            for c in range(1, limit):

                if a*q1 + b*q2 + c*q3 == 0:

                    return reduce_numbers([a, b, c])

    return None


def generate_ternaries():

    cations = []

    for element, charges in OXIDATION_STATES.items():

        if element == "O":
            continue

        for charge in charges:

            if charge > 0:
                cations.append((element, charge))

    formulas = set()

    for (el1, q1), (el2, q2) in combinations(cations, 2):

        charges = [q1, q2, -2]

        stoich = solve_stoichiometry(charges)

        if stoich:

            elements = [el1, el2, "O"]

            formula = format_formula(elements, stoich)

            formulas.add(formula)

    return sorted(formulas)


if __name__ == "__main__":

    print("Electroneutral ternary oxides:\n")

    for formula in generate_ternaries():
        print(formula)
