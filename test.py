from paraview.simple import *
import os
import ast
import pandas as pd
import numpy as np

# === Config ===
csv_path = r'C:\Users\magnuswe\OneDrive - SINTEF\Simvascular\results\two_last_cycles\AAA023_sim_0-15_1-8mill-two_last_cycles\centerline_points_and_tangents_table.csv'
num_planes = 6  # You have six points

print(f"[Macro] Reading: {csv_path}")

# === Load CSV ===
data = pd.read_csv(csv_path)
points = {}
tangents = {}

for col in data.columns:
    if col.startswith('point_'):
        points[int(col.split('_')[1])] = ast.literal_eval(data[col].iloc[0])
    elif col.startswith('tangent_'):
        tangents[int(col.split('_')[1])] = ast.literal_eval(data[col].iloc[0])

# Sort by index to keep order consistent
sorted_indices = sorted(points.keys())
if num_planes > len(sorted_indices):
    num_planes = len(sorted_indices)

selected_indices = sorted_indices[:num_planes]

print(f"[Macro] Generating {len(selected_indices)} planes")

# === Create and display planes ===
for i, idx in enumerate(selected_indices):
    center = points[idx]
    normal = tangents[idx]

    # Normalize normal vector
    norm = sum(x**2 for x in normal)**0.5
    if norm == 0:
        print(f"[Macro] Skipping index {idx} due to zero-length tangent.")
        continue
    normal = [x / norm for x in normal]

    plane = Plane()
    plane.Origin = center
    plane.Normal = normal
    plane.XResolution = 20
    plane.YResolution = 20
    plane_display = Show(plane)
    plane_display.Representation = 'Surface'
    plane_display.Opacity = 0.5
    plane_display.DiffuseColor = [1.0, 0.8, 0.3]

    RenameSource(f"Plane_{i}", plane)
    print(f"[Macro] Plane_{i} → Origin: {center}, Normal: {normal}")

# Focus camera on newly added planes
ResetCamera()
Render()
print("[Macro] Done.")
