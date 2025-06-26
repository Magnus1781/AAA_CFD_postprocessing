"""

@author: Magnus Wennemo

"""
import pandas as pd
from pyGCS import GCS, GCI
import os
import numpy as np

# ─────────────────────────────────────────────────────────────────────────────
# 1) Paths & mesh info
# ─────────────────────────────────────────────────────────────────────────────
file_500k    = r"C:\Users\magnuswe\OneDrive - SINTEF\Simvascular\results\last_cycle\AAA001_sim_0,26_500k-6th_cycle"
file_1_1mill = r"C:\Users\magnuswe\OneDrive - SINTEF\Simvascular\results\last_cycle\AAA001_sim_0-19_1-1mill-last_cycle"
file_2_5mill = r"C:\Users\magnuswe\OneDrive - SINTEF\Simvascular\results\last_cycle\AAA001_sim_0,14_2,5mill-last_cycle"

# Mesh info (fine → medium → coarse)
cells_geo = [2465237, 1102627, 493360]
volume_geo = 325.30233  # Geometric domain volume in mm³

# ─────────────────────────────────────────────────────────────────────────────
# 2) Helper: load mean‐WSS per time step
# ─────────────────────────────────────────────────────────────────────────────
def load_mean_wss_per_timestep(file_path, sep=';'):
    """
    Load a WSS CSV and compute mean WSS at each time step.
    Returns a pandas Series: index = time labels, values = mean WSS.
    """
    df = pd.read_csv(file_path, sep=sep)
    return df.mean(axis=0)

# ─────────────────────────────────────────────────────────────────────────────
# 3) Load mean WSS for each mesh & each region
# ─────────────────────────────────────────────────────────────────────────────
mean_wss_500k_aorta    = load_mean_wss_per_timestep(os.path.join(file_500k,    "WSS_full_time_series_aorta.csv"))
mean_wss_1_1mill_aorta = load_mean_wss_per_timestep(os.path.join(file_1_1mill, "WSS_full_time_series_aorta.csv"))
mean_wss_2_5mill_aorta = load_mean_wss_per_timestep(os.path.join(file_2_5mill, "WSS_full_time_series_aorta.csv"))

mean_wss_500k_aneurysm    = load_mean_wss_per_timestep(os.path.join(file_500k,    "WSS_full_time_series_aneurysm.csv"))
mean_wss_1_1mill_aneurysm = load_mean_wss_per_timestep(os.path.join(file_1_1mill, "WSS_full_time_series_aneurysm.csv"))
mean_wss_2_5mill_aneurysm = load_mean_wss_per_timestep(os.path.join(file_2_5mill, "WSS_full_time_series_aneurysm.csv"))

# ─────────────────────────────────────────────────────────────────────────────
# 4) NEW: Top‐N WSS at time=20 → compute GCI from those means
# ─────────────────────────────────────────────────────────────────────────────
#
# We assume each CSV has a column header exactly "20" (string). If your
# CSV uses "20.00" or something else, change the following line accordingly:
time_label = "20.00"

# Load the raw DataFrames (so we can pick top‐N by value)
df_500k_aorta    = pd.read_csv(os.path.join(file_500k,    "WSS_full_time_series_aorta.csv"),    sep=';')
df_1_1mill_aorta = pd.read_csv(os.path.join(file_1_1mill, "WSS_full_time_series_aorta.csv"),    sep=';')
df_2_5mill_aorta = pd.read_csv(os.path.join(file_2_5mill, "WSS_full_time_series_aorta.csv"),    sep=';')

df_500k_aner    = pd.read_csv(os.path.join(file_500k,    "WSS_full_time_series_aneurysm.csv"), sep=';')
df_1_1mill_aner = pd.read_csv(os.path.join(file_1_1mill, "WSS_full_time_series_aneurysm.csv"), sep=';')
df_2_5mill_aner = pd.read_csv(os.path.join(file_2_5mill, "WSS_full_time_series_aneurysm.csv"), sep=';')

