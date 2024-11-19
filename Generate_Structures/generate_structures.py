import numpy as np

def polyvinyl_chloride(chain_length, output_filename, input_data):
    """
    Generates a preliminary structure of a polyvinyl chloride (PVC) polymer chain with the specified chain length.
    The generated structure can be further optimized using computational chemistry software such as Gaussian or Orca, 
    depending on the provided input data.
    
    Parameters:
    chain_length (int): The number of monomer units in the PVC chain.
    output_filename (str): The name of the file where the generated structure will be saved.
    input_data (dict or str): Information or settings required for the structure optimization process.
    
    Returns: positions
    """
    positions = []
    distance_C_Cl = 1.6
    distance_C_C = 1.2
    distance_C_H = 0.8
    
    for i in range(chain_length):
        # Coordinates of atoms in the structure
        C_Cl = np.array([i * distance_C_C, 0, 0])  # Carbon bonded to Cl
        C_H = np.array([i * distance_C_C, distance_C_C / 2, 0])  # Carbon bonded to H
        H_left = np.array([i * distance_C_C, distance_C_C / 2, distance_C_H])  # Left hydrogen
        H_right = np.array([i * distance_C_C, distance_C_C / 2, -distance_C_H])  # Right hydrogen
        Cl = np.array([i * distance_C_C, -distance_C_Cl, 0])  # Chlorine atom
        H_extra = np.array([i * distance_C_C, (distance_C_C / 2) + distance_C_H, 0])  # Extra hydrogen
        
        # Alternate structure composition
        if i % 2 == 0:
            positions.append(("H", H_right, "C", C_Cl, "Cl", Cl))
        else:
            positions.append(("H", H_left, "C", C_H, "H", H_extra))
        
    with open(output_filename, "w") as file:
        file.write(input_data)
        for unit in positions:
            for index in range(0, len(unit), 2):
                element = unit[index]
                coordinates = unit[index + 1]
                file.write(f"{element} {coordinates[0]:.2f} {coordinates[1]:.2f} {coordinates[2]:.2f}\n")
        print(f"File '{output_filename}' successfully created.")
    return positions

def Solvation_Spheres(n, radius, central_atom, molecular_central_atom, output_filename, input_data):
    """
    Generates a configuration of solvation spheres surrounding a central atom with a specified number of molecules, 
    arranged in a circular pattern of a given radius. The molecular arrangement is based on input coordinates 
    for each atom, and the output is saved to a specified file format.

    Parameters:
    n (int): The number of molecules to arrange around the central atom.
    radius (float): The radius of the circle where the molecules are distributed.
    central_atom (str): The symbol of the central atom (e.g., 'Hg').
    molecular_central_atom (str): The symbol of the central atom in each surrounding molecule (e.g., 'N' for pyrrole).
    output_filename (str): The name of the file to save the generated configuration.
    input_data (str): Additional input data or configuration settings to be written to the file.

    Returns: return positions
    """
    coordinates = [
        ("C", [0.0, 1.2, 0.0]),  # Carbon 1 (single bond)
        ("C", [1.2, 0.4, 0.0]),  # Carbon 2 (double bond)
        ("C", [0.7, -1.0, 0.0]),  # Carbon 3 (single bond)
        ("C", [-0.7, -1.0, 0.0]),  # Carbon 4 (double bond)
        (molecular_central_atom, [-1.2, 0.4, 0.0])  # Example: 'N' (pyrrole), 'S' (thiophene), 'O' (furan)
    ]

    positions = []
    # Add the central atom (e.g., Mercury)
    positions.append((central_atom, np.array([0, 0, 0])))

    # Generate positions in a circle with a given radius
    angle_increment = 360 / n  # Divide 360 degrees into n sections
    for i in range(n):
        # Calculate the angle in radians
        theta = np.radians(i * angle_increment)  # Angle in the xy-plane

        # Calculate the coordinates of the main atom in the xy-plane
        x_primary = radius * np.cos(theta)
        y_primary = radius * np.sin(theta)
        z_primary = 0

        # Position the molecule with the central atom pointing towards Mercury
        for atom, coords in coordinates:
            new_pos = [
                x_primary + coords[0],
                y_primary + coords[1],
                z_primary + coords[2]
            ]
            positions.append((atom, np.array(new_pos)))

    # Write the generated positions to a file
    with open(output_filename, "w") as file:
        file.write(input_data)
        for element, coords in positions:
            file.write(f"{element} {coords[0]:.2f} {coords[1]:.2f} {coords[2]:.2f}\n")
    print(f"File '{output_filename}' created successfully.")
    return positions