"""

@author: Magnus Wennemo

"""

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
AAA033 = "AAA033_sim_0-15_2mill"
AAA039 = "AAA039_sim_0-15_1-9mill"
AAA042 = "AAA042_0-18_1-9mill"
AAA046 = "AAA046_sim_0-17_1-5mill"
AAA087 = "AAA087_sim_0-15_1-6mill"
AAA088 = "AAA088_sim_0-15_1-7mill"
AAA091 = "AAA091_sim_0-15_1-5mill"
AAA092 = "AAA092_sim_0-15_1mill"

model = AAA001

cwd = f"C:/Users/magnuswe/OneDrive - SINTEF/Simvascular/results/two_last_cycles/{model}-two_last_cycles/"

# Plot config
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 14
})

plot_file = os.path.join(cwd, "particle_age_plot.png")
csv_paths = [os.path.join(cwd, f"particle_age_stats_{i}.csv") for i in range(5)]
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple']
labels = [f'ParticleTracer_{i}' for i in range(5)]
markers = ['o', 's', '^', 'D', '*']


# … your existing plotting code goes here …



# --- 2) Sanity‐check: totalCount == 95 * count(injectionTime==0) ---
total_count = 0
zero_count  = 0
for path in csv_paths:
    with open(path, newline='') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            cnt = int(row["Count"])
            it  = float(row["Time of Injection"])
            total_count += cnt
            if it == 0.0:
                zero_count += cnt

expected = zero_count * 95
print(f"✓ Total particles = {total_count},",
      f"95×zero-injection = {expected}")
if total_count == expected:
    print("✔️  Check passed")
else:
    print("❌  MISMATCH!")


fig, ax = plt.subplots(figsize=(10, 6))
group_means_by_injection = defaultdict(list)
all_trimmed_ages_group = defaultdict(list)
tracer_labels = []

for i, (path, color, label, marker) in enumerate(zip(csv_paths, colors, labels, markers)):
    ages_by_time = defaultdict(list)

    with open(path, newline='') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            try:
                injection_time = float(row["Time of Injection"])
                age = float(row["Particle age"])
                exited_count = int(row["Count"])
            except ValueError:
                print("Error with reading data: ", ValueError)
                continue
            ages_by_time[injection_time].extend([age] * exited_count)

    injection_times = sorted(ages_by_time.keys())
    mean_ages_trimmed = []

    for t in injection_times:
        ages = np.array(ages_by_time[t])
        if len(ages) >= 20:  # Ensure there are enough samples to trim meaningfully
            lower = np.percentile(ages, 5)
            upper = np.percentile(ages, 95)
            trimmed_ages = ages[(ages >= lower) & (ages <= upper)]
        else:
            print("Not enough data to have a 10 percent trim")
            trimmed_ages = ages  # Skip trimming if too few values
        mean_val = trimmed_ages.mean() if len(trimmed_ages) > 0 else np.nan
        mean_ages_trimmed.append(mean_val)
        group_means_by_injection[t].append(mean_val)
        all_trimmed_ages_group[t].extend(trimmed_ages.tolist())

    ax.plot(
        injection_times,
        mean_ages_trimmed,
        linestyle='-',
        marker=marker,
        color=color,
        label=f"{label}, Mean: {np.nanmean(mean_ages_trimmed):.3f}s"
    )
    ax.set_yscale('log')
    tracer_labels.append(label)

# Save summary CSV
output_csv_path = os.path.join(cwd, "particle_age_final_stats.csv")
all_injection_times = sorted(group_means_by_injection.keys())
all_trimmed_ages_flat = [age for t in all_injection_times for age in all_trimmed_ages_group[t]]
overall_trimmed_mean = np.mean(all_trimmed_ages_flat)

with open(output_csv_path, 'w', newline='') as out_csv:
    writer = csv.writer(out_csv, delimiter=';')
    writer.writerow(["Injection Time (s)"] + tracer_labels + ["All Tracers Mean", "Trimmed Mean"])
    for t in all_injection_times:
        tracer_means = group_means_by_injection[t]
        all_mean = np.mean(all_trimmed_ages_group[t])
        writer.writerow([t] + [round(x, 5) for x in tracer_means] + [round(all_mean, 5), round(overall_trimmed_mean, 5)])

# Finalize plot
ax.set_title(f"{model} - Mean Particle Age", fontsize=15)
ax.set_xlabel("Time of Injection (s)")
ax.set_ylabel("Mean Particle Age (s)")
ax.axhline(0, color='black', linewidth=1)
ax.axvline(0, color='black', linewidth=1)
ax.grid(True)
ax.legend(fontsize=10)
plt.tight_layout()
plt.savefig(plot_file, dpi=300)
plt.show()

# Log output
print(f"Group CSV saved to: {output_csv_path}")
print(f"Plot saved to: {plot_file}")
