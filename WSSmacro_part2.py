#####load vtu files and clip below renals and the two extensions, change cwd then run this macroo########

from paraview.simple import *
import csv
import os
import math
import ast
import pandas as pd
import numpy as np

AAA001 = "AAA001_sim_0-19_1-1mill"

AAA001_500k = r"C:\Users\magnuswe\OneDrive - SINTEF\Simvascular\results\last_cycle\AAA001_sim_0,26_500k-6th_cycle"
AAA001_2_2mill = r"C:\Users\magnuswe\OneDrive - SINTEF\Simvascular\results\last_cycle\AAA001_sim_0,14_2,5mill-last_cycle"

AAA004 = "AAA004_sim_0-15_1-3mill"
AAA013 = "AAA013_sim_0-15_1-9mill"
AAA014 = "AAA014_sim_0,14_1,3mill"
AAA017 = "AAA017_sim_0-17_1-6mill"
AAA023 = "AAA023_sim_0-15_1-8mill"
AAA033 = "AAA033_sim_0-15_2mill"
AAA039 = "AAA039_sim_0-15_1-9mill"
AAA042 = "AAA042_0-18_1-9mill" #ekstra klipp
AAA046 = "AAA046_sim_0-17_1-5mill"
AAA087 = "AAA087_sim_0-15_1-6mill"
AAA088 = "AAA088_sim_0-15_1-7mill"
AAA091 = "AAA091_sim_0-15_1-5mill"
AAA092 = "AAA092_sim_0-15_1mill"

#####Change only this######
model = AAA042
extraClip_exists = True
######################

cwd = f'C://Users//magnuswe//OneDrive - SINTEF//Simvascular//results//last_cycle//{model}-last_cycle'
#cwd = AAA001_2_2mill

SaveState(os.path.join(cwd, 'WSS_part2_pre.pvsm'))
#################Logging setup####################
log_file_path = os.path.join(cwd, "WSS_log_2.txt")
log_file = open(log_file_path, "w")

def log(msg):
    log_file.write(str(msg) + "\n")
    log_file.flush()
log("created log")



all_results_04770vtp= FindSource('all_results_04770.vtp*')

clipAorta= FindSource('ClipAorta')
clipBifur= FindSource('ClipBifur')

# create a new 'Temporal Interpolator'
temporalInterpolator1 = TemporalInterpolator(registrationName='TemporalInterpolator1', Input=all_results_04770vtp)

# get animation scene
scene = GetAnimationScene()

# update animation scene based on data timesteps
scene.UpdateAnimationUsingDataTimeSteps()

# Properties modified on temporalInterpolator1
temporalInterpolator1.DiscreteTimeStepInterval = 1.0


# Properties modified on animationScene1
scene.AnimationTime = 20.0

# get the time-keeper
timeKeeper1 = GetTimeKeeper()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')


##### PART 1: vWSS magnitude → five‐point min/max averages #####

# 1a) Compute vWSS magnitude on your two clips
calcAorta = Calculator(registrationName='calcAorta', Input=clipAorta)
calcAorta.Set(
    ResultArrayName='vWSS_Magnitude_1',
    Function='sqrt(vWSS_X^2+vWSS_Y^2+vWSS_Z^2)',
)

calcAneurysm = Calculator(registrationName='calcAneurysm', Input=clipBifur)
calcAneurysm.Set(
    ResultArrayName='vWSS_Magnitude_1',
    Function='sqrt(vWSS_X^2+vWSS_Y^2+vWSS_Z^2)',
)

renderView1.Update()

all_results_04770vtp.UpdatePipeline()
calcAorta.UpdatePipeline()
calcAneurysm.UpdatePipeline()


# 1b) Fetch, sort, and average the five lowest/highest values

