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

def df_analysis_from_excel(df, position=0, plot=False, color='blue', linestyle='-', linewidth=2, spectra=None, change=5):
    """
    Extracts and processes spectral data from a multi-level Excel DataFrame. The function retrieves 
    x and y data from specified columns, formats the data into NumPy arrays, and optionally plots 
    the extracted data using Matplotlib with customizable styles.

    Parameters:
    df (pd.DataFrame): A multi-level DataFrame containing spectral data with labeled columns. 
                       The first row of the selected columns should contain axis labels.
    position (int, optional): The column index (zero-based) indicating the start of the x and y data. 
                              Default is 0.
    plot (bool, optional): A flag to enable or disable plotting of the extracted data. If True, the 
                           function generates a plot with the specified styles. Default is False.
    color (str, optional): The color of the plot line. Accepts any Matplotlib-supported color format. 
                           Default is 'blue'.
    linestyle (str, optional): The line style for the plot (e.g., '-', '--', '-.', ':'). 
                               Default is '-'.
    linewidth (float, optional): The width of the plot line. Default is 2.
    spectra (str, optional): A string representing the type of spectra being processed. This is used 
                             in the plot title if plotting is enabled. Default is None.

    Returns:
    tuple: A tuple containing:
        - name (str): The name of the column group extracted from the DataFrame.
        - data (list): A list containing two NumPy arrays:
            - x (numpy.ndarray): The array of x-axis values (independent variable).
            - y (numpy.ndarray): The array of y-axis values (dependent variable).

    Example:
    --------
    >>> data = pd.DataFrame({
    >>>     ('Spectra 1', 'Wavelength'): ['Wavelength', 400, 500, 600],
    >>>     ('Spectra 1', 'Intensity'): ['Intensity', 1.0, 0.8, 0.6]
    >>> })
    >>> result = subtract_data_excel(data, position=0, plot=True, spectra="IR")
    >>> print(result)
    ('Spectra 1', [array([400., 500., 600.]), array([1.0, 0.8, 0.6])])
    """
    
    # Extract the name of the column group at the specified position
    name = df.columns.get_level_values(0)[position]
    
    # Select the relevant columns (x and y data) for processing
    data = df.iloc[:, position:position + 2]
    
    # Convert the selected data into a NumPy array for easier manipulation
    array = data.to_numpy()
    
    # Extract x (independent variable) and y (dependent variable) values, skipping the header
    x = array[1:, 0].astype(float)
    y = array[1:, 1].astype(float)
    
    # Create a tuple containing the name and the extracted x and y arrays
    info = (name, [x, y])

    # Plotting block (if plot=True)
    if plot:
        # Extract labels for the x and y axes from the first row of the data
        x_label = array[0, 0]
        y_label = array[0, 1]
        
        # Create a plot with specified figure size
        plt.figure(figsize=(10, 6))
        
        # Plot the data with the specified line style, color, and width
        plt.plot(x, y, linestyle=linestyle, color=color, linewidth=linewidth)
        
        # Add axis labels with specific font size
        plt.xlabel(x_label, fontsize=14)
        plt.ylabel(y_label, fontsize=14)
        
        # Set y and x axis limits with some padding for better visibility
        plt.ylim(min(y) - change, max(y) + change)
        plt.xlim(min(x) - 2*change, max(x) + 2*change)
        
        # Add a title to the plot
        plt.title(f"{spectra} Spectra {name}", fontsize=16)
        
        # Enable grid lines with a specific style and color
        plt.grid(True, linestyle=':', color='gray', linewidth=0.8)
        
        # Display the plot
        plt.show()
    
    # Return the extracted name and data as a tuple
    return info

