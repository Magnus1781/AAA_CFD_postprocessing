"""

@author: Magnus Wennemo

"""
from paraview.simple import *
import numpy as np
import os
import pandas as pd
import ast

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
model = AAA013
clipped_iliacs = False
normal_from_data = True
###############################
cwd = f"C:/Users/magnuswe/OneDrive - SINTEF/Simvascular/results/last_cycle/{model}-last_cycle/"
geo_file_path = f"C:/Users/magnuswe/OneDrive - SINTEF/Simvascular/results/two_last_cycles/{model}-two_last_cycles/"

log_path = os.path.join(cwd, 'KE_log.txt')
data=pd.read_csv(os.path.join(geo_file_path, 'geometric_values.csv'), sep=";")



#################Logging setup####################
log_file_path = os.path.join(cwd, "KE_log.txt")
log_file = open(log_file_path, "w")

def log(msg):
    log_file.write(str(msg) + "\n")
    log_file.flush()

###############Normal#################
log("Extracting bifurcation origin and normal from data...")
bifurcation_origin = ast.literal_eval(data['bifurcation_origin'].iloc[0])
log("Extracted origin")
if normal_from_data:
    bifurcation_normal = ast.literal_eval(data['bifurcation_normal'].iloc[0])
else:
    bifurcation_normal = [0.0, 0.0, 1.0]
log("Extracted normal")





log(bifurcation_normal)
log(bifurcation_origin)
log("Bifurcation origin and normal set.")

# get animation scene
animationScene1 = GetAnimationScene()

# Properties modified on animationScene1
animationScene1.AnimationTime = 20.0
log("Animation time set to 20.0.")

log("Starting kinetic energy calculation...")       
# find source
all_results_04770vtu = FindSource('all_results_04770.vtu*')

# find source
clip1 = FindSource('Clip1')

if clipped_iliacs:
    clip99 = FindSource("Clip99")
    clip2 = Clip(registrationName='Clip2', Input=clip99)
else:
    clip2 = Clip(registrationName='Clip2', Input=all_results_04770vtu)


clip2.ClipType.Origin = clip1.ClipType.Origin
clip2.ClipType.Normal = clip1.ClipType.Normal

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# create a new 'Clip'
clip3 = Clip(registrationName='Clip3', Input=clip2)

# Properties modified on clip2.ClipType
clip3.ClipType.Set(
    Origin=bifurcation_origin,
    Normal=bifurcation_normal,
)
clip3.Invert = 0

Delete(clip1)
del clip1

for name in ['Clip10', 'all_results_03820.vtu*', 'Transform1', 'abdominal_aorta.vtp']:
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





# get the time-keeper
timeKeeper1 = GetTimeKeeper()

# create a new 'Cell Size'
cellSize1 = CellSize(registrationName='CellSize1', Input=clip3)

# get layout
layout1 = GetLayout()

# split cell
layout1.SplitHorizontal(0, 0.5)
log("Layout split into two horizontal sections.")
# set active view
SetActiveView(None)

# Create a new 'SpreadSheet View'
spreadSheetView1 = CreateView('SpreadSheetView')
spreadSheetView1.Set(
    ColumnToSort='',
    BlockSize=1024,
)

# assign view to a particular cell in the layout
AssignViewToLayout(view=spreadSheetView1, layout=layout1, hint=2)

# set active source
SetActiveSource(cellSize1)

# show data in view
cellSize1Display = Show(cellSize1, spreadSheetView1, 'SpreadSheetRepresentation')

# Properties modified on spreadSheetView1
spreadSheetView1.FieldAssociation = 'Cell Data'





# show data in view
cellSize1Display = Show(cellSize1, spreadSheetView1, 'SpreadSheetRepresentation')


# create a new 'Point Data to Cell Data'
pointDatatoCellData1 = PointDatatoCellData(registrationName='PointDatatoCellData1', Input=cellSize1)

# show data in view
pointDatatoCellData1Display = Show(pointDatatoCellData1, spreadSheetView1, 'SpreadSheetRepresentation')

# hide data in view
Hide(cellSize1, spreadSheetView1)

# update the view to ensure updated data information
spreadSheetView1.Update()
log("Point data converted to cell data.")
output_file = os.path.join(cwd, f'KE_data_at_t={animationScene1.AnimationTime}.csv')
# export view
ExportView(output_file, view=spreadSheetView1, RealNumberPrecision=9)
log(f"Data exported to {output_file}.")
#================================================================
# addendum: following script captures some of the application
# state to faithfully reproduce the visualization during playback
#================================================================

#--------------------------------
# saving layout sizes for layouts

# layout/tab size in pixels
layout1.SetSize(1355, 993)

#-----------------------------------
# saving camera placements for views

# current camera placement for renderView1
camera1 = renderView1.GetActiveCamera()

renderView1.Set(
    CameraPosition=camera1.GetPosition(),
    CameraFocalPoint=camera1.GetFocalPoint(),
    CameraViewUp=camera1.GetViewUp(),
    CameraParallelScale=renderView1.CameraParallelScale,
)

# show data in view
clip3Display = Show(clip3, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
clip3Display.Representation = 'Surface'

# show color bar/color legend
clip3Display.SetScalarBarVisibility(renderView1, True)

# reset view to fit data
renderView1.ResetCamera(False, 0.9)
clip3Display.Set(
    AmbientColor=[1.0, 0.3333333432674408, 1.0],
    DiffuseColor=[1.0, 0.3333333432674408, 1.0],
)

# show data in view
clip2Display = Show(clip2, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
clip2Display.Representation = 'Surface'

# show color bar/color legend
clip2Display.SetScalarBarVisibility(renderView1, True)

# turn off scalar coloring
ColorBy(clip2Display, None)

SaveState(os.path.join(cwd, 'paraview_KE.pvsm'))
log("State saved")