from paraview.simple import *
import numpy as np
import os
import pandas as pd
import ast
import math
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

#####Change only this##########
model = AAA091
#extract_slices_from_folder = True # Must run this when only the vtu file is in the pipeline browser #not implemented yet
log_slice_data = True
###############################
cwd = f"C:/Users/magnuswe/OneDrive - SINTEF/Simvascular/results/last_cycle/{model}-last_cycle/"

log_path = os.path.join(cwd,'neckAngle_log.txt')
log_file = open(log_path, "w")

def log(msg):
    log_file.write(str(msg) + "\n")
    log_file.flush()

SaveState(os.path.join(cwd, 'paraview_neckAngle_pre.pvsm'))

renderView1 = GetActiveViewOrCreate('RenderView')
all_results_04770vtu= FindSource('all_results_04770.vtu*')

def compute_slice_centroid(sliceName):
    """Apply IntegrateVariables and CenterOfMass filters, return centroid tuple."""
    src = FindSource(sliceName)
    if not src:
        raise RuntimeError(f"Slice source '{sliceName}' not found")
    # (1) Preserve their Integrate Variables object
    log(f"found source {sliceName}")
    iv = IntegrateVariables(registrationName=f"{sliceName}_intvar", Input=src)
    calc = Calculator(registrationName=f"{sliceName}_calc", Input=iv)
    calc.Set(
    ResultArrayName='coords',
    Function='coords',
    )

    center = servermanager.Fetch(calc).GetPointData().GetArray("coords")
    center = np.array(center)
    log(f"numpy center is {center}")
    center = center[0].tolist()
    log(f"center is {center}")
    renderView1.Update()
    return center


def angle_at(p_prev, p_center, p_next):
    """Return angle (degrees) at p_center between p_prev→p_center and p_center→p_next."""
    v1 = [p_prev[i] - p_center[i] for i in range(3)]
    v2 = [p_next[i] - p_center[i] for i in range(3)]
    dot = sum(a*b for a,b in zip(v1, v2))
    mag1 = math.sqrt(sum(a*a for a in v1))
    mag2 = math.sqrt(sum(b*b for b in v2))
    return math.degrees(math.acos(dot / (mag1*mag2)))


point1=compute_slice_centroid("Slice1")
point2=compute_slice_centroid("Slice2")
point3=compute_slice_centroid("Slice3")
point4=compute_slice_centroid("Slice4")


angle_1_2_3 = angle_at(point1, point2, point3)
angle_2_3_4 = angle_at(point2, point3, point4)

log(f"Beta angle from python calc: {angle_1_2_3:.2f}°")
log(f"Alpha angle from python calc: {angle_2_3_4:.2f}°")



########Creating protractors in paraview to verify the calculation################

pro1_list = []
pro2_list = []
for p in point1:
    pro1_list.append(p)
for p in point2:
    pro1_list.append(p)
for p in point3:
    pro1_list.append(p)

protractor1 = Protractor(registrationName='Protractor1')
protractor1.Points = pro1_list
protractor1Display = Show(protractor1, renderView1, 'ProtractorRepresentation')

for p in point2:
    pro2_list.append(p)
for p in point3:
    pro2_list.append(p)
for p in point4:
    pro2_list.append(p)

protractor2 = Protractor(registrationName='Protractor2')
protractor2.Points = pro2_list
protractor2Display = Show(protractor2, renderView1, 'ProtractorRepresentation')

angle_csv_path = os.path.join(cwd, "neckAngle.csv")
with open(angle_csv_path, "w", newline="") as csvfile:
    writer = csv.writer(csvfile, delimiter=";")
    writer.writerow(["Beta_angle_deg", "Alpha_angle_deg"])
    writer.writerow([f"{angle_1_2_3:.2f}", f"{angle_2_3_4:.2f}"])

log(f"Angles saved to {angle_csv_path}")


# Create output folder if it doesn't exist
slices_folder = os.path.join(cwd, "neckAngle_slices")
os.makedirs(slices_folder, exist_ok=True)

if log_slice_data:
    for i, slice_name in enumerate(["Slice1", "Slice2", "Slice3", "Slice4"], start=1):
        src = FindSource(slice_name)
        if not src:
            log(f"Slice source '{slice_name}' not found, skipping.")
            continue
        origin = src.SliceType.Origin
        normal = src.SliceType.Normal

        csv_path = os.path.join(slices_folder, f"slice{i}.csv")
        with open(csv_path, "w", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["origin", "normal"])
            writer.writerow(list(origin) + list(normal))
        log(f"Saved {slice_name} origin/normal to {csv_path}")

SaveState(os.path.join(cwd, 'paraview_neckAngle_post.pvsm'))
log("State saved")
log_file.close()