# Ensure the column exists
if time_label not in df_500k_aorta.columns or \
   time_label not in df_1_1mill_aorta.columns or \
   time_label not in df_2_5mill_aorta.columns:
    raise KeyError(f"Time column '{time_label}' not found in one of the aorta CSVs.")

if time_label not in df_500k_aner.columns or \
   time_label not in df_1_1mill_aner.columns or \
   time_label not in df_2_5mill_aner.columns:
    raise KeyError(f"Time column '{time_label}' not found in one of the aneurysm CSVs.")

# Convert that column to Pa (divide by 10) and drop zeros
wss_500k_aorta_vals    = df_500k_aorta[time_label].astype(float).replace(0.0, np.nan).dropna() / 10.0
wss_1_1mill_aorta_vals = df_1_1mill_aorta[time_label].astype(float).replace(0.0, np.nan).dropna() / 10.0
wss_2_5mill_aorta_vals = df_2_5mill_aorta[time_label].astype(float).replace(0.0, np.nan).dropna() / 10.0

wss_500k_aner_vals    = df_500k_aner[time_label].astype(float).replace(0.0, np.nan).dropna() / 10.0
wss_1_1mill_aner_vals = df_1_1mill_aner[time_label].astype(float).replace(0.0, np.nan).dropna() / 10.0
wss_2_5mill_aner_vals = df_2_5mill_aner[time_label].astype(float).replace(0.0, np.nan).dropna() / 10.0

# Define which top‐N we want:
top_ns = [1, 5, 10, 20, 50, 100]

# Prepare results storage
topN_records = []

for region_name, (coarse_vals, med_vals, fine_vals) in [
    ("Aorta",    (wss_500k_aorta_vals,    wss_1_1mill_aorta_vals,    wss_2_5mill_aorta_vals)),
    ("Aneurysm", (wss_500k_aner_vals,     wss_1_1mill_aner_vals,     wss_2_5mill_aner_vals))
]:
    for N in top_ns:
        # For each mesh, take the top N values (largest N), then compute their mean:
        coarse_topN = coarse_vals.nlargest(N) if len(coarse_vals) >= N else coarse_vals
        med_topN    = med_vals.nlargest(N)    if len(med_vals)    >= N else med_vals
        fine_topN   = fine_vals.nlargest(N)   if len(fine_vals)   >= N else fine_vals

        mean_coarse = coarse_topN.mean()
        mean_med    = med_topN.mean()
        mean_fine   = fine_topN.mean()

        # Convert to floats
        mean_coarse = float(mean_coarse)
        mean_med    = float(mean_med)
        mean_fine   = float(mean_fine)

        # Compute GCI on these three means:
        solutions = [mean_fine, mean_med, mean_coarse]
        gci_calc = GCI(
            dimension=3,
            simulation_order=2,
            volume=volume_geo,
            cells=cells_geo,
            solution=solutions
        )
        p_val, = [gci_calc.get("apparent_order")]
        gci_12, gci_23 = gci_calc.get("gci")

        topN_records.append({
            "region": region_name,
            "N": N,
            "mean_fine":   round(mean_fine,   6),
            "mean_med":    round(mean_med,    6),
            "mean_coarse": round(mean_coarse, 6),
            "apparent_order_p":     p_val,
            "GCI_coarse_to_medium": gci_12,
            "GCI_medium_to_fine":   gci_23
        })

# Write top‐N GCI results to CSV
topN_df = pd.DataFrame(topN_records)
topN_df.to_csv("GCI_topN_at_time20.csv", sep=";", index=False)
print("Wrote GCI_topN_at_time20.csv")


