import pandas as pd
import re
import numpy as np
from typing import Dict


class CompoundAbundanceScorer:
    def __init__(self, excel_file_path: str, sheet_name: str = None):
        """
        Initialize the scorer with element abundance data from Excel file.

        Args:
            excel_file_path: Path to Excel file containing element abundance data
            sheet_name: Name of sheet to read (if None, reads first sheet)
        """
        self.abundance_data = self._load_abundance_data(excel_file_path, sheet_name)

    def _load_abundance_data(self, file_path: str, sheet_name: str = None) -> Dict[str, float]:
        """Load element abundance data from Excel file."""
        try:
            # Read Excel file
            if sheet_name is None:
                excel_data = pd.read_excel(file_path, sheet_name=None)
                if isinstance(excel_data, dict):
                    sheet_names = list(excel_data.keys())
                    df = excel_data[sheet_names[0]]
                else:
                    df = excel_data
            else:
                df = pd.read_excel(file_path, sheet_name=sheet_name)

            # Try to identify element and abundance columns
            element_col = None
            abundance_col = None

            # Check for common element column names
            for col in df.columns:
                col_lower = str(col).lower()
                if any(keyword in col_lower for keyword in ['element', 'symbol', 'elem']):
                    element_col = col
                    break

            # Check for common abundance column names
            for col in df.columns:
                col_lower = str(col).lower()
                if any(keyword in col_lower for keyword in ['abundance', 'percent', '%', 'ppm', 'concentration']):
                    abundance_col = col
                    break

            # If not found, use first two columns
            if element_col is None:
                element_col = df.columns[0]
            if abundance_col is None:
                abundance_col = df.columns[1]

            # Create dictionary mapping element symbols to abundances
            abundance_dict = {}
            for _, row in df.iterrows():
                try:
                    element = str(row[element_col]).strip()
                    abundance = float(row[abundance_col])
                    if element and element.lower() not in ['nan', 'none', '']:
                        abundance_dict[element] = abundance
                except (ValueError, TypeError):
                    continue

            return abundance_dict

        except Exception as e:
            raise Exception(f"Error loading Excel file: {e}")

    def _parse_chemical_formula(self, formula: str) -> Dict[str, int]:
        """Parse a chemical formula and return element counts."""
        formula = formula.replace(" ", "")
        pattern = r'([A-Z][a-z]?)(\d*)'
        matches = re.findall(pattern, formula)

        element_counts = {}
        for element, count in matches:
            count = int(count) if count else 1
            element_counts[element] = element_counts.get(element, 0) + count

        return element_counts

    def calculate_compound_score(self, formula: str, scoring_method: str = 'geometric_mean') -> float:
        """
        Calculate abundance score for a chemical compound.

        Args:
            formula: Chemical formula string (e.g., "H2SO4", "CaCO3", "Fe2O3")
            scoring_method: Method to calculate score ('geometric_mean', 'arithmetic_mean',
                          'harmonic_mean', 'minimum', 'sum_weighted')

        Returns:
            Float abundance score (returns 0.0 if calculation fails or elements are missing)
        """
        try:
            element_counts = self._parse_chemical_formula(formula)

            # Get abundances for each element
            weighted_abundances = []

            for element, count in element_counts.items():
                if element in self.abundance_data:
                    abundance = self.abundance_data[element]
                else:
                    abundance = 0.0  # Missing elements get 0 abundance

                # Weight by element count in formula
                weighted_abundances.extend([abundance] * count)

            if not weighted_abundances:
                return 0.0

            # Calculate score based on selected method
            if scoring_method == 'geometric_mean':
                if 0 in weighted_abundances:
                    return 0.0
                else:
                    return float(np.prod(weighted_abundances) ** (1 / len(weighted_abundances)))

            elif scoring_method == 'arithmetic_mean':
                return float(np.mean(weighted_abundances))

            elif scoring_method == 'harmonic_mean':
                if 0 in weighted_abundances:
                    return 0.0
                else:
                    return float(len(weighted_abundances) / np.sum(1 / np.array(weighted_abundances)))

            elif scoring_method == 'minimum':
                return float(min(weighted_abundances))

            elif scoring_method == 'sum_weighted':
                return float(sum(weighted_abundances))

            else:
                raise ValueError(f"Unknown scoring method: {scoring_method}")

        except Exception:
            return 0.0


# Example usage
if __name__ == "__main__":
    # Replace with your Excel file path
    excel_file = "element-abundances.xlsx"

    try:
        # Initialize scorer
        scorer = CompoundAbundanceScorer(excel_file)

        # Get abundance score for a single compound
        compound = "SiO2"
        score = scorer.calculate_compound_score(compound)
        print(f"Abundance score for {compound}: {score}")

        # Try different scoring methods
        methods = ['geometric_mean', 'arithmetic_mean', 'minimum', 'sum_weighted']
        for method in methods:
            score = scorer.calculate_compound_score(compound, method)
            print(f"{compound} ({method}): {score}")

    except Exception as e:
        print(f"Error: {e}")