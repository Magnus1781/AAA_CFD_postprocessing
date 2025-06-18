from paraview.simple import *
import numpy as np
import os
import pandas as pd
import ast
import csv
import math
from collections import defaultdict

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

##Change this part only##
model = AAA039
normal_from_data = True
iliac_aneurysm = False
#########################

cwd = f"C:/Users/magnuswe/OneDrive - SINTEF/Simvascular/results/two_last_cycles/{model}-two_last_cycles/"
offset_distance = 0.001  # 10 micrometres in cm from the surface 
#################Logging setup####################
log_file_path = os.path.join(cwd, "washout_log.txt")
log_file = open(log_file_path, "w")

def log(msg):
    log_file.write(str(msg) + "\n")
    log_file.flush()
log("created log")


############For every model except the AAA013 this is valid, but because there is a different clip for the aneurysm in AAA013 i need a different method####
if not iliac_aneurysm:
    geo_file_path = f"C:/Users/magnuswe/OneDrive - SINTEF/Simvascular/results/two_last_cycles/{model}-two_last_cycles/"
    geo_data=pd.read_csv(os.path.join(geo_file_path, 'geometric_values.csv'), sep=";")
else:
    ##This is the method for AAA013. Where i create a csv file manually (easy to script but too late at this point), and then call it bottom_aneurysm.csv##
    geo_file_path = f"C:/Users/magnuswe/OneDrive - SINTEF/Simvascular/results/two_last_cycles/{model}-two_last_cycles/"
    geo_data=pd.read_csv(os.path.join(geo_file_path, 'bottom_aneurysm.csv'), sep=";")
SaveState(os.path.join(cwd, 'paraview_washout_pre.pvsm'))

####I take a shortcut here for AAA013, where bottom_aneurysm is assigned to the bifurcation parameters.
###############Normal#################
if not iliac_aneurysm:
    log("Extracting bifurcation origin and normal from data...")
    bifurcation_origin = ast.literal_eval(geo_data['bifurcation_origin'].iloc[0])
    log("Extracted origin")
    if normal_from_data:
        bifurcation_normal = ast.literal_eval(geo_data['bifurcation_normal'].iloc[0])
    else:
        bifurcation_normal = [0.0, 0.0, 1.0]
    log("Extracted normal")
    bifur_invert = 0 #1 or 0
else:
    log("hERE")
    bifurcation_origin = ast.literal_eval(geo_data['bottom_aneurysm_origin'].iloc[0])
    log("hERE")
    bifurcation_normal = ast.literal_eval(geo_data['bottom_aneurysm_normal'].iloc[0])
    bifur_invert = 1
log("hERE")
######Creating directory for storing screenshots###############
frame_dir = os.path.join(cwd, "particle_washout_screenshots")

log("hERE")
os.makedirs(frame_dir, exist_ok=True)

log("hERE")

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
renderView2 = FindViewOrCreate('RenderView2', viewtype='RenderView')

# update the view to ensure updated data information
renderView1.Update()
log("hERE")
for name in ['Clip10', 'PointDatatoCellData1', 'CellSize1']:
    try:
        src = FindSource(name)
        if src is not None:
            Delete(src)
            del src
            log(f"Deleted {name}")
        else:
            log(f"{name} not present (returned None)")
    except Exception as e:
        log(f"Lookup/deletion of {name} failed, skipping: {e}")


all_results_03820vtu= FindSource('all_results_03820.vtu*')

all_results_04770vtp= FindSource('all_results_04770.vtp')

temporalInterpolator1 = FindSource("TemporalInterpolator1")

temporalInterpolator1.DiscreteTimeStepInterval = 0.02

# hide data in view
Hide(temporalInterpolator1, renderView1)


###############Adding surface normals to vtp#################
# create a new 'Surface Normals'
surfaceNormals1 = SurfaceNormals(registrationName='SurfaceNormals1', Input=all_results_04770vtp)

# show data in view
surfaceNormals1Display = Show(surfaceNormals1, renderView1, 'GeometryRepresentation')

# trace defaults for the display properties.
surfaceNormals1Display.Representation = 'Surface'

#################Copying clips to vtp####################
clipInlet = FindSource('inlet')

clip5 = Clip(registrationName = 'Clip5', Input=surfaceNormals1)
clip5.ClipType.Origin = clipInlet.ClipType.Origin
clip5.ClipType.Normal = clipInlet.ClipType.Normal