# ─────────────────────────────────────────────────────────────────────────────
# 5) Compute overall mean WSS across all timesteps for each mesh,
#    then calculate a single GCI from those three overall means
# ─────────────────────────────────────────────────────────────────────────────
overall_mean_aorta_coarse = mean_wss_500k_aorta.mean()
overall_mean_aorta_med    = mean_wss_1_1mill_aorta.mean()
overall_mean_aorta_fine   = mean_wss_2_5mill_aorta.mean()

overall_mean_aneurysm_coarse = mean_wss_500k_aneurysm.mean()
overall_mean_aneurysm_med    = mean_wss_1_1mill_aneurysm.mean()
overall_mean_aneurysm_fine   = mean_wss_2_5mill_aneurysm.mean()

aorta_coarse = float(overall_mean_aorta_coarse)
aorta_med    = float(overall_mean_aorta_med)
aorta_fine   = float(overall_mean_aorta_fine)

aneurysm_coarse = float(overall_mean_aneurysm_coarse)
aneurysm_med    = float(overall_mean_aneurysm_med)
aneurysm_fine   = float(overall_mean_aneurysm_fine)

# Compute single‐value GCI for aorta
solutions_aorta       = [aorta_fine, aorta_med, aorta_coarse]
gci_aorta_overall     = GCI(dimension=3,
                           simulation_order=2,
                           volume=volume_geo,
                           cells=cells_geo,
                           solution=solutions_aorta)
p_val_aorta_overall, = [gci_aorta_overall.get("apparent_order")]  # unpack
gci_aorta_12_overall, gci_aorta_23_overall = gci_aorta_overall.get("gci")

# Compute single‐value GCI for aneurysm
solutions_aneurysm       = [aneurysm_fine, aneurysm_med, aneurysm_coarse]
gci_aneurysm_overall     = GCI(dimension=3,
                               simulation_order=2,
                               volume=volume_geo,
                               cells=cells_geo,
                               solution=solutions_aneurysm)
p_val_aneurysm_overall, = [gci_aneurysm_overall.get("apparent_order")]
gci_aneurysm_12_overall, gci_aneurysm_23_overall = gci_aneurysm_overall.get("gci")

print("=== Overall GCI from mean‐WSS across all timesteps ===")
print(f"Aorta overall mean WSS   (fine, med, coarse): "
      f"{aorta_fine:.6f}, {aorta_med:.6f}, {aorta_coarse:.6f}")
print(f"  Apparent order p       = {p_val_aorta_overall:.4f}")
print(f"  GCI coarse→medium      = {gci_aorta_12_overall:.6f}")
print(f"  GCI medium→fine        = {gci_aorta_23_overall:.6f}\n")

print(f"Aneurysm overall mean WSS (fine, med, coarse): "
      f"{aneurysm_fine:.6f}, {aneurysm_med:.6f}, {aneurysm_coarse:.6f}")
print(f"  Apparent order p       = {p_val_aneurysm_overall:.4f}")
print(f"  GCI coarse→medium      = {gci_aneurysm_12_overall:.6f}")
print(f"  GCI medium→fine        = {gci_aneurysm_23_overall:.6f}\n")

# ─────────────────────────────────────────────────────────────────────────────
# 6) Compute GCI for AORTA per timestep and store results
# ─────────────────────────────────────────────────────────────────────────────
aorta_records = []

for time in mean_wss_500k_aorta.index:
    wss_coarse_pd = mean_wss_500k_aorta[time]
    wss_medium_pd = mean_wss_1_1mill_aorta[time]
    wss_fine_pd   = mean_wss_2_5mill_aorta[time]

    wss_coarse = float(wss_coarse_pd)
    wss_medium = float(wss_medium_pd)
    wss_fine   = float(wss_fine_pd)

    solutions = [wss_fine, wss_medium, wss_coarse]
    gci = GCI(
        dimension=3,
        simulation_order=2,
        volume=volume_geo,
        cells=cells_geo,
        solution=solutions
    )

    p_val = gci.get("apparent_order")
    gci_12, gci_23 = gci.get("gci")

    aorta_records.append({
        "time_s": float(time),
        "wss_fine":   round(wss_fine,   6),
        "wss_medium": round(wss_medium, 6),
        "wss_coarse": round(wss_coarse, 6),
        "apparent_order_p":     p_val,
        "GCI_coarse_to_medium": gci_12,
        "GCI_medium_to_fine":   gci_23
    })