# Aorta
data = servermanager.Fetch(calcAorta)
arr  = data.GetPointData().GetArray('vWSS_Magnitude_1')
vals = sorted(
    arr.GetValue(i)
    for i in range(arr.GetNumberOfTuples())
    if arr.GetValue(i) != 0.0
    )
log(f"Five highest WSS values aorta: {vals[-5:]}")
log(f"Five lowest WSS values aorta: {vals[:5]}")
log("These will not be used for max and min WSS, as the postprocessing script will do that.")


#Aneurysm
data = servermanager.Fetch(calcAneurysm)
arr  = data.GetPointData().GetArray('vWSS_Magnitude_1')
vals = sorted(
    arr.GetValue(i)
    for i in range(arr.GetNumberOfTuples())
    if arr.GetValue(i) != 0.0
    )
log(f"Five highest WSS values aneurysm: {vals[-5:]}")
log(f"Five lowest WSS values aneurysm: {vals[:5]}")
log("These will not be used for max and min WSS, as the postprocessing script will do that.")


##### PART 2: threshold & integrate#####

#############Copying clips to average_results#############
# 1) Load your averaged result
average_resultvtp = XMLPolyDataReader(
    registrationName='average_result.vtp',
    FileName=[os.path.join(cwd, 'average_result.vtp')]
)

clipRenals = FindSource('ClipRenals')
clipInlet  = FindSource('ClipInlet')



def clone_clip(clip_src, new_name, new_input):
    """
    Clone whatever Clip filter `clip_src` is (Plane or Box) onto `new_input`,
    giving it the registrationName `new_name`.
    """
    # figure out whether it's a Plane‐type clip or a Box‐type clip
    ct = clip_src.ClipType
    ct_name = type(ct).__name__
    new_clip = Clip(registrationName=new_name, Input=new_input)
    if "Plane" in ct_name:
        log("it was a plane")
        # copy origin & normal
        new_clip.ClipType = 'Plane'
        new_clip.ClipType.Origin = clip_src.ClipType.Origin
        new_clip.ClipType.Normal = clip_src.ClipType.Normal
        new_clip.Invert = clip_src.Invert
    elif "Box" in ct_name:
        log("It was a box")
        new_clip.ClipType = 'Box'
        new_clip.ClipType.Position = clip_src.ClipType.Position
        new_clip.ClipType.Rotation = clip_src.ClipType.Rotation
        new_clip.ClipType.Length = clip_src.ClipType.Length
        new_clip.Invert = clip_src.Invert
    else:
        raise RuntimeError(f"clone_clip: unsupported ClipType {ct_name}")
    return new_clip

if extraClip_exists:
    extraClip = FindSource('extraClip')
    extraClip_avg = clone_clip(extraClip, 'extraClip_Avg', average_resultvtp)
    clipInlet_avg = clone_clip(clipInlet, 'ClipInlet_Avg', extraClip_avg)
else:
    clipInlet_avg = clone_clip(clipInlet, 'ClipInlet_Avg', average_resultvtp)

# 3) Copy “below-renals” cut onto the averaged data
clipRenals_avg = clone_clip(clipRenals, 'ClipRenals_Avg', average_resultvtp)

# 4) Copy the “aorta” cut (same plane, chained) onto that
clipAorta_avg  = clone_clip(clipAorta, 'ClipAorta_Avg',  clipRenals_avg)

# 6) Finally chain the bifurcation cut onto the inlet-clipped average
clipBifur_avg  = clone_clip(clipBifur, 'ClipBifur_Avg',  clipInlet_avg)

#############################################################


# 2) Compute mean non-zero vTAWSS_wss on each clip
def mean_nonzero(proxy, array_name):
    data = servermanager.Fetch(proxy)
    arr  = data.GetPointData().GetArray(array_name)
    vals = [arr.GetValue(i) for i in range(arr.GetNumberOfTuples())
            if arr.GetValue(i) != 0.0]
    if not vals:
        return 0.0
    return sum(vals) / len(vals)