clip6 = Clip(registrationName = 'Clip6', Input=clip5)
clip6.ClipType.Origin = bifurcation_origin
clip6.ClipType.Normal = bifurcation_normal
clip6.Invert = bifur_invert


clip3 = FindSource('Clip3')

clip3Display = Show(clip3, renderView1, 'UnstructuredGridRepresentation')

clip3Display.Opacity = 0.3

# update the view to ensure updated data information
renderView1.Update()


# create a new 'Calculator'
calculator1 = Calculator(registrationName='Calculator1', Input=clip6)

# Properties modified on calculator1
calculator1.Set(
    ResultArrayName='scaled_Normals',
    Function=f'Normals*{offset_distance}',
)

# Fetch the output of the Calculator that contains "scaled_Normals"
calculator_output = servermanager.Fetch(calculator1)

offset_points = []       # List to store new offset points

points = calculator_output.GetPoints()
normals = calculator_output.GetPointData().GetArray("scaled_Normals")

if normals is None:
    log("ERROR: 'scaled_Normals' array not found in calculator output.")
    raise ValueError("Missing normals in calculator output.")
    
log("Getting points")
for i in range(points.GetNumberOfPoints()):
    p = np.array(points.GetPoint(i))             # Original point as NumPy array
    n = np.array(normals.GetTuple(i))            # Normal vector'
    offset_point = p + n       # New point inside domain
    offset_points.append(offset_point)
renderView1.Update()



# create a new 'Poly Point Source'
polyPointSource1 = PolyPointSource(registrationName='PolyPointSource1')
# get display properties
polyPointSource1Display = GetRepresentation(polyPointSource1, view=renderView1)




log("got points")
log(f"Number of offset points: {len(offset_points)}")
log(f"First 3 offset points: {[p.tolist() for p in offset_points[:3]]}")
log("making sources")

point_list=[]

for point in offset_points:
   point_list.extend(point)

polyPointSource1.Points = point_list

# show data in view
polyPointSource1Display = Show(polyPointSource1, renderView1, 'GeometryRepresentation')

# trace defaults for the display properties.
polyPointSource1Display.Representation = 'Surface'
renderView1.Update()

log("done making source")

log("making tracer")

tracer = ParticleTracer(registrationName=f'ParticleTracer', Input=clip3, SeedSource=polyPointSource1)
tracerDisplay = Show(tracer, renderView1, 'GeometryRepresentation')
tracerDisplay.Representation = 'Surface'

log("Making temp pathlines")

temppar_obj = TemporalParticlesToPathlines(registrationName='temporalParticlesToPathline', Input=tracer, Selection=None)
temppar_obj.MaskPoints = 0


log(f"TemporalParticlesToPathlines created with input Tracer")

renderView1.Update()

camera1 = renderView1.GetActiveCamera()
camera2 = renderView2.GetActiveCamera()

renderView1.Set(
    CameraPosition=camera1.GetPosition(),
    CameraFocalPoint=camera1.GetFocalPoint(),
    CameraViewUp=camera1.GetViewUp(),
    CameraParallelScale=renderView1.CameraParallelScale,
)

# current camera placement for renderView2
renderView2.Set(
    CameraPosition=camera2.GetPosition(),
    CameraFocalPoint=camera2.GetFocalPoint(),
    CameraViewUp=camera2.GetViewUp(),
    CameraParallelScale=renderView2.CameraParallelScale,
)

Hide(all_results_03820vtu, renderView1)
Hide(all_results_04770vtp, renderView1)
Hide(surfaceNormals1, renderView1)
Hide(polyPointSource1, renderView1)
Hide(tracer, renderView1)

for name in ['Transform1', 'abdominal_aorta.vtp', 'TransformSTL', f'{model[:6]}.stl']:
    try:
        src = FindSource(name)
        if src is not None:
            Delete(src)
            del src
            log(f"Deleted {name}")
        else:
            log(f"{name} not present (returned None)")
    except Exception as e:
        log(f"Lookup/deletion of {name} failed, skipping: {e}")

# get layout
layout1 = GetLayout()
try:
    layout1.SplitHorizontal(0, 0.5)
    layout1.AssignView(0, renderView1)
    layout1.AssignView(1, renderView2)
except RuntimeError:
    # layout was already split, so skip
    pass
#--------------------------------
# saving layout sizes for layouts



layout1.SetSize(2484, 708)

