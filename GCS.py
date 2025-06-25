import pandas as pd
from pyGCS import GCS, GCI

# ---- File paths ----
file_500k = r"C:\Users\magnuswe\OneDrive - SINTEF\Simvascular\results\last_cycle\AAA001_sim_0,26_500k-6th_cycle\all_results-flows.txt"
file_1_1mill = r"C:\Users\magnuswe\OneDrive - SINTEF\Simvascular\results\last_cycle\AAA001_sim_0-19_1-1mill-last_cycle\all_results-flows.txt"
file_2_5mill = r"C:\Users\magnuswe\OneDrive - SINTEF\Simvascular\results\last_cycle\AAA001_sim_0,14_2,5mill-last_cycle\all_results-flows.txt"

# ---- Mesh and volume info ----
cells_geo = [2465237, 1102627, 493360]
volume_geo = 325.30233

# ---- Read and parse all files ----
df_500k = pd.read_csv(file_500k, delimiter='\t')
df_1_1mill = pd.read_csv(file_1_1mill, delimiter='\t')
df_2_5mill = pd.read_csv(file_2_5mill, delimiter='\t')

# ---- Ensure all files have the same steps ----
assert list(df_500k['step']) == list(df_1_1mill['step']) == list(df_2_5mill['step']), "Timestep mismatch"

# ---- Containers for results ----
p_values = []
gci_values = []

# ---- Loop over all rows and only iliac columns ----
for idx in range(len(df_500k)):
    for col in ['left_iliac', 'right_iliac']:  # inflow excluded
        s_500k = df_500k.iloc[idx][col]
        s_1_1mill = df_1_1mill.iloc[idx][col]
        s_2_5mill = df_2_5mill.iloc[idx][col]

        solutions = [s_2_5mill, s_1_1mill, s_500k]

        gcs = GCS(dimension=3, simulation_order=2, volume=volume_geo, cells=cells_geo, solution=solutions)
        gci = GCI(dimension=3, simulation_order=2, volume=volume_geo, cells=cells_geo, solution=solutions)

        p_values.append(gci.get('apparent_order'))
        gci_values.extend(gci.get('gci'))

        # Optional: export table
        # table_path = f'GCS_step{idx+1}_{col}'
        # gcs.print_table(output_type='markdown', output_path=table_path)

# ---- Final stats ----
average_p = sum(p_values) / len(p_values)
average_gci = sum(gci_values) / len(gci_values)

print(f"Average p value (iliac only): {average_p}")
print(f"Average GCI error value (iliac only): {average_gci}")
