"""

@author: Magnus Wennemo

"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import os
import matplotlib.patches as mpatches
import csv

# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────

TRIM_COUNT_AN = 10
TRIM_COUNT_AO = 2
TOP_PERCENT = 0.1




MODELS = [
    "AAA001_sim_0-19_1-1mill", "AAA004_sim_0-15_1-3mill", "AAA013_sim_0-15_1-9mill",
    "AAA014_sim_0,14_1,3mill", "AAA017_sim_0-17_1-6mill", "AAA023_sim_0-15_1-8mill",
    "AAA033_sim_0-15_2mill", "AAA039_sim_0-15_1-9mill", "AAA042_0-18_1-9mill",
    "AAA046_sim_0-17_1-5mill", "AAA087_sim_0-15_1-6mill", "AAA088_sim_0-15_1-7mill",
    "AAA091_sim_0-15_1-5mill", "AAA092_sim_0-15_1mill"
]

scale= 1.2  # Scale factor for figure size

plt.rcParams.update({
    "font.family":       "serif",
    "font.serif":        ["Times New Roman","Palatino","serif"],
    "font.size":         16*scale,
    "axes.titlesize":    16*scale,
    "axes.labelsize":    16*scale,
    "xtick.labelsize":   14*scale,
    'lines.linewidth':   2*scale,
    "ytick.labelsize":   14*scale,
    "legend.fontsize":   14*scale,
    "figure.titlesize":  18*scale,
    "axes.grid":         True,
    "grid.linestyle":    "--",
    "grid.alpha":        0.5,
})

csv_out_path = r"C:\Users\magnuswe\OneDrive - SINTEF\Simvascular\results\minWSS_maxWSS_meanWSS.csv"


# ─────────────────────────────────────────────────────────────────────────────
# Functions
# ─────────────────────────────────────────────────────────────────────────────

def compute_trimmed_stats(csv_path, drop_count, p):
    """
    Reads a semicolon-delimited WSS CSV, divides by 10 (dynes/cm² → Pa),
    then for each column/timepoint returns:
    - times      : list of floats (column header / 100)
    - q1_vals    : np.array of 25th percentile (after trimming)
    - q3_vals    : np.array of 75th percentile (after trimming)
    - mean_vals  : np.array of arithmetic means (after trimming)
    - top_vals   : np.array of mean of top p% (after trimming)
    - bot_vals   : np.array of mean of bottom p% (after trimming)
    """
    df = pd.read_csv(csv_path, sep=';') / 10.0 # Read and convert dynes/cm² to Pa
    n_rows = df.shape[0]
    times = [float(col) / 100.0 for col in df.columns]

    q1_vals, q3_vals, mean_vals = [], [], []
    top_vals, bot_vals = [], []

    for col in df.columns:
        col_vals = df[col].values
        sorted_vals = np.sort(col_vals)
        if drop_count > 0 and (n_rows - 2 * drop_count) >= 1:
            trimmed = sorted_vals[drop_count : n_rows - drop_count]
        else:
            raise ValueError("drop_count is too high for the number of rows in the CSV.")
        m = trimmed.size
        q1_vals.append(np.percentile(trimmed, 25))
        q3_vals.append(np.percentile(trimmed, 75))
        mean_vals.append(trimmed.mean())
        count_p = max(int(math.floor(m * p / 100.0)), 2)
        top_subset = np.sort(trimmed)[-count_p:]
        bot_subset = np.sort(trimmed)[:count_p]
        top_vals.append(top_subset.mean())
        bot_vals.append(bot_subset.mean())

    return (
        times,
        np.array(q1_vals),
        np.array(q3_vals),
        np.array(mean_vals),
        np.array(top_vals),
        np.array(bot_vals),
        count_p,
    )

# ─────────────────────────────────────────────────────────────────────────────
# Data Processing
# ─────────────────────────────────────────────────────────────────────────────

all_data = []
for model in MODELS:
    cwd = f"C:\\Users\\magnuswe\\OneDrive - SINTEF\\Simvascular\\results\\last_cycle\\{model}-last_cycle"
    aneurysm_csv = f"{cwd}\\WSS_full_time_series_aneurysm.csv"
    aorta_csv    = f"{cwd}\\WSS_full_time_series_aorta.csv"

    (
        t_an, q1_an, q3_an, mean_an, top_an, bot_an, count_p_an
    ) = compute_trimmed_stats(aneurysm_csv, drop_count=TRIM_COUNT_AN, p=TOP_PERCENT)
    (
        t_ao, q1_ao, q3_ao, mean_ao, top_ao, bot_ao, count_p_ao
    ) = compute_trimmed_stats(aorta_csv, drop_count=TRIM_COUNT_AO, p=TOP_PERCENT)

    all_data.append({
        "model": model,
        "t_an": t_an, "q1_an": q1_an, "q3_an": q3_an, "mean_an": mean_an,
        "top_an": top_an, "bot_an": bot_an,
        "t_ao": t_ao, "q1_ao": q1_ao, "q3_ao": q3_ao, "mean_ao": mean_ao,
        "top_ao": top_ao, "bot_ao": bot_ao
    })


rows = []
for data in all_data:
    # For each model, get min, max, mean for both aneurysm and aorta
    row = {
        "model": data["model"],
        "minWSS_aorta": data["bot_ao"][20],
        "maxWSS_aorta": data["top_ao"][20],
        "minWSS_aneurysm": data["bot_an"][20],
        "maxWSS_aneurysm": data["top_an"][20],
        "meanWSS_aorta": data["mean_ao"][20],
        "meanWSS_aneurysm": data["mean_an"][20],
    }
    rows.append(row)

# Write to CSV
with open(csv_out_path, "w", newline="") as csvfile:
    writer = csv.DictWriter(
        csvfile,
        fieldnames=[
            "model",
            "minWSS_aorta", "maxWSS_aorta", 
            "minWSS_aneurysm", "maxWSS_aneurysm", 
            "meanWSS_aorta", "meanWSS_aneurysm"
        ],
        delimiter=";"
    )
    writer.writeheader()
    writer.writerows(rows)

print(f"Saved min/max/mean WSS values to {csv_out_path}")

# ─────────────────────────────────────────────────────────────────────────────
# Plotting first part of the data
# ─────────────────────────────────────────────────────────────────────────────

save_path = "C:\\Users\\magnuswe\\OneDrive - SINTEF\\Dokumenter\\Visualization"

figure_size = (14 * 0.5, 56 * 0.5)
dots_per_inch = 300

fig, axes = plt.subplots(7, 2, figsize=figure_size, sharey=True)
plot_legend = True
for idx, data in enumerate(all_data[:7]):
    # Aneurysm plot (left column)
    ax_an = axes[idx, 0]
    ax_an.fill_between(data["t_an"], data["bot_an"], data["top_an"], color="lightgrey", alpha=0.5)
    ax_an.fill_between(data["t_an"], data["q1_an"], data["q3_an"], color="red", alpha=0.15)
    ax_an.plot(data["t_an"], data["mean_an"], linestyle="-", color="green", linewidth=1.5, label="Mean")
    ax_an.plot(data["t_an"], data["top_an"], linestyle="--", color="blue", linewidth=1.5, label="Max")
    ax_an.plot(data["t_an"], data["bot_an"], linestyle=":", color="blue", linewidth=1.5, label="Min")
    ax_an.set_xticks(np.arange(0, 1.2, 0.2))
    ax_an.set_ylim(0, 20)
    if plot_legend:
        # Custom patch for Q1–Q3
        q1q3_patch = mpatches.Patch(color='red', alpha=0.15, label='Q1–Q3')
        handles, labels = axes[0,0].get_legend_handles_labels()
        handles.insert(0, q1q3_patch)
        labels.insert(0, 'Q1–Q3')

        # Remove duplicate labels while preserving order
        unique = dict()
        for h, l in zip(handles, labels):
            if l not in unique:
                unique[l] = h
        ax_an.legend(list(unique.values()), list(unique.keys()), loc="upper left", ncol=1)
        plot_legend = False
    if idx == 0:
        ax_an.set_title("Aneurysm")
    ax_an.grid(True)
    if idx == 6:
        ax_an.set_xlabel("Time (s)")
    ax_an.set_ylabel(f"{data['model'][:6]}\nWSS (Pa)")  # <-- Add model name as y-label

    # Aorta plot (right column)
    ax_ao = axes[idx, 1]
    ax_ao.fill_between(data["t_ao"], data["bot_ao"], data["top_ao"], color="lightgrey", alpha=0.5)
    ax_ao.fill_between(data["t_ao"], data["q1_ao"], data["q3_ao"], color="red", alpha=0.15)
    ax_ao.plot(data["t_ao"], data["mean_ao"], linestyle="-", color="green", linewidth=1.5, label="Mean")
    ax_ao.plot(data["t_ao"], data["top_ao"], linestyle="--", color="blue", linewidth=1.5, label="Max")
    ax_ao.plot(data["t_ao"], data["bot_ao"], linestyle=":", color="blue", linewidth=1.5, label="Min")
    ax_ao.set_ylim(0, 20)
    ax_ao.set_xticks(np.arange(0, 1.2, 0.2))
    ax_ao.grid(True)
    

    if idx == 0:
        ax_ao.set_title("Aorta")
    if idx == 6:
        ax_ao.set_xlabel("Time (s)")


fig.savefig(os.path.join(save_path, "WSS_graphs1.png"), bbox_inches='tight', dpi=dots_per_inch)

plt.tight_layout()
plt.show()

# ─────────────────────────────────────────────────────────────────────────────
# Plotting second part of the data
# ─────────────────────────────────────────────────────────────────────────────

fig, axes = plt.subplots(7, 2, figsize=figure_size, sharey=True)

for idx, data in enumerate(all_data[7:]):
    # Aneurysm plot (left column)
    ax_an = axes[idx, 0]
    ax_an.fill_between(data["t_an"], data["bot_an"], data["top_an"], color="lightgrey", alpha=0.5)
    ax_an.fill_between(data["t_an"], data["q1_an"], data["q3_an"], color="red", alpha=0.15)
    ax_an.plot(data["t_an"], data["mean_an"], linestyle="-", color="green", linewidth=1.5, label="Mean")
    ax_an.plot(data["t_an"], data["top_an"], linestyle="--", color="blue", linewidth=1.5, label="Max")
    ax_an.plot(data["t_an"], data["bot_an"], linestyle=":", color="blue", linewidth=1.5, label="Min")
    ax_an.set_ylim(0, 20)
    ax_an.set_xticks(np.arange(0, 1.2, 0.2))
    if idx == 0:
        ax_an.set_title("Aneurysm")
    ax_an.grid(True)
    if idx == 6:
        ax_an.set_xlabel("Time (s)")
    ax_an.set_ylabel(f"{data['model'][:6]}\nWSS (Pa)")  # <-- Add model name as y-label

    # Aorta plot (right column)
    ax_ao = axes[idx, 1]
    ax_ao.fill_between(data["t_ao"], data["bot_ao"], data["top_ao"], color="lightgrey", alpha=0.5)
    ax_ao.fill_between(data["t_ao"], data["q1_ao"], data["q3_ao"], color="red", alpha=0.15)
    ax_ao.plot(data["t_ao"], data["mean_ao"], linestyle="-", color="green", linewidth=1.5, label="Mean")
    ax_ao.plot(data["t_ao"], data["top_ao"], linestyle="--", color="blue", linewidth=1.5, label="Max")
    ax_ao.plot(data["t_ao"], data["bot_ao"], linestyle=":", color="blue", linewidth=1.5, label="Min")
    ax_ao.set_ylim(0, 20)
    ax_ao.set_xticks(np.arange(0, 1.2, 0.2))
    ax_ao.grid(True)
    if idx == 0:
        ax_ao.set_title("Aorta")
    if idx == 6:
        ax_ao.set_xlabel("Time (s)")

# Custom patch for Q1–Q3
q1q3_patch = mpatches.Patch(color='red', alpha=0.15, label='Q1–Q3')
handles, labels = axes[0,0].get_legend_handles_labels()
handles.insert(0, q1q3_patch)
labels.insert(0, 'Q1–Q3')

# Remove duplicate labels while preserving order
unique = dict()
for h, l in zip(handles, labels):
    if l not in unique:
        unique[l] = h

fig.savefig(os.path.join(save_path, "WSS_graphs2.png"), bbox_inches='tight', dpi=dots_per_inch)

plt.tight_layout()
plt.show()