# find view
renderView1 = FindViewOrCreate('RenderView1', viewtype='RenderView')

# set active view
SetActiveView(renderView1)

# find source
all_results_03820vtu = FindSource('all_results_03820.vtu*')

# hide data in view
Hide(all_results_03820vtu, renderView1)

# find source
temporalInterpolator1 = FindSource('TemporalInterpolator1')

# hide data in view
Hide(temporalInterpolator1, renderView1)


# hide data in view
Hide(clipInlet, renderView1)




# show data in view
temporalParticlesToPathlineDisplay = Show(OutputPort(temppar_obj, 1), renderView1, 'GeometryRepresentation')

# trace defaults for the display properties.
temporalParticlesToPathlineDisplay.Representation = 'Surface'

# get display properties
clip3Display = GetRepresentation(clip3, view=renderView1)

# Properties modified on 3Display
clip3Display.Opacity = 0.3


objDisplay = Show(OutputPort(temppar_obj, 1), renderView2, 'GeometryRepresentation')
objDisplay.Representation = 'Surface'

clip3renderview2Display = Show(clip3, renderView2, 'UnstructuredGridRepresentation')
clip3renderview2Display.Opacity = 0.3
clip3Display.SetScalarBarVisibility(renderView1, False)
clip3renderview2Display.SetScalarBarVisibility(renderView2, False)

#######Adding time annotation###########
# create a new 'Python Annotation'
pythonAnnotation1 = PythonAnnotation(registrationName='PythonAnnotation1', Input=all_results_03820vtu)
pythonAnnotation1.Expression = '"Time: %5.3f s" % (time_value/100)'
pythonAnnotation1Display = Show(pythonAnnotation1, renderView1, 'TextSourceRepresentation')
renderView1.Update()
renderView1.AxesGrid.Visibility = 0
#################Washout tracking####################
# Get time range from the animation scene
scene = GetAnimationScene()
t0 = scene.TimeKeeper.TimestepValues[0]  # Start time
t1 = scene.TimeKeeper.TimestepValues[-1] # End time

# Set fine time resolution
dt = 0.02


fine_timesteps = np.arange(t0, t1 + dt, dt)
log(f"Timestep is set to {dt}")
log(f"First timestep: {t0}, Last timestep: {t1}")


data = servermanager.Fetch(tracer)
points = data.GetPoints()
num_points_start = points.GetNumberOfPoints()


skip = 3 
frame_counter = 0

log(f"Number of points at beginning: {num_points_start}")

SaveState(os.path.join(cwd, 'paraview_washout_post.pvsm'))

for t in fine_timesteps:
    scene.AnimationTime = float(t)
    t= round(t, 2)
    # update the view to ensure updated data information
    renderView1.Update()
    data = servermanager.Fetch(tracer)
    points = data.GetPoints()
    num_points = points.GetNumberOfPoints()
    if t%1 == 0:
        log(f"Number of points at t = {t}: {num_points}")
    if abs(t - 95) < 1e-06:
        num_points_end_first_cycle = num_points
        log(f"Number of points after the first cycle: {num_points_end_first_cycle}")
    

    # Inside your loop over time steps:
    if abs(t - 190.0) < 1e-6:
        num_points_end_second_cycle = num_points
        log(f"Number of points after the second cycle: {num_points_end_second_cycle}")
    if frame_counter % skip == 0:
        img_idx = frame_counter // skip
        frame_filename = os.path.join(frame_dir, f"frame_{img_idx:05d}.png")
        SaveScreenshot(frame_filename, layout1, ImageResolution=[2484, 708])
    frame_counter += 1


washout_first = 100 * (1 - num_points_end_first_cycle / num_points_start)
washout_second = 100 * (1 - num_points_end_second_cycle / num_points_start)

summary_data = [
    ("Points at beginning", num_points_start),
    ("Points at end of first cycle", num_points_end_first_cycle),
    ("Points at end of second cycle", num_points_end_second_cycle),
    ("Washout probability first cycle", f"{washout_first:.2f}%"),
    ("Washout probability second cycle", f"{washout_second:.2f}%")
]

summary_df = pd.DataFrame(summary_data, columns=["Metric", "Value"])
summary_path = os.path.join(cwd, "washout_values.csv")
summary_df.to_csv(summary_path, index=False, sep=';')

log(f"Saved washout summary to {summary_path}")



log_file.close()
