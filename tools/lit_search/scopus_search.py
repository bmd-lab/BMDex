#!/usr/bin/env python3

"""
Search Scopus for a list of chemical formulae.

Input
-----
A plain-text file containing one chemical formula per line.

Output
------
A CSV file containing:

    formula,papers

Existing results are detected automatically, allowing an interrupted
search to be restarted without repeating completed queries.

The formula is searched exactly as supplied using:

    TITLE-ABS-KEY("FORMULA")

No formula normalization or reordering is performed.
"""

from pathlib import Path
import csv
import time
import traceback

from pybliometrics.scopus import ScopusSearch


# ----------------------------------------------------------------------
# User settings
# ----------------------------------------------------------------------

INPUT_FILE = "formulae.txt"
OUTPUT_FILE = "scopus_counts.csv"

# Maximum number of new queries during this run.
# Set to None to process the entire input file.
MAX_QUERIES = 20000

# Pause between successful queries.
SLEEP_TIME = 0.1

# Print progress every N successful queries.
REPORT_EVERY = 100


# ----------------------------------------------------------------------
# Read formulae
# ----------------------------------------------------------------------

def read_formulae(filename):
    """
    Read formulae from a text file.

    Blank lines are ignored. Formulae are returned exactly as written
    apart from surrounding whitespace.
    """

    formulae = []

    with open(filename) as f:
        for line in f:
            formula = line.strip()

            if formula:
                formulae.append(formula)

    return formulae


# ----------------------------------------------------------------------
# Read completed searches
# ----------------------------------------------------------------------

def read_completed(filename):
    """
    Read formulae already present in an existing output CSV.

    This allows an interrupted search to be restarted without repeating
    completed queries.

    Rows marked ERROR are not considered complete and will therefore be
    retried on the next run.
    """

    completed = set()

    if not Path(filename).exists():
        return completed

    with open(filename, newline="") as f:
        reader = csv.reader(f)

        # Skip header
        next(reader, None)

        for row in reader:

            if len(row) < 2:
                continue

            formula = row[0].strip()
            result = row[1].strip()

            if formula and result != "ERROR":
                completed.add(formula)

    return completed


# ----------------------------------------------------------------------
# Scopus search
# ----------------------------------------------------------------------

def search_formula(formula):
    """
    Search Scopus for a chemical formula.

    The formula is quoted so that Scopus searches for the compact
    formula string rather than interpreting its components as
    independent search terms.
    """

    query = f'TITLE-ABS-KEY("{formula}")'

    search = ScopusSearch(
        query,
        download=False,
    )

    count = search.get_results_size()

    return count, search


# ----------------------------------------------------------------------
# Main search
# ----------------------------------------------------------------------

def run_search(input_file, output_file):
    """
    Search all formulae in input_file and write publication counts
    to output_file.
    """

    input_path = Path(input_file)
    output_path = Path(output_file)

    if not input_path.exists():
        raise FileNotFoundError(
            f"Input file not found: {input_path}"
        )

    formulae = read_formulae(input_path)
    completed = read_completed(output_path)

    print(f"Input formulae:     {len(formulae)}")
    print(f"Already completed: {len(completed)}")

    remaining = sum(
        formula not in completed
        for formula in formulae
    )

    print(f"Remaining:          {remaining}")
    print()

    # Determine whether the CSV header needs to be written.
    new_file = (
        not output_path.exists()
        or output_path.stat().st_size == 0
    )

    queries_done = 0

    with open(output_path, "a", newline="") as fout:

        writer = csv.writer(fout)

        if new_file:
            writer.writerow(["formula", "papers"])
            fout.flush()

        for formula in formulae:

            # ----------------------------------------------------------
            # Skip completed formulae
            # ----------------------------------------------------------

            if formula in completed:
                continue

            # ----------------------------------------------------------
            # Stop after requested number of new queries
            # ----------------------------------------------------------

            if (
                MAX_QUERIES is not None
                and queries_done >= MAX_QUERIES
            ):
                print()
                print(
                    f"Reached MAX_QUERIES = {MAX_QUERIES}."
                )
                break

            # ----------------------------------------------------------
            # Query Scopus
            # ----------------------------------------------------------

            try:

                count, search = search_formula(formula)

                writer.writerow([formula, count])

                # Write each result immediately so that progress is
                # preserved if the search is interrupted.
                fout.flush()

                completed.add(formula)
                queries_done += 1

                # ------------------------------------------------------
                # Progress report
                # ------------------------------------------------------

                if (
                    REPORT_EVERY
                    and queries_done % REPORT_EVERY == 0
                ):

                    remaining_quota = (
                        search.get_key_remaining_quota()
                    )

                    print(
                        f"{queries_done:6d}   "
                        f"{formula:20s}   "
                        f"{count:8d}   "
                        f"Remaining quota: {remaining_quota}",
                        flush=True,
                    )

                # ------------------------------------------------------
                # Small delay between API requests
                # ------------------------------------------------------

                if SLEEP_TIME:
                    time.sleep(SLEEP_TIME)

            # ----------------------------------------------------------
            # Safe interruption
            # ----------------------------------------------------------

            except KeyboardInterrupt:

                print()
                print("Search stopped by user.")
                print(
                    f"{queries_done} new results were written "
                    f"to {output_path}."
                )

                raise

            # ----------------------------------------------------------
            # API/query error
            # ----------------------------------------------------------

            except Exception as error:

                writer.writerow([formula, "ERROR"])
                fout.flush()

                print()
                print(f"Error querying {formula}")
                print(repr(error))

                traceback.print_exc()

                # Give the API some time before continuing.
                time.sleep(5)

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    print()
    print("Finished.")
    print(f"New queries: {queries_done}")
    print(f"Output:      {output_path}")


# ----------------------------------------------------------------------
# Run
# ----------------------------------------------------------------------

if __name__ == "__main__":

    run_search(
        INPUT_FILE,
        OUTPUT_FILE,
    )
