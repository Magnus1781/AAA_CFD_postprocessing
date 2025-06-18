#!/usr/bin/env python3
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

scale=1.4
# Matplotlib "paper" style
plt.rcParams.update({
    "font.family":       "serif",
    "font.serif":        ["Times New Roman", "Palatino", "serif"],
    "font.size":         14*scale,    # base font size
    "axes.titlesize":    14*scale,    # axes title
    "axes.labelsize":    14*scale,    # x and y labels
    "xtick.labelsize":   13*scale,
    "ytick.labelsize":   12*scale,
    "legend.fontsize":   12*scale,
    "figure.titlesize":  16*scale,
    "lines.linewidth":   2.2*scale,
    "axes.grid":         True,
    "grid.linestyle":    "--",
    "grid.alpha":        0.5,
})

# Path to your data file
file_path = r"C:\Users\magnuswe\OneDrive - SINTEF\Simvascular\results\AAA001_sim_0-19_1-1mill-6cycles\all_results-flows.txt"

# Load the data (whitespace- or tab-delimited)
df = pd.read_csv(file_path, delim_whitespace=True)

# Extract and process the 'inflow' column:
#   1) invert the sign
#   2) take only the first 94 samples
inflow = -df['inflow'].values[-96:] #Getting last cycle values

# Create a time vector, starting at 0, with 0.01 s intervals
time = np.arange(len(inflow)) * 0.01

# Plotting
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(time, inflow)
ax.set_xlabel('t (s)')
ax.set_xticks(np.arange(0, 1.01, 0.2))

ax.set_ylabel('Flow rate (ml/s)')
ax.legend()
plt.tight_layout()
plt.show()
