import pandas as pd
import matplotlib.pyplot as plt
import os

### Models (unchanged) ###
AAA001 = "AAA001_sim_0-19_1-1mill-last_cycle"
AAA002 = "AAA001_sim_0,14_2,5mill-last_cycle"
AAA003 = "AAA001_sim_0,26_500k-6th_cycle"
AAA004 = "AAA004_sim_0-15_1-3mill-last_cycle"
AAA013 = "AAA013_sim_0-15_1-9mill-last_cycle"
AAA014 = "AAA014_sim_0,14_1,3mill-last_cycle"
AAA017 = "AAA017_sim_0-17_1-6mill-last_cycle"

model1 = AAA001
model2 = AAA002
model3 = AAA003
model4 = AAA004
model5 = AAA013
model6 = AAA014
model7 = AAA017

# ─────────────────────────────────────────────────────────────────────────────
# User‐specified y‐axis limits (in Pa):
y_min_hard = 0.0
y_max_hard = 3.0
# ─────────────────────────────────────────────────────────────────────────────

def load_wss_dataframe(csv_path: str, sep: str = ';') -> pd.DataFrame:
    """
    Load a “full time‐series” WSS CSV file into a DataFrame.
    """
    return pd.read_csv(csv_path, sep=sep)

def plot_wss_box_over_time(
    ax: plt.Axes,
    df: pd.DataFrame,
    title: str = None,
    tick_interval: float = 10,
    y_min: float = None,
    y_max: float = None
) -> None:
    """
    Draw a vertical boxplot of WSS (converted to Pa) at each time‐step,
    then apply y‐limits if provided.
    """
    # 1) Extract the time labels as floats
    time_strings = list(df.columns)
    times = [float(t) for t in time_strings]

    # 2) Build a list of arrays: one per column, dividing by 10 and dropping zeros
    data = []
    for col in time_strings:
        arr = df[col].dropna().astype(float)
        arr = arr[arr != 0.0]  # drop zero‐entries
        arr = arr / 10.0       # convert to Pa
        data.append(arr.values)

    # 3) Draw a vertical boxplot on `ax`, showing outliers as small dots
    ax.boxplot(
        data,
        positions=range(len(times)),
        patch_artist=True,
        showfliers=True,
        flierprops=dict(
            marker='.',        # small dot
            markersize=2,      # subtle size
            linestyle='none',
            markerfacecolor='black',
            markeredgecolor='none'
        )
    )

    # 4) Pick out only those positions where time is an integer multiple of tick_interval
    tick_positions = [
        i
        for i, t in enumerate(times)
        if abs((t / tick_interval) - round(t / tick_interval)) < 1e-6
    ]
    tick_labels = [f"{times[i]:.1f}" for i in tick_positions]

    # 5) Set x‐ticks and labels (horizontal)
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels, rotation=0, fontsize=6)

    # 6) Labels + title
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("WSS (Pa)")
    if title:
        ax.set_title(title, fontsize=8)

    # 7) Show small tick marks on x‐axis
    ax.tick_params(axis='x', which='both', length=4)

    # 8) Apply hardcoded y‐limits if provided
    if y_min is not None and y_max is not None:
        ax.set_ylim(y_min, y_max)

def make_14_panel_figure(dataset_info, model_names, out_png=None):
    """
    Create a 2×7 grid of boxplots (Aorta top row, Aneurysm bottom row),
    with y‐axis fixed to [y_min_hard, y_max_hard] for all subplots.
    """
    n = len(dataset_info)
    if n != 7 or len(model_names) != 7:
        raise ValueError("Expected exactly 7 dataset pairs and 7 model names.")

    fig, axes = plt.subplots(2, n, figsize=(4 * n, 6))

    for i, ((aorta_csv, aneurysm_csv), model_name) in enumerate(zip(dataset_info, model_names)):
        df_aorta = load_wss_dataframe(aorta_csv, sep=';')
        df_aneu  = load_wss_dataframe(aneurysm_csv, sep=';')

        # Aorta subplot
        plot_wss_box_over_time(
            axes[0, i],
            df_aorta,
            title=f"{model_name[:15]} – Aorta",
            tick_interval=10,
            y_min=y_min_hard,
            y_max=y_max_hard
        )

        # Aneurysm subplot
        plot_wss_box_over_time(
            axes[1, i],
            df_aneu,
            title=f"{model_name[:15]} – Aneurysm",
            tick_interval=10,
            y_min=y_min_hard,
            y_max=y_max_hard
        )

    plt.tight_layout()
    if out_png:
        fig.savefig(out_png, dpi=150)
    plt.show()


# ─────────────────────────────────────────────────────────────────────────────
# Helper functions to build file paths. Adjust these if your folder structure differs:
def aorta_csv_path(model_id: str) -> str:
    base = f"C:/Users/magnuswe/OneDrive - SINTEF/Simvascular/results/last_cycle/{model_id}"
    return os.path.join(base, "WSS_full_time_series_aorta.csv")

def aneurysm_csv_path(model_id: str) -> str:
    base = f"C:/Users/magnuswe/OneDrive - SINTEF/Simvascular/results/last_cycle/{model_id}"
    return os.path.join(base, "WSS_full_time_series_aneurysm.csv")

# Build model list and dataset_info:
model_names = [model1, model2, model3, model4, model5, model6, model7]

dataset_info = []
for mid in model_names:
    a_path  = aorta_csv_path(mid)
    an_path = aneurysm_csv_path(mid)
    if not (os.path.exists(a_path) and os.path.exists(an_path)):
        raise FileNotFoundError(f"Missing CSV for model {mid}: {a_path} or {an_path} not found.")
    dataset_info.append((a_path, an_path))

# Draw all 14 panels with horizontal time labels, tick marks, and hardcoded y‐axis:
make_14_panel_figure(
    dataset_info,
    model_names,
    out_png="all_14_boxplots_pa.png"
)
