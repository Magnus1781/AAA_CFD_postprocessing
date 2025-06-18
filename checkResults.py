import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import os
import numpy as np

AAA001 = "AAA001_sim_0-19_1-1mill"

AAAfine = "AAA001_sim_0,14_2,5mill"
AAAcourse = "AAA001_sim_0,26_500k"

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
# -----------------------
# Matplotlib "paper" style
# -----------------------
plt.rcParams.update({
    "font.family":       "serif",
    "font.serif":        ["Times New Roman","Palatino","serif"],
    "font.size":         14,    # base font size
    "axes.titlesize":    14,    # axes title
    "axes.labelsize":    14,    # x and y labels
    "xtick.labelsize":   12,
    'lines.linewidth':   1.5,   # makes all plot lines thicker by default
    "ytick.labelsize":   12,
    "legend.fontsize":   12,
    "figure.titlesize":  16,
    "axes.grid":         True,
    "grid.linestyle":    "--",
    "grid.alpha":        0.5,
})

results_list = []

# Change this variable to switch model
for model in [AAA001, AAA004, AAA013, AAA014, AAA017, AAA023, AAA033, AAA039, AAA042, AAA046, AAA087, AAA088, AAA091, AAA092]:
    cwd = f"C:/Users/magnuswe/OneDrive - SINTEF/Simvascular/results/{model}-6cycles/"
    print(f"Processing model: {model}")
    def load_slice_data(slice_name):
        """Load flow and pressure data for a specific slice."""
        flow_file = os.path.join(cwd, f"surface_flow_{slice_name}.csv")
        pressure_file = os.path.join(cwd, f"p_avg_{slice_name}.csv")

        # Load flow data
        flow_res = pd.read_csv(flow_file, sep=";")
        flow = flow_res['Flow'].to_numpy()

        # Load pressure data
        pressure_res = pd.read_csv(pressure_file, sep=";")
        pressure = pressure_res['Pressure'].to_numpy() / 1333.22  # Convert to mmHg

        return flow, pressure

    # Define slices
    slices = ['aorta', 'left', 'right']

    # Load data for each slice
    data = {}
    for slice_name in slices:
        flow, pressure = load_slice_data(slice_name)
        data[slice_name] = {'flow': flow, 'pressure': pressure}

    # Assume all slices have the same length
    time_length = len(data['aorta']['flow'])
    time = [step * 0.01 for step in range(time_length)]

    # Correct flow directions: aorta should be negative, iliacs should be positive
    if data['aorta']['flow'][19] > 0:
        data['aorta']['flow'] *= -1

    if data['left']['flow'][19] < 0:
        data['left']['flow'] *= -1

    if data['right']['flow'][19] < 0:
        data['right']['flow'] *= -1

    # Volume conservation check for flows
    volume_f = (
        data['aorta']['flow']
        + data['left']['flow']
        + data['right']['flow']
    )

    results_list.append({
        "model": model,
        "time": time,
        "aorta_flow": data['aorta']['flow'],
        "left_flow": data['left']['flow'],
        "right_flow": data['right']['flow'],
        "aorta_pressure": data['aorta']['pressure'],
        "left_pressure": data['left']['pressure'],
        "right_pressure": data['right']['pressure'],
        "volume_balance": volume_f
    })


#--------------------------------------------------


colmap = {
    'aorta':  'tab:blue',
    'left':   'tab:orange',
    'right':  'tab:green'
}

figure_size = (15, 20)  # Adjusted figure size for better readability
dots_per_inch = 300

save_path = "C:\\Users\\magnuswe\\OneDrive - SINTEF\\Dokumenter\\Visualization"

# ─────────────────────────────────────────────────────────────────────────────
# Plotting first part of the data
# ─────────────────────────────────────────────────────────────────────────────

fig, axes = plt.subplots(7, 3, figsize=figure_size)
plt.subplots_adjust(left=0.18)  # Increase as needed (default is ~0.125)

for i, model in enumerate(results_list[:7]):
    # 1) Volume balance
    axes[i, 0].plot(model['time'], model['volume_balance'], color='tab:purple', label='Volume balance')
    if i == 6:
        axes[i, 0].set_xlabel('t (s)')
    #axs[0].set_title(r"$\dot Q_{\mathrm{net}} = -\dot Q_{\mathrm{aorta}} + \dot Q_{\mathrm{left}} + \dot Q_{\mathrm{right}}$", fontsize=14)
    axes[i, 0].set_ylim(-0.12, 0.12)
    if i == 0:
        axes[i, 0].set_title('Volume balance', fontsize=14)
    axes[i, 0].grid(True)
    axes[i, 0].set_ylabel(f"{model['model'][:6]}\n$\dot Q_{{\mathrm{{net}}}}$ (ml/s)", rotation=90, labelpad=20, va='center')
    #axs[0].legend(fontsize='x-small', loc='upper right')

    # 2) Inlet + outlet flows
    axes[i, 1].plot(model['time'], -model['aorta_flow'],   color=colmap['aorta'], label='Aorta')
    axes[i, 1].plot(model['time'],  model['left_flow'],    color=colmap['left'], label='Left iliac')
    axes[i, 1].plot(model['time'],  model['right_flow'],   color=colmap['right'], label='Right iliac')
    if i == 6:
        axes[i, 1].set_xlabel('t (s)')
    axes[i, 1].set_ylabel(r"$\dot Q$ (ml/s)", labelpad=-3)
    axes[i, 1].set_ylim(-20, 120)
    if i == 0:
        axes[i, 1].set_title('Flow rates')
    axes[i, 1].grid(True)
    #axs[1].legend(fontsize='x-small', loc='upper right')

    # 3) Pressures
    axes[i, 2].plot(model['time'], model['aorta_pressure'], color=colmap['aorta'], label='Aorta')
    axes[i, 2].plot(model['time'], model['left_pressure'],  color=colmap['left'], label='Left iliac')
    axes[i, 2].plot(model['time'], model['right_pressure'], color=colmap['right'], label='Right iliac')
    if i == 6:
        axes[i, 2].set_xlabel('t (s)')
    axes[i, 2].set_ylabel('P (mmHg)', labelpad=-1)
    axes[i, 2].set_ylim(80, 150)
    if i == 0:
        axes[i, 2].set_title('Pressures')
    axes[i, 2].grid(True)
    #axs[2].legend(fontsize='x-small', loc='upper right')
    # Collect handles + labels from all three axes
    all_handles, all_labels = [], []
    for ax in axes[i]:
        h, l = ax.get_legend_handles_labels()
        all_handles += h
        all_labels  += l
        
        #Setting ticks
        ax.set_xticks(np.arange(0, max(time)+1, 1))


    # Draw the single legend on the right, centered vertically