mean_vTAWSS_wss_aorta    = mean_nonzero(clipAorta_avg, 'vTAWSS_wss')
mean_vTAWSS_wss_aneurysm = mean_nonzero(clipBifur_avg, 'vTAWSS_wss')

log(f"Aorta  mean vTAWSS_wss:    {mean_vTAWSS_wss_aorta:.4f}")
log(f"Aneurysm mean vTAWSS_wss:    {mean_vTAWSS_wss_aneurysm:.4f}")

# 2a) Threshold on vOSI_wss
threshold1 = Threshold(registrationName='Threshold1', Input=clipBifur_avg)
threshold1.Scalars          = ['POINTS', 'vOSI_wss']
threshold1.UpperThreshold   = 0.3
threshold1.ThresholdMethod  = 'Above Upper Threshold'

# 2b) Threshold on vTAWSS_wss
threshold2 = Threshold(registrationName='Threshold2', Input=clipBifur_avg)
threshold2.Scalars          = ['POINTS', 'vTAWSS_wss']
threshold2.LowerThreshold   = 4.0
threshold2.ThresholdMethod  = 'Below Lower Threshold'

# 2c) Integrate areas
int1 = IntegrateVariables(registrationName='Int_vOSI_wss', Input=threshold1)
int2 = IntegrateVariables(registrationName='Int_vTAWSS_wss', Input=threshold2)
int3 = IntegrateVariables(registrationName='Surface_area', Input=clipBifur_avg)
renderView1.Update()

# 2d) Fetch areas
OSI_area   = servermanager.Fetch(int1).GetCellData().GetArray("Area").GetValue(0)
TAWSS_area = servermanager.Fetch(int2).GetCellData().GetArray("Area").GetValue(0)
Surface_area = servermanager.Fetch(int3).GetCellData().GetArray("Area").GetValue(0)

# 2e) Write to CSV
output_csv = os.path.join(cwd, "TAWSS_OSI_parameters.csv")
with open(output_csv, 'w', newline='') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow([
    "mean_TAWSS_aorta (Pa)",
    "mean_TAWSS_aneurysm (Pa)",
    f"TAWSS_area (cm^2) (< {str(threshold2.LowerThreshold)} dynes/cm^2)",
    f"OSI_area  (cm^2) (> {str(threshold1.UpperThreshold)})",
    "Surface_area (cm^2) (total area of aneurysm)"
    ])
    # values in exactly the same order
    writer.writerow([
        mean_vTAWSS_wss_aorta/10,
        mean_vTAWSS_wss_aneurysm/10,
        TAWSS_area,
        OSI_area,
        Surface_area
    ])

# get layout
layout1 = GetLayout()

# split cell
layout1.SplitHorizontal(0, 0.5)

# set active view
SetActiveView(None)

# Create a new 'SpreadSheet View'
spreadSheetView1 = CreateView('SpreadSheetView')
spreadSheetView1.Set(
    ColumnToSort='',
    BlockSize=1024,
)



# show data in view
calcAneurysmDisplay = Show(calcAneurysm, spreadSheetView1, 'SpreadSheetRepresentation')

# assign view to a particular cell in the layout
AssignViewToLayout(view=spreadSheetView1, layout=layout1, hint=2)

# set active view
SetActiveView(renderView1)

# split cell
layout1.SplitVertical(1, 0.5)

# set active view
SetActiveView(None)

# Create a new 'SpreadSheet View'
spreadSheetView2 = CreateView('SpreadSheetView')
spreadSheetView2.Set(
    ColumnToSort='',
    BlockSize=1024,
)

# show data in view
calcAneurysmDisplay_1 = Show(calcAneurysm, spreadSheetView1, 'SpreadSheetRepresentation')

# assign view to a particular cell in the layout
AssignViewToLayout(view=spreadSheetView2, layout=layout1, hint=4)

# find source
calcAorta = FindSource('calcAorta')