# Write Aorta per‐timestep GCI to CSV
aorta_df = pd.DataFrame(aorta_records)
aorta_df.to_csv("GCI_results_aorta.csv", sep=";", index=False)
print("Wrote GCI_results_aorta.csv")

# ─────────────────────────────────────────────────────────────────────────────
# 7) Compute GCI for ANEURYSM per timestep and store results
# ─────────────────────────────────────────────────────────────────────────────
aneurysm_records = []

for time in mean_wss_500k_aneurysm.index:
    wss_coarse_pd = mean_wss_500k_aneurysm[time]
    wss_medium_pd = mean_wss_1_1mill_aneurysm[time]
    wss_fine_pd   = mean_wss_2_5mill_aneurysm[time]

    wss_coarse = float(wss_coarse_pd)
    wss_medium = float(wss_medium_pd)
    wss_fine   = float(wss_fine_pd)

    solutions = [wss_fine, wss_medium, wss_coarse]
    gci = GCI(
        dimension=3,
        simulation_order=2,
        volume=volume_geo,
        cells=cells_geo,
        solution=solutions
    )

    p_val = gci.get("apparent_order")
    gci_12, gci_23 = gci.get("gci")

    aneurysm_records.append({
        "time_s": float(time),
        "wss_fine":   round(wss_fine,   6),
        "wss_medium": round(wss_medium, 6),
        "wss_coarse": round(wss_coarse, 6),
        "apparent_order_p":     p_val,
        "GCI_coarse_to_medium": gci_12,
        "GCI_medium_to_fine":   gci_23
    })

# Write Aneurysm per‐timestep GCI to CSV
aneurysm_df = pd.DataFrame(aneurysm_records)
aneurysm_df.to_csv("GCI_results_aneurysm.csv", sep=";", index=False)
print("Wrote GCI_results_aneurysm.csv")

# ─────────────────────────────────────────────────────────────────────────────
# 8) Calculate and print mean apparent‐order (and GCI) across all timesteps
# ─────────────────────────────────────────────────────────────────────────────
aorta_df["apparent_order_p"] = pd.to_numeric(aorta_df["apparent_order_p"], errors="coerce")
aneurysm_df["apparent_order_p"] = pd.to_numeric(aneurysm_df["apparent_order_p"], errors="coerce")

mean_p_aorta     = aorta_df["apparent_order_p"].mean()
mean_gci_aorta12 = aorta_df["GCI_coarse_to_medium"].mean()
mean_gci_aorta23 = aorta_df["GCI_medium_to_fine"].mean()

mean_p_aneurysm     = aneurysm_df["apparent_order_p"].mean()
mean_gci_aneurysm12 = aneurysm_df["GCI_coarse_to_medium"].mean()
mean_gci_aneurysm23 = aneurysm_df["GCI_medium_to_fine"].mean()

print("\n===== PER‐TIMESTEP SUMMARY =====")
print(f"Aorta:     mean(apparent_order_p)     = {mean_p_aorta:.4f}")
print(f"           mean(GCI coarse→medium)   = {mean_gci_aorta12:.6f}")
print(f"           mean(GCI medium→fine)     = {mean_gci_aorta23:.6f}")

print(f"Aneurysm:  mean(apparent_order_p)     = {mean_p_aneurysm:.4f}")
print(f"           mean(GCI coarse→medium)   = {mean_gci_aneurysm12:.6f}")
print(f"           mean(GCI medium→fine)     = {mean_gci_aneurysm23:.6f}")
