from paraview.simple import *
import numpy as np
import os
import pandas as pd
import ast
import csv
import math

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
second_cl_clip = False
#########################

cwd = f"C:/Users/magnuswe/OneDrive - SINTEF/Simvascular/results/two_last_cycles/{model}-two_last_cycles/"
vtp_dir = f"C:\\Users\\magnuswe\\OneDrive - SINTEF\\Simvascular\\results\\last_cycle\\{model}-last_cycle"


#################Logging setup####################
log_file_path = os.path.join(cwd, "particle_log1.txt")
log_file = open(log_file_path, "w")

def log(msg):
    log_file.write(msg + "\n")
    log_file.flush()

SaveState(os.path.join(cwd, 'paraview_particle_age_part1_pre.pvsm'))
log("Pre state saved.")



log("loading the centerline")
##############Load the centerline##############
# create a new 'XML PolyData Reader'
abdominal_aortavtp = FindSource("abdominal_aorta.vtp")
############Change to = FindSource('left/right_iliac.vtp') if iliac aneurysm
# Properties modified on abdominal_aortavtp
abdominal_aortavtp.TimeArray = 'None'

all_results_03820vtu= FindSource('all_results_03820.vtu*')

log("abdominal_aortavtp loaded")
############### Div render view ###############
# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
abdominal_aortavtpDisplay = Show(abdominal_aortavtp, renderView1, 'GeometryRepresentation')

# trace defaults for the display properties.
abdominal_aortavtpDisplay.Representation = 'Surface'

# reset view to fit data
renderView1.ResetCamera(False, 0.9)

# get the material library
materialLibrary1 = GetMaterialLibrary()

# update the view to ensure updated data information
renderView1.Update()

transform1 = FindSource("Transform1")

log("Transform applied to abdominal_aortavtp")
####################### Copy the inlet clip to the centerline #######################
# find source
clip1 = FindSource('Clip1')

# create a new 'Clip'
clip2 = Clip(registrationName='Clip2', Input=transform1)
#Adding a clip to the centerline



slice1 = Slice(registrationName='Slice1', Input=all_results_03820vtu)

# Copy the clip type and settings from clip1 to clip2
clip2.ClipType.Origin = clip1.ClipType.Origin
clip2.ClipType.Normal = clip1.ClipType.Normal
log("Clip2 at centerline created from Clip1 at vtu file")

################if second clip###########
if second_cl_clip:
    clip10 = FindSource("Clip10")
    clip3 = Clip(registrationName='Clip3', Input=clip2)
    clip3.ClipType.Origin = clip10.ClipType.Origin
    clip3.ClipType.Normal = clip10.ClipType.Normal

##########################Calculate inlet area, perimeter, circle_diameter and D_hyd=4*R_hyd###############################


log("Calculating inlet cross-sectional properties...")

# Step 1: Slice at inlet to get Area
slice1.SliceType.Origin = clip1.ClipType.Origin
slice1.SliceType.Normal = clip1.ClipType.Normal

integrateVariables1 = IntegrateVariables(registrationName='IntegrateVariables1', Input=slice1)
renderView1.Update()

data = servermanager.Fetch(integrateVariables1)
area_array = data.GetCellData().GetArray('Area')

if area_array is None:
    log("ERROR: 'Area' array not found in IntegrateVariables1 output")
    area = 0.0
else:
    area = area_array.GetValue(0)
    log(f"Extracted area: {area}")
    circle_formula_dia = math.sqrt(4 * area / math.pi)

# Step 2: Slice vtp file and integrate to get Perimeter
vtp_file = os.path.join(vtp_dir, 'all_results_04770.vtp')
all_results_04770vtp = XMLPolyDataReader(registrationName='all_results_04770.vtp', FileName=[vtp_file])

slice2 = Slice(registrationName='Slice2', Input=all_results_04770vtp)
slice2.SliceType.Origin = clip1.ClipType.Origin
slice2.SliceType.Normal = clip1.ClipType.Normal

Hide(all_results_04770vtp, renderView1)

integrateVariables2 = IntegrateVariables(registrationName='IntegrateVariables2', Input=slice2)
data2 = servermanager.Fetch(integrateVariables2)
perimeter_array = data2.GetCellData().GetArray('Length')

if perimeter_array is None:
    log("ERROR: 'Length' array not found in IntegrateVariables2 output")
    perimeter = 0.0
    D_hyd = 0.0
else:
    perimeter = perimeter_array.GetValue(0)
    D_hyd = 4 * area / perimeter
    log(f"Extracted perimeter: {perimeter}")
    log(f"Hydraulic diameter: {D_hyd}")

# Save values to CSV
diameter_csv_path = os.path.join(cwd, "inlet_area_dia_perimeter.csv")

df = pd.DataFrame({
    'Area (cm^2)': [area],
    'Perimeter (cm)': [perimeter],
    'Circle formula D (cm)': [circle_formula_dia],
    'Hydraulic D_hyd (cm)': [D_hyd]
})
df.to_csv(diameter_csv_path, sep=";", index=False)

log(f"Saved cross-section data to {diameter_csv_path}")

##########################################################################

#########################Render the centerline#########################
HideAll(renderView1)

