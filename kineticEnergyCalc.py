import pandas as pd
import os
import numpy as np
# Load CSV files

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

model = AAA013

cwd = f"C:/Users/magnuswe/OneDrive - SINTEF/Simvascular/results/last_cycle/{model}-last_cycle/"
data_file = os.path.join(cwd, 'KE_data_at_t=20.0.csv')  # CSV file with slice points
data = pd.read_csv(data_file)  # Assume column 'Velocity'


# Extract columns
velocities = data['velocity_Magnitude'].to_numpy()
velocities *= 1e-2  # Convert cm/s to m/s
cell_volumes = data['Volume'].to_numpy()*-1
cell_volumes *= 1e-6 # Convert cm^3 to m^3
# Blood density
rho = 1060

# Compute KE
KE = 0.5 * rho * np.sum((velocities ** 2) * cell_volumes)

#deviding the KE bu the total volume
total_volume = np.sum(cell_volumes)
KE_per_vol = KE/total_volume
# Print the result
print(f"Total Volume: {total_volume:.6e} m^3")
print(f"Total Volume: {total_volume*1e6} cm^3")
print(f"Total Kinetic Energy: {KE:.6e} J")
print(f"Total Kinetic Energy per unit volume: {KE_per_vol:.6e} J/m^3")

results = {
    'Total Volume (m^3)': [total_volume],
    'Total Volume (cm^3)': [total_volume*1e6],
    'Total Kinetic Energy (J)': [KE],
    'Kinetic Energy per Volume (J/m^3)': [KE_per_vol]
}

results_df = pd.DataFrame(results)
output_file = os.path.join(cwd, 'kinetic_energy_and_volume_results.csv')
results_df.to_csv(output_file, sep=';', index=False)
print(f"Results saved to {output_file}")