import csv
import os
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np



###Models

AAA001 = "AAA001_sim_0-19_1-1mill"
AAA004 = "AAA004_sim_0-15_1-3mill"
AAA013 = "AAA013_sim_0-15_1-9mill"
AAA014 = "AAA014_sim_0,14_1,3mill"
AAA017 = "AAA017_sim_0-17_1-6mill"
AAA023 = "AAA023_sim_0-15_1-8mill"
AAA033 = ""
AAA039 = ""
AAA042 = ""
AAA046 = ""
AAA087 = ""
AAA088 = ""
AAA091 = ""
AAA092 = ""

model = AAA014

cwd = f"C:/Users/magnuswe/OneDrive - SINTEF/Simvascular/results/two_last_cycles/{model}-two_last_cycles/"

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 14
})

plot_file = os.path.join(cwd, "particle_age_plot.png")

# Three groups of files
"""
csv_sets = [
    [os.path.join(cwd, f"particle_age_stats_{i}.csv") for i in range(5)],
    [os.path.join(cwd, f"particle_age_stats_{i}_-1.csv") for i in range(5)],
    [os.path.join(cwd, f"particle_age_stats_{i}_1.csv") for i in range(5)],
    [os.path.join(cwd, f"particle_age_stats_{i}_2.csv") for i in range(5)]
]

colors_sets = [
    ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple'],
    ['navy', 'darkorange', 'seagreen', 'crimson', 'orchid'],
    ['tab:cyan', 'tab:pink', 'tab:olive', 'tab:brown', 'tab:gray'],
    ['magenta', 'gold', 'darkcyan', 'coral', 'lime']
]

labels_sets = [
    [f'Group 0 - ParticleTracer_{i}' for i in range(5)],
    [f'Group -1 - ParticleTracer_{i}' for i in range(5)],
    [f'Group 1 - ParticleTracer_{i}' for i in range(5)],
    [f'Group 2 - ParticleTracer_{i}' for i in range(5)]
]

markers_sets = [
    ['o', 's', '^', 'D', '*'],
    ['1', '2', '3', '4', '|'],
    ['x', '+', 'v', '<', '>'],
    ['h', 'H', 'd', 'p', '8']
]


overall_ages_all = [[], [], [], []]  # keep ages to compute overall trimmed means per group
"""
csv_sets= [[os.path.join(cwd, f"particle_age_stats_{i}.csv") for i in range(5)]]
colors_sets = [['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple']]
labels_sets = [[f'ParticleTracer_{i}' for i in range(5)]]
markers_sets = [['o', 's', '^', 'D', '*']]

# Create 4 subplots now
#fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(10, 20), sharex=True)
fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(10, 20), sharex=True)
def get_suffix_label(filename):
    if filename.endswith('_1.csv'):
        return "_1"
    elif filename.endswith('_2.csv'):
        return "_2"
    elif filename.endswith('_-1.csv'):
        return "_-1"
    else:
        return "none"

for group_index, csv_files in enumerate(csv_sets):
    ax = axes[group_index]
    group_means_by_injection = defaultdict(list)  # injection_time -> list of means from each tracer
    all_trimmed_ages_group = defaultdict(list)    # injection_time -> all trimmed ages from all tracers
    tracer_labels = []

    for file_idx, (file_path, color, label, marker) in enumerate(zip(csv_files, colors_sets[group_index], labels_sets[group_index], markers_sets[group_index])):
        ages_by_time = defaultdict(list)
        all_ages_for_file = []

        with open(file_path, newline='') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                try:
                    injection_time = float(row["Time of Injection"])
                    age = float(row["Particle age"])
                    exited_count = int(row["Count"])
                except ValueError:
                    print("Could not read columns")
                    continue

                ages_by_time[injection_time].extend([age] * exited_count)

        injection_times = sorted(ages_by_time.keys())
        mean_ages_trimmed = []

        for t in injection_times:
            ages = np.array(ages_by_time[t])
            if len(ages) == 0:
                mean_ages_trimmed.append(np.nan)
                continue
            #lower = np.percentile(ages, 5)
            #upper = np.percentile(ages, 95)
            #trimmed_ages = ages[(ages >= lower) & (ages <= upper)]
            trimmed_ages = ages
            mean_val = trimmed_ages.mean() if len(trimmed_ages) > 0 else np.nan
            mean_ages_trimmed.append(mean_val)
            group_means_by_injection[t].append(mean_val)
            all_trimmed_ages_group[t].extend(trimmed_ages.tolist())

        # Plot as before
        ax.plot(
            injection_times,
            mean_ages_trimmed,
            linestyle='-',
            marker=marker,
            color=color,
            label=f"{label}, Mean: {np.nanmean(mean_ages_trimmed):.3f}s"
        )
        tracer_labels.append(label)

    # --- Write group CSV ---
    output_csv_path = os.path.join(cwd, f"group_{group_index+1}_trimmed_means.csv")
    all_injection_times = sorted(group_means_by_injection.keys())
    # Flatten all trimmed ages for the group
    all_trimmed_ages_group_flat = []
    for t in all_injection_times:
        all_trimmed_ages_group_flat.extend(all_trimmed_ages_group[t])
    group_overall_trimmed_mean = np.mean(all_trimmed_ages_group_flat) if len(all_trimmed_ages_group_flat) > 0 else np.nan

    with open(output_csv_path, 'w', newline='') as out_csv:
        writer = csv.writer(out_csv, delimiter=';')

        header = ["Injection Time (s)"] + tracer_labels + ["All Tracers Mean", "Group Overall Trimmed Mean"]
        writer.writerow(header)
        for t in all_injection_times:
            tracer_means = group_means_by_injection[t]
            all_tracers_ages = all_trimmed_ages_group[t]
            all_tracers_mean = np.mean(all_tracers_ages) if len(all_tracers_ages) > 0 else np.nan
            writer.writerow([t] + [round(x, 5) for x in tracer_means] + [round(all_tracers_mean, 5), round(group_overall_trimmed_mean, 5)])
    
    ax.set_ylabel('Mean Particle Age (s) [5% trimmed]', fontsize=14)
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)
    ax.grid(True)
    ax.legend(fontsize=10)
    if group_index == 0:
        ax.set_title(f'Group 1 - little brownian motion, half of 3 and 4 ', fontsize=15)
    elif group_index == 1:
        ax.set_title(f'Group 2 - no brownian motion', fontsize=15)
    elif group_index == 2:
        ax.set_title(f'Group 3 - brownian motion 1', fontsize=15)
    elif group_index == 3:
        ax.set_title(f'Group 4 - brownian motion 2', fontsize=15)

axes[-1].set_xlabel('Time of Injection (s)', fontsize=14)
plt.tight_layout()
plt.savefig(plot_file, dpi=300)
plt.show()

# Print overall trimmed means per group
for group_index in range(1):
    csv_path = os.path.join(cwd, f"group_{group_index+1}_trimmed_means.csv")
    print(f"Group {group_index + 1} CSV saved to: {csv_path}")
print(f"Styled trimmed plot saved to: {plot_file}")