# set active source
SetActiveSource(calcAorta)

# show data in view
calcAortaDisplay = Show(calcAorta, spreadSheetView2, 'SpreadSheetRepresentation')

# --- Full‐distribution WSS → CSV export ---
scene.AnimationTime = 0

# 1) Times from 0 to 95 s in 0.1 s steps
t0, t_end, dt = 0.0, 95.0, 1
times = np.arange(t0, t_end + dt, dt)

# 2) Helper to fetch & sort descending all vWSS values
def fetch_sorted(descCalc):
    data = servermanager.Fetch(descCalc)
    arr  = data.GetPointData().GetArray('vWSS_Magnitude_1')
    vals = [arr.GetValue(i) for i in range(arr.GetNumberOfTuples())
            if arr.GetValue(i) != 0.0]
    return sorted(vals, reverse=True)

# 3) Loop over time, collect columns
cols_aorta    = []
cols_aneurysm = []

for t in times:
    scene.AnimationTime = t
    renderView1.Update()
    all_results_04770vtp.UpdatePipeline()
    calcAorta.UpdatePipeline()
    calcAneurysm.UpdatePipeline()
    
    #Aorta
    data = servermanager.Fetch(calcAorta)
    arr  = data.GetPointData().GetArray('vWSS_Magnitude_1')
    vals = [arr.GetValue(i) for i in range(arr.GetNumberOfTuples())
            if arr.GetValue(i) != 0.0]
    cols_aorta.append(sorted(vals, reverse=True))

    #Aneurysm
    data = servermanager.Fetch(calcAneurysm)
    arr  = data.GetPointData().GetArray('vWSS_Magnitude_1')
    vals = [arr.GetValue(i) for i in range(arr.GetNumberOfTuples())
            if arr.GetValue(i) != 0.0]
    cols_aneurysm.append(sorted(vals, reverse=True))

# 4) Number of rows = number of points in region
n_rows_aorta    = max(len(col) for col in cols_aorta)
n_rows_aneurysm = max(len(col) for col in cols_aneurysm)

# 4.5) Compute mean WSS at each timestep
mean_aorta    = [ sum(col)/len(col) if col else 0.0 for col in cols_aorta ]
mean_aneurysm = [ sum(col)/len(col) if col else 0.0 for col in cols_aneurysm ]

log(f"Mean aorta: {mean_aorta}")
log(f"Mean aneurysm: {mean_aneurysm}")

# 4.75) Pad shorter lists with 0.0 so they all have length n_rows_*
for col in cols_aorta:
    if len(col) < n_rows_aorta:
        col.extend([0.0] * (n_rows_aorta - len(col)))

for col in cols_aneurysm:
    if len(col) < n_rows_aneurysm:
        col.extend([0.0] * (n_rows_aneurysm - len(col)))

# 5) Write Aorta CSV
csv_a = os.path.join(cwd, 'WSS_full_time_series_aorta.csv')
with open(csv_a, 'w', newline='') as f:
    writer = csv.writer(f, delimiter=';')
    # header = times
    writer.writerow([f"{t:.2f}" for t in times])
    # each row k = k-th largest over all times
    for k in range(n_rows_aorta):
        writer.writerow([ cols_aorta[i][k] for i in range(len(times)) ])

log(f"Saved full Aorta WSS time‐series to {csv_a}")

# 6) Write Aneurysm CSV
csv_an = os.path.join(cwd, 'WSS_full_time_series_aneurysm.csv')
with open(csv_an, 'w', newline='') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow([f"{t:.2f}" for t in times])
    for k in range(n_rows_aneurysm):
        writer.writerow([ cols_aneurysm[i][k] for i in range(len(times)) ])

log(f"Saved full Aneurysm WSS time‐series to {csv_an}")

# --- end export ---



SaveState(os.path.join(cwd, 'WSS_part2_post.pvsm'))
log_file.close()