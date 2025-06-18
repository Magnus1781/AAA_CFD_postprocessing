import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import os
import matplotlib.patches as mpatches

#####load vtu files and clip below renals and the two extensions, change cwd then run this macroo########

AAA001 = "AAA001_sim_0-19_1-1mill"
AAA004 = "AAA004_sim_0-15_1-3mill"
AAA013 = "AAA013_sim_0-15_1-9mill"
AAA014 = "AAA014_sim_0,14_1,3mill"
AAA017 = "AAA017_sim_0-17_1-6mill"
AAA023 = "AAA023_sim_0-15_1-8mill"
AAA033 = "AAA033_sim_0-15_2mill"
AAA039 = "AAA039_sim_0-15_1-9mill"
AAA042 = "AAA042_0-18_1-9mill"
AAA046 = "AAA046_sim_0-17_1-5mill"
AAA087 = "AAA087_sim_0-15_1-6mill"
AAA088 = "AAA088_sim_0-15_1-7mill"
AAA091 = "AAA091_sim_0-15_1-5mill"
AAA092 = "AAA092_sim_0-15_1mill"
models = [
    AAA001, AAA004, AAA013, AAA014, AAA017, AAA023, AAA033, AAA039, AAA042, AAA046, AAA087, AAA088, AAA091, AAA092
]

plt.rcParams.update({
    "font.family":       "serif",
    "font.serif":        ["Times New Roman","Palatino","serif"],
    "font.size":         16,    # base font size
    "axes.titlesize":    16,    # axes title
    "axes.labelsize":    16,    # x and y labels
    "xtick.labelsize":   14,
    'lines.linewidth':   2,   # makes all plot lines thicker by default
    "ytick.labelsize":   14,
    "legend.fontsize":   14,
    "figure.titlesize":  18,
    "axes.grid":         True,
    "grid.linestyle":    "--",
    "grid.alpha":        0.5,
})

