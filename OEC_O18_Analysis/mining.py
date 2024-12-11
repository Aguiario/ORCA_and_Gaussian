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
