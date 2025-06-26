"""

@author: Magnus Wennemo

"""

#####load vtu files and clip below renals and the two extensions, change cwd then run this macroo########

from paraview.simple import *
import csv
import os
import math
import ast
import pandas as pd

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
AAA042 = "AAA042_0-18_1-9mill"
AAA046 = "AAA046_sim_0-17_1-5mill"
AAA087 = "AAA087_sim_0-15_1-6mill"
AAA088 = "AAA088_sim_0-15_1-7mill"
AAA091 = "AAA091_sim_0-15_1-5mill"
AAA092 = "AAA092_sim_0-15_1mill"

#####Change only this######
model = AAA039
extraClip_exists = False
iliac_aneurysm = False
normal_from_data = False
######################

#cwd = f'C://Users//magnuswe//OneDrive - SINTEF//Simvascular//results//last_cycle//{model}-last_cycle'
cwd = AAA001_2_2mill
SaveState(os.path.join(cwd, 'WSS_part1_pre.pvsm'))

log_file_path = os.path.join(cwd, "WSS_log_1.txt")
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


# 1) Load your source by its exact name
all_results_04770vtp= FindSource('all_results_04770.vtp*')

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

# …after loading average_resultvtp, and after grabbing the original clips…
clip1 = FindSource('Clip1')
inlet_first = FindSource('inlet')

if extraClip_exists:
    extraClip_first = FindSource('extraClip')
    extraClip  = clone_clip(extraClip_first,  "extraClip",  all_results_04770vtp)
    inletClip  = clone_clip(inlet_first,  "ClipInlet",  extraClip)

else:
    inletClip  = clone_clip(inlet_first,  "ClipInlet",  all_results_04770vtp)


clipBifur = Clip(registrationName = 'ClipBifur', Input=inletClip)
clipBifur.ClipType.Origin = bifurcation_origin
clipBifur.ClipType.Normal = bifurcation_normal
clipBifur.Invert = bifur_invert

clipRenals = clone_clip(clip1, "ClipRenals", all_results_04770vtp)
clipAorta  = clone_clip(clip1,  "ClipAorta",  clipRenals)
clipAorta.Invert = 0



# List all the registration names you want to remove
sources_to_delete = [
    'PointDatatoCellData1',
    'Transform1',
    'TransformSTL',
    f'{model[:6]}.stl',
    'Clip3',
    'Clip2',
    'Clip1',
    'TemporalInterpolator1',
    'inlet',
    'all_results_03820.vtu*',
    'CellSize1',
    'Clip13',
    'Clip12',
    'all_results_04770.vtu*',
    'abdominal_aorta.vtp',
    'all_results_03820.vtu*'
]

for name in sources_to_delete:
    src = FindSource(name)
    if src is not None:
        Delete(src)
        # remove the Python reference
        del src

renderView1 = GetActiveViewOrCreate('RenderView')
Hide(all_results_04770vtp, renderView1)

clipRenalsDisplay = Show(clipRenals, renderView1, 'UnstructuredGridRepresentation')

clipRenalsDisplay.Representation = 'Surface'

clipRenalsDisplay.SetScalarBarVisibility(renderView1, True)
clipAortaDisplay = Show(clipAorta, renderView1, 'UnstructuredGridRepresentation')

clipAortaDisplay.Representation = 'Surface'

clipAortaDisplay.SetScalarBarVisibility(renderView1, True)

clipInletDisplay = Show(inletClip, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
clipInletDisplay.Representation = 'Surface'

# show color bar/color legend
clipInletDisplay.SetScalarBarVisibility(renderView1, True)

clipBifurDisplay = Show(clipBifur, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
clipBifurDisplay.Representation = 'Surface'

# show color bar/color legend
clipBifurDisplay.SetScalarBarVisibility(renderView1, True)

SaveState(os.path.join(cwd, 'WSS_part1_post.pvsm'))

log("Saved state. Done.")

