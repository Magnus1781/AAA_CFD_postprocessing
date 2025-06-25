import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Settings
models = ['500k', '1.1mill', '2.5mill']
timesteps = ['0,30', '0,40', '0,50', '0,60', '0,70', '0,80', '0,90']
data_dir = r"C:\Users\magnuswe\OneDrive - SINTEF\Simvascular\results\last_cycle\AAA001_sim_0-19_1-1mill-last_cycle"
slice_file = 'slice_points.csv'

# Set reference point manually (instead of using slice_points.csv)
reference_point = np.array([0.745156, -18.0747, 97.2329])

# Initialize data containers
distances_area_com_slice = {model: [] for model in models}
distances_volume_com_slice = {model: [] for model in models}
distances_area_com_ref = {model: [] for model in models}
distances_volume_com_ref = {model: [] for model in models}
area_data = {model: [] for model in models}
volume_data = {model: [] for model in models}
area_volume_ratio = {model: [] for model in models}
qcriterion_com = {model: [] for model in models}
qcriterion_com_dist_slice = {model: [] for model in models}
qcriterion_com_dist_ref = {model: [] for model in models}

# Load slice points
slice_filepath = os.path.join(data_dir, slice_file)
slice_df = pd.read_csv(slice_filepath)
slice_points = slice_df[['Points_0', 'Points_1', 'Points_2']].to_numpy()

# Process data
for model in models:
    for timestep in timesteps:
        base_filename = f"{model}_{timestep}"
        area_file = os.path.join(data_dir, f"{base_filename}_area.csv")
        volume_file = os.path.join(data_dir, f"{base_filename}_volume.csv")
        q_file = os.path.join(data_dir, f"{base_filename}_qcriterion.csv")

        try:
            # Read area points and compute COM
            area_df = pd.read_csv(area_file)
            area = float(area_df['Area'].iloc[0])
            area_points = area_df[['Points_0', 'Points_1', 'Points_2']].to_numpy()
            com_area = np.mean(area_points, axis=0)

            # Read volume points and compute COM
            volume_df = pd.read_csv(volume_file)
            volume = float(volume_df['Volume'].iloc[0])
            volume_points = volume_df[['Points_0', 'Points_1', 'Points_2']].to_numpy()
            com_volume = np.mean(volume_points, axis=0)

            # Compute distances
            min_dist_area = np.min(np.linalg.norm(slice_points - com_area, axis=1))
            min_dist_volume = np.min(np.linalg.norm(slice_points - com_volume, axis=1))
            dist_area_ref = np.linalg.norm(reference_point - com_area)
            dist_volume_ref = np.linalg.norm(reference_point - com_volume)

            # Store data
            distances_area_com_slice[model].append(min_dist_area)
            distances_volume_com_slice[model].append(min_dist_volume)
            distances_area_com_ref[model].append(dist_area_ref)
            distances_volume_com_ref[model].append(dist_volume_ref)
            area_data[model].append(area)
            volume_data[model].append(volume)
            area_volume_ratio[model].append(area / volume if volume != 0 else np.nan)

        except Exception as e:
            print(f"Error processing {base_filename} area/volume: {e}")
            for d in [distances_area_com_slice, distances_volume_com_slice,
                      distances_area_com_ref, distances_volume_com_ref,
                      area_data, volume_data, area_volume_ratio]:
                d[model].append(np.nan)

        try:
            q_df = pd.read_csv(q_file)
            points = q_df[['Points_0', 'Points_1', 'Points_2']].to_numpy()
            q_values = q_df['Q Criterion'].to_numpy()

            # Skip if all Q values are zero or NaN
            if np.all(np.isnan(q_values)) or np.sum(np.abs(q_values)) == 0:
                raise ValueError("All Q values are NaN or zero")

            # Weighted COM calculation
            weights = q_values
            weighted_com = np.average(points, axis=0, weights=weights)

            # Store weighted COM
            qcriterion_com[model].append(weighted_com)

            # Compute distances
            min_dist_q = np.min(np.linalg.norm(slice_points - weighted_com, axis=1))
            dist_q_ref = np.linalg.norm(reference_point - weighted_com)

            qcriterion_com_dist_slice[model].append(min_dist_q)
            qcriterion_com_dist_ref[model].append(dist_q_ref)

        except Exception as e:
            print(f"Error processing Q file {base_filename}: {e}")
            qcriterion_com[model].append([np.nan, np.nan, np.nan])
            qcriterion_com_dist_slice[model].append(np.nan)
            qcriterion_com_dist_ref[model].append(np.nan)

# --- Plotting functions ---
def plot_geometry_metrics():
    fig, axes = plt.subplots(3, 1, figsize=(12, 12))
    titles = ['Area [mm²]', 'Volume [mm³]', 'Area / Volume']
    data_dicts = [area_data, volume_data, area_volume_ratio]

    for ax, title, data_dict in zip(axes, titles, data_dicts):
        for model in models:
            values = data_dict[model]
            if all(np.isnan(values)):
                continue
            ax.plot(timesteps, values, marker='o', label=model)
        ax.set_title(title)
        ax.set_xlabel("Timestep")
        ax.set_ylabel(title)
        ax.grid(True)
        ax.legend()

    plt.tight_layout()
    plt.show()

def plot_distance_metrics():
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    metrics = [
        (distances_area_com_slice, "Area COM to Nearest Slice"),
        (distances_volume_com_slice, "Volume COM to Nearest Slice"),
        (distances_area_com_ref, f"Area COM to Ref Point {reference_point}"),
        (distances_volume_com_ref, f"Volume COM to Ref Point {reference_point}")
    ]

    for ax, (data_dict, title) in zip(axes.flat, metrics):
        for model in models:
            values = data_dict[model]
            if all(np.isnan(values)):
                continue
            ax.plot(timesteps, values, marker='o', label=model)
        ax.set_title(title)
        ax.set_xlabel("Timestep")
        ax.set_ylabel("Distance [mm]")
        ax.grid(True)
        ax.legend()

    plt.tight_layout()
    plt.show()

def plot_qcriterion_com_distances():
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    metrics = [
        (qcriterion_com_dist_slice, "Q-Criterion COM to Nearest Slice"),
        (qcriterion_com_dist_ref, f"Q-Criterion COM to Ref Point {reference_point}")
    ]

    for ax, (data_dict, title) in zip(axes, metrics):
        for model in models:
            values = data_dict[model]
            if all(np.isnan(values)):
                continue
            ax.plot(timesteps, values, marker='o', label=model)
        ax.set_title(title)
        ax.set_xlabel("Timestep")
        ax.set_ylabel("Distance [mm]")
        ax.grid(True)
        ax.legend()

    plt.tight_layout()
    plt.show()

# --- Plotting ---
plot_geometry_metrics()
plot_distance_metrics()
plot_qcriterion_com_distances()
