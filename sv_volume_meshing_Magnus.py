"""

@author: Patryk Rygiel, Magnus Wennemo

@Note: Patryk Rygiel wrote the baseline script with setting meshing parameters and writing out file. Magnus Wennemo added radius based meshing

"""

import csv
import os
import sys
from typing import Dict
import numpy as np

import sv
import vtk

def save_vtk(mesh, filename):
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName(filename)
    writer.SetInputData(mesh)
    writer.Update()

def prepare_volumetric_mesh(
        input_model: str, 
        output_path: str, 
        face_dict: Dict[str, int], 
        global_edge_size: float, 
        ):
    # Initialize mesher
    mesher = sv.meshing.TetGen()
    mesher.load_model(input_model)

    # Running initial meshing to compute caps area and center
    mesher.set_walls([face_dict["wall"]])
    options = sv.meshing.TetGenOptions()
    options.global_edge_size = 0.3
    options.surface_mesh_flag = True
    options.volume_mesh_flag = True
    mesher.generate_mesh(options)

    # Running desired meshing
    mesher.set_boundary_layer_options(
        number_of_layers=5, edge_size_fraction=0.3, layer_decreasing_ratio=0.7, constant_thickness=True
    )
    list = []
    min_radius = 10
    for face_name, face_id in face_dict.items():
        if face_name == "wall":
            continue
        else:
            caps_polydata=mesher.get_face_polydata(face_id)

            # Center of caps
            center_of_mass_obj=vtk.vtkCenterOfMass()
            center_of_mass_obj.SetInputData(caps_polydata)
            center_of_mass_obj.Update()
            center_tuple = center_of_mass_obj.GetCenter()
            center = [float(coord) for coord in center_tuple]

            # Area of caps
            caps_area_obj=vtk.vtkMassProperties()
            caps_area_obj.SetInputData(caps_polydata)
            caps_area_obj.Update()
            area=caps_area_obj.GetSurfaceArea()
            radius=np.sqrt(area/np.pi)
            if radius < min_radius:
                min_radius = radius
            
            # Spherical refinement

            # Factor to increase the edge size of the aorta
            """
            if face_name == "inflow":
                aorta_factor = 1.3
            else:
                aorta_factor = 1.0
            """
            sphere1 = { 'edge_size': global_edge_size, 'radius': radius, 'center': center }
            list.append(sphere1)
    sphere_edge_size_factor =1
    for sphere in list:
        sphere['edge_size'] *= np.sqrt(sphere['radius']/min_radius) * sphere_edge_size_factor# increase edge size with radius
        sphere['radius'] *= 9 # 9 is a factor to increase the radius
        # Append sphere to options
        options.sphere_refinement.append(sphere)
    
    
    
    # Set other options
    options.global_edge_size = global_edge_size
    options.surface_mesh_flag = True
    options.volume_mesh_flag = True
    options.optimization = 22
    options.quality_ratio = 1.5
    options.use_mmg = True #False for some of the geometries
    options.no_bisect = True
    options.sphere_refinement_on = True
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
    os.remove("boundarylayermesh_normals.vtu")
    os.remove("boundarylayermesh.vtu")
    os.remove("innerSurface.vtu")

if __name__ == "__main__":
    input_model = sys.argv[1]
    output_dir = sys.argv[2]
    face_map_file = sys.argv[3]
    global_edge_size = float(sys.argv[4])

    with open(face_map_file) as f:
        face_dict = dict(filter(None, csv.reader(f)))
        face_dict = {k: int(v) for k, v in face_dict.items()}

    prepare_volumetric_mesh(input_model, output_dir, face_dict, global_edge_size)
    print("Done")