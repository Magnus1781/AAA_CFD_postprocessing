from paraview.simple import *
import csv
import os


# Output folder for CSVs
output_folder = r"C:/Users/magnuswe/OneDrive - SINTEF/Simvascular/results/last_cycle/AAA001_sim_0-19_1-1mill-last_cycle/"  # Change as needed
os.makedirs(output_folder, exist_ok=True)

# Set timestep to 20
animationScene = GetAnimationScene()
animationScene.UpdateAnimationUsingDataTimeSteps()
time_steps = animationScene.TimeKeeper.TimestepValues



# Ensure timestep 20 exists
if 20.0 in time_steps:
    animationScene.TimeKeeper.Time = 20.0
else:
    raise ValueError("Timestep 20 not found in the loaded data.")


# Clip names and threshold values
model_clips = {
    "model_500k": "Clip3",
    "model_1.1mill": "Clip6",
    "model_2.5mill": "Clip9"
}


thresholds = list(range(10, 0, -1))  # From 10 to 1

for model_name, clip_name in model_clips.items():
    clip = FindSource(clip_name)
    if not clip:
        print(f"Warning: {clip_name} not found.")
        continue

    results = []

    for thresh in thresholds:
        # Threshold filter
        threshold = Threshold(Input=clip)
        threshold.Scalars = ['POINTS', 'vWSS']
        threshold.SelectedComponent = 'Magnitude'
        threshold.ThresholdMethod = 'Below Lower Threshold'
        threshold.LowerThreshold = thresh

        RenameSource(f"{clip_name}_Thresh_{thresh}", threshold)

        # Integrate before CellDataToPointData
        integrator = IntegrateVariables(Input=threshold)
        RenameSource(f"{clip_name}_Integrate_{thresh}", integrator)
        UpdatePipeline()

        # Extract surface area
        data = servermanager.Fetch(integrator)
        area = None
        if data.GetCellData().HasArray("Area"):
            area = data.GetCellData().GetArray("Area").GetTuple(0)[0]

        results.append([thresh, area])

        # CellDataToPointData (just for visual/reference if needed)
        cd2pd = CellDatatoPointData(Input=threshold)
        RenameSource(f"{clip_name}_CD2PD_{thresh}", cd2pd)

    # Write threshold vs. area to CSV
    output_file = os.path.join(output_folder, f"{model_name}_area_vs_threshold.csv")
    with open(output_file, 'r', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(["Threshold", "Area"])
        writer.writerows(results)

    print(f"✅ Saved CSV: {output_file}")
