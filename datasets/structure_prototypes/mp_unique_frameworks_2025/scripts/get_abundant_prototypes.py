import os
from pymatgen.core import Structure
from pymatgen.analysis.structure_matcher import StructureMatcher, FrameworkComparator
from abundance_rank import CompoundAbundanceScorer


def compare_frameworks(dir_path, abundance_excel_path, sheet_name=None):
    """
    Processes all .cif files in a single subdirectory, keeping the representative
    file with the largest volume for each unique framework and saving them in the same subdirectory.

    Parameters:
        dir_path (str): Path to the subdirectory to process.
    """
    unique_structures = []  # List to store tuples of (structure, file_path, cell_volume, count)

    # Initialize the structure matcher
    matcher = StructureMatcher(comparator=FrameworkComparator())

    scorer = CompoundAbundanceScorer(abundance_excel_path, sheet_name=sheet_name)

    # number of files processed
    count = 0

    # Loop over each .cif file in the subdirectory
    for file in sorted(os.listdir(dir_path)):
        if file.endswith(".cif"):
            count += 1

            file_path = os.path.join(dir_path, file)

            # Load the structure from the CIF file
            structure = Structure.from_file(file_path)
            primitive_structure = structure.get_primitive_structure()
            reduced_formula = structure.composition.reduced_formula
            abundance_score = float(scorer.calculate_compound_score(reduced_formula))
            cell_volume = primitive_structure.volume


            # Check if this structure matches any in the unique structures list
            is_unique = True
            for i, (rep_structure, rep_file, rep_abundance, abundant_structure, rep_volume, rep_count) in enumerate(unique_structures):
                if matcher.fit(primitive_structure, rep_structure):
                    is_unique = False
                    # Update the representative if the current structure has a larger volume
                    if cell_volume > rep_volume:
                        if abundance_score > rep_abundance:
                            unique_structures[i] = (primitive_structure, file_path, abundance_score, primitive_structure, cell_volume,rep_count + 1)
                        else:
                            unique_structures[i] = (primitive_structure, file_path, rep_abundance, abundant_structure, cell_volume, rep_count + 1)

                    else:
                        # Increment the count for this framework
                        if abundance_score > rep_abundance:
                            unique_structures[i] = (rep_structure, rep_file, abundance_score, primitive_structure, rep_volume, rep_count + 1)
                        else:
                            unique_structures[i] = (rep_structure, rep_file, rep_abundance, abundant_structure, rep_volume, rep_count + 1)
                    break

            # If unique, add to the list with a count of 1
            if is_unique:
                unique_structures.append((primitive_structure, file_path, abundance_score, primitive_structure, cell_volume, 1))

            if count % 1000 == 0:
                print(f"Processed {count} files...")

    # Sorting the structures that the most popular would appear first
    sorted_structures = sorted(unique_structures, key=lambda x: x[5], reverse=True)

    return sorted_structures
