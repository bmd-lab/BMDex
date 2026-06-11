import os
from pathlib import Path
from get_abundant_prototypes import compare_frameworks
from pymatgen.core.composition import Composition


# ----------------------------------------------------------------------
# User settings
# ----------------------------------------------------------------------

MAIN_FOLDER = "path/to/dir"
MIN_AMOUNT = 2
ABUNDANCE_FILE = (
    Path(__file__).resolve().parents[2]
    / "datasets"
    / "element_abundances"
    / "earth-abundance.yaml"
)
SHEET_NAME = None

def process_main_folder(main_dir: str, min_amount: int, abundance_file_name: str, sheet_name=None):
    """
    Processes each subdirectory in the main folder using the process_subdirectory function.

    Parameters:
        main_dir (str): Path to the main folder containing subdirectories.
        min_amount: minimal amount of occurrences to add to the list.
    """

    for subdir in os.listdir(main_dir):
        structures = []
        subdir_path = os.path.join(main_dir, subdir)
        if os.path.isdir(subdir_path):
            print(f"Processing {subdir_path}...")
            structures = compare_frameworks(subdir_path, abundance_file_name, sheet_name)
            # Write the unique structures information to a text file in the subdirectory
            output_file_path = os.path.join(subdir_path, "unique_structures.txt")
            with open(output_file_path, "w") as output_file:
                for rep_structure, rep_file, rep_abundance, abundant_structure, rep_volume, rep_count in structures:
                    if rep_count >= min_amount:
                        # Get the orientation matrix
                        orientation_matrix = rep_structure.lattice.matrix
                        # Format the orientation matrix as a string
                        orientation_matrix_str = "\n".join(
                            ["\t".join(f"{value:.2f}" for value in row) for row in orientation_matrix])
                        # Get chemical formula of the material
                        formula = abundant_structure.composition.formula
                        comp = Composition(formula)
                        chem_not = comp.reduced_formula
                        space_group_symbol, space_group_number = rep_structure.get_space_group_info()
                        atoms_coordinates = []
                        for site in abundant_structure:
                            species = site.species_string  # Element symbol
                            frac_coords = site.frac_coords  # Fractional coordinates
                            atoms_coordinates.append((species, frac_coords))
                        atoms_coordinates_str = "\n".join("".join(f"{atom}\t{location}") for atom, location in atoms_coordinates)
                        # Write details to the text file
                        output_file.write(f"Filename: {os.path.basename(rep_file)}  {chem_not}  appeared: {rep_count} times"
                                          f"\nSpace Group: {space_group_symbol} no. {space_group_number}\n"
                                          f"Orientation Matrix:\n{orientation_matrix_str}\nAtoms Locations:\n{atoms_coordinates_str}\n\n")


if __name__ == "__main__":
    process_main_folder(MAIN_FOLDER, MIN_AMOUNT, ABUNDANCE_FILE, SHEET_NAME)
    print(f"Done processing all folders in {MAIN_FOLDER}.")
