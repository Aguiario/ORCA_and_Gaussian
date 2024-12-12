import os

def extract_oxygen_atoms(file_path, show = False):
    """
    Extracts the coordinates of atoms with the identifier 'O(Iso=18)' from a specified file.

    Parameters:
    file_path (str): The path to the file to be processed.

    Returns:
    list: A list of tuples containing the atom index and its X, Y, Z coordinates.
    """
    try:
        # Open the file for reading
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Search for the line containing "Title Card Required"
        start_line_index = None
        for i, line in enumerate(lines):
            if "Charge" in line:
                start_line_index = i+1
                break

        if start_line_index is None:
            print("The 'Title Card Required' section was not found.")
            return

        # Extract atom data starting from the identified section
        atom_data = []
        for i in range(start_line_index, len(lines)):
            line = lines[i].strip()
            if line.startswith("Grad"):  # Stop if we reach the "Grad" line
                break
            parts = line.split()
            # Check if the line contains the required atom data
            if len(parts) >= 4 and "O(Iso=18)" in parts[0]:
                atom_index = i - start_line_index + 1  # Relative position of the atom
                x, y, z = float(parts[1]), float(parts[2]), float(parts[3])  # Extract coordinates
                atom_data.append((atom_index, x, y, z))
        # Display the results
        if atom_data:
            if show:
                print("Atoms found with 'O(Iso=18)':")
                for atom in atom_data:
                    print(f"Position: {atom[0]}, Coordinates: X={atom[1]}, Y={atom[2]}, Z={atom[3]}")

            # Save results to a file
            output_dir = os.path.join("18O")
            os.makedirs(output_dir, exist_ok=True)  # Create the output directory if it doesn't exist

            output_file = os.path.join(output_dir, os.path.basename(file_path).replace(".log", ".txt"))
            with open(output_file, 'w') as output:
                output.write("ID X Y Z\n")
                for atom in atom_data:
                    output.write(f"{atom[0]} {atom[1]} {atom[2]} {atom[3]}\n")
            if show:
                print(f"Data saved to: {output_file}")
        else:
            print("No atoms with 'O(Iso=18)' were found.")

        return atom_data

    except FileNotFoundError:
        print(f"The file was not found at the specified path: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def process_all_log_files(directory):
    """
    Processes all .log files in a specified directory to extract oxygen atom data.

    Parameters:
    directory (str): The path to the directory containing the .log files.

    Returns:
    None
    """
    try:
        # Ensure the directory exists
        if not os.path.exists(directory):
            print(f"The directory {directory} does not exist.")
            return

        # Find all .log files in the directory
        log_files = [f for f in os.listdir(directory) if f.endswith('.log')]
        if not log_files:
            print("No .log files were found in the directory.")
            return

        # Process each file using the extract_oxygen_atoms function
        for log_file in log_files:
            file_path = os.path.join(directory, log_file)
            print(f"Processing file: {file_path}")
            extract_oxygen_atoms(file_path)

    except Exception as e:
        print(f"An error occurred during processing: {e}")

import os

def summarize_txt_files(directory):
    # Check if the directory exists
    if not os.path.exists(directory):
        print(f"The directory {directory} does not exist.")
        return

    # Create the summary.txt file
    summary_file_path = os.path.join("summary.txt")

    with open(summary_file_path, "w", encoding="utf-8") as summary_file:
        # Iterate through all files in the directory
        for file_name in os.listdir(directory):
            file_path = os.path.join(directory, file_name)

            # Check if the file is a text file
            if os.path.isfile(file_path) and file_name.endswith(".txt") and file_name != "summary.txt":
                with open(file_path, "r", encoding="utf-8") as txt_file:
                    # Write the name of the file
                    summary_file.write(f"File: {file_name}\n")

                    # Write the content of the file
                    summary_file.write(txt_file.read())

                    # Add a space between files
                    summary_file.write("\n")

    print(f"summary.txt file successfully created in {directory}")


def process_frequencies(file_path, output_folder="Frequencies"):
    """
    Processes frequency data from a log file and generates an output file containing atomic frequencies,
    positions, and related properties filtered within a specific range.

    Parameters:
        file_path (str): Path to the input log file containing atomic data.
        output_folder (str): Directory to save the output files (default: "Frequencies").

    Returns:
        list: List of atom IDs extracted from the input file.
    """
    input_file = "summary.txt"

    atom_positions = []

    # Read the input file to find the target file and atom IDs
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Derive the target file name from the input file path
    target_file = file_path.replace('data\\', '').replace('.log', '.txt')
    found_file = False

    # Search for the target file name in the input file
    for i, line in enumerate(lines):
        if f"File: {target_file}" in line:
            found_file = True
            start_index = i + 2  # Data starts two lines after the match
            break

    if not found_file:
        print(f"File {target_file} not found in the input document.")
        return atom_positions

    # Extract atom IDs from the relevant section of the input file
    for line in lines[start_index:]:
        if line.strip() == "" or line.startswith("File:"):
            break
        atom_id = line.split()[0]  # Extract the first element as the atom ID
        atom_positions.append(int(atom_id))

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Prepare the output file name
    base_name = os.path.basename(file_path).replace(".log", "_seb.txt")
    output_file = os.path.join(output_folder, base_name)

    # Read the log file content
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Initialize a dictionary to store data grouped by atom and frequency
    atom_data = {atom: {} for atom in atom_positions}

    for i, line in enumerate(lines):
        if line.strip().startswith("Frequencies --"):
            # Extract frequencies from the line
            freqs = [float(f) for f in line.split()[2:] if f.replace('-', '').replace('.', '').isdigit()]

            # Initialize placeholders for IR Intensity and Raman Activity
            ir_inten = []
            raman_activ = []

            # Search for IR Intensity and Raman Activity in subsequent lines
            for j in range(1, 6):
                if i + j < len(lines):
                    if lines[i + j].strip().startswith("IR Inten    --"):
                        ir_inten = [float(x) for x in lines[i + j].split()[2:] if x.replace('-', '').replace('.', '').isdigit()]
                    elif lines[i + j].strip().startswith("Raman Activ --"):
                        raman_activ = [float(x) for x in lines[i + j].split()[2:] if x.replace('-', '').replace('.', '').isdigit()]

            # Search for atomic data corresponding to the frequencies
            for j in range(6, 9):
                if i + j < len(lines):
                    next_line = lines[i + j]
                    if next_line.strip().startswith("Atom"):
                        for atom_line in lines[i + j + 1:]:
                            if atom_line.strip() == "":
                                break
                            atom_parts = atom_line.split()
                            if len(atom_parts) > 4 and atom_parts[0].isdigit():
                                atom_id = int(atom_parts[0])
                                if atom_id in atom_positions:
                                    # Extract X, Y, Z displacements for each frequency
                                    x_values = [float(x) for x in atom_parts[2::3]]
                                    y_values = [float(y) for y in atom_parts[3::3]]
                                    z_values = [float(z) for z in atom_parts[4::3]]
                                    for idx, freq in enumerate(freqs):
                                        if 200 < freq < 750:  # Filter frequencies within range
                                            if idx < len(x_values) and idx < len(y_values) and idx < len(z_values):
                                                if freq not in atom_data[atom_id]:
                                                    atom_data[atom_id][freq] = {
                                                        "X": x_values[idx],
                                                        "Y": y_values[idx],
                                                        "Z": z_values[idx],
                                                        "IR": ir_inten[idx] if idx < len(ir_inten) else "--",
                                                        "Raman": raman_activ[idx] if idx < len(raman_activ) else "--"
                                                    }
                        break

    # Write the processed data to the output file
    with open(output_file, 'w') as f:
        for atom_id, freq_data in atom_data.items():
            f.write(f"Atom: {atom_id}\n")
            f.write(f"Frequency   X       Y       Z       IR      Raman\n")
            for freq, entry in sorted(freq_data.items()):
                f.write(f"{freq:.4f}  {entry['X']:.2f}  {entry['Y']:.2f}  {entry['Z']:.2f}  {entry['IR']}  {entry['Raman']}\n")
            f.write("\n")

def process_all_frequencies(folder_path, output_folder="Frequencies"):
    """
    Processes all .log files in the specified folder using the process_frequencies function.

    Parameters:
        folder_path (str): Path to the folder containing .log files.
        output_folder (str): Directory to save the output files (default: "Frequencies").
    """
    # Ensure the folder exists
    if not os.path.exists(folder_path):
        print(f"The folder '{folder_path}' does not exist.")
        return

    # Iterate over all .log files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".log"):
            file_path = os.path.join(folder_path, file_name)
            print(f"Processing file: {file_path}")
            process_frequencies(file_path, output_folder)

