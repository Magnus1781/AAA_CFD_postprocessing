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
model = AAA092
#########################

cwd = f"C:/Users/magnuswe/OneDrive - SINTEF/Simvascular/results/last_cycle/{model}-last_cycle/"
#################Logging setup####################
log_file_path = os.path.join(cwd, "Qcrit_log.txt")
log_file = open(log_file_path, "w")

def log(msg):
    log_file.write(str(msg) + "\n")
    log_file.flush()
log("created log")
# get active view
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









renderView1 = GetActiveViewOrCreate('RenderView')

all_results_04770vtu= FindSource('all_results_04770.vtu*')

# show data in view
all_results_04770vtuDisplay = Show(all_results_04770vtu, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
all_results_04770vtuDisplay.Representation = 'Surface'

# show color bar/color legend
all_results_04770vtuDisplay.SetScalarBarVisibility(renderView1, True)
ColorBy(all_results_04770vtuDisplay, None)

# Properties modified on all_results_04770vtuDisplay
all_results_04770vtuDisplay.Opacity = 0.3

clip6 = FindSource('Clip6')
inlet = FindSource('inlet')


bifur = clone_clip(clip6, 'bifur', inlet)

# List all the registration names you want to remove
sources_to_delete = [
#    'PointDatatoCellData1',
#    'Transform1',
#    'TransformSTL',
#    f'{model[:6]}.stl',
#    'temporalParticlesToPathline'
#    'ParticleTracer',
#    'PolyPointSource1',
    'PythonAnnotation1',
    'Clip3',
    'Clip2',
    'Clip1',
    'TemporalInterpolator1',
    'all_results_03820.vtu*',
    'CellSize1',
    'Calculator1',
    'Clip6',
    'Clip5',
    'SurfaceNormals1',
    'all_results_04770.vtp'
]

for name in sources_to_delete:
    src = FindSource(name)
    if src is not None:
        log(f"Deleting source: {name}")
        Delete(src)
        # remove the Python reference
        del src

# create a new 'Temporal Interpolator'
temporalInterpolator1 = TemporalInterpolator(registrationName='TemporalInterpolator1', Input=all_results_04770vtu)

# get animation scene
scene = GetAnimationScene()

# Properties modified on temporalInterpolator1
temporalInterpolator1.DiscreteTimeStepInterval = 1.0
# update animation scene based on data timesteps
scene.UpdateAnimationUsingDataTimeSteps()

# Properties modified on animationScene1
scene.AnimationTime = 60

# get the time-keeper
timeKeeper1 = GetTimeKeeper()


# show data in view
bifurDisplay = Show(bifur, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
bifurDisplay.Representation = 'Surface'

# show color bar/color legend
bifurDisplay.SetScalarBarVisibility(renderView1, True)
ColorBy(bifurDisplay, None)
bifurDisplay.Set(
    AmbientColor=[1.0, 1.0, 1.0],
    DiffuseColor=[1.0, 1.0, 1.0],
)

# Properties modified on bifurDisplay
bifurDisplay.Opacity = 0.3

###############Gradient and Contour####################

# create a new 'Gradient'
gradient1 = Gradient(registrationName='Gradient1', Input=bifur)


# Properties modified on gradient1
gradient1.Set(
    ScalarArray=['POINTS', 'velocity'],
    ComputeQCriterion=1,
)

# show data in view
gradient1Display = Show(gradient1, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
gradient1Display.Representation = 'Surface'


# show color bar/color legend
gradient1Display.SetScalarBarVisibility(renderView1, True)


# create a new 'Contour'
contour1 = Contour(registrationName='Contour1', Input=gradient1)

# Properties modified on contour1
contour1.Set(
    ContourBy=['POINTS', 'Q Criterion'],
    Isosurfaces=[500.0],
)



# hide data in view
Hide(gradient1, renderView1)

# update the view to ensure updated data information
renderView1.Update()



try:
    renderView2 = FindViewOrCreate('RenderView2', viewtype='RenderView')
    # set active view
    SetActiveView(renderView2)
    # destroy renderView2
    Delete(renderView2)
    del renderView2
except:
    log("RenderView2 did not exist, so it was not deleted.")

layout1 = GetLayoutByName("Layout #1")
layout1.Collapse(2)
Hide(all_results_04770vtu, renderView1)


# show data in view
contour1Display = Show(contour1, renderView1, 'GeometryRepresentation')

# trace defaults for the display properties.
contour1Display.Representation = 'Surface'

# show color bar/color legend
contour1Display.SetScalarBarVisibility(renderView1, True)


# create a new 'Ruler'
ruler1 = Ruler(registrationName='Ruler1')


# Properties modified on ruler1
ruler1.Set(
    Point1=inlet.ClipType.Origin,
    Point2=bifur.ClipType.Origin,
)

# show data in view
ruler1Display = Show(ruler1, renderView1, 'RulerSourceRepresentation')

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on ruler1Display
ruler1Display.NumberOfTicks = 10


# Properties modified on ruler1Display
ruler1Display.AxisLineWidth = 2.0


# Properties modified on ruler1Display
ruler1Display.LabelFormat = '%6.2f'

# Properties modified on ruler1Display
ruler1Display.Visibility = 1


# Properties modified on ruler1Display
ruler1Display.Color = [0.0, 0.0, 0.0]

# Properties modified on ruler1Display
ruler1Display.FontFamily = 'Courier'

# Properties modified on renderView1
renderView1.UseColorPaletteForBackground = 0
# Properties modified on renderView1
renderView1.Background = [1.0, 1.0, 1.0]

# Properties modified on ruler1Display
ruler1Display.AxisColor = [0.3333333432674408, 0.3333333432674408, 1.0]

Hide(inlet, renderView1)
outpath = r"C:\Users\magnuswe\OneDrive - SINTEF\Dokumenter\Qcrit_VFT_figures"
SaveState(os.path.join(outpath, f'{model[:6]}_state.pvsm'))
log(f"Saved state to {model[:6]}_state.pvsm")
log("Done.")
log_file.close()