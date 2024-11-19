import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def subtract_data(file_path, spectra_type='IR', xlabeling='Wavenumber (cm⁻¹)', plot=False):
    """
    Reads and processes spectral data from a file containing harmonic curve plots, applicable for various 
    types of spectra (e.g., IR, Raman). The function extracts frequency and intensity values, normalizes 
    the intensity data, and optionally plots the processed spectra using Matplotlib.

    Parameters:
    file_path (str): The path to the file containing the spectral data. The file should include a section 
                     marked by the line "# Plot Curve (Harmonic)" to indicate where relevant data begins.
    spectra_type (str, optional): The type of spectra being processed (e.g., 'IR', 'Raman'). 
                                  Used for labeling or other custom settings. Default is 'IR'.
    xlabeling (str, optional): Label for the x-axis in the plot, such as 'Wavenumber (cm⁻¹)' or another 
                               descriptor relevant to the spectra type. Default is 'Wavenumber (cm⁻¹)'.
    plot (bool, optional): A flag indicating whether to plot the spectra after processing. 
                           If set to True, the function generates a plot of the normalized intensity 
                           versus the frequency. Default is False.

    Returns:
    tuple: A tuple containing two NumPy arrays:
        - frequencies (numpy.ndarray): The array of frequency values extracted from the file.
        - intensity_normalized (numpy.ndarray): The array of intensity values normalized to a range from 0 to 1.
    """
    # Read the file and find the line containing "# Plot Curve (Harmonic)"
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Find the line that contains "# Plot Curve (Harmonic)"
    skiprows = next(i + 1 for i, line in enumerate(lines) if "# Plot Curve (Harmonic)" in line)
    
    # Read the CSV data starting from the row after the found line
    df = pd.read_csv(file_path, delim_whitespace=True, skiprows=skiprows)
    
    # Drop unnecessary columns and rename the remaining ones
    df = df.drop(columns=['Y', 'DY/DX'], errors='ignore')  # Drop columns if they exist
    df.columns = ['X', 'Y']  # Rename columns to 'X' and 'Y'

    # Convert the DataFrame to a NumPy array
    array = df.to_numpy()
    frequencies = array[:, 0]  # Extract the frequency (first column)
    intensity = array[:, 1]  # Extract the intensity (second column)
    # Normalize intensity to a range from 0 to 1
    intensity_normalized = (intensity - np.min(intensity)) / (np.max(intensity) - np.min(intensity))

    if plot == True:
        # Plot the harmonic curve
        plt.plot(frequencies, intensity_normalized, color='red')

        # Add labels and a title to the plotxlabeling
        plt.xlabel(xlabeling) 
        plt.ylabel('Normalized Intensity')
        plt.title(f'{spectra_type} Spectra')  

        # Display the plot
        plt.show()

    return frequencies, intensity_normalized

