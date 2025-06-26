"""

@author: Magnus Wennemo

"""

from paraview.simple import *
import os
import numpy as np
from vtk.util.numpy_support import vtk_to_numpy

# ─────────────────────────────────────────────────────────────────────────────
# 1) Model selection and directory setup
# ─────────────────────────────────────────────────────────────────────────────
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

# Change this variable to switch model
model = AAA092

cwd = f"C:/Users/magnuswe/OneDrive - SINTEF/Simvascular/results/{model}-6cycles/"
SaveState(os.path.join(cwd, "paraview_SurfaceflowPressure_pre.pvsm"))

##Logging setup##
log_file_path = os.path.join(cwd, "surfaceFlowPressure_log.txt")
log_file = open(log_file_path, "w")

def log(msg):
    log_file.write(msg + "\n")
    log_file.flush()
log("Created log")

# ─────────────────────────────────────────────────────────────────────────────
# 2) Safe deletion helper
# ─────────────────────────────────────────────────────────────────────────────
def safe_delete(source_name):
    try:
        src = FindSource(source_name)
        if src is not None:
            Delete(src)
            del src
    except Exception:
        pass

# ─────────────────────────────────────────────────────────────────────────────
# 3) Initial pipeline setup
# ─────────────────────────────────────────────────────────────────────────────
all_results_vtu = FindSource('all_results_00010.vtu*')
renderView1 = GetActiveViewOrCreate('RenderView')



# Remove unused pipeline items if they exist
safe_delete('all_results_04770.vtp')
safe_delete('Transform1')
safe_delete('AAA001.stl')
safe_delete('PointDatatoCellData1')
safe_delete('CellSize1')
safe_delete('Clip13')
safe_delete('Clip12')
safe_delete('all_results_04770.vtu*')
# ─────────────────────────────────────────────────────────────────────────────
# 4) Animation setup and create slices by cloning existing clips
# ─────────────────────────────────────────────────────────────────────────────
animationScene = GetAnimationScene()
animationScene.GoToFirst()

def clone_clip(clip_src, new_name, new_input):
    """
    Clone whatever Clip filter `clip_src` is (Plane or Box) onto `new_input`,
    giving it the registrationName `new_name`.
    """
    ct = clip_src.ClipType
    ct_name = type(ct).__name__
    new_slice = Slice(registrationName=new_name, Input=new_input)
    if "Plane" in ct_name:
        new_slice.SliceType = 'Plane'
        new_slice.SliceType.Origin = clip_src.ClipType.Origin
        new_slice.SliceType.Normal = clip_src.ClipType.Normal
    elif "Box" in ct_name:
        new_slice.SliceType = 'Box'
        new_slice.SliceType.Position = clip_src.ClipType.Position
        new_slice.SliceType.Rotation = clip_src.ClipType.Rotation
        new_slice.SliceType.Length   = clip_src.ClipType.Length
    else:
        raise RuntimeError(f"clone_clip: unsupported ClipType {ct_name}")
    return new_slice

# Assume clips named “aorta”, “left”, “right” already exist in the pipeline
aorta = FindSource('aorta')
left  = FindSource('left')
right = FindSource('right')

slice_aorta  = clone_clip(aorta,  "Slice_aorta",  all_results_vtu)
slice_left   = clone_clip(left,   "Slice_left",   all_results_vtu)
slice_right  = clone_clip(right,  "Slice_right",  all_results_vtu)

# ─────────────────────────────────────────────────────────────────────────────
# 5) Create Calculator + SurfaceFlow filters for each slice
# ─────────────────────────────────────────────────────────────────────────────
calculators = {}
flows       = {}

# Aorta
iv  = IntegrateVariables(Input=slice_aorta)
ctp = CellDatatoPointData(Input=iv)
calc = Calculator(registrationName="Calc_aorta", Input=ctp)
calc.ResultArrayName = "p_avg_aorta"
calc.Function        = "pressure / Area"
sf   = SurfaceFlow(registrationName="Flow_aorta", Input=slice_aorta)
sf.SelectInputVectors = ['POINTS', 'velocity']

calculators['aorta'] = calc
flows      ['aorta'] = sf

# Left
iv  = IntegrateVariables(Input=slice_left)
ctp = CellDatatoPointData(Input=iv)
calc = Calculator(registrationName="Calc_left", Input=ctp)
calc.ResultArrayName = "p_avg_left"
calc.Function        = "pressure / Area"
sf   = SurfaceFlow(registrationName="Flow_left", Input=slice_left)
sf.SelectInputVectors = ['POINTS', 'velocity']

calculators['left'] = calc
flows      ['left'] = sf

# Right
iv  = IntegrateVariables(Input=slice_right)
ctp = CellDatatoPointData(Input=iv)
calc = Calculator(registrationName="Calc_right", Input=ctp)
calc.ResultArrayName = "p_avg_right"
calc.Function        = "pressure / Area"
sf   = SurfaceFlow(registrationName="Flow_right", Input=slice_right)
sf.SelectInputVectors = ['POINTS', 'velocity']

calculators['right'] = calc
flows      ['right'] = sf




#################### Setting up spreadsheets ####################

# 5a) Arrange a 3×2 grid of SpreadsheetViews in the layout:
#     Row order:    [Calc_aorta,    Flow_aorta]
#                   [Calc_left,    Flow_left]
#                   [Calc_right,   Flow_right]

# Get the main layout
layout1 = GetLayout()

