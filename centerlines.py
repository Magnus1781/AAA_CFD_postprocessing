'''Test vmtk.centerlines() method.

   The centerlines geometry is written to 'centerlines-result.vtp'.
'''
import os
from pathlib import Path
import sv
import sys
import vtk

if __name__ == "__main__":
    input_model = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])
## Set some directory paths. 
#script_path = Path(os.path.realpath(__file__)).parent
#parent_path = Path(os.path.realpath(__file__)).parent.parent
#data_path = parent_path / 'data'

#try:
    #sys.path.insert(1, str(parent_path / 'graphics'))
    #import graphics as gr
#except:
    #print("Can't find the new-api-tests/graphics package.")

#win_width = 500
#win_height = 500
#renderer, renderer_window = gr.init_graphics(win_width, win_height)

# Create a modeler.
kernel = sv.modeling.Kernel.POLYDATA
modeler = sv.modeling.Modeler(kernel)

# Read model geometry.
model_file = str(input_model)
model = modeler.read(model_file)

model_polydata = model.get_polydata()
print("Model: num nodes: {0:d}".format(model_polydata.GetNumberOfPoints()))
#gr.add_geometry(renderer, model_polydata, color=[0.0, 1.0, 0.0], wire=True)

# Get model center.
com_filter = vtk.vtkCenterOfMass()
com_filter.SetInputData(model_polydata)
com_filter.SetUseScalarsAsWeights(False)
com_filter.Update()
center = com_filter.GetCenter()

## Print data arrays.
#
num_cells = model_polydata.GetNumberOfCells()
num_arrays = model_polydata.GetCellData().GetNumberOfArrays()
print("Model: num data arrays: {0:d}".format(num_arrays))

for i in range(num_arrays):
  data_type = model_polydata.GetCellData().GetArray(i).GetDataType()
  data_name = model_polydata.GetCellData().GetArrayName(i)
  cell_data = model_polydata.GetCellData().GetArray(data_name)
  print("Data name: {0:s}".format(data_name))
  if (data_name == "CapID") or (data_name == "ModelFaceID"):
      ids = set()
      for cell_id in range(num_cells):
          value = cell_data.GetValue(cell_id)
          ids.add(value)
      print("  Number of IDs: {0:d}".format(len(ids)))
      print("  IDs: {0:s}".format(str(ids)))

## Calculate centelines. 
#
# Use node IDs.
inlet_ids = [5719]
outlet_ids = [1113, 529]
#centerlines_polydata = sv.vmtk.centerlines(model_polydata, inlet_ids, outlet_ids)

# Use face IDs.
inlet_ids = [3]
outlet_ids = [2, 4]

#inlet_ids = [2]
#outlet_ids = [1,3]
centerlines_polydata = sv.vmtk.centerlines(model_polydata, inlet_ids, outlet_ids, use_face_ids=True)
#centerlines_polydata = sv.vmtk.centerlines(model_polydata, inlet_ids, outlet_ids, split=False, use_face_ids=True)

## Write the capped surface.
file_name = str(output_dir / 'centerlines-result.vtp')
print("Write centerlines to: {0:s}".format(file_name))
writer = vtk.vtkXMLPolyDataWriter()
writer.SetFileName(file_name)
writer.SetInputData(centerlines_polydata)
writer.Update()
writer.Write()

print("Centerlines: num nodes: {0:d}".format(centerlines_polydata.GetNumberOfPoints()))
#gr.add_geometry(renderer, centerlines_polydata, color=[1.0, 0.0, 0.0])

## Show geometry.
#
#camera = renderer.GetActiveCamera();
#camera.Zoom(0.5)
#camera.SetPosition(center[0], center[1], center[2])
#camera.SetFocalPoint(center[0], center[1], center[2])
#data_name = "ModelFaceID"
#gr.display(renderer_window)




