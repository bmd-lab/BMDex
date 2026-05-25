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

from _datasets import load_representative_84


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

    oxidation_states = load_representative_84()

    cations = []

    for element, charges in oxidation_states.items():

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
