# Vascular Simulation Pre- and Post-Processing Pipelines

This repository documents multiple pre- and post-processing pipelines used in vascular simulations. Each pipeline includes a structured workflow with macros and scripts. The order of the pipelines are important as state files are created in some of the first pipelines and are loaded into some of the later pipelines. The Particle Age pipeline for example creates the paraview_valid_region.pvsm state file. The purpose of state files is to retrieve clips and slices information, to be consistent in the metrics calculations. There are some bugs in paraview, which results in clips and slices sometimes being read wrong. This could be fairly easily improved, by saving csv files with the respective normal and center of clips and slices.

---

## 📁 Overview

- [VMTK Model and SimVascular Mesh Generation Pipeline](#vmtk-model-and-simVascular-mesh-generation-pipeline)
- [AAA Vascular Geometry Processing](#aaa-vascular-geometry-processing-aaa_geometrystats_cleanipynb)
- [WSS pipeline](wss-pipeline)
- [Particle Age Pipeline](#particle-age-pipeline)
- [Post-Processing Flow/Pressure Pipeline](#post-processing-flowpressure-pipeline)
- [Neck Angle Analysis Pipeline](#neck-angle-analysis-pipeline)
- [Qcrit Pipeline (Vortex Core Visualization)](#qcrit-pipeline-(vortex-core-visualization))
- [Washout Pipeline](#washout-pipeline)
- [WSS Analysis and Visualization (WSSdata_post-process.py)](#wss-analysis-and-visualization-wssdata_post-processpy)
- [WSS Mesh Comparison Script (meshConvergenceWSSgraphs.py)](#wss-mesh-comparison-script-meshconvergencewssgraphspy)
- [Windkessel Model Parameter Estimation from Flow Profile (RCR_modified_new.py)](#windkessel-model-parameter-estimation-from-flow-profile-rcr_modified_newpy)
- [RCR Parameter Splitting for Vascular Outlets (RCRsplit_modified.py)](#rcr-parameter-splitting-for-vascular-outlets-rcrsplit_modifiedpy)
- [Periodic Convergence Visualization of Flow and Pressure in Aorto-Iliac Models (checkResults.py)](#periodic-convergence-visualization-of-flow-and-pressure-in-aorto-iliac-models-checkresultspy)
- [Pressure Work and Energy Loss in Aorto-Iliac Models (PressureEnergyLoss.py)](#pressure-work-and-energy-loss-in-aorto-iliac-models-pressureenergylosspy)
- [Correlation Analysis of Hemodynamic and Morphological Metrics (R) (correlation_analysis.R)](#correlation-analysis-of-hemodynamic-and-morphological-metrics-r-correlation_analysisr)
- [Grid Convergence Study (GCS) for Pressure Differences (GCI2_pressure.py)](#grid-convergence-study-gcs-for-pressure-differences-gci2_pressurepy)
- [Vortex Formation Time (VFT) Estimation from Inlet Flow Profiles (VFTcalc.py)](#vortex-formation-time-vft-estimation-from-inlet-flow-profiles-vftcalcpy)
- [Kinetic Energy Calculation from Velocity Data (kineticEnergyCalc.py)](#kinetic-energy-calculation-from-velocity-data-kineticenergycalcpy)
- [WSS GCS – GCI Analysis (GCS_WSS_from_data.py)](#wss-gcs--gci-analysis-gcs_wss_from_datapy)
- [Kinetic Energy Pipeline](#kinetic-energy-pipeline)
---
# VMTK Model and SimVascular Mesh Generation Pipeline

This pipeline describes the step-by-step process for preparing vascular models using VMTK and SimVascular, from STL conversion through to meshing.

## Prerequisites
- VMTK installed and accessible in your terminal  
- SimVascular installed (for Python scripting)

## Pipeline Steps

1. **Convert STL to VTP**  
`vmtksurfacewriter -ifile STLfiler/AAAxxx.stl -ofile steg1/AAAxxx.vtp`

2. **Clip Renals**  
`vmtksurfaceclipper -ifile steg1/AAAxxx.vtp -ofile steg2/AAAxxx_cl.vtp`

3. **Cap Renals**  
`vmtksurfacecapper -ifile steg2/AAAxxx_cl.vtp -ofile steg3/AAAxxx_cap.vtp`

4. **Remesh Surface**  
`vmtksurfaceremeshing -ifile steg3/AAAxxx_cap.vtp -ofile steg4/AAAxxx_remesh.vtp -elementsizemode edgelength -entityidsarray CellEntityIds -preserveboundary 1 -edgelength 0.5`

5. **Smooth Surface**  
`vmtksurfacesmoothing -ifile steg4/AAAxxx_remesh.vtp -passband 0.1 -iterations 1000 -ofile steg5/AAAxxx_sm.vtp --pipe vmtksurfaceviewer`

6. **Check Volume and Smoothing**  
`vmtksurfacemassproperties -ifile steg4/AAAxxx_remesh.vtp`  
`vmtksurfacemassproperties -ifile steg5/AAAxxx_sm.vtp`

Show the difference from smoothed to unsmoothed model (Optional visualization)
`vmtksurfacereader -ifile steg4/AAAxxx_remesh.vtp --pipe vmtksurfacesmoothing -iterations 1000 -passband 0.1 --pipe vmtkrenderer --pipe vmtksurfaceviewer -display 0 --pipe vmtksurfaceviewer -i @vmtksurfacereader.o -color 1 0 0 -display 1`

7. **Clip Inlet and Outlets**  
`vmtksurfaceclipper -ifile steg5/AAAxxx_sm.vtp -ofile steg6/AAAxxx_io.vtp`

8. **Create Extensions**  
`vmtksurfacereader -ifile steg6/AAAxxx_io.vtp --pipe vmtkcenterlines -seedselector openprofiles --pipe vmtkflowextensions -adaptivelength 1 -extensionratio 10 -normalestimationratio 1 -interactive 0 --pipe vmtksurfacecapper --pipe vmtksurfacewriter -ofile steg7/AAAxxx_ex10.vtp`

9. **Remesh Extensions**  
`vmtksurfaceremeshing -ifile steg7/AAAxxx_ex10.vtp -ofile steg8/AAAxxx_ex10_remesh.vtp -elementsizemode edgelength -entityidsarray CellEntityIds -preserveboundary 1 -edgelength 0.5`

10. **Scale Model**  
`vmtksurfacescaling -ifile steg8/AAAxxx_ex10_remesh.vtp -scale 0.1 -ofile steg9/AAAxxx_ex10_scaled.vtp`

11. **Create ModelFaceIDs**  
`/Applications/SimVascular.app/Contents/Resources/simvascular --python -- scripts/create_ModelFaceID.py Simvascular/geometrier/steg9/AAAxxx_ex10_scaled.vtp Simvascular/geometrier/steg10/AAAxxx_FaceID.vtp`

12. **Mesh Model**  
`/Applications/SimVascular.app/Contents/Resources/simvascular --python -- scripts/sv_volume_meshing_Magnus.py Simvascular/geometrier/steg10/AAAxxx_FaceID.vtp Simvascular/geometrier/steg11/AAAxxx_0.15_ Simvascular/input/face_dict.csv 0.15`

## Notes
- Replace `AAAxxx` with your actual model identifiers.  
- Adjust paths depending on your folder structure.  
- Make sure required scripts/tools are accessible in your system path.

---

# AAA Vascular Geometry Processing (AAA_GeometryStats_clean.ipynb)

The code resamples aortic and iliac centerlines, computes important geometric features such as tortuosity, cross-sectional area, diameter, and perimeter along the vessels. It also identifies the bifurcation origin and normal vector, highlights the point of maximum aortic diameter, and saves key vessel metrics for further analysis or modeling. The script has two branches: One branch calculates geomtric values, while the other computes particle age pipeline necessities.

## Features

- **Centerline resampling:** Interpolates centerline points evenly along the vessel arc length.
- **Cross-sectional analysis:** Computes vessel cross-sectional area, perimeter, and maximum diameter from 3D vascular meshes at multiple locations.
- **Tortuosity calculation:** Quantifies vessel curvature from resampled centerlines.
- **Bifurcation detection:** Locates the bifurcation point and calculates the normal vector at that location.
- **Visualization:** Interactive 3D visualization of the mesh and centerlines with Plotly.
- **Data export:** Saves computed geometric properties and centerline data as CSV files for external analysis.
- **Configurable model selection** for batch processing of multiple AAA cases.

---

# WSS Pipeline

## Purpose
Stores time-dependent WSS for aortic and aneurysmal section, and calculates spatially-averaged TAWSS, low shear areas, and high oscillatory shear index (OSI) regions over one cardiac cycle.

## Steps
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

## Output
- Spatially-averaged TAWSS, low shear and high OSI areas
- Time-dependent WSS values

---

# Particle Age Pipeline

## Purpose
Estimates particle residence time in the domain by seeding particles and tracking their age over time.

## Steps
1. **Load Data**
   - Load `.vtu` files from the **last two cycles**.
2. **Update Model Names**
   - Update in scripts: `particleAgeMacro_part_1`, `particleAgeMacro_part_2`, `AAA_GeometryStats_clean`, and `plottingParticleAge`.
3. **Clip Domain**
   - Clip geometry at the aneurysm inlet.
   - Load the centerline, transform, and check.
   - If clipped a second time because of errors in centerline: 
     - Set `second_cl_clip = True`.
     - Rename `Clip2` to `Clip10`.
   - Else: set `second_cl_clip = False`.

4. **Run Part1 Macro**
   - **Input:** `Clip1`
   - Generates inlet geometry data and prepares the UI.
   - **Output:**
     - `inlet_area_dia_perimeter.csv`
     - `clipped_centerline.vtp`

5. **Run AAA_GeometryStats_clean Script**
   - Set `particle_calculation = True`.
   - Check for error messages in terminal and “geo_log.txt”
   - **Input:** Clipped centerline
   - **Output:**
     - `centerline_points_and_tangents_table.csv`
     - `geometric_values.csv`

6. **Setup Clips for Particle Domain**
   - Add three clips under temp interpolator:
     - One below the renals
     - Two for iliac extensions

7. **Run Part2 Macro**    
   - Have to run from "Script Editor" in ParaView
   - **Input:** `Clip3`
   - Seeds particles on five planes every 10 ms in the first cycle.
   - Stops once all particles from first cycle have exited.
   - **Output:** `particle_age_stats_{i}.csv`
   - Check `particle_log2.txt` for particle count consistency.

9. **Run Plotting Script**
   - `plottingParticleAge.py` in VS Code
   - **Input:** `particle_tracer_stats_{i}.csv`
   - **Output:**
     - `Particle_age_final_stats.csv`
     - `particle_age_plot.png`

---

# Post-Processing Flow/Pressure Pipeline

## Purpose
Extracts average surface pressure and flow rates at aorta and branch slices for multiple cardiac cycles.

## Steps
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

## What the Macro Does
- Copies `aorta`, `right`, and `left` to slices.
- Applies:
  - `Integrate Variables` → gets area × pressure
  - `Calculator` → divides by area for true average pressure
  - `Surface Flow` filter
- Iterates over timesteps and extracts:
  - Surface flow
  - Pressure values

---


# Neck Angle Analysis Pipeline

This pipeline calculates neck angles (α and β) in vascular geometries by integrating centroid data across slices from `.vtu` files. The angles are computed based on artificial lines between slice centroids.


## 📋 Workflow Overview

1. **Load Data**
   - Load `.vtu` files from the **last cardiac cycle**.

2. **Create Slices**
   - Slice the geometry from **top to bottom**.
   - **Important:** Naming matters — the macro assumes:
     - `Slice1` = top
     - `Slice2` = second
     - ...
     - `Slice4` = bottom

3. **Run the Macro**
   - The macro performs the following steps:
     - Applies `Integrate Variables` on each slice to obtain the **centroid**.
     - Constructs three lines:
       - `Line12`: connects Slice1 and Slice2
       - `Line23`: connects Slice2 and Slice3
       - `Line34`: connects Slice3 and Slice4
     - Computes:
       - **Angle α** between `Line12` and `Line23`
       - **Angle β** between `Line23` and `Line34`

---


# Qcrit Pipeline (Vortex Core Visualization)

This pipeline visualizes vortex structures in CFD data by computing and displaying the Q-criterion isosurface at a value of 500.

## 📋 Workflow Overview

1. **Load Data**  
   - Open the `paraview_washout_post.pvsm` state file.  
   - If the `04770.vtu*` file is missing:  
     - Load it from the `last_cycle` folder.  
     - Rename the inlet source to `"inlet"` by copying and deleting the old inlet.

2. **Prepare the Scene**  
   - Delete the Particle Tracer.  
   - Update the model name in the `QcritMacro.py` script.

3. **Run the Macro**  
   - The macro computes the Q-criterion using a gradient filter.  
   - Displays the Q-criterion isosurface at `Q = 500`.  
   - Adds a ruler from the inlet to the bifurcation.

4. **Post-processing**  
   - Clip iliac arteries if needed.  
   - Adjust ruler position.

5. **Save Results**  
   - Save a screenshot of the visualization.

---

# Washout Pipeline

This pipeline depends on the Geometry script and the Particle Age pipeline to analyze washout in vascular simulations.

## 📋 Workflow Overview

1. **Change Model Name**  
   - Update the model name inside the `WashOutMacro.py` script.

2. **Load States**  
   - Load the `paraview_valid_region` state from the `two_last_cycle` folder.  
   - Load the `particle_age_part1_PRE` state file from the `two_last_cycle` folder.

3. **Load Geometry**  
   - Load the `.vtp` file at the first timestep only (e.g., `04770.vtp`) from the last cycle.

4. **Rename Clip**  
   - Change the name of the single clip under `all_results` to `"inlet"`.

5. **Setup Views**  
   - Create another RenderView and place `clip3` there.  
   - Adjust the camera angles for all models to good visualization perspectives.

6. **Run the Washout Macro**  
   - The macro performs point offsetting, seeding, and tracer simulation through two cardiac cycles.

7. **Create Video (Optional)**  
   - To generate a video from rendered frames, run the following command in CMD:  
     ```
     \Users\magnuswe\ffmpeg-7.1.1-essentials_build\bin\ffmpeg -y -framerate 20 -i frame_%05d.png -c:v libx264 -crf 18 -pix_fmt yuv420p washout_video.mp4
     ```

---

# WSS Analysis and Visualization (WSSdata_post-process.py)

This Python script processes wall shear stress (WSS) time series data from multiple vascular models, computes trimmed statistical metrics, saves summary data to CSV, and generates detailed WSS time series plots for aneurysm and aorta regions.

## Features

- Reads WSS time series CSV files (aneurysm and aorta) for multiple models
- Converts units from dynes/cm² to Pascals (Pa)
- Computes trimmed statistics (mean, quartiles, min/max averages after trimming)
- Saves min/max/mean WSS values at a specific timepoint to a CSV file
- Generates and saves publication-quality WSS time series plots for multiple models

---

# WSS Mesh Comparison Script (meshConvergenceWSSgraphs.py)

This script processes and visualizes wall shear stress (WSS) data from vascular simulations to compare different mesh resolutions. It computes and plots trimmed statistics (mean, interquartile range, and top/bottom percentiles) for both the aneurysm and aorta regions over a cardiac cycle.

---

# Windkessel Model Parameter Estimation from Flow Profile (RCR_modified_new.py)

This Python script estimates optimal parameters for a 3-element Windkessel model (Z, C, R) and initial pressure offset by fitting simulated pressure to an inlet flow profile using numerical integration and optimization. It ensures the simulated pressure matches key physiological targets (systolic/diastolic pressure, mean pressure, and periodicity).

---

# RCR Parameter Splitting for Vascular Outlets (RCRsplit_modified.py)

This Python script defines a utility function to split lumped 3-element Windkessel model parameters (`RCR`) into distributed outlet-specific values, based on their relative cross-sectional areas.

---

# Periodic Convergence Visualization of Flow and Pressure in Aorto-Iliac Models (checkResults.py)

This script processes time-resolved flow and pressure data for a series of aorto-iliac vascular models and visualizes:

- **Volume balance** (net flow consistency)
- **Inlet and outlet flow rates**
- **Pressures** across aorta and iliac arteries

It generates two multi-panel figures summarizing 14 models across three key plots per model.

---

# Pressure Work and Energy Loss in Aorto-Iliac Models (PressureEnergyLoss.py)

This script estimates the pressure-related energy transfer in aorto-iliac vascular models by computing:

1. **Pressure Work**: Work done by the heart to push blood through each iliac outlet.
2. **Energy Loss**: Net pressure-volume energy discrepancy between inlet and outlets.

---

# Correlation Analysis of Hemodynamic and Morphological Metrics (R) (correlation_analysis.R)

This R script performs correlation analysis and visualization using a dataset of metrics.

---

# Grid Convergence Study (GCS) for Pressure Differences (GCI2_pressure.py)

This script performs a Grid Convergence Study (GCS) based on pressure differences extracted from three mesh resolutions in a vascular simulation. It calculates the **apparent order of convergence** and **Grid Convergence Index (GCI)** between:

- Coarse: 500k cells
- Medium: 1.1 million cells
- Fine: 2.5 million cells

---

# Vortex Formation Time (VFT) Estimation from Inlet Flow Profiles (VFTcalc.py)

This script calculates the **Vortex Formation Time (VFT)** during systole for multiple AAA (abdominal aortic aneurysm) models based on inlet flow data and anatomical throat areas.

---

# Kinetic Energy Calculation from Velocity Data (kineticEnergyCalc.py)

This script calculates the total **kinetic energy (KE)** of blood flow in a 3D vascular domain based on velocity magnitudes and cell volumes exported from SimVascular.

---

# WSS GCS – GCI Analysis (GCS_WSS_from_data.py)

This script performs a **Grid Convergence Study (GCS)** on **wall shear stress (WSS)** data extracted from three different mesh resolutions of a vascular model. It uses the **Grid Convergence Index (GCI)** methodology to evaluate numerical uncertainty and apparent order of convergence for both aorta and aneurysm regions.

---


# Kinetic Energy Pipeline

This pipeline calculates kinetic energy (KE) in vascular CFD simulations based on velocity fields and geometry. The metric was not included in the article as it is assumed to be strongly correlated to volume and Dmax, as the inflow profile were equal in all simulations, making it sort of uninteresting. 

## 📋 Workflow Overview

1. **Run Geometry Script**  
   - Execute the geometry preparation script before starting.

2. **Configure Macros**  
   - Change the model name inside both the KE macro and KE calculation scripts.  
   - Set `normal_from_data=True` in the KE macro.

3. **Load Data**  
   - Load `.vtu` files from the last cardiac cycle.  
   - Load the `particle_age_part1_PRE` state file from the `two_last_cycles` folder.

4. **Clip Iliacs if Needed**  
   - Check if iliac arteries should be clipped away (e.g., if located above bifurcation).  
   - If clipping is needed, name this clip `"extraClip"`.

5. **Run KE Macro**  
   - Execute the KE macro script.

6. **Check Bifurcation Clip**  
   - Inspect the bifurcation clipping; if required, apply a Z-normal clip.

7. **Review KE Log**  
   - Check the `KE_log` for kinetic energy results and relevant info.

8. **Run KE Calculation**  
   - Run the KE calculation script to finalize kinetic energy analysis.

---

## 🛠 Requirements

- ParaView (tested with v5.13 nightly)