for model in models:

    # assume cwd already uses double-forward-slashes:
    cwd    = f"C:\\Users\\magnuswe\\OneDrive - SINTEF\\Simvascular\\results\\last_cycle\\{model}-last_cycle"


    aneurysm_csv = f"{cwd}\\WSS_full_time_series_aneurysm.csv"
    aorta_csv    = f"{cwd}\\WSS_full_time_series_aorta.csv"


    # ─────────────────────────────────────────────────────────────────────────────
    # Settings:
    # ─────────────────────────────────────────────────────────────────────────────
    trim_count_an    = 10     # drop top 10 & bottom 10 rows for Aneurysm
    trim_count_ao    = 2      # drop top 2  & bottom 2  rows for Aorta

    top_percent      = 0.1    # only use 0.1% for top/bottom means
    # ─────────────────────────────────────────────────────────────────────────────


    def compute_trimmed_stats(csv_path, drop_count, p):
        """
        Reads a semicolon-delimited WSS CSV, divides by 10 (dynes/cm² → Pa),
        then for each column/timepoint returns:
        - times      : list of floats (column header / 100)
        - q1_vals    : np.array of 25th percentile (after trimming)
        - q3_vals    : np.array of 75th percentile (after trimming)
        - mean_vals  : np.array of arithmetic means (after trimming)
        - min_vals   : np.array of minimum values (after trimming)
        - max_vals   : np.array of maximum values (after trimming)
        - top_vals   : np.array of mean of top p% (after trimming)
        - bot_vals   : np.array of mean of bottom p% (after trimming)
        """
        df = pd.read_csv(csv_path, sep=';') / 10.0
        n_rows = df.shape[0]
        times = [float(col) / 100.0 for col in df.columns]

        q1_vals   = []
        q3_vals   = []
        mean_vals = []
        min_vals  = []
        max_vals  = []
        top_vals  = []
        bot_vals  = []

        for col in df.columns:
            col_vals = df[col].values
            sorted_vals = np.sort(col_vals)

            # 1) Drop `drop_count` from each tail if possible
            if drop_count > 0 and (n_rows - 2 * drop_count) >= 1:
                trimmed = sorted_vals[drop_count : n_rows - drop_count]
            else:
                raise ValueError("drop_count is too high for the number of rows in the CSV.")

            m = trimmed.size

            # 2) Compute Q1, Q3, mean, min, max on trimmed
            q1_vals.append(np.percentile(trimmed, 25))
            q3_vals.append(np.percentile(trimmed, 75))
            mean_vals.append(trimmed.mean())
            min_vals.append(trimmed.min())
            max_vals.append(trimmed.max())

            # 3) Compute top/bottom p%
            count_p = int(math.floor(m * p / 100.0))
            count_p = max(count_p, 2)      # ensure at least 2 values
            top_subset = np.sort(trimmed)[-count_p:]
            bot_subset = np.sort(trimmed)[:count_p]

            top_vals.append(top_subset.mean())
            bot_vals.append(bot_subset.mean())

        return (
            times,
            np.array(q1_vals),
            np.array(q3_vals),
            np.array(mean_vals),
            np.array(min_vals),
            np.array(max_vals),
            np.array(top_vals),
            np.array(bot_vals),
            count_p,  # return count_p for debugging purposes
        )


    # ─────────────────────────────────────────────────────────────────────────────
    # Meshes (label, aneurysm-CSV, aorta-CSV)
    # ─────────────────────────────────────────────────────────────────────────────
    meshes = [
        ("", aneurysm_csv, aorta_csv)
    ]

    # ─────────────────────────────────────────────────────────────────────────────
    # First pass: compute stats for each mesh and track global y-limits
    # ─────────────────────────────────────────────────────────────────────────────
    all_data = []
    global_an_min, global_an_max = np.inf, -np.inf
    global_ao_min, global_ao_max = np.inf, -np.inf

    for mesh_label, aneurysm_csv, aorta_csv in meshes:
        # Aneurysm (drop 10)
        (
            t_an,
            q1_an,
            q3_an,
            mean_an,
            min_an,
            max_an,
            top_an,
            bot_an,
            count_p_an  # for debugging purposes
        ) = compute_trimmed_stats(aneurysm_csv, drop_count=trim_count_an, p=top_percent)
        print(f"Processed Aneurysm for model: {model[:6]} with count_p_an={count_p_an}")
        # Aorta (drop 2)
        (
            t_ao,
            q1_ao,
            q3_ao,
            mean_ao,
            min_ao,
            max_ao,
            top_ao,
            bot_ao,
            count_p_ao  # for debugging purposes
        ) = compute_trimmed_stats(aorta_csv, drop_count=trim_count_ao, p=top_percent)
        print(f"Processed Aorta for model: {model[:6]} with count_p_ao={count_p_ao}")
        # Update global y‐limits for aneurysm
        global_an_min = min(global_an_min, min_an.min(), q1_an.min(), top_an.min(), bot_an.min())
        global_an_max = max(global_an_max, max_an.max(), q3_an.max(), top_an.max(), bot_an.max())

        # Update global y‐limits for aorta
        global_ao_min = min(global_ao_min, min_ao.min(), q1_ao.min(), top_ao.min(), bot_ao.min())
        global_ao_max = max(global_ao_max, max_ao.max(), q3_ao.max(), top_ao.max(), bot_ao.max())

        all_data.append({
            "label": mesh_label,
            "t_an": t_an,
            "q1_an": q1_an,
            "q3_an": q3_an,
            "mean_an": mean_an,
            "min_an": min_an,
            "max_an": max_an,
            "top_an": top_an,
            "bot_an": bot_an,
            "t_ao": t_ao,
            "q1_ao": q1_ao,
            "q3_ao": q3_ao,
            "mean_ao": mean_ao,
            "min_ao": min_ao,
            "max_ao": max_ao,
            "top_ao": top_ao,
            "bot_ao": bot_ao
        })
    # ─────────────────────────────────────────────────────────────────────────────
    # Second pass: plot Aneurysm and Aorta side by side, sharing the same Y‐axis
    # ─────────────────────────────────────────────────────────────────────────────
   # ...existing code up to plotting section...