# Ensure layout starts with a single cell
# (if there are leftover subviews, they’ll be overwritten by our splits)
# Split into three horizontal rows
layout1.SplitHorizontal(0, 0.33)   # now have two rows: [0], [1]
layout1.SplitHorizontal(1, 0.50)   # now have three rows: [0], [1], [2]

# Row 0: split into two columns (Calc_aorta / Flow_aorta)
layout1.SplitVertical(0, 0.50)

# Row 1: split into two columns (Calc_left / Flow_left)
layout1.SplitVertical(2, 0.50)

# Row 2: split into two columns (Calc_right / Flow_right)
layout1.SplitVertical(4, 0.50)

# Now create one SpreadSheetView per filter and assign to corresponding cell:
# ─────────────────────────────────────────────────────────────────────────
# Row 0, Col 0: Calc_aorta
spreadSheetCalcAorta = CreateView('SpreadSheetView')
spreadSheetCalcAorta.Set(BlockSize=1024)
AssignViewToLayout(view=spreadSheetCalcAorta, layout=layout1, hint=0)
Show(calculators['aorta'], spreadSheetCalcAorta, 'SpreadSheetRepresentation')

# Row 0, Col 1: Flow_aorta
spreadSheetFlowAorta = CreateView('SpreadSheetView')
spreadSheetFlowAorta.Set(BlockSize=1024)
AssignViewToLayout(view=spreadSheetFlowAorta, layout=layout1, hint=1)
Show(flows['aorta'], spreadSheetFlowAorta, 'SpreadSheetRepresentation')

# Row 1, Col 0: Calc_left
spreadSheetCalcLeft = CreateView('SpreadSheetView')
spreadSheetCalcLeft.Set(BlockSize=1024)
AssignViewToLayout(view=spreadSheetCalcLeft, layout=layout1, hint=2)
Show(calculators['left'], spreadSheetCalcLeft, 'SpreadSheetRepresentation')

# Row 1, Col 1: Flow_left
spreadSheetFlowLeft = CreateView('SpreadSheetView')
spreadSheetFlowLeft.Set(BlockSize=1024)
AssignViewToLayout(view=spreadSheetFlowLeft, layout=layout1, hint=3)
Show(flows['left'], spreadSheetFlowLeft, 'SpreadSheetRepresentation')

# Row 2, Col 0: Calc_right
spreadSheetCalcRight = CreateView('SpreadSheetView')
spreadSheetCalcRight.Set(BlockSize=1024)
AssignViewToLayout(view=spreadSheetCalcRight, layout=layout1, hint=4)
Show(calculators['right'], spreadSheetCalcRight, 'SpreadSheetRepresentation')

# Row 2, Col 1: Flow_right
spreadSheetFlowRight = CreateView('SpreadSheetView')
spreadSheetFlowRight.Set(BlockSize=1024)
AssignViewToLayout(view=spreadSheetFlowRight, layout=layout1, hint=5)
Show(flows['right'], spreadSheetFlowRight, 'SpreadSheetRepresentation')

################## End adjusted section ##################







# ─────────────────────────────────────────────────────────────────────────────
# 6) Iterate through timesteps, fetch pressure & flow, and write CSVs
# ─────────────────────────────────────────────────────────────────────────────
num_timesteps = 572
timestep_interval = 1  # each index corresponds to 1.0 time unit
time_values = np.arange(num_timesteps) * timestep_interval

# Prepare storage arrays
pressure_data = {name: [] for name in ['aorta','left','right']}
flow_data     = {name: [] for name in ['aorta','left','right']}

# Create TemporalInterpolator if not already present
temporalInterpolator2 = TemporalInterpolator(registrationName='TemporalInterpolator2', Input=all_results_vtu)
temporalInterpolator2.DiscreteTimeStepInterval = 1.0
animationScene.UpdateAnimationUsingDataTimeSteps()
for t in range(num_timesteps):
    animationScene.AnimationTime = t
    renderView1.Update()
    for name in ['aorta', 'left', 'right']:
        # Update the calculator filter to current time
        renderView1.Update()
        calc = calculators[name]
        calc.UpdatePipeline()
        c_table = servermanager.Fetch(calc)
        p_arr = c_table.GetPointData().GetArray(f"p_avg_{name}")
        # There should be exactly one value (integrated average); read index 0
        p_val = p_arr.GetValue(0)
        pressure_data[name].append(p_val)

        # Update the SurfaceFlow filter to current time
        sf = flows[name]
        sf.UpdatePipeline()
        f_table = servermanager.Fetch(sf)
        f_arr = f_table.GetPointData().GetArray("Surface Flow")
        f_val = f_arr.GetValue(0)
        flow_data[name].append(f_val)

# Write out CSVs with “;” separator
for name in ['aorta', 'left', 'right']:
    # Pressure CSV
    with open(os.path.join(cwd, f"p_avg_{name}.csv"), "w") as f:
        f.write("Time;Pressure\n")
        for t, val in zip(time_values, pressure_data[name]):
            f.write(f"{t};{val}\n")

    # Flow CSV
    with open(os.path.join(cwd, f"surface_flow_{name}.csv"), "w") as f:
        f.write("Time;Flow\n")
        for t, val in zip(time_values, flow_data[name]):
            f.write(f"{t};{val}\n")

# ─────────────────────────────────────────────────────────────────────────────
# 7) Save ParaView state for later inspection
# ─────────────────────────────────────────────────────────────────────────────
SaveState(os.path.join(cwd, "paraview_SurfaceflowPressure_post.pvsm"))
