# Vascular Simulation Post-Processing Pipelines

This repository documents multiple ParaView-based post-processing pipelines used in vascular simulations. The pipelines analyze wall shear stress (WSS), particle age (residence time), and flow/pressure across arterial branches. Each pipeline includes a structured workflow with macros and scripts.

---

## 📁 Pipelines Overview

- [WSS Pipeline](#wss-pipeline)
- [Particle Age Pipeline](#particle-age-pipeline)
- [Post-Processing Flow/Pressure Pipeline](#post-processing-flowpressure-pipeline)

---

## WSS Pipeline

### Purpose
Calculates time-averaged wall shear stress (TAWSS), low shear areas, and high oscillatory shear index (OSI) regions over one cardiac cycle.

### Steps
1. **Load Data**
   - Load `.vtp` files from the **last cycle**.
2. **Preparation**
   - Update the model name in `WSSmacro_part1` and `WSSmacro_part2`.
   - Load state file: `paraview_valid_region.pvsm`.
   - Load state file: `particle_age_part1_PRE.pvsm`.
   - Rename the clip under `all_results` to `inlet`.
3. **Run Scripts**
   - Run `WSSmacro_part1`.
   - Adjust clip positions:
     - Slide `clipAorta` down for aorta surface.
     - Move `bifurclip` and `inlet` to isolate the aneurysm.
   - Run `WSSmacro_part2`.

### Output
- Mean TAWSS, low shear and high OSI areas
- Time-dependent WSS values for box plots

---

## Particle Age Pipeline

### Purpose
Estimates particle residence time in the domain by seeding particles and tracking their age over time.

### Steps
1. **Load Data**
   - Load `.vtu` files from the **last two cycles**.
2. **Update Model Names**
   - Update in scripts: `Part1`, `Part2`, `Geo`, and `Plotting`.
3. **Clip Domain**
   - Clip geometry at the aneurysm inlet.
   - Load and check transformed centerline.
   - If clipped: 
     - Set `second_cl_clip = True`.
     - Rename `Clip2` to `Clip10`.
   - Else: set `second_cl_clip = False`.

4. **Run Part1 Macro**
   - **Input:** `Clip1`
   - Generates inlet geometry data and prepares the UI.
   - **Output:**
     - `inlet_area_dia_perimeter.csv`
     - `clipped_centerline.vtp`

5. **Run Geo Script**
   - Set `particle_calculation = True`.
   - **Input:** Clipped centerline
   - **Output:**
     - `centerline_points_and_tangents_table.csv`
     - `geometric_values.csv`

6. **Setup Clips for Particle Domain**
   - Add three clips under temp interpolator:
     - One below the renals
     - Two for iliac extensions

7. **Run Part2 Macro**
   - **Input:** `Clip3`
   - Seeds particles on five planes every 10 ms.
   - Stops once all particles from first cycle have exited.
   - **Output:** `particle_age_stats_{i}.csv`
   - Check `particle_log2.txt` for particle count consistency.

8. **Run Plotting Script**
   - `plottingParticleAge.py` in VS Code
   - **Input:** `particle_tracer_stats_{i}.csv`
   - **Output:**
     - `Particle_age_final_stats.csv`
     - `particle_age_plot.png`
   - Copy the mean value from `Particle_age_final_stats.csv`

---

## Post-Processing Flow/Pressure Pipeline

### Purpose
Extracts average surface pressure and flow rates at aorta and branch slices for multiple cardiac cycles.

### Steps
1. **Load Data**
   - Load `.vtu` files with **6 cardiac cycles** (excluding timestep 0).
2. **Load State**
   - Open `paraview_washout_pre.pvsm`.
3. **Rename Clips**
   - `Clip1` → `aorta`
   - `Clip2` → `right`
   - `Clip3` → `left`
   - ⚠️ Ensure clips do not intersect more than one artery. Use `box` if necessary.
   - Try to keep slices perpendicular to the flow for accuracy.

4. **Run Script**
   - Execute `SurfaceflowPressureMacro.py`

### What the Macro Does
- Copies `aorta`, `right`, and `left` to slices.
- Applies:
  - `Integrate Variables` → gets area × pressure
  - `Calculator` → divides by area for true average pressure
  - `Surface Flow` filter
- Iterates over timesteps and extracts:
  - Surface flow
  - Pressure values

---

## 🛠 Requirements

- ParaView (tested with v5.11+)
- Python scripting enabled in ParaView
- VS Code (recommended for `plottingParticleAge.py`)

---

## 📂 File Outputs Summary

| Pipeline                | Key Outputs                              |
|-------------------------|------------------------------------------|
| **WSS**                 | `TAWSS.csv`, WSS time series, plots      |
| **Particle Age**        | `Particle_age_final_stats.csv`, `particle_age_plot.png` |
| **Flow/Pressure**       | Time-resolved flow/pressure data         |