# ...existing code up to plotting section...

fig, axes = plt.subplots(7, 2, figsize=(16, 28), sharey=True)

for i in range(7):

    ax_an1 = axes[i, 0]
    ax_ao1 = axes[i, 1]


    ax_an1_path = f"C:\\Users\\magnuswe\\OneDrive - SINTEF\\Simvascular\\results\\last_cycle\\{model[i]}-last_cycle\\WSS_full_time_series_aneurysm.csv"
    ax_ao1_path = f"C:\\Users\\magnuswe\\OneDrive - SINTEF\\Simvascular\\results\\last_cycle\\{model[i]}-last_cycle\\WSS_full_time_series_aorta.csv"

    # Compute stats for aneurysm
    (
        t_an, q1_an, q3_an, mean_an, min_an, max_an, top_an, bot_an, count_p_an
    ) = compute_trimmed_stats(aneurysm_csv, drop_count=trim_count_an, p=top_percent)
    # Compute stats for aorta
    (
        t_ao, q1_ao, q3_ao, mean_ao, min_ao, max_ao, top_ao, bot_ao, count_p_ao
    ) = compute_trimmed_stats(aorta_csv, drop_count=trim_count_ao, p=top_percent)


    # Plot aneurysm
    ax_an1.fill_between(t_an, bot_an, top_an, color="lightgrey", alpha=0.5)
    ax_an1.fill_between(t_an, q1_an, q3_an, color="red", alpha=0.15)
    ax_an1.plot(t_an, mean_an, linestyle="-", color="green", linewidth=1.5, label="Aneurysm Mean")
    ax_an1.plot(t_an, top_an, linestyle="--", color="darkgreen", linewidth=1.5, label="Aneurysm Max")
    ax_an1.plot(t_an, bot_an, linestyle=":", color="darkgreen", linewidth=1.5, label="Aneurysm Min")
    ax_an1.set_ylim(0, 20)
    ax_an1.set_title(f"Aneurysm")
    ax_an1.grid(True)
    ax_an1.set_ylabel("WSS (Pa)")
    if i == 13:
        ax_an1.set_xlabel("Time (s)")

    # Plot aorta
    ax_ao1.fill_between(t_ao, bot_ao, top_ao, color="lightgrey", alpha=0.5)
    ax_ao1.fill_between(t_ao, q1_ao, q3_ao, color="red", alpha=0.15)
    ax_ao1.plot(t_ao, mean_ao, linestyle="-", color="blue", linewidth=1.5, label="Aorta Mean")
    ax_ao1.plot(t_ao, top_ao, linestyle="--", color="navy", linewidth=1.5, label="Aorta Max")
    ax_ao1.plot(t_ao, bot_ao, linestyle=":", color="navy", linewidth=1.5, label="Aorta Min")
    ax_ao1.set_ylim(0, 20)
    ax_ao1.set_title(f"Aorta")
    ax_ao1.grid(True)
    if i == 13:
        ax_ao1.set_xlabel("Time (s)")


# Custom patch for Q1–Q3
q1q3_patch = mpatches.Patch(color='red', alpha=0.15, label='Q1–Q3')
handles, labels = axes[0,0].get_legend_handles_labels()
handles.insert(0, q1q3_patch)
labels.insert(0, 'Q1–Q3')

fig.legend(
    handles[:4],
    labels[:4],
    loc="upper right",
    ncol=1,
    bbox_to_anchor=(0.99, 0.99)
)

plt.tight_layout(rect=[0, 0, 0.96, 1])
plt.subplots_adjust(right=0.95)
plt.show()