fig.legend(
    all_handles[:4],
    all_labels[:4],
    ncol=4,                           # number of columns in the legend
    loc='upper center',               # place at upper center
    bbox_to_anchor=(0.5, 0.92),       # just above the axes area
    frameon=False                     # optional: no box around legend
)


fig.savefig(os.path.join(save_path, "Periodic_convergence1.png"), bbox_inches='tight', dpi=dots_per_inch)

plt.tight_layout()
plt.show()


# ─────────────────────────────────────────────────────────────────────────────
# Plotting second part of the data
# ─────────────────────────────────────────────────────────────────────────────


fig, axes = plt.subplots(7, 3, figsize=figure_size)
plt.subplots_adjust(left=0.18)  # Increase as needed (default is ~0.125)

for i, model in enumerate(results_list[7:]):
    # 1) Volume balance
    axes[i, 0].plot(model['time'], model['volume_balance'], color='tab:purple', label='Volume balance')
    if i == 6:
        axes[i, 0].set_xlabel('t (s)')
    #axs[0].set_title(r"$\dot Q_{\mathrm{net}} = -\dot Q_{\mathrm{aorta}} + \dot Q_{\mathrm{left}} + \dot Q_{\mathrm{right}}$", fontsize=14)
    axes[i, 0].set_ylim(-0.12, 0.12)
    if i == 0:
        axes[i, 0].set_title('Volume balance', fontsize=14)
    axes[i, 0].grid(True)
    axes[i, 0].set_ylabel(f"{model['model'][:6]}\n$\dot Q_{{\mathrm{{net}}}}$ (ml/s)", rotation=90, labelpad=20, va='center')
    #axs[0].legend(fontsize='x-small', loc='upper right')

    # 2) Inlet + outlet flows
    axes[i, 1].plot(model['time'], -model['aorta_flow'],   color=colmap['aorta'], label='Aorta')
    axes[i, 1].plot(model['time'],  model['left_flow'],    color=colmap['left'], label='Left iliac')
    axes[i, 1].plot(model['time'],  model['right_flow'],   color=colmap['right'], label='Right iliac')
    if i == 6:
        axes[i, 1].set_xlabel('t (s)')
    axes[i, 1].set_ylabel(r"$\dot Q$ (ml/s)", labelpad=-3)
    axes[i, 1].set_ylim(-20, 120)
    if i == 0:
        axes[i, 1].set_title('Flow rates')
    axes[i, 1].grid(True)
    #axs[1].legend(fontsize='x-small', loc='upper right')

    # 3) Pressures
    axes[i, 2].plot(model['time'], model['aorta_pressure'], color=colmap['aorta'], label='Aorta')
    axes[i, 2].plot(model['time'], model['left_pressure'],  color=colmap['left'], label='Left iliac')
    axes[i, 2].plot(model['time'], model['right_pressure'], color=colmap['right'], label='Right iliac')
    if i == 6:
        axes[i, 2].set_xlabel('t (s)')
    axes[i, 2].set_ylabel('P (mmHg)', labelpad=-1)
    axes[i, 2].set_ylim(80, 150)
    if i == 0:
        axes[i, 2].set_title('Pressures')
    axes[i, 2].grid(True)
    #axs[2].legend(fontsize='x-small', loc='upper right')
    # Collect handles + labels from all three axes
    all_handles, all_labels = [], []
    for ax in axes[i]:
        h, l = ax.get_legend_handles_labels()
        all_handles += h
        all_labels  += l
        
        #Setting ticks
        ax.set_xticks(np.arange(0, max(time)+1, 1))


    # Draw the single legend on the right, centered vertically

fig.legend(
    all_handles[:4],
    all_labels[:4],
    ncol=4,                           # number of columns in the legend
    loc='upper center',               # place at upper center
    bbox_to_anchor=(0.5, 0.92),       # just above the axes area
    frameon=False                     # optional: no box around legend
)


fig.savefig(os.path.join(save_path, "Periodic_convergence2.png"), bbox_inches='tight', dpi=dots_per_inch)

plt.tight_layout()
plt.show()