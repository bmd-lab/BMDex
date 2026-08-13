#!/usr/bin/env python3

"""
Check the Scopus API connection and current quota.

This script performs a small test search and reports:

    - whether the Scopus search succeeded
    - the number of results returned
    - the remaining API quota
    - the quota reset time

Scopus API credentials are read from the user's pybliometrics
configuration. No API key is stored in this script.
"""

from pybliometrics.scopus import ScopusSearch


# ----------------------------------------------------------------------
# Test query
# ----------------------------------------------------------------------

TEST_FORMULA = "CaTiO3"


# ----------------------------------------------------------------------
# Check Scopus
# ----------------------------------------------------------------------

def check_quota():
    """Run a test Scopus query and display API quota information."""

    query = f'TITLE-ABS-KEY("{TEST_FORMULA}")'

    print("Checking Scopus API...")
    print(f"Query: {query}")
    print()

    try:

        search = ScopusSearch(
            query,
            download=False,
        )

        results = search.get_results_size()
        remaining = search.get_key_remaining_quota()
        reset_time = search.get_key_reset_time()

        print("Scopus API connection successful.")
        print()
        print(f"Test formula:    {TEST_FORMULA}")
        print(f"Results:         {results}")
        print(f"Remaining quota: {remaining}")
        print(f"Reset time:      {reset_time}")

    except Exception as error:

        print("Scopus API check failed.")
        print()
        print(f"{type(error).__name__}: {error}")

        raise


# ----------------------------------------------------------------------
# Run
# ----------------------------------------------------------------------

if __name__ == "__main__":

    check_quota()