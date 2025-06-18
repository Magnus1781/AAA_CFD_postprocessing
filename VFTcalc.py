import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#Bruker 0.1 til 0.4s. 

#Flow rate from t=0.1 to t=0.4s
flow_profile = [
12.96037031799911,
21.50272837238223,
32.58489138543805,
45.57702602720818,
59.741729500673365,
73.96404269260702,
87.09483318877575,
98.09234121,
106.19058193911636,
111.0064374296712,
112.54991412655679,
111.2295156068361,
107.72259168385891,
102.74663253953831,
96.96966029673568,
90.88947664101518,
84.80483923007252,
78.81758366511202,
72.89354390382606,
66.94366374,
60.88886450007489,
54.66510756071173,
48.30776004451827,
41.882283423382454,
35.47676428188346,
29.189389585329327,
23.002326448749407,
16.98736585900085,
11.193188144255167,
5.687741798150034,
0.5498281098952633
]

aorta_flow_rate = np.array(flow_profile) * 1.0e-6  # Convert ml/s to m^3/s

iliac_profile = [
-6.320585659,
-10.56242586,
-16.04160309,
-22.84491771,
-29.93578458,
-37.0691547,
-43.66223049,
-49.18368846,
-53.24834599,
-55.66094488,
-56.42999677,
-55.76037395,
-53.96494807,
-51.4276946,
-48.49282885,
-45.41630241,
-42.34276716,
-39.32990599,
-36.35420647,
-33.37070118,
-30.33055224,
-27.21359821,
-24.02881331,
-20.8107137,
-17.60336071,
-14.44431508,
-11.35702216,
-8.361373829,
-5.474350696,
-2.734988076,
-0.193859936,
]

iliac_flow_rate = np.array(iliac_profile) * 1.0e-6 * (-1) # Convert ml/s to m^3/s and invert sign
 
def compute_vortex_formation_time(time_array, flowrate_array, exit_area_m2):
    """
    Compute vortex formation time (VFT) from tabel of flow rate and a fixed nozzle area
 
    Input parametre:
        time_array (np.ndarray): Time points in seconds
        flowrate_array (np.ndarray): Flow rate Q(t) in m^3/s
        exit_area_m2 (float): Nozzle exit area in m^2
 
    Returnerer:
        L (float): Stroke length in meters
        D (float): Nozzle equivalent diameter in meters
        VFT (float): Vortex formation time (L/D)
    """
    # Compute exit velocity: U(t) = Q(t) / A
    velocity_array = flowrate_array / exit_area_m2
 
    # Integrate U(t) to get stroke length L
    L = np.trapezoid(velocity_array, time_array)

    # Compute nozzle equivalent diameter D
    D = np.sqrt(4 * exit_area_m2 / np.pi)
 
    # Compute vortex formation time
    VFT = L / D
 
    return L, D, VFT
 
# --------------- EXAMPLE OF HOW TO USE ---------------------------------------------
# User needs to define the systolic flow rate as a function of time
# and the exit area, here we use the inlet area at the top of the aneurysm as area
# if the diameter is known instead, just re-caculate the area as A = 0.25*np.pi*D*D
# The last time in the table will be the time constant for the VFT calculation
# -----------------------------------------------------------------------------------

AAA_Area_inlet = {
    "AAA001": 4.43,
    "AAA004": 2.84,
    "AAA013": 1.80,
    "AAA014": 2.06,
    "AAA017": 7.69,
    "AAA023": 3.37,
    "AAA033": 3.96,
    "AAA039": 4.55,
    "AAA042": 3.33,
    "AAA046": 3.66,
    "AAA087": 2.79,
    "AAA088": 2.70,
    "AAA091": 4.44,
    "AAA092": 3.11
}

# Prepare a list to hold each model’s results
results = []


for model in AAA_Area_inlet.keys():

    # Sample time and flow rate (m^3/s) Add table, example uses sinus curve
    time = np.linspace(0, 0.3, len(flow_profile))  # 0 to 0.3 seconds, systole lasts 300 ms
    #Q0        = 500.0e-6         |      # Multiplying by e-6 converts ml -> m3
    #flow_rate = Q0 * np.sin(np.pi * time / 0.25)**2  # Smooth pulse of flow


    """
    # Input nozzle area in m^2 (e.g. circular diameter = 2 cm -> A ≈ 3.14e-4 m^2)
    D_aaa_in = 20.0e-3
    A_aaa_in = 0.25*np.pi*D_aaa_in**2
    """
    #Use the exact inlet area from the AAA model, instead of calculating it from the diameter
    A_aaa_in = AAA_Area_inlet[model] * 1.0e-4  # Convert from cm^2 to m^2

    # Compute
    if model == "AAA013":
        L, D, VFT = compute_vortex_formation_time(time, iliac_flow_rate, A_aaa_in)
        V_tot_systole = np.trapezoid(iliac_flow_rate, time)  # Total flow volume in m^3

    else:
        L, D, VFT = compute_vortex_formation_time(time, aorta_flow_rate, A_aaa_in)
        V_tot_systole = np.trapezoid(aorta_flow_rate, time)  # Total flow volume in m^3
    print(f"Model: {model}")
    print(f"Stroke length             L  = {L:.4f} m")
    print(f"AAA throat diameter       D  = {D:.4f} m")
    print(f"Vortex Formation Time (L/D)  = {VFT:.2f}")
    # Convert total flow to mL
    V_tot_ml = V_tot_systole * 1e6
    print(f"Total flow volume in systoli = {V_tot_ml:.6f} ml")
    print("-" * 50)

    # Append a dict of results
    results.append({
        "Model":              model,
        "StrokeLength_m":     L,
        "ThroatDiameter_m":   D,
        "VortexFormationTime": VFT,
        "TotalFlow_ml":       V_tot_ml
    })

    # For debugging: plot flow rate and velocity
    """
    velocity = flow_rate / A_aaa_in
    plt.figure(figsize=(10,5))
    plt.subplot(1,2,1)
    plt.plot(time, flow_rate*1e6)
    plt.title("Flow Rate Q(t)")
    plt.ylabel("Flow rate [ml/s]")
    plt.xlabel("Time [s]")
    
    plt.subplot(1,2,2)
    plt.plot(time, velocity)
    plt.title("Exit Velocity U(t)")
    plt.ylabel("Velocity [m/s]")
    plt.xlabel("Time [s]")
    
    plt.tight_layout()
    plt.show()
    """

# Build a DataFrame
df = pd.DataFrame(results,
                  columns=["Model", "StrokeLength_m", "ThroatDiameter_m",
                           "VortexFormationTime", "TotalFlow_ml"])

# Write to CSV
outpath = r"C:\Users\magnuswe\OneDrive - SINTEF\Dokumenter\vft_results.csv"
df.to_csv(outpath, sep=";", index=False)
print(f"Results saved to {outpath}")