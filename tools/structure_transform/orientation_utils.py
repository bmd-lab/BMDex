"""
Orientation utilities for BMDex structure workflows.
"""


def describe_orientation(miller_index):
    """
    Return a human-readable orientation string.
    """

    return (
        f"Surface orientation: "
        f"({miller_index[0]} "
        f"{miller_index[1]} "
        f"{miller_index[2]})"
    )
