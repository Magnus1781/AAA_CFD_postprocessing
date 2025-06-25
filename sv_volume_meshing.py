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
"""
def change_from_CellEntityIds_to_ModelFaceID(input_file):
    reader = vtk.vtkXMLPolyDataReader()
    reader.SetFileName(input_file)
    reader.Update()
    read_polydata = reader.GetOutput()
    print("Read polydata: " + read_polydata.GetCellData())
    # Create a model from the PolyData object.
    model = sv.modeling.PolyData()
    model.set_surface(surface=read_polydata)

    # Create the ModelFaceID.
    face_ids = model.compute_boundary_faces(angle=60.0)
    print("Model face IDs: " + str(face_ids))

    file_name = "temporary_model"
    file_format = "vtp"
    model.write(file_name=file_name, format=file_format)



def rename_vtp_field(input_file, old_name, new_name):
    reader = vtk.vtkXMLPolyDataReader()
    reader.SetFileName(input_file)
    reader.Update()
    
    polydata = reader.GetOutput()
    
    cell_data = polydata.GetCellData()
    
    array = cell_data.GetArray(old_name)
    if array:
        array.SetName(new_name)
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName(temporary_model)
    writer.SetInputData(polydata)
    writer.Write()
"""
def prepare_volumetric_mesh(
    output_path: str, face_dict: Dict[str, int], global_edge_size: float = 0.3
):
    # Initialize mesher
    mesher = sv.meshing.TetGen()
    mesher.load_model(temporary_model)

    # Set mesher options
    mesher.set_walls([face_dict["wall"]])
    mesher.set_boundary_layer_options(
        number_of_layers=5, edge_size_fraction=0.3, layer_decreasing_ratio=0.7, constant_thickness=True
    )

    options = sv.meshing.TetGenOptions()
    options.global_edge_size = global_edge_size
    options.surface_mesh_flag = True
    options.volume_mesh_flag = True
    options.optimization = 22
    options.quality_ratio = 1.4
    options.use_mmg = True
    options.no_bisect = True

    # Read centerlines
                          
    reader = vtk.vtkXMLPolyDataReader()                                  
    reader.SetFileName(centerlines_path)                                 
    reader.Update()
    centerlines=reader.GetOutput()
    print(centerlines)                           
    options.radius_meshing_centerlines = centerlines
    #print(centerlines)
    ##Dette er en mulighet, har centerlines fra AAA100 dataene og her kan vi også velge scaling på radius meshing ser det ut som, helt supert
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
    input_mesh = sys.argv[1]
    output_dir = sys.argv[2]
    face_map_file = sys.argv[3]
    global_edge_size = float(sys.argv[4])
    centerlines_path = sys.argv[5]

    with open(face_map_file) as f:
        face_dict = dict(filter(None, csv.reader(f)))
        face_dict = {k: int(v) for k, v in face_dict.items()}
        
    temporary_model = "temporary_model.vtp"

    rename_vtp_field(input_mesh, "CellEntityIds", "ModelFaceID")
    #change_from_CellEntityIds_to_ModelFaceID(input_mesh)
    prepare_volumetric_mesh(output_dir, face_dict, global_edge_size)
