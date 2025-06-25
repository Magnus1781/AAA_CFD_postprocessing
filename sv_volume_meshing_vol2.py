import csv
import os
import sys
from typing import Dict

import sv
import vtk


def save_vtk(mesh, filename):
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName(filename)
    writer.SetInputData(mesh)
    writer.Update()

def rename_vtp_field(input_file, old_name, new_name):

    # Read the input file.
    reader = vtk.vtkXMLPolyDataReader()
    reader.SetFileName(input_file)
    reader.Update()
    
    # Rename the field.
    polydata = reader.GetOutput()
    cell_data = polydata.GetCellData()
    array = cell_data.GetArray(old_name)
    if array:
        array.SetName(new_name)
    
    # Write the output file.
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName(temporary_model)
    writer.SetInputData(polydata)
    writer.Write()
def compute_centerlines(model_file):

    # Create a modeler
    kernel = sv.modeling.Kernel.POLYDATA
    modeler = sv.modeling.Modeler(kernel)
    help(sv.meshing.TetGenOptions)
    # Read model geometry.
    model = modeler.read(model_file)
    #model_polydata = model.get_polydata()

    # Get face IDs.
    #face_ids = model.get_face_ids()
    #cap_ids = model.identify_caps()
    #print("Face IDs: {0:s}".format(str(face_ids)))
    #print("Caps: {0:s}".format(str(cap_ids)))

    inlet_ids = [face_dict["inflow"]]
    outlet_ids = [face_dict["outlet_iliac_left"],face_dict["outlet_iliac_right"]]

    print("Inlet IDs: {0:s}".format(str(inlet_ids)))
    print("Outlet IDs: {0:s}".format(str(outlet_ids)))
    
    # Compute centerlines.
    centerlines = model.compute_centerlines(inlet_ids, outlet_ids, True)

    # Write the centerlines. 
    file_name = str(centerlines_output)
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName(file_name)
    writer.SetInputData(centerlines)
    writer.Update()
    writer.Write()

    return centerlines

def prepare_volumetric_mesh(
    output_path: str, face_dict: Dict[str, int], global_edge_size: float = 0.3
):
    # Initialize mesher
    mesher = sv.meshing.TetGen()
    mesher.load_model(temporary_model)

    # Set mesher options
    mesher.set_walls([face_dict["wall"]])
    mesher.set_boundary_layer_options(
        number_of_layers=3, edge_size_fraction=0.3, layer_decreasing_ratio=0.7, constant_thickness=True
    )

    options = sv.meshing.TetGenOptions()
    options.global_edge_size = global_edge_size
    options.surface_mesh_flag = True
    options.volume_mesh_flag = True
    options.optimization = 22
    options.quality_ratio = 1.4
    #options.use_mmg = True
    options.no_bisect = True

    # Read centerlines
    #reader = vtk.vtkXMLPolyDataReader()
    #reader.SetFileName(centerlines_file) 
    #reader.Update()
    centerlines = compute_centerlines(temporary_model)
    print(centerlines)
    #Dette er en mulighet, har centerlines fra AAA100 dataene og her kan vi også velge scaling på radius meshing ser det ut som, helt supert
    options.radius_meshing_centerlines = centerlines
    options.radius_meshing_scale = 0.4
    options.radius_meshing_on = True

    # Generate mesh
    mesher.generate_mesh(options)

    # Save output files
    output_path = os.path.join(output_path, "mesh-complete")
    surfaces_output_path = os.path.join(output_path, "mesh-surfaces")
    os.makedirs(surfaces_output_path, exist_ok=True)

    mesher.write_mesh(os.path.join(output_path, "mesh-complete.mesh.vtu"))
    save_vtk(mesher.get_surface(), os.path.join(output_path, "mesh-complete.exterior.vtp"))

    for face_name, face_id in face_dict.items():
        save_vtk(mesher.get_face_polydata(face_id), os.path.join(surfaces_output_path, face_name + ".vtp"))

        if face_name == "wall":
            save_vtk(mesher.get_face_polydata(face_id), os.path.join(output_path, "walls_combined.vtp"))

    # Remove unnecessary files
    #os.remove("boundarylayermesh_normals.vtu")
    #os.remove("boundarylayermesh.vtu")
    #os.remove("innerSurface.vtu")
    os.remove("temporary_model.vtp")


if __name__ == "__main__":
    input_model = sys.argv[1]
    output_dir = sys.argv[2]
    face_map_file = sys.argv[3]
    global_edge_size = float(sys.argv[4])
    centerlines_output = sys.argv[5]

    with open(face_map_file) as f:
        face_dict = dict(filter(None, csv.reader(f)))
        face_dict = {k: int(v) for k, v in face_dict.items()}
        
    temporary_model = "temporary_model.vtp"

    rename_vtp_field(input_model, "CellEntityIds", "ModelFaceID")
    #compute_centerlines(temporary_model, centerlines_output)
    #change_from_CellEntityIds_to_ModelFaceID(input_mesh)
    prepare_volumetric_mesh(output_dir, face_dict, global_edge_size)
