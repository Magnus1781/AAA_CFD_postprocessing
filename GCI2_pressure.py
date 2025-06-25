import pandas as pd
from pyGCS import GCS, GCI

# File paths
file_500k = r"C:\Users\magnuswe\OneDrive - SINTEF\Simvascular\results\last_cycle\AAA001_sim_0-19_1-1mill-last_cycle\p_avg_500k.csv"
file_1_1mill = r"C:\Users\magnuswe\OneDrive - SINTEF\Simvascular\results\last_cycle\AAA001_sim_0-19_1-1mill-last_cycle\p_avg_1.1mill.csv"
file_2_5mill = r"C:\Users\magnuswe\OneDrive - SINTEF\Simvascular\results\last_cycle\AAA001_sim_0-19_1-1mill-last_cycle\p_avg_2.5mill.csv"

# Mesh info
cells_geo = [2465237, 1102627, 493360]
volume_geo = 325.30233

# Function to read and reorder pressure values
def read_and_order_pressures(file, order):
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()
    pressures = df["p_avg_mmhg"].tolist()
    return [pressures[i] for i in order]

# Spatial order from highest to lowest
ordered_indices = [0, 6, 5, 1, 2, 3, 7, 4] #Have to reorder the indices. 6 and 7 is similarly placed.

# Read and reorder pressures
p_500k = read_and_order_pressures(file_500k, ordered_indices)
p_1_1mill = read_and_order_pressures(file_1_1mill, ordered_indices)
p_2_5mill = read_and_order_pressures(file_2_5mill, ordered_indices)

# Loop through all i < j combinations
# Initialize separate lists
p_values = []
gci_12_values = []  # GCI between coarse and medium
gci_23_values = []  # GCI between medium and fine

chosen_pairs = [(0, 3), (2, 4), (3, 6), (3, 5)]

for i, j in chosen_pairs:
    dp_500k = p_500k[i] - p_500k[j]
    dp_1_1mill = p_1_1mill[i] - p_1_1mill[j]
    dp_2_5mill = p_2_5mill[i] - p_2_5mill[j]
    solutions = [dp_2_5mill, dp_1_1mill, dp_500k]

    gcs = GCS(dimension=3, simulation_order=2, volume=volume_geo, cells=cells_geo, solution=solutions)
    gci = GCI(dimension=3, simulation_order=2, volume=volume_geo, cells=cells_geo, solution=solutions)

    p_val = gci.get("apparent_order")
    gci_12, gci_23 = gci.get("gci")

    p_values.append(p_val)
    gci_12_values.append(gci_12)
    gci_23_values.append(gci_23)

    print(f"ΔP (ordered rows {i} - {j}): {[round(s, 6) for s in solutions]}")
    print(f"  Apparent order p: {p_val:.4f}")
    print(f"  GCI coarse→medium: {gci_12:.6f}")
    print(f"  GCI medium→fine:   {gci_23:.6f}\n")

# Average results
average_p = sum(p_values) / len(p_values)
average_gci_12 = sum(gci_12_values) / len(gci_12_values)
average_gci_23 = sum(gci_23_values) / len(gci_23_values)

print(f"Average apparent order p: {average_p:.4f}")
print(f"Average GCI coarse→medium: {average_gci_12:.6f}")
print(f"Average GCI medium→fine:   {average_gci_23:.6f}")