# set active source
SetActiveSource(clip2)

# toggle interactive widget visibility (only when running from the GUI)
HideInteractiveWidgets(proxy=clip1.ClipType)

# toggle interactive widget visibility (only when running from the GUI)
ShowInteractiveWidgets(proxy=clip2.ClipType)

# show data in view
clip2Display = Show(clip2, renderView1, 'UnstructuredGridRepresentation')

# reset view to fit data
renderView1.ResetCamera(False, 0.9)

####################### Get the new centerline points #######################
# Access the output data

if second_cl_clip:
    clipped_data = servermanager.Fetch(clip3)
else:
    clipped_data = servermanager.Fetch(clip2)

# Extract point coordinates
points = clipped_data.GetPoints()
num_points = points.GetNumberOfPoints()

for i in range(num_points):
    pt = points.GetPoint(i)
    log(f"Point {i}: {pt}")



if second_cl_clip:
    extractSurface1 = ExtractSurface(registrationName='ExtractSurface1', Input=clip3)
    log("Exctracting double clipped centerline")
else:
    extractSurface1 = ExtractSurface(registrationName='ExtractSurface1', Input=clip2)
    log("Exctracting single clipped centerline")
# set active source
SetActiveSource(extractSurface1)
log("ExtractSurface1 set as active source")
# show data in view
clip1Display = Show(clip1, renderView1, 'UnstructuredGridRepresentation')
log("Clip1 display properties set")
# Properties modified on clip1Display
clip1Display.Opacity = 0.3
log("Clip1 opacity set to 0.3")
# toggle interactive widget visibility (only when running from the GUI)
ShowInteractiveWidgets(proxy=clip1.ClipType)

# show data in view
clip1Display = Show(clip1, renderView1, 'UnstructuredGridRepresentation')
log("Clip1 display properties set")
# trace defaults for the display properties.
clip1Display.Representation = 'Surface'

# show color bar/color legend
clip1Display.SetScalarBarVisibility(renderView1, True)


####################### Save the clipped centerline as a .vtp file #######################
# Define the output path
output_vtp_path = os.path.join(cwd, "clipped_centerline.vtp")

# Save Clip2 as a .vtp file
SaveData(output_vtp_path, proxy=extractSurface1)

log(f"Clip2 saved as VTP to {output_vtp_path}")


SaveState(os.path.join(cwd, 'paraview_particle_age_part1_post.pvsm'))
log("Post state saved.")



#################################Resetting session and preparing for part 2############################

log("Deleting pipeline objects except the vtu files")


clip1 = FindSource('Clip1')
integrateVariables1 = FindSource('IntegrateVariables1')
integrateVariables2 = FindSource('IntegrateVariables2')
slice2 = FindSource('Slice2')
extractSurface1 = FindSource('ExtractSurface1')
clip2 = FindSource('Clip2')


if second_cl_clip:
    Delete(clip3)
    del clip3
    Delete(clip10)
    del clip10

Delete(integrateVariables1)
del integrateVariables1

Delete(integrateVariables2)
del integrateVariables2

Delete(slice1)
del slice1

Delete(slice2)
del slice2

Delete(extractSurface1)
del extractSurface1

Delete(clip2)
del clip2


Delete(all_results_04770vtp)
del all_results_04770vtp

Delete(clip1)
del clip1  

Delete(transform1)
del transform1

Delete(abdominal_aortavtp)
del abdominal_aortavtp





log("Finished deleting")




renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
all_results_03820vtuDisplay = Show(all_results_03820vtu, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
all_results_03820vtuDisplay.Representation = 'Surface'




# show color bar/color legend
all_results_03820vtuDisplay.SetScalarBarVisibility(renderView1, True)



# create a new 'Temporal Interpolator'
temporalInterpolator1 = TemporalInterpolator(registrationName='TemporalInterpolator1', Input=all_results_03820vtu)

# show data in view
temporalInterpolator1Display = Show(temporalInterpolator1, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
temporalInterpolator1Display.Representation = 'Surface'

# hide data in view
Hide(all_results_03820vtu, renderView1)

# show color bar/color legend
temporalInterpolator1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# create a new 'STL Reader'
AAAstl = STLReader(registrationName=f"{model[:6]}.stl", FileNames=[f'C:\\Users\\magnuswe\\OneDrive - SINTEF\\Simvascular\\geometrier\\STLfiler\\{model[:6]}.stl'])

# show data in view
AAAstlDisplay = Show(AAAstl, renderView1, 'GeometryRepresentation')

# trace defaults for the display properties.
AAAstlDisplay.Representation = 'Surface'

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Transform'
transform1 = Transform(registrationName='TransformSTL', Input=AAAstl)


# Properties modified on transform1.Transform
transform1.Transform.Scale = [0.1, 0.1, 0.1]

# show data in view
transform1Display = Show(transform1, renderView1, 'GeometryRepresentation')

# trace defaults for the display properties.
transform1Display.Representation = 'Surface'

# hide data in view
Hide(AAAstl, renderView1)

# Reset the camera to fit all visible data
renderView1.ResetCamera(False, 0.9)

# update the view to ensure updated data information
renderView1.Update()

log("Finished with setup, ready for geometry script and part2")

