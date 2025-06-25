
import sv
import sys
import vtk

if __name__ == "__main__":
    model_file = sys.argv[1]


# Create a modeler.
kernel = sv.modeling.Kernel.POLYDATA
modeler = sv.modeling.Modeler(kernel)

# Read model geometry.
model = modeler.read(model_file)

model_polydata = model.get_polydata()

# Use node or face IDs.
use_face_ids = True 
#use_face_ids = False

# Use face IDs.
#
if use_face_ids:
    face_ids = model.get_face_ids()
    cap_ids = model.identify_caps()
    print("Face IDs: {0:s}".format(str(face_ids)))
    print("Caps: {0:s}".format(str(cap_ids)))
    inlet_ids = [2]
    outlet_ids = [3,4]


# Compute centerlines.
centerlines = model.compute_centerlines(inlet_ids, outlet_ids, use_face_ids)

## Write the centerlines. 
file_name = str('polydata-centerlines-resultstesttesttest.vtp')
writer = vtk.vtkXMLPolyDataWriter()
writer.SetFileName(file_name)
writer.SetInputData(centerlines)
writer.Update()
writer.Write()


