import matplotlib.pyplot as plt
import numpy as np
import os

def plot(file_path, plot = True, plot_curve=True, plot_bar = True, sigma = 0.1, name = "Absorption Spectrum"):

    # Leer el encabezado del primer archivo
    with open(file_path, 'r') as f:
        headers = f.readline().strip().split('\t')  # Leer y dividir los encabezados

    energy_header = headers[0]  # Nombre de la primera columna
    intensity_header = headers[1]  # Nombre de la segunda columna

    # Datos iniciales
    data = np.loadtxt(file_path, skiprows=1)

    # Extraer energía e intensidad
    energy = data[:, 0]
    intensity = data[:, 1]

    # Filtrar intensidades no nulas
    nonzero_indices = intensity != 0
    energy_nonzero = energy[nonzero_indices]
    intensity_nonzero = intensity[nonzero_indices]

    # Función para generar perfiles de líneas gaussianas
    def gaussian_lineshape(x, x0, I, sigma):
        return I * np.exp(-((x - x0)**2) / (2 * sigma**2))

    # Crear un rango de energía para graficar el perfil de línea
    energy_range = np.linspace(energy_nonzero.min() - 0.5, energy_nonzero.max() + 0.5, 1000)

    # Crear el perfil de líneas sumando gaussianas para cada energía con intensidad no nula
    gaussian_profile = np.zeros_like(energy_range)
    for x0, I in zip(energy_nonzero, intensity_nonzero):
        gaussian_profile += gaussian_lineshape(energy_range, x0, I, sigma)

    if plot:
        # Graficar ambos conjuntos de datos
        plt.figure(figsize=(10, 6))
        if plot_curve:
            # Gráfica de líneas para el primer conjunto de datos
            plt.plot(energy_range, gaussian_profile, label="Gaussian Lineshape", color='blue', linewidth=2)
        if plot_bar:
            # Gráfica de barras para los datos "sticks"
            plt.bar(energy_nonzero, intensity_nonzero, width=0.01, color='orange', label="Datos originales (sticks)")

        # Configuración del gráfico
        plt.xlabel(energy_header)
        plt.ylabel(intensity_header)
        plt.title(name)
        plt.grid(True)

        # Mostrar el gráfico
        plt.show()
    curve = [energy_range, gaussian_profile]
    bar = [energy_nonzero, intensity_nonzero]
    return curve, bar