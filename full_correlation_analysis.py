
import pandas as pd
from scipy.stats import pearsonr, spearmanr
import numpy as np
import matplotlib.pyplot as plt
import itertools
import os
# Load Excel data
file_path = r"C:\Users\magnuswe\OneDrive - SINTEF\Dokumenter\Parametere_table_for_plotting_statistics.xlsx"
df = pd.read_excel(file_path)

# Drop fully empty columns and rows
df = df.dropna(axis=1, how='all').dropna(how='all')

# Rename columns for consistency
df.columns = ["Patient", "WSS_min_aorta", "WSS_max_aorta", "WSS_min_aneurysm", "WSS_max_aneurysm",
    "TAWSS_mean_aorta", "TAWSS_mean_aneurysm", "LSA", "HOSA", "KE", "VFT",
    "Tortuosity", "Volume", "D_max", "D_max_hyd", "D_max_hyd_by_D_min_hyd", "Beta", "Alpha"
]

# Drop non-numeric for analysis
df_numeric = df.drop(columns=["Patient"])

# Prepare results list
results = []

# Compute all pairwise correlations
for x_param, y_param in itertools.combinations(df_numeric.columns, 2):
    df_pair = df_numeric[[x_param, y_param]].dropna()
    if df_pair.shape[0] > 2:
        pearson_r, pearson_p = pearsonr(df_pair[x_param], df_pair[y_param])
        spearman_r, spearman_p = spearmanr(df_pair[x_param], df_pair[y_param])
        results.append({
            "Parameter_X": x_param,
            "Parameter_Y": y_param,
            "Pearson_r": round(pearson_r, 3),
            "Pearson_p": round(pearson_p, 5),
            "Spearman_rho": round(spearman_r, 3),
            "Spearman_p": round(spearman_p, 5),
            "N": df_pair.shape[0]
        })

# Convert to DataFrame
results_df = pd.DataFrame(results)

# Get the directory of the Excel file
output_dir = os.path.dirname(file_path)

# Create full path for new CSV file
output_path = os.path.join(output_dir, "parameter_correlations_without_iliac_an.csv")

# Save the CSV
results_df.to_csv(output_path, index=False, sep=";")

print(f"Correlation analysis complete. Results saved to: {output_path}")


# Filter strong correlations
strong_corrs = results_df[results_df["Pearson_r"].abs() > 0.8]

# Prepare plot
num_plots = strong_corrs.shape[0]
if num_plots == 0:
    print("No strong correlations (|r| > 0.8) found.")
else:
    cols = 3  # adjust based on preferred layout
    rows = int(np.ceil(num_plots / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(6 * cols, 5 * rows))
    axes = axes.flatten()

    for i, (_, row) in enumerate(strong_corrs.iterrows()):
        x_param = row["Parameter_X"]
        y_param = row["Parameter_Y"]
        ax = axes[i]

        # Drop NaNs for the two parameters
        plot_data = df_numeric[[x_param, y_param]].dropna()

        # Scatter plot
        ax.scatter(plot_data[x_param], plot_data[y_param], alpha=0.7)
        
        # Regression line
        m, b = np.polyfit(plot_data[x_param], plot_data[y_param], 1)
        ax.plot(plot_data[x_param], m * plot_data[x_param] + b, color='red')

        # Titles and labels
        ax.set_title(f"{x_param} vs {y_param}\nPearson r = {row['Pearson_r']}")
        ax.set_xlabel(x_param)
        ax.set_ylabel(y_param)

    # Hide unused subplots
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()

    # Filter strong Spearman correlations
strong_spearman = results_df[results_df["Spearman_rho"].abs() > 0.8]

# Prepare plot
num_plots = strong_spearman.shape[0]
if num_plots == 0:
    print("No strong Spearman correlations (|rho| > 0.8) found.")
else:
    cols = 3  # adjust as needed
    rows = int(np.ceil(num_plots / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(6 * cols, 5 * rows))
    axes = axes.flatten()

    for i, (_, row) in enumerate(strong_spearman.iterrows()):
        x_param = row["Parameter_X"]
        y_param = row["Parameter_Y"]
        ax = axes[i]

        # Drop NaNs for the two parameters
        plot_data = df_numeric[[x_param, y_param]].dropna()

        # Scatter plot
        ax.scatter(plot_data[x_param], plot_data[y_param], alpha=0.7)

        # Since Spearman is rank-based, no regression line is strictly necessary,
        # but we can still draw a trend line if desired
        m, b = np.polyfit(plot_data[x_param], plot_data[y_param], 1)
        ax.plot(plot_data[x_param], m * plot_data[x_param] + b, color='green')

        # Titles and labels
        ax.set_title(f"{x_param} vs {y_param}\nSpearman ρ = {row['Spearman_rho']}")
        ax.set_xlabel(x_param)
        ax.set_ylabel(y_param)

    # Hide unused subplots
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()
