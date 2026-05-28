# The Unique Structure Prototypes of All Materials

This repository contains the datasets and code associated with the Master's thesis **"The Unique Structure Prototypes of All Materials"** (Tel Aviv University, 2025).

## 📖 Overview

Crystal structure offers a compact, composition-independent basis for understanding materials behavior and accelerating discovery. This project presents an automated and reproducible workflow for identifying structure prototypes directly from atomic geometries, rather than relying on database metadata.

By analyzing **23,160** experimentally observed thermodynamic ground state inorganic materials from the Materials Project, we utilized a geometric matching algorithm to identify unique structural frameworks.

## 📊 Data Availability

Each Directory inculde all the cif files for the certain stoichiometry group.

The full lists of prototypes is available at the ```unique_structures.txt``` file. Each prototype is shown with the following information: 
* **Filename** (as obtained from the Materials Project)
* **Chemical formula**
* **Match count** (how many materials matched this prototype)
* **Space group** (both in Hermann-Mauguin and IUCr notation)
* **Orientation matrix** (in Ångström)
* **Fractional coordinates** for each atom

### Example Entry
```text
Filename: mp-614603.cif  CaO  appeared: 122 times
Space Group: Fm-3m no. 225
Orientation Matrix:
4.78	0.00	2.76
1.59	4.51	2.76
0.00	0.00	5.52
Atoms Locations:
Ca	[0. 0. 0.]
O	[0.5 0.5 0.5]
