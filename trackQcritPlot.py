import os
import numpy as np
import pandas as pd
from pathlib import Path

# === CONFIG ===
models = ["500", "2.5", "1.1"]
timesteps = [f"0.{i:02d}" for i in range(30, 75, 5)]  # e.g., '0,30', '0,35', ..., '0,70'
base_dir = Path(r"C:\Users\magnuswe\OneDrive - SINTEF\Simvascular\results\last_cycle\AAA001_sim_0-19_1-1mill-last_cycle")
ref_point_file = base_dir / "ref_point.csv"

# === Load reference point ===
ref_df = pd.read_csv(ref_point_file)
ref_coords = ref_df[['Points_0', 'Points_1', 'Points_2']].values.flatten()
if ref_coords.shape != (3,):
    raise ValueError("ref_point.csv must contain one row with 'Points_0', 'Points_1', 'Points_2' columns.")

# === Process data files ===
results = []

for model in models:
    for ts in timesteps:
        filename = f"{model}_{ts}.csv"
        filepath = base_dir / filename
        if not filepath.exists():
            print(f"Warning: {filename} not found.")
            continue

        try:
            df = pd.read_csv(filepath)
            if not all(col in df.columns for col in ['Points_0', 'Points_1', 'Points_2']):
                print(f"Warning: Missing coordinate columns in {filename}.")
                continue

            # Extract points and compute distances to the reference
            points = df[['Points_0', 'Points_1', 'Points_2']].values
            distances = np.linalg.norm(points - ref_coords, axis=1)

            # Save mean distance per file
            results.append({
                "model": model,
                "timestep": ts,
                "mean_distance": distances.mean(),
                "min_distance": distances.min(),
                "max_distance": distances.max()
            })
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            continue

# === Output ===
df_out = pd.DataFrame(results)

import matplotlib.pyplot as plt

# Convert timestep strings like '0,30' to floats like 0.30
df_out["timestep_float"] = df_out["timestep"].str.replace(',', '.').astype(float)

# Sort the DataFrame for proper plotting
df_out = df_out.sort_values(by=["model", "timestep_float"])

# Plot
plt.figure(figsize=(10, 6))

for model in df_out["model"].unique():
    model_data = df_out[df_out["model"] == model]
    plt.plot(model_data["timestep_float"], model_data["mean_distance"], label=f"Model {model}", marker='o')

plt.xlabel("Timestep")
plt.ylabel("Mean Distance to Reference Point")
plt.title("Distance to Reference Point Over Time")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("distance_plot.png")
plt.show()














