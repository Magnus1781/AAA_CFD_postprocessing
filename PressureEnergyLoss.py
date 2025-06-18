import pandas as pd
import numpy as np
import os
import csv
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

models = [AAA001,
AAA004,
AAA013,
AAA014,
AAA017,
AAA023,
AAA033,
AAA039,
AAA042,
AAA046,
AAA087,
AAA088,
AAA091,
AAA092]

from_dyn_to_pascal = 1e-1
from_ml_to_m3 = 1e-6
from_J_to_mJ = 1e3
results = []

for model in models:
    cwd = f"C:/Users/magnuswe/OneDrive - SINTEF/Simvascular/results/{model}-6cycles/"
    
    # --- Load CSV files with the correct delimiter ---
    p_aorta = pd.read_csv(os.path.join(cwd, "p_avg_aorta.csv"), delimiter=';')
    p_left = pd.read_csv(os.path.join(cwd, "p_avg_left.csv"), delimiter=';')
    p_right = pd.read_csv(os.path.join(cwd, "p_avg_right.csv"), delimiter=';')

    q_aorta = pd.read_csv(os.path.join(cwd,"surface_flow_aorta.csv"), delimiter=';') #Trenger egentlig ikke denne
    q_left = pd.read_csv(os.path.join(cwd,"surface_flow_left.csv"), delimiter=';')
    q_right = pd.read_csv(os.path.join(cwd, "surface_flow_right.csv"), delimiter=';')

    # --- Extract the last 95 values (1 full cycle assumed) ---
    # Pressure is in dynes/cm2
    p_in = p_aorta['Pressure'].iloc[-95:].reset_index(drop=True) * from_dyn_to_pascal
    p_out_left = p_left['Pressure'].iloc[-95:].reset_index(drop=True) * from_dyn_to_pascal
    p_out_right = p_right['Pressure'].iloc[-95:].reset_index(drop=True) * from_dyn_to_pascal
    
    # Flow is in ml
    q_aorta_last = q_aorta['Flow'].iloc[-95:].reset_index(drop=True) * from_ml_to_m3 #Trenger egentlig ikke denne
    q_left_last = q_left['Flow'].iloc[-95:].reset_index(drop=True) * from_ml_to_m3
    q_right_last = q_right['Flow'].iloc[-95:].reset_index(drop=True) * from_ml_to_m3

    # --- Ensure outflows are positive ---
    if q_left_last.mean() < 0:
        q_left_last *= -1
    if q_right_last.mean() < 0:
        q_right_last *= -1
    # --- Ensure inflow is also postive ---
    if q_aorta_last.mean() < 0:
        q_aorta_last *= -1
    # --- Determine time step from the inlet pressure time series ---
    time = p_aorta['Time'].iloc[-95:].astype(float).reset_index(drop=True) / 100 #convert from 95 to 0.95 s
    delta_t = np.mean(np.diff(time))  # Assumes uniform spacing


#-----------------------------------------------
#           First calculation
#-----------------------------------------------

    # --- Compute instantaneous pressure differences ---
    dp_left = p_in - p_out_left
    dp_right = p_in - p_out_right

    # --- Compute pressure work for each outlet: W = sum(ΔP * Q * Δt) ---
    work_left = np.sum(dp_left * q_left_last * delta_t) * from_J_to_mJ
    work_right = np.sum(dp_right * q_right_last * delta_t) * from_J_to_mJ

    # --- Total work ---
    total_work = work_left + work_right
    
    # --- Output results ---
    print(f"Model: {model[:6]}")
    print(f"Pressure work (left):  {work_left:.2f} mJ")
    print(f"Pressure work (right): {work_right:.2f} mJ")
    print(f"Total pressure work:   {total_work:.2f} mJ")

#-----------------------------------------------
#           Second calculation
#-----------------------------------------------
    #####Another calculation for verification##########
    T = time.iloc[-1] - time.iloc[0]

    # --- Calculate Q*P*dt/T for aorta and outflows ---
    qpdt_aorta = np.sum(q_aorta_last * p_in * delta_t) * from_J_to_mJ
    qpdt_left = np.sum(q_left_last * p_out_left * delta_t) * from_J_to_mJ
    qpdt_right = np.sum(q_right_last * p_out_right * delta_t) * from_J_to_mJ

    qpdt_out_sum = qpdt_left + qpdt_right
    qpdt_drop = qpdt_aorta - qpdt_out_sum

    # --- Output results ---
    print(f"QP_aorta (sum Q*P*dt):      {qpdt_aorta:.2f} mJ")
    print(f"QP_outflows (sum Q*P*dt):   {qpdt_out_sum:.2f} mJ")
    print(f"QP_drop (aorta - outflows): {qpdt_drop:.2f} mJ")



    # --- Store all results ---
    results.append({
        "Model": model[:6],
        "Pressure_work_left": round(work_left, 2),
        "Pressure_work_right": round(work_right, 2),
        "Total_pressure_work": round(total_work, 2),
        "QP_aorta_per_T": round(qpdt_aorta, 4),
        "QP_outflows_per_T": round(qpdt_out_sum, 4),
        "QP_drop": round(qpdt_drop, 4)
    })


# --- Write results to CSV in cwd ---
output_csv = r"C:/Users/magnuswe/OneDrive - SINTEF/Dokumenter/pressure_energy_loss.csv"
with open(output_csv, "w", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "Model",
            "Pressure_work_left",
            "Pressure_work_right",
            "Total_pressure_work",
            "QP_aorta_per_T",
            "QP_outflows_per_T",
            "QP_drop"
        ],
        delimiter=";"
    )
    writer.writeheader()
    writer.writerows(results)
print(f"Results saved to {output_csv}")