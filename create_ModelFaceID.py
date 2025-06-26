"""

@author: Magnus Wennemo

"""
import sys
import vtk


def rename_vtp_field(input_file, output_file):
    # Read the input file.
    reader = vtk.vtkXMLPolyDataReader()
    reader.SetFileName(input_file)
    reader.Update()
    polydata = reader.GetOutput()
    cell_data = polydata.GetCellData()
    
    # Rename the field.
    array = cell_data.GetArray("CellEntityIds")
    if array:
        array.SetName("ModelFaceID")
    
    # Write the output file.
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName(output_file)
    writer.SetInputData(polydata)
    writer.Write()

if __name__ == "__main__":
    input_mesh = sys.argv[1]
    output_file = sys.argv[2]



    rename_vtp_field(input_mesh, output_file)
    #change_from_CellEntityIds_to_ModelFaceID(input_mesh)

