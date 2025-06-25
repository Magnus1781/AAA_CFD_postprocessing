# trace generated using paraview version 5.13.3-1595-ge004b7dfe7
#import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 13

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()


file_path='C:/Users/magnuswe/OneDrive - SINTEF/Simvascular/results/AAA001_sim_0-19_1-1mill-6cycles/'

# find source
all_results_00010vtu = FindSource('all_results_00010.vtu*')

# set active source
SetActiveSource(all_results_00010vtu)

# get color transfer function/color map for 'pressure'
pressureLUT = GetColorTransferFunction('pressure')

# get opacity transfer function/opacity map for 'pressure'
pressurePWF = GetOpacityTransferFunction('pressure')

# get 2D transfer function for 'pressure'
pressureTF2D = GetTransferFunction2D('pressure')

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# get display properties
all_results_00010vtuDisplay = GetRepresentation(all_results_00010vtu, view=renderView1)

# find source
slice1 = FindSource('Slice1')

# set active source
SetActiveSource(slice1)

# toggle interactive widget visibility (only when running from the GUI)
ShowInteractiveWidgets(proxy=slice1.SliceType)

# get display properties
slice1Display = GetRepresentation(slice1, view=renderView1)

# create a new 'Integrate Variables'
integrateVariables1 = IntegrateVariables(registrationName='IntegrateVariables1', Input=slice1)

# find source
slice2 = FindSource('Slice2')

# set active source
SetActiveSource(slice2)

# toggle interactive widget visibility (only when running from the GUI)
ShowInteractiveWidgets(proxy=slice2.SliceType)

# get display properties
slice2Display = GetRepresentation(slice2, view=renderView1)

# create a new 'Integrate Variables'
integrateVariables2 = IntegrateVariables(registrationName='IntegrateVariables2', Input=slice2)

# find source
slice3 = FindSource('Slice3')

# set active source
SetActiveSource(slice3)

# toggle interactive widget visibility (only when running from the GUI)
ShowInteractiveWidgets(proxy=slice3.SliceType)

# get display properties
slice3Display = GetRepresentation(slice3, view=renderView1)

# create a new 'Integrate Variables'
integrateVariables3 = IntegrateVariables(registrationName='IntegrateVariables3', Input=slice3)

# Create a new 'SpreadSheet View'
spreadSheetView1 = CreateView('SpreadSheetView')
spreadSheetView1.Set(
    ColumnToSort='',
    BlockSize=1024,
)

# show data in view
integrateVariables3Display = Show(integrateVariables3, spreadSheetView1, 'SpreadSheetRepresentation')

# get layout
layout1 = GetLayoutByName("Layout #1")

# add view to a layout so it's visible in UI
AssignViewToLayout(view=spreadSheetView1, layout=layout1, hint=0)

# show data in view
integrateVariables2Display = Show(integrateVariables2, spreadSheetView1, 'SpreadSheetRepresentation')

# show data in view
integrateVariables1Display = Show(integrateVariables1, spreadSheetView1, 'SpreadSheetRepresentation')

# update the view to ensure updated data information
renderView1.Update()

# update the view to ensure updated data information
spreadSheetView1.Update()

# set active source
SetActiveSource(integrateVariables1)

# create a new 'Cell Data to Point Data'
cellDatatoPointData1 = CellDatatoPointData(registrationName='CellDatatoPointData1', Input=integrateVariables1)

# set active source
SetActiveSource(integrateVariables2)

# create a new 'Cell Data to Point Data'
cellDatatoPointData2 = CellDatatoPointData(registrationName='CellDatatoPointData2', Input=integrateVariables2)

# set active source
SetActiveSource(integrateVariables3)

# create a new 'Cell Data to Point Data'
cellDatatoPointData3 = CellDatatoPointData(registrationName='CellDatatoPointData3', Input=integrateVariables3)

# show data in view
cellDatatoPointData2Display = Show(cellDatatoPointData2, spreadSheetView1, 'SpreadSheetRepresentation')

# hide data in view
Hide(integrateVariables2, spreadSheetView1)

# show data in view
cellDatatoPointData1Display = Show(cellDatatoPointData1, spreadSheetView1, 'SpreadSheetRepresentation')

# hide data in view
Hide(integrateVariables1, spreadSheetView1)

# show data in view
cellDatatoPointData3Display = Show(cellDatatoPointData3, spreadSheetView1, 'SpreadSheetRepresentation')

# hide data in view
Hide(integrateVariables3, spreadSheetView1)

# update the view to ensure updated data information
spreadSheetView1.Update()

# set active source
SetActiveSource(slice1)

# toggle interactive widget visibility (only when running from the GUI)
ShowInteractiveWidgets(proxy=slice1.SliceType)

# set active source
SetActiveSource(cellDatatoPointData1)

# toggle interactive widget visibility (only when running from the GUI)
HideInteractiveWidgets(proxy=slice1.SliceType)

# create a new 'Calculator'
calculator1 = Calculator(registrationName='Calculator1', Input=cellDatatoPointData1)

# set active source
SetActiveSource(cellDatatoPointData2)

# create a new 'Calculator'
calculator2 = Calculator(registrationName='Calculator2', Input=cellDatatoPointData2)

# set active source
SetActiveSource(cellDatatoPointData3)

# create a new 'Calculator'
calculator3 = Calculator(registrationName='Calculator3', Input=cellDatatoPointData3)

# Properties modified on calculator1
calculator1.Set(
    ResultArrayName='p_avg_aorta',
    Function='pressure/Area',
)

# show data in view
calculator1Display = Show(calculator1, spreadSheetView1, 'SpreadSheetRepresentation')

# hide data in view
Hide(cellDatatoPointData1, spreadSheetView1)

# Properties modified on calculator2
calculator2.Set(
    ResultArrayName='p_avg_right',
    Function='pressure/Area',
)

# show data in view
calculator2Display = Show(calculator2, spreadSheetView1, 'SpreadSheetRepresentation')

# hide data in view
Hide(cellDatatoPointData2, spreadSheetView1)

# Properties modified on calculator3
calculator3.Set(
    ResultArrayName='p_avg_left',
    Function='pressure/Area',
)

# show data in view
calculator3Display = Show(calculator3, spreadSheetView1, 'SpreadSheetRepresentation')

# hide data in view
Hide(cellDatatoPointData3, spreadSheetView1)

# update the view to ensure updated data information
spreadSheetView1.Update()

# set active source
SetActiveSource(slice1)

# toggle interactive widget visibility (only when running from the GUI)
ShowInteractiveWidgets(proxy=slice1.SliceType)

# create a new 'Surface Flow'
surfaceFlow1 = SurfaceFlow(registrationName='SurfaceFlow1', Input=slice1)

# set active source
SetActiveSource(slice2)

# toggle interactive widget visibility (only when running from the GUI)
ShowInteractiveWidgets(proxy=slice2.SliceType)

# create a new 'Surface Flow'
surfaceFlow2 = SurfaceFlow(registrationName='SurfaceFlow2', Input=slice2)

# set active source
SetActiveSource(slice3)

# toggle interactive widget visibility (only when running from the GUI)
ShowInteractiveWidgets(proxy=slice3.SliceType)

# create a new 'Surface Flow'
surfaceFlow3 = SurfaceFlow(registrationName='SurfaceFlow3', Input=slice3)

# show data in view
surfaceFlow2Display = Show(surfaceFlow2, spreadSheetView1, 'SpreadSheetRepresentation')

# show data in view
surfaceFlow3Display = Show(surfaceFlow3, spreadSheetView1, 'SpreadSheetRepresentation')

# show data in view
surfaceFlow1Display = Show(surfaceFlow1, spreadSheetView1, 'SpreadSheetRepresentation')

# update the view to ensure updated data information
spreadSheetView1.Update()

# set active source
SetActiveSource(surfaceFlow1)

# set active source
SetActiveSource(surfaceFlow2)

# set active source
SetActiveSource(surfaceFlow1)

# hide data in view
Hide(surfaceFlow1, spreadSheetView1)

# set active source
SetActiveSource(surfaceFlow2)

# show data in view
surfaceFlow2Display = Show(surfaceFlow2, spreadSheetView1, 'SpreadSheetRepresentation')

# show data in view
surfaceFlow2Display = Show(surfaceFlow2, spreadSheetView1, 'SpreadSheetRepresentation')

# hide data in view
Hide(surfaceFlow2, spreadSheetView1)

# set active source
SetActiveSource(surfaceFlow3)

# show data in view
surfaceFlow3Display = Show(surfaceFlow3, spreadSheetView1, 'SpreadSheetRepresentation')

# show data in view
surfaceFlow3Display = Show(surfaceFlow3, spreadSheetView1, 'SpreadSheetRepresentation')

# set active source
SetActiveSource(calculator1)

# create a new 'Plot Data Over Time'
plotDataOverTime1 = PlotDataOverTime(registrationName='PlotDataOverTime1', Input=calculator1)

# set active source
SetActiveSource(surfaceFlow1)

# create a new 'Plot Data Over Time'
plotDataOverTime2 = PlotDataOverTime(registrationName='PlotDataOverTime2', Input=surfaceFlow1)

# set active source
SetActiveSource(calculator2)

# create a new 'Plot Data Over Time'
plotDataOverTime3 = PlotDataOverTime(registrationName='PlotDataOverTime3', Input=calculator2)

# set active source
SetActiveSource(surfaceFlow2)

# create a new 'Plot Data Over Time'
plotDataOverTime4 = PlotDataOverTime(registrationName='PlotDataOverTime4', Input=surfaceFlow2)

# set active source
SetActiveSource(calculator3)

# create a new 'Plot Data Over Time'
plotDataOverTime5 = PlotDataOverTime(registrationName='PlotDataOverTime5', Input=calculator3)

# set active source
SetActiveSource(surfaceFlow3)

# create a new 'Plot Data Over Time'
plotDataOverTime6 = PlotDataOverTime(registrationName='PlotDataOverTime6', Input=surfaceFlow3)

# Create a new 'Quartile Chart View'
quartileChartView1 = CreateView('QuartileChartView')

# show data in view
plotDataOverTime3Display = Show(plotDataOverTime3, quartileChartView1, 'QuartileChartRepresentation')

# add view to a layout so it's visible in UI
AssignViewToLayout(view=quartileChartView1, layout=layout1, hint=2)

# show data in view
plotDataOverTime5Display = Show(plotDataOverTime5, quartileChartView1, 'QuartileChartRepresentation')

# show data in view
plotDataOverTime4Display = Show(plotDataOverTime4, quartileChartView1, 'QuartileChartRepresentation')

# show data in view
plotDataOverTime6Display = Show(plotDataOverTime6, quartileChartView1, 'QuartileChartRepresentation')

# show data in view
plotDataOverTime2Display = Show(plotDataOverTime2, quartileChartView1, 'QuartileChartRepresentation')

# show data in view
plotDataOverTime1Display = Show(plotDataOverTime1, quartileChartView1, 'QuartileChartRepresentation')

# update the view to ensure updated data information
quartileChartView1.Update()

# Properties modified on plotDataOverTime6Display
plotDataOverTime6Display.Set(
    SeriesOpacity=['Surface Flow (stats)', '1', 'velocity (0) (stats)', '1', 'velocity (1) (stats)', '1', 'velocity (2) (stats)', '1', 'velocity (Magnitude) (stats)', '1', 'X (stats)', '1', 'Y (stats)', '1', 'Z (stats)', '1', 'N (stats)', '1', 'Time (stats)', '1', 'vtkValidPointMask (stats)', '1'],
    SeriesPlotCorner=['N (stats)', '0', 'Surface Flow (stats)', '0', 'Time (stats)', '0', 'X (stats)', '0', 'Y (stats)', '0', 'Z (stats)', '0', 'velocity (0) (stats)', '0', 'velocity (1) (stats)', '0', 'velocity (2) (stats)', '0', 'velocity (Magnitude) (stats)', '0', 'vtkValidPointMask (stats)', '0'],
    SeriesLineStyle=['N (stats)', '1', 'Surface Flow (stats)', '1', 'Time (stats)', '1', 'X (stats)', '1', 'Y (stats)', '1', 'Z (stats)', '1', 'velocity (0) (stats)', '1', 'velocity (1) (stats)', '1', 'velocity (2) (stats)', '1', 'velocity (Magnitude) (stats)', '1', 'vtkValidPointMask (stats)', '1'],
    SeriesLineThickness=['N (stats)', '2', 'Surface Flow (stats)', '2', 'Time (stats)', '2', 'X (stats)', '2', 'Y (stats)', '2', 'Z (stats)', '2', 'velocity (0) (stats)', '2', 'velocity (1) (stats)', '2', 'velocity (2) (stats)', '2', 'velocity (Magnitude) (stats)', '2', 'vtkValidPointMask (stats)', '2'],
    SeriesMarkerStyle=['N (stats)', '0', 'Surface Flow (stats)', '0', 'Time (stats)', '0', 'X (stats)', '0', 'Y (stats)', '0', 'Z (stats)', '0', 'velocity (0) (stats)', '0', 'velocity (1) (stats)', '0', 'velocity (2) (stats)', '0', 'velocity (Magnitude) (stats)', '0', 'vtkValidPointMask (stats)', '0'],
    SeriesMarkerSize=['N (stats)', '4', 'Surface Flow (stats)', '4', 'Time (stats)', '4', 'X (stats)', '4', 'Y (stats)', '4', 'Z (stats)', '4', 'velocity (0) (stats)', '4', 'velocity (1) (stats)', '4', 'velocity (2) (stats)', '4', 'velocity (Magnitude) (stats)', '4', 'vtkValidPointMask (stats)', '4'],
)

HideAll(quartileChartView1)

# set active view
SetActiveView(spreadSheetView1)

# clear all selections
ClearSelection()

# set active source
SetActiveSource(surfaceFlow3)

# set active source
SetActiveSource(plotDataOverTime1)

# show data in view
plotDataOverTime1Display_1 = Show(plotDataOverTime1, spreadSheetView1, 'SpreadSheetRepresentation')

# Properties modified on spreadSheetView1
spreadSheetView1.HiddenColumnLabels = []

# Properties modified on spreadSheetView1
spreadSheetView1.HiddenColumnLabels = ['Block Name', 'Block Number', 'Row ID', 'avg(Area)', 'avg(average_pressure)', 'avg(average_speed)', 'avg(GlobalElementID)', 'avg(GlobalNodeID)', 'avg(p_avg_aorta)', 'avg(pressure)', 'avg(timeDeriv (0))', 'avg(timeDeriv (1))', 'avg(timeDeriv (2))', 'avg(timeDeriv (3))', 'avg(timeDeriv (Magnitude))', 'avg(velocity (0))', 'avg(velocity (1))', 'avg(velocity (2))', 'avg(velocity (Magnitude))', 'avg(vinplane_traction (0))', 'avg(vinplane_traction (1))', 'avg(vinplane_traction (2))', 'avg(vinplane_traction (Magnitude))', 'avg(vWSS (0))', 'avg(vWSS (1))', 'avg(vWSS (2))', 'avg(vWSS (Magnitude))', 'avg(X)', 'avg(Y)', 'avg(Z)', 'max(Area)', 'max(average_pressure)', 'max(average_speed)', 'max(GlobalElementID)', 'max(GlobalNodeID)', 'max(p_avg_aorta)', 'max(pressure)', 'max(timeDeriv (0))', 'max(timeDeriv (1))', 'max(timeDeriv (2))', 'max(timeDeriv (3))', 'max(timeDeriv (Magnitude))', 'max(velocity (0))', 'max(velocity (1))', 'max(velocity (2))', 'max(velocity (Magnitude))', 'max(vinplane_traction (0))', 'max(vinplane_traction (1))', 'max(vinplane_traction (2))', 'max(vinplane_traction (Magnitude))', 'max(vWSS (0))', 'max(vWSS (1))', 'max(vWSS (2))', 'max(vWSS (Magnitude))', 'max(X)', 'max(Y)', 'max(Z)', 'med(Area)', 'med(average_pressure)', 'med(average_speed)', 'med(GlobalElementID)', 'med(GlobalNodeID)', 'med(p_avg_aorta)', 'med(pressure)', 'med(timeDeriv (0))', 'med(timeDeriv (1))', 'med(timeDeriv (2))', 'med(timeDeriv (3))', 'med(timeDeriv (Magnitude))', 'med(velocity (0))', 'med(velocity (1))', 'med(velocity (2))', 'med(velocity (Magnitude))', 'med(vinplane_traction (0))', 'med(vinplane_traction (1))', 'med(vinplane_traction (2))', 'med(vinplane_traction (Magnitude))', 'med(vWSS (0))', 'med(vWSS (1))', 'med(vWSS (2))', 'med(vWSS (Magnitude))', 'med(X)', 'med(Y)', 'med(Z)', 'min(Area)', 'min(average_pressure)', 'min(average_speed)', 'min(GlobalElementID)', 'min(GlobalNodeID)', 'min(p_avg_aorta)', 'min(pressure)', 'min(timeDeriv (0))', 'min(timeDeriv (1))', 'min(timeDeriv (2))', 'min(timeDeriv (3))', 'min(timeDeriv (Magnitude))', 'min(velocity (0))', 'min(velocity (1))', 'min(velocity (2))', 'min(velocity (Magnitude))', 'min(vinplane_traction (0))', 'min(vinplane_traction (1))', 'min(vinplane_traction (2))', 'min(vinplane_traction (Magnitude))', 'min(vWSS (0))', 'min(vWSS (1))', 'min(vWSS (2))', 'min(vWSS (Magnitude))', 'min(X)', 'min(Y)', 'min(Z)', 'N', 'q1(Area)', 'q1(average_pressure)', 'q1(average_speed)', 'q1(GlobalElementID)', 'q1(GlobalNodeID)', 'q1(p_avg_aorta)', 'q1(pressure)', 'q1(timeDeriv (0))', 'q1(timeDeriv (1))', 'q1(timeDeriv (2))', 'q1(timeDeriv (3))', 'q1(timeDeriv (Magnitude))', 'q1(velocity (0))', 'q1(velocity (1))', 'q1(velocity (2))', 'q1(velocity (Magnitude))', 'q1(vinplane_traction (0))', 'q1(vinplane_traction (1))', 'q1(vinplane_traction (2))', 'q1(vinplane_traction (Magnitude))', 'q1(vWSS (0))', 'q1(vWSS (1))', 'q1(vWSS (2))', 'q1(vWSS (Magnitude))', 'q1(X)', 'q1(Y)', 'q1(Z)', 'q3(Area)', 'q3(average_pressure)', 'q3(average_speed)', 'q3(GlobalElementID)', 'q3(GlobalNodeID)', 'q3(p_avg_aorta)', 'q3(pressure)', 'q3(timeDeriv (0))', 'q3(timeDeriv (1))', 'q3(timeDeriv (2))', 'q3(timeDeriv (3))', 'q3(timeDeriv (Magnitude))', 'q3(velocity (0))', 'q3(velocity (1))', 'q3(velocity (2))', 'q3(velocity (Magnitude))', 'q3(vinplane_traction (0))', 'q3(vinplane_traction (1))', 'q3(vinplane_traction (2))', 'q3(vinplane_traction (Magnitude))', 'q3(vWSS (0))', 'q3(vWSS (1))', 'q3(vWSS (2))', 'q3(vWSS (Magnitude))', 'q3(X)', 'q3(Y)', 'q3(Z)', 'std(Area)', 'std(average_pressure)', 'std(average_speed)', 'std(GlobalElementID)', 'std(GlobalNodeID)', 'std(p_avg_aorta)', 'std(pressure)', 'std(timeDeriv (0))', 'std(timeDeriv (1))', 'std(timeDeriv (2))', 'std(timeDeriv (3))', 'std(timeDeriv (Magnitude))', 'std(velocity (0))', 'std(velocity (1))', 'std(velocity (2))', 'std(velocity (Magnitude))', 'std(vinplane_traction (0))', 'std(vinplane_traction (1))', 'std(vinplane_traction (2))', 'std(vinplane_traction (Magnitude))', 'std(vWSS (0))', 'std(vWSS (1))', 'std(vWSS (2))', 'std(vWSS (Magnitude))', 'std(X)', 'std(Y)', 'std(Z)', 'sum(Area)', 'sum(average_pressure)', 'sum(average_speed)', 'sum(GlobalElementID)', 'sum(GlobalNodeID)', 'sum(p_avg_aorta)', 'sum(pressure)', 'sum(timeDeriv (0))', 'sum(timeDeriv (1))', 'sum(timeDeriv (2))', 'sum(timeDeriv (3))', 'sum(timeDeriv (Magnitude))', 'sum(velocity (0))', 'sum(velocity (1))', 'sum(velocity (2))', 'sum(velocity (Magnitude))', 'sum(vinplane_traction (0))', 'sum(vinplane_traction (1))', 'sum(vinplane_traction (2))', 'sum(vinplane_traction (Magnitude))', 'sum(vWSS (0))', 'sum(vWSS (1))', 'sum(vWSS (2))', 'sum(vWSS (Magnitude))', 'sum(X)', 'sum(Y)', 'sum(Z)', 'Time', 'vtkValidPointMask']

# Properties modified on spreadSheetView1
spreadSheetView1.HiddenColumnLabels = ['Block Name', 'Block Number', 'Row ID', 'avg(Area)', 'avg(average_pressure)', 'avg(average_speed)', 'avg(GlobalElementID)', 'avg(GlobalNodeID)', 'avg(pressure)', 'avg(timeDeriv (0))', 'avg(timeDeriv (1))', 'avg(timeDeriv (2))', 'avg(timeDeriv (3))', 'avg(timeDeriv (Magnitude))', 'avg(velocity (0))', 'avg(velocity (1))', 'avg(velocity (2))', 'avg(velocity (Magnitude))', 'avg(vinplane_traction (0))', 'avg(vinplane_traction (1))', 'avg(vinplane_traction (2))', 'avg(vinplane_traction (Magnitude))', 'avg(vWSS (0))', 'avg(vWSS (1))', 'avg(vWSS (2))', 'avg(vWSS (Magnitude))', 'avg(X)', 'avg(Y)', 'avg(Z)', 'max(Area)', 'max(average_pressure)', 'max(average_speed)', 'max(GlobalElementID)', 'max(GlobalNodeID)', 'max(p_avg_aorta)', 'max(pressure)', 'max(timeDeriv (0))', 'max(timeDeriv (1))', 'max(timeDeriv (2))', 'max(timeDeriv (3))', 'max(timeDeriv (Magnitude))', 'max(velocity (0))', 'max(velocity (1))', 'max(velocity (2))', 'max(velocity (Magnitude))', 'max(vinplane_traction (0))', 'max(vinplane_traction (1))', 'max(vinplane_traction (2))', 'max(vinplane_traction (Magnitude))', 'max(vWSS (0))', 'max(vWSS (1))', 'max(vWSS (2))', 'max(vWSS (Magnitude))', 'max(X)', 'max(Y)', 'max(Z)', 'med(Area)', 'med(average_pressure)', 'med(average_speed)', 'med(GlobalElementID)', 'med(GlobalNodeID)', 'med(p_avg_aorta)', 'med(pressure)', 'med(timeDeriv (0))', 'med(timeDeriv (1))', 'med(timeDeriv (2))', 'med(timeDeriv (3))', 'med(timeDeriv (Magnitude))', 'med(velocity (0))', 'med(velocity (1))', 'med(velocity (2))', 'med(velocity (Magnitude))', 'med(vinplane_traction (0))', 'med(vinplane_traction (1))', 'med(vinplane_traction (2))', 'med(vinplane_traction (Magnitude))', 'med(vWSS (0))', 'med(vWSS (1))', 'med(vWSS (2))', 'med(vWSS (Magnitude))', 'med(X)', 'med(Y)', 'med(Z)', 'min(Area)', 'min(average_pressure)', 'min(average_speed)', 'min(GlobalElementID)', 'min(GlobalNodeID)', 'min(p_avg_aorta)', 'min(pressure)', 'min(timeDeriv (0))', 'min(timeDeriv (1))', 'min(timeDeriv (2))', 'min(timeDeriv (3))', 'min(timeDeriv (Magnitude))', 'min(velocity (0))', 'min(velocity (1))', 'min(velocity (2))', 'min(velocity (Magnitude))', 'min(vinplane_traction (0))', 'min(vinplane_traction (1))', 'min(vinplane_traction (2))', 'min(vinplane_traction (Magnitude))', 'min(vWSS (0))', 'min(vWSS (1))', 'min(vWSS (2))', 'min(vWSS (Magnitude))', 'min(X)', 'min(Y)', 'min(Z)', 'N', 'q1(Area)', 'q1(average_pressure)', 'q1(average_speed)', 'q1(GlobalElementID)', 'q1(GlobalNodeID)', 'q1(p_avg_aorta)', 'q1(pressure)', 'q1(timeDeriv (0))', 'q1(timeDeriv (1))', 'q1(timeDeriv (2))', 'q1(timeDeriv (3))', 'q1(timeDeriv (Magnitude))', 'q1(velocity (0))', 'q1(velocity (1))', 'q1(velocity (2))', 'q1(velocity (Magnitude))', 'q1(vinplane_traction (0))', 'q1(vinplane_traction (1))', 'q1(vinplane_traction (2))', 'q1(vinplane_traction (Magnitude))', 'q1(vWSS (0))', 'q1(vWSS (1))', 'q1(vWSS (2))', 'q1(vWSS (Magnitude))', 'q1(X)', 'q1(Y)', 'q1(Z)', 'q3(Area)', 'q3(average_pressure)', 'q3(average_speed)', 'q3(GlobalElementID)', 'q3(GlobalNodeID)', 'q3(p_avg_aorta)', 'q3(pressure)', 'q3(timeDeriv (0))', 'q3(timeDeriv (1))', 'q3(timeDeriv (2))', 'q3(timeDeriv (3))', 'q3(timeDeriv (Magnitude))', 'q3(velocity (0))', 'q3(velocity (1))', 'q3(velocity (2))', 'q3(velocity (Magnitude))', 'q3(vinplane_traction (0))', 'q3(vinplane_traction (1))', 'q3(vinplane_traction (2))', 'q3(vinplane_traction (Magnitude))', 'q3(vWSS (0))', 'q3(vWSS (1))', 'q3(vWSS (2))', 'q3(vWSS (Magnitude))', 'q3(X)', 'q3(Y)', 'q3(Z)', 'std(Area)', 'std(average_pressure)', 'std(average_speed)', 'std(GlobalElementID)', 'std(GlobalNodeID)', 'std(p_avg_aorta)', 'std(pressure)', 'std(timeDeriv (0))', 'std(timeDeriv (1))', 'std(timeDeriv (2))', 'std(timeDeriv (3))', 'std(timeDeriv (Magnitude))', 'std(velocity (0))', 'std(velocity (1))', 'std(velocity (2))', 'std(velocity (Magnitude))', 'std(vinplane_traction (0))', 'std(vinplane_traction (1))', 'std(vinplane_traction (2))', 'std(vinplane_traction (Magnitude))', 'std(vWSS (0))', 'std(vWSS (1))', 'std(vWSS (2))', 'std(vWSS (Magnitude))', 'std(X)', 'std(Y)', 'std(Z)', 'sum(Area)', 'sum(average_pressure)', 'sum(average_speed)', 'sum(GlobalElementID)', 'sum(GlobalNodeID)', 'sum(p_avg_aorta)', 'sum(pressure)', 'sum(timeDeriv (0))', 'sum(timeDeriv (1))', 'sum(timeDeriv (2))', 'sum(timeDeriv (3))', 'sum(timeDeriv (Magnitude))', 'sum(velocity (0))', 'sum(velocity (1))', 'sum(velocity (2))', 'sum(velocity (Magnitude))', 'sum(vinplane_traction (0))', 'sum(vinplane_traction (1))', 'sum(vinplane_traction (2))', 'sum(vinplane_traction (Magnitude))', 'sum(vWSS (0))', 'sum(vWSS (1))', 'sum(vWSS (2))', 'sum(vWSS (Magnitude))', 'sum(X)', 'sum(Y)', 'sum(Z)', 'Time', 'vtkValidPointMask']

# export view
ExportView(file_path+'p_avg_aorta.csv', view=spreadSheetView1)

# set active source
SetActiveSource(plotDataOverTime2)

# show data in view
plotDataOverTime2Display_1 = Show(plotDataOverTime2, spreadSheetView1, 'SpreadSheetRepresentation')

# hide data in view
Hide(plotDataOverTime2, spreadSheetView1)

# show data in view
plotDataOverTime2Display_1 = Show(plotDataOverTime2, spreadSheetView1, 'SpreadSheetRepresentation')

# show data in view
plotDataOverTime2Display_1 = Show(plotDataOverTime2, spreadSheetView1, 'SpreadSheetRepresentation')

# Properties modified on spreadSheetView1
spreadSheetView1.HiddenColumnLabels = []

# Properties modified on spreadSheetView1
spreadSheetView1.HiddenColumnLabels = ['Block Name', 'Block Number', 'Row ID', 'avg(Surface Flow)', 'avg(velocity (0))', 'avg(velocity (1))', 'avg(velocity (2))', 'avg(velocity (Magnitude))', 'avg(X)', 'avg(Y)', 'avg(Z)', 'max(Surface Flow)', 'max(velocity (0))', 'max(velocity (1))', 'max(velocity (2))', 'max(velocity (Magnitude))', 'max(X)', 'max(Y)', 'max(Z)', 'med(Surface Flow)', 'med(velocity (0))', 'med(velocity (1))', 'med(velocity (2))', 'med(velocity (Magnitude))', 'med(X)', 'med(Y)', 'med(Z)', 'min(Surface Flow)', 'min(velocity (0))', 'min(velocity (1))', 'min(velocity (2))', 'min(velocity (Magnitude))', 'min(X)', 'min(Y)', 'min(Z)', 'N', 'q1(Surface Flow)', 'q1(velocity (0))', 'q1(velocity (1))', 'q1(velocity (2))', 'q1(velocity (Magnitude))', 'q1(X)', 'q1(Y)', 'q1(Z)', 'q3(Surface Flow)', 'q3(velocity (0))', 'q3(velocity (1))', 'q3(velocity (2))', 'q3(velocity (Magnitude))', 'q3(X)', 'q3(Y)', 'q3(Z)', 'std(Surface Flow)', 'std(velocity (0))', 'std(velocity (1))', 'std(velocity (2))', 'std(velocity (Magnitude))', 'std(X)', 'std(Y)', 'std(Z)', 'sum(Surface Flow)', 'sum(velocity (0))', 'sum(velocity (1))', 'sum(velocity (2))', 'sum(velocity (Magnitude))', 'sum(X)', 'sum(Y)', 'sum(Z)', 'Time', 'vtkValidPointMask', 'avg(Area)', 'avg(average_pressure)', 'avg(average_speed)', 'avg(GlobalElementID)', 'avg(GlobalNodeID)', 'avg(pressure)', 'avg(timeDeriv (0))', 'avg(timeDeriv (1))', 'avg(timeDeriv (2))', 'avg(timeDeriv (3))', 'avg(timeDeriv (Magnitude))', 'avg(vinplane_traction (0))', 'avg(vinplane_traction (1))', 'avg(vinplane_traction (2))', 'avg(vinplane_traction (Magnitude))', 'avg(vWSS (0))', 'avg(vWSS (1))', 'avg(vWSS (2))', 'avg(vWSS (Magnitude))', 'max(Area)', 'max(average_pressure)', 'max(average_speed)', 'max(GlobalElementID)', 'max(GlobalNodeID)', 'max(p_avg_aorta)', 'max(pressure)', 'max(timeDeriv (0))', 'max(timeDeriv (1))', 'max(timeDeriv (2))', 'max(timeDeriv (3))', 'max(timeDeriv (Magnitude))', 'max(vinplane_traction (0))', 'max(vinplane_traction (1))', 'max(vinplane_traction (2))', 'max(vinplane_traction (Magnitude))', 'max(vWSS (0))', 'max(vWSS (1))', 'max(vWSS (2))', 'max(vWSS (Magnitude))', 'med(Area)', 'med(average_pressure)', 'med(average_speed)', 'med(GlobalElementID)', 'med(GlobalNodeID)', 'med(p_avg_aorta)', 'med(pressure)', 'med(timeDeriv (0))', 'med(timeDeriv (1))', 'med(timeDeriv (2))', 'med(timeDeriv (3))', 'med(timeDeriv (Magnitude))', 'med(vinplane_traction (0))', 'med(vinplane_traction (1))', 'med(vinplane_traction (2))', 'med(vinplane_traction (Magnitude))', 'med(vWSS (0))', 'med(vWSS (1))', 'med(vWSS (2))', 'med(vWSS (Magnitude))', 'min(Area)', 'min(average_pressure)', 'min(average_speed)', 'min(GlobalElementID)', 'min(GlobalNodeID)', 'min(p_avg_aorta)', 'min(pressure)', 'min(timeDeriv (0))', 'min(timeDeriv (1))', 'min(timeDeriv (2))', 'min(timeDeriv (3))', 'min(timeDeriv (Magnitude))', 'min(vinplane_traction (0))', 'min(vinplane_traction (1))', 'min(vinplane_traction (2))', 'min(vinplane_traction (Magnitude))', 'min(vWSS (0))', 'min(vWSS (1))', 'min(vWSS (2))', 'min(vWSS (Magnitude))', 'q1(Area)', 'q1(average_pressure)', 'q1(average_speed)', 'q1(GlobalElementID)', 'q1(GlobalNodeID)', 'q1(p_avg_aorta)', 'q1(pressure)', 'q1(timeDeriv (0))', 'q1(timeDeriv (1))', 'q1(timeDeriv (2))', 'q1(timeDeriv (3))', 'q1(timeDeriv (Magnitude))', 'q1(vinplane_traction (0))', 'q1(vinplane_traction (1))', 'q1(vinplane_traction (2))', 'q1(vinplane_traction (Magnitude))', 'q1(vWSS (0))', 'q1(vWSS (1))', 'q1(vWSS (2))', 'q1(vWSS (Magnitude))', 'q3(Area)', 'q3(average_pressure)', 'q3(average_speed)', 'q3(GlobalElementID)', 'q3(GlobalNodeID)', 'q3(p_avg_aorta)', 'q3(pressure)', 'q3(timeDeriv (0))', 'q3(timeDeriv (1))', 'q3(timeDeriv (2))', 'q3(timeDeriv (3))', 'q3(timeDeriv (Magnitude))', 'q3(vinplane_traction (0))', 'q3(vinplane_traction (1))', 'q3(vinplane_traction (2))', 'q3(vinplane_traction (Magnitude))', 'q3(vWSS (0))', 'q3(vWSS (1))', 'q3(vWSS (2))', 'q3(vWSS (Magnitude))', 'std(Area)', 'std(average_pressure)', 'std(average_speed)', 'std(GlobalElementID)', 'std(GlobalNodeID)', 'std(p_avg_aorta)', 'std(pressure)', 'std(timeDeriv (0))', 'std(timeDeriv (1))', 'std(timeDeriv (2))', 'std(timeDeriv (3))', 'std(timeDeriv (Magnitude))', 'std(vinplane_traction (0))', 'std(vinplane_traction (1))', 'std(vinplane_traction (2))', 'std(vinplane_traction (Magnitude))', 'std(vWSS (0))', 'std(vWSS (1))', 'std(vWSS (2))', 'std(vWSS (Magnitude))', 'sum(Area)', 'sum(average_pressure)', 'sum(average_speed)', 'sum(GlobalElementID)', 'sum(GlobalNodeID)', 'sum(p_avg_aorta)', 'sum(pressure)', 'sum(timeDeriv (0))', 'sum(timeDeriv (1))', 'sum(timeDeriv (2))', 'sum(timeDeriv (3))', 'sum(timeDeriv (Magnitude))', 'sum(vinplane_traction (0))', 'sum(vinplane_traction (1))', 'sum(vinplane_traction (2))', 'sum(vinplane_traction (Magnitude))', 'sum(vWSS (0))', 'sum(vWSS (1))', 'sum(vWSS (2))', 'sum(vWSS (Magnitude))']

# Properties modified on spreadSheetView1
spreadSheetView1.HiddenColumnLabels = ['Block Name', 'Block Number', 'Row ID', 'avg(velocity (0))', 'avg(velocity (1))', 'avg(velocity (2))', 'avg(velocity (Magnitude))', 'avg(X)', 'avg(Y)', 'avg(Z)', 'max(Surface Flow)', 'max(velocity (0))', 'max(velocity (1))', 'max(velocity (2))', 'max(velocity (Magnitude))', 'max(X)', 'max(Y)', 'max(Z)', 'med(Surface Flow)', 'med(velocity (0))', 'med(velocity (1))', 'med(velocity (2))', 'med(velocity (Magnitude))', 'med(X)', 'med(Y)', 'med(Z)', 'min(Surface Flow)', 'min(velocity (0))', 'min(velocity (1))', 'min(velocity (2))', 'min(velocity (Magnitude))', 'min(X)', 'min(Y)', 'min(Z)', 'N', 'q1(Surface Flow)', 'q1(velocity (0))', 'q1(velocity (1))', 'q1(velocity (2))', 'q1(velocity (Magnitude))', 'q1(X)', 'q1(Y)', 'q1(Z)', 'q3(Surface Flow)', 'q3(velocity (0))', 'q3(velocity (1))', 'q3(velocity (2))', 'q3(velocity (Magnitude))', 'q3(X)', 'q3(Y)', 'q3(Z)', 'std(Surface Flow)', 'std(velocity (0))', 'std(velocity (1))', 'std(velocity (2))', 'std(velocity (Magnitude))', 'std(X)', 'std(Y)', 'std(Z)', 'sum(Surface Flow)', 'sum(velocity (0))', 'sum(velocity (1))', 'sum(velocity (2))', 'sum(velocity (Magnitude))', 'sum(X)', 'sum(Y)', 'sum(Z)', 'Time', 'vtkValidPointMask', 'avg(Area)', 'avg(average_pressure)', 'avg(average_speed)', 'avg(GlobalElementID)', 'avg(GlobalNodeID)', 'avg(pressure)', 'avg(timeDeriv (0))', 'avg(timeDeriv (1))', 'avg(timeDeriv (2))', 'avg(timeDeriv (3))', 'avg(timeDeriv (Magnitude))', 'avg(vinplane_traction (0))', 'avg(vinplane_traction (1))', 'avg(vinplane_traction (2))', 'avg(vinplane_traction (Magnitude))', 'avg(vWSS (0))', 'avg(vWSS (1))', 'avg(vWSS (2))', 'avg(vWSS (Magnitude))', 'max(Area)', 'max(average_pressure)', 'max(average_speed)', 'max(GlobalElementID)', 'max(GlobalNodeID)', 'max(p_avg_aorta)', 'max(pressure)', 'max(timeDeriv (0))', 'max(timeDeriv (1))', 'max(timeDeriv (2))', 'max(timeDeriv (3))', 'max(timeDeriv (Magnitude))', 'max(vinplane_traction (0))', 'max(vinplane_traction (1))', 'max(vinplane_traction (2))', 'max(vinplane_traction (Magnitude))', 'max(vWSS (0))', 'max(vWSS (1))', 'max(vWSS (2))', 'max(vWSS (Magnitude))', 'med(Area)', 'med(average_pressure)', 'med(average_speed)', 'med(GlobalElementID)', 'med(GlobalNodeID)', 'med(p_avg_aorta)', 'med(pressure)', 'med(timeDeriv (0))', 'med(timeDeriv (1))', 'med(timeDeriv (2))', 'med(timeDeriv (3))', 'med(timeDeriv (Magnitude))', 'med(vinplane_traction (0))', 'med(vinplane_traction (1))', 'med(vinplane_traction (2))', 'med(vinplane_traction (Magnitude))', 'med(vWSS (0))', 'med(vWSS (1))', 'med(vWSS (2))', 'med(vWSS (Magnitude))', 'min(Area)', 'min(average_pressure)', 'min(average_speed)', 'min(GlobalElementID)', 'min(GlobalNodeID)', 'min(p_avg_aorta)', 'min(pressure)', 'min(timeDeriv (0))', 'min(timeDeriv (1))', 'min(timeDeriv (2))', 'min(timeDeriv (3))', 'min(timeDeriv (Magnitude))', 'min(vinplane_traction (0))', 'min(vinplane_traction (1))', 'min(vinplane_traction (2))', 'min(vinplane_traction (Magnitude))', 'min(vWSS (0))', 'min(vWSS (1))', 'min(vWSS (2))', 'min(vWSS (Magnitude))', 'q1(Area)', 'q1(average_pressure)', 'q1(average_speed)', 'q1(GlobalElementID)', 'q1(GlobalNodeID)', 'q1(p_avg_aorta)', 'q1(pressure)', 'q1(timeDeriv (0))', 'q1(timeDeriv (1))', 'q1(timeDeriv (2))', 'q1(timeDeriv (3))', 'q1(timeDeriv (Magnitude))', 'q1(vinplane_traction (0))', 'q1(vinplane_traction (1))', 'q1(vinplane_traction (2))', 'q1(vinplane_traction (Magnitude))', 'q1(vWSS (0))', 'q1(vWSS (1))', 'q1(vWSS (2))', 'q1(vWSS (Magnitude))', 'q3(Area)', 'q3(average_pressure)', 'q3(average_speed)', 'q3(GlobalElementID)', 'q3(GlobalNodeID)', 'q3(p_avg_aorta)', 'q3(pressure)', 'q3(timeDeriv (0))', 'q3(timeDeriv (1))', 'q3(timeDeriv (2))', 'q3(timeDeriv (3))', 'q3(timeDeriv (Magnitude))', 'q3(vinplane_traction (0))', 'q3(vinplane_traction (1))', 'q3(vinplane_traction (2))', 'q3(vinplane_traction (Magnitude))', 'q3(vWSS (0))', 'q3(vWSS (1))', 'q3(vWSS (2))', 'q3(vWSS (Magnitude))', 'std(Area)', 'std(average_pressure)', 'std(average_speed)', 'std(GlobalElementID)', 'std(GlobalNodeID)', 'std(p_avg_aorta)', 'std(pressure)', 'std(timeDeriv (0))', 'std(timeDeriv (1))', 'std(timeDeriv (2))', 'std(timeDeriv (3))', 'std(timeDeriv (Magnitude))', 'std(vinplane_traction (0))', 'std(vinplane_traction (1))', 'std(vinplane_traction (2))', 'std(vinplane_traction (Magnitude))', 'std(vWSS (0))', 'std(vWSS (1))', 'std(vWSS (2))', 'std(vWSS (Magnitude))', 'sum(Area)', 'sum(average_pressure)', 'sum(average_speed)', 'sum(GlobalElementID)', 'sum(GlobalNodeID)', 'sum(p_avg_aorta)', 'sum(pressure)', 'sum(timeDeriv (0))', 'sum(timeDeriv (1))', 'sum(timeDeriv (2))', 'sum(timeDeriv (3))', 'sum(timeDeriv (Magnitude))', 'sum(vinplane_traction (0))', 'sum(vinplane_traction (1))', 'sum(vinplane_traction (2))', 'sum(vinplane_traction (Magnitude))', 'sum(vWSS (0))', 'sum(vWSS (1))', 'sum(vWSS (2))', 'sum(vWSS (Magnitude))']

# export view
ExportView(file_path+'surface_flow_aorta.csv', view=spreadSheetView1)

# set active source
SetActiveSource(plotDataOverTime3)

# clear all selections
ClearSelection()

# set active source
SetActiveSource(plotDataOverTime2)

# set active source
SetActiveSource(plotDataOverTime3)

# show data in view
plotDataOverTime3Display_1 = Show(plotDataOverTime3, spreadSheetView1, 'SpreadSheetRepresentation')

# hide data in view
Hide(plotDataOverTime3, spreadSheetView1)

# show data in view
plotDataOverTime3Display_1 = Show(plotDataOverTime3, spreadSheetView1, 'SpreadSheetRepresentation')

# show data in view
plotDataOverTime3Display_1 = Show(plotDataOverTime3, spreadSheetView1, 'SpreadSheetRepresentation')

# Properties modified on spreadSheetView1
spreadSheetView1.HiddenColumnLabels = []

# Properties modified on spreadSheetView1
spreadSheetView1.HiddenColumnLabels = ['Block Name', 'Block Number', 'Row ID', 'avg(Area)', 'avg(average_pressure)', 'avg(average_speed)', 'avg(GlobalElementID)', 'avg(GlobalNodeID)', 'avg(p_avg_right)', 'avg(pressure)', 'avg(timeDeriv (0))', 'avg(timeDeriv (1))', 'avg(timeDeriv (2))', 'avg(timeDeriv (3))', 'avg(timeDeriv (Magnitude))', 'avg(velocity (0))', 'avg(velocity (1))', 'avg(velocity (2))', 'avg(velocity (Magnitude))', 'avg(vinplane_traction (0))', 'avg(vinplane_traction (1))', 'avg(vinplane_traction (2))', 'avg(vinplane_traction (Magnitude))', 'avg(vWSS (0))', 'avg(vWSS (1))', 'avg(vWSS (2))', 'avg(vWSS (Magnitude))', 'avg(X)', 'avg(Y)', 'avg(Z)', 'max(Area)', 'max(average_pressure)', 'max(average_speed)', 'max(GlobalElementID)', 'max(GlobalNodeID)', 'max(p_avg_right)', 'max(pressure)', 'max(timeDeriv (0))', 'max(timeDeriv (1))', 'max(timeDeriv (2))', 'max(timeDeriv (3))', 'max(timeDeriv (Magnitude))', 'max(velocity (0))', 'max(velocity (1))', 'max(velocity (2))', 'max(velocity (Magnitude))', 'max(vinplane_traction (0))', 'max(vinplane_traction (1))', 'max(vinplane_traction (2))', 'max(vinplane_traction (Magnitude))', 'max(vWSS (0))', 'max(vWSS (1))', 'max(vWSS (2))', 'max(vWSS (Magnitude))', 'max(X)', 'max(Y)', 'max(Z)', 'med(Area)', 'med(average_pressure)', 'med(average_speed)', 'med(GlobalElementID)', 'med(GlobalNodeID)', 'med(p_avg_right)', 'med(pressure)', 'med(timeDeriv (0))', 'med(timeDeriv (1))', 'med(timeDeriv (2))', 'med(timeDeriv (3))', 'med(timeDeriv (Magnitude))', 'med(velocity (0))', 'med(velocity (1))', 'med(velocity (2))', 'med(velocity (Magnitude))', 'med(vinplane_traction (0))', 'med(vinplane_traction (1))', 'med(vinplane_traction (2))', 'med(vinplane_traction (Magnitude))', 'med(vWSS (0))', 'med(vWSS (1))', 'med(vWSS (2))', 'med(vWSS (Magnitude))', 'med(X)', 'med(Y)', 'med(Z)', 'min(Area)', 'min(average_pressure)', 'min(average_speed)', 'min(GlobalElementID)', 'min(GlobalNodeID)', 'min(p_avg_right)', 'min(pressure)', 'min(timeDeriv (0))', 'min(timeDeriv (1))', 'min(timeDeriv (2))', 'min(timeDeriv (3))', 'min(timeDeriv (Magnitude))', 'min(velocity (0))', 'min(velocity (1))', 'min(velocity (2))', 'min(velocity (Magnitude))', 'min(vinplane_traction (0))', 'min(vinplane_traction (1))', 'min(vinplane_traction (2))', 'min(vinplane_traction (Magnitude))', 'min(vWSS (0))', 'min(vWSS (1))', 'min(vWSS (2))', 'min(vWSS (Magnitude))', 'min(X)', 'min(Y)', 'min(Z)', 'N', 'q1(Area)', 'q1(average_pressure)', 'q1(average_speed)', 'q1(GlobalElementID)', 'q1(GlobalNodeID)', 'q1(p_avg_right)', 'q1(pressure)', 'q1(timeDeriv (0))', 'q1(timeDeriv (1))', 'q1(timeDeriv (2))', 'q1(timeDeriv (3))', 'q1(timeDeriv (Magnitude))', 'q1(velocity (0))', 'q1(velocity (1))', 'q1(velocity (2))', 'q1(velocity (Magnitude))', 'q1(vinplane_traction (0))', 'q1(vinplane_traction (1))', 'q1(vinplane_traction (2))', 'q1(vinplane_traction (Magnitude))', 'q1(vWSS (0))', 'q1(vWSS (1))', 'q1(vWSS (2))', 'q1(vWSS (Magnitude))', 'q1(X)', 'q1(Y)', 'q1(Z)', 'q3(Area)', 'q3(average_pressure)', 'q3(average_speed)', 'q3(GlobalElementID)', 'q3(GlobalNodeID)', 'q3(p_avg_right)', 'q3(pressure)', 'q3(timeDeriv (0))', 'q3(timeDeriv (1))', 'q3(timeDeriv (2))', 'q3(timeDeriv (3))', 'q3(timeDeriv (Magnitude))', 'q3(velocity (0))', 'q3(velocity (1))', 'q3(velocity (2))', 'q3(velocity (Magnitude))', 'q3(vinplane_traction (0))', 'q3(vinplane_traction (1))', 'q3(vinplane_traction (2))', 'q3(vinplane_traction (Magnitude))', 'q3(vWSS (0))', 'q3(vWSS (1))', 'q3(vWSS (2))', 'q3(vWSS (Magnitude))', 'q3(X)', 'q3(Y)', 'q3(Z)', 'std(Area)', 'std(average_pressure)', 'std(average_speed)', 'std(GlobalElementID)', 'std(GlobalNodeID)', 'std(p_avg_right)', 'std(pressure)', 'std(timeDeriv (0))', 'std(timeDeriv (1))', 'std(timeDeriv (2))', 'std(timeDeriv (3))', 'std(timeDeriv (Magnitude))', 'std(velocity (0))', 'std(velocity (1))', 'std(velocity (2))', 'std(velocity (Magnitude))', 'std(vinplane_traction (0))', 'std(vinplane_traction (1))', 'std(vinplane_traction (2))', 'std(vinplane_traction (Magnitude))', 'std(vWSS (0))', 'std(vWSS (1))', 'std(vWSS (2))', 'std(vWSS (Magnitude))', 'std(X)', 'std(Y)', 'std(Z)', 'sum(Area)', 'sum(average_pressure)', 'sum(average_speed)', 'sum(GlobalElementID)', 'sum(GlobalNodeID)', 'sum(p_avg_right)', 'sum(pressure)', 'sum(timeDeriv (0))', 'sum(timeDeriv (1))', 'sum(timeDeriv (2))', 'sum(timeDeriv (3))', 'sum(timeDeriv (Magnitude))', 'sum(velocity (0))', 'sum(velocity (1))', 'sum(velocity (2))', 'sum(velocity (Magnitude))', 'sum(vinplane_traction (0))', 'sum(vinplane_traction (1))', 'sum(vinplane_traction (2))', 'sum(vinplane_traction (Magnitude))', 'sum(vWSS (0))', 'sum(vWSS (1))', 'sum(vWSS (2))', 'sum(vWSS (Magnitude))', 'sum(X)', 'sum(Y)', 'sum(Z)', 'Time', 'vtkValidPointMask', 'max(Surface Flow)', 'med(Surface Flow)', 'min(Surface Flow)', 'q1(Surface Flow)', 'q3(Surface Flow)', 'std(Surface Flow)', 'sum(Surface Flow)', 'max(p_avg_aorta)', 'med(p_avg_aorta)', 'min(p_avg_aorta)', 'q1(p_avg_aorta)', 'q3(p_avg_aorta)', 'std(p_avg_aorta)', 'sum(p_avg_aorta)']

# Properties modified on spreadSheetView1
spreadSheetView1.HiddenColumnLabels = ['Block Name', 'Block Number', 'Row ID', 'avg(Area)', 'avg(average_pressure)', 'avg(average_speed)', 'avg(GlobalElementID)', 'avg(GlobalNodeID)', 'avg(pressure)', 'avg(timeDeriv (0))', 'avg(timeDeriv (1))', 'avg(timeDeriv (2))', 'avg(timeDeriv (3))', 'avg(timeDeriv (Magnitude))', 'avg(velocity (0))', 'avg(velocity (1))', 'avg(velocity (2))', 'avg(velocity (Magnitude))', 'avg(vinplane_traction (0))', 'avg(vinplane_traction (1))', 'avg(vinplane_traction (2))', 'avg(vinplane_traction (Magnitude))', 'avg(vWSS (0))', 'avg(vWSS (1))', 'avg(vWSS (2))', 'avg(vWSS (Magnitude))', 'avg(X)', 'avg(Y)', 'avg(Z)', 'max(Area)', 'max(average_pressure)', 'max(average_speed)', 'max(GlobalElementID)', 'max(GlobalNodeID)', 'max(p_avg_right)', 'max(pressure)', 'max(timeDeriv (0))', 'max(timeDeriv (1))', 'max(timeDeriv (2))', 'max(timeDeriv (3))', 'max(timeDeriv (Magnitude))', 'max(velocity (0))', 'max(velocity (1))', 'max(velocity (2))', 'max(velocity (Magnitude))', 'max(vinplane_traction (0))', 'max(vinplane_traction (1))', 'max(vinplane_traction (2))', 'max(vinplane_traction (Magnitude))', 'max(vWSS (0))', 'max(vWSS (1))', 'max(vWSS (2))', 'max(vWSS (Magnitude))', 'max(X)', 'max(Y)', 'max(Z)', 'med(Area)', 'med(average_pressure)', 'med(average_speed)', 'med(GlobalElementID)', 'med(GlobalNodeID)', 'med(p_avg_right)', 'med(pressure)', 'med(timeDeriv (0))', 'med(timeDeriv (1))', 'med(timeDeriv (2))', 'med(timeDeriv (3))', 'med(timeDeriv (Magnitude))', 'med(velocity (0))', 'med(velocity (1))', 'med(velocity (2))', 'med(velocity (Magnitude))', 'med(vinplane_traction (0))', 'med(vinplane_traction (1))', 'med(vinplane_traction (2))', 'med(vinplane_traction (Magnitude))', 'med(vWSS (0))', 'med(vWSS (1))', 'med(vWSS (2))', 'med(vWSS (Magnitude))', 'med(X)', 'med(Y)', 'med(Z)', 'min(Area)', 'min(average_pressure)', 'min(average_speed)', 'min(GlobalElementID)', 'min(GlobalNodeID)', 'min(p_avg_right)', 'min(pressure)', 'min(timeDeriv (0))', 'min(timeDeriv (1))', 'min(timeDeriv (2))', 'min(timeDeriv (3))', 'min(timeDeriv (Magnitude))', 'min(velocity (0))', 'min(velocity (1))', 'min(velocity (2))', 'min(velocity (Magnitude))', 'min(vinplane_traction (0))', 'min(vinplane_traction (1))', 'min(vinplane_traction (2))', 'min(vinplane_traction (Magnitude))', 'min(vWSS (0))', 'min(vWSS (1))', 'min(vWSS (2))', 'min(vWSS (Magnitude))', 'min(X)', 'min(Y)', 'min(Z)', 'N', 'q1(Area)', 'q1(average_pressure)', 'q1(average_speed)', 'q1(GlobalElementID)', 'q1(GlobalNodeID)', 'q1(p_avg_right)', 'q1(pressure)', 'q1(timeDeriv (0))', 'q1(timeDeriv (1))', 'q1(timeDeriv (2))', 'q1(timeDeriv (3))', 'q1(timeDeriv (Magnitude))', 'q1(velocity (0))', 'q1(velocity (1))', 'q1(velocity (2))', 'q1(velocity (Magnitude))', 'q1(vinplane_traction (0))', 'q1(vinplane_traction (1))', 'q1(vinplane_traction (2))', 'q1(vinplane_traction (Magnitude))', 'q1(vWSS (0))', 'q1(vWSS (1))', 'q1(vWSS (2))', 'q1(vWSS (Magnitude))', 'q1(X)', 'q1(Y)', 'q1(Z)', 'q3(Area)', 'q3(average_pressure)', 'q3(average_speed)', 'q3(GlobalElementID)', 'q3(GlobalNodeID)', 'q3(p_avg_right)', 'q3(pressure)', 'q3(timeDeriv (0))', 'q3(timeDeriv (1))', 'q3(timeDeriv (2))', 'q3(timeDeriv (3))', 'q3(timeDeriv (Magnitude))', 'q3(velocity (0))', 'q3(velocity (1))', 'q3(velocity (2))', 'q3(velocity (Magnitude))', 'q3(vinplane_traction (0))', 'q3(vinplane_traction (1))', 'q3(vinplane_traction (2))', 'q3(vinplane_traction (Magnitude))', 'q3(vWSS (0))', 'q3(vWSS (1))', 'q3(vWSS (2))', 'q3(vWSS (Magnitude))', 'q3(X)', 'q3(Y)', 'q3(Z)', 'std(Area)', 'std(average_pressure)', 'std(average_speed)', 'std(GlobalElementID)', 'std(GlobalNodeID)', 'std(p_avg_right)', 'std(pressure)', 'std(timeDeriv (0))', 'std(timeDeriv (1))', 'std(timeDeriv (2))', 'std(timeDeriv (3))', 'std(timeDeriv (Magnitude))', 'std(velocity (0))', 'std(velocity (1))', 'std(velocity (2))', 'std(velocity (Magnitude))', 'std(vinplane_traction (0))', 'std(vinplane_traction (1))', 'std(vinplane_traction (2))', 'std(vinplane_traction (Magnitude))', 'std(vWSS (0))', 'std(vWSS (1))', 'std(vWSS (2))', 'std(vWSS (Magnitude))', 'std(X)', 'std(Y)', 'std(Z)', 'sum(Area)', 'sum(average_pressure)', 'sum(average_speed)', 'sum(GlobalElementID)', 'sum(GlobalNodeID)', 'sum(p_avg_right)', 'sum(pressure)', 'sum(timeDeriv (0))', 'sum(timeDeriv (1))', 'sum(timeDeriv (2))', 'sum(timeDeriv (3))', 'sum(timeDeriv (Magnitude))', 'sum(velocity (0))', 'sum(velocity (1))', 'sum(velocity (2))', 'sum(velocity (Magnitude))', 'sum(vinplane_traction (0))', 'sum(vinplane_traction (1))', 'sum(vinplane_traction (2))', 'sum(vinplane_traction (Magnitude))', 'sum(vWSS (0))', 'sum(vWSS (1))', 'sum(vWSS (2))', 'sum(vWSS (Magnitude))', 'sum(X)', 'sum(Y)', 'sum(Z)', 'Time', 'vtkValidPointMask', 'max(Surface Flow)', 'med(Surface Flow)', 'min(Surface Flow)', 'q1(Surface Flow)', 'q3(Surface Flow)', 'std(Surface Flow)', 'sum(Surface Flow)', 'max(p_avg_aorta)', 'med(p_avg_aorta)', 'min(p_avg_aorta)', 'q1(p_avg_aorta)', 'q3(p_avg_aorta)', 'std(p_avg_aorta)', 'sum(p_avg_aorta)']

# export view
ExportView(file_path+'p_avg_right.csv', view=spreadSheetView1)

# hide data in view
Hide(plotDataOverTime3, spreadSheetView1)

# set active source
SetActiveSource(plotDataOverTime4)

# show data in view
plotDataOverTime4Display_1 = Show(plotDataOverTime4, spreadSheetView1, 'SpreadSheetRepresentation')

# export view
ExportView(file_path+'surface_flow_right.csv', view=spreadSheetView1)

# hide data in view
Hide(plotDataOverTime4, spreadSheetView1)

# set active source
SetActiveSource(plotDataOverTime5)

# show data in view
plotDataOverTime5Display_1 = Show(plotDataOverTime5, spreadSheetView1, 'SpreadSheetRepresentation')

# Properties modified on spreadSheetView1
spreadSheetView1.HiddenColumnLabels = []

# Properties modified on spreadSheetView1
spreadSheetView1.HiddenColumnLabels = ['Block Name', 'Block Number', 'Row ID', 'avg(Area)', 'avg(average_pressure)', 'avg(average_speed)', 'avg(GlobalElementID)', 'avg(GlobalNodeID)', 'avg(p_avg_left)', 'avg(pressure)', 'avg(timeDeriv (0))', 'avg(timeDeriv (1))', 'avg(timeDeriv (2))', 'avg(timeDeriv (3))', 'avg(timeDeriv (Magnitude))', 'avg(velocity (0))', 'avg(velocity (1))', 'avg(velocity (2))', 'avg(velocity (Magnitude))', 'avg(vinplane_traction (0))', 'avg(vinplane_traction (1))', 'avg(vinplane_traction (2))', 'avg(vinplane_traction (Magnitude))', 'avg(vWSS (0))', 'avg(vWSS (1))', 'avg(vWSS (2))', 'avg(vWSS (Magnitude))', 'avg(X)', 'avg(Y)', 'avg(Z)', 'max(Area)', 'max(average_pressure)', 'max(average_speed)', 'max(GlobalElementID)', 'max(GlobalNodeID)', 'max(p_avg_left)', 'max(pressure)', 'max(timeDeriv (0))', 'max(timeDeriv (1))', 'max(timeDeriv (2))', 'max(timeDeriv (3))', 'max(timeDeriv (Magnitude))', 'max(velocity (0))', 'max(velocity (1))', 'max(velocity (2))', 'max(velocity (Magnitude))', 'max(vinplane_traction (0))', 'max(vinplane_traction (1))', 'max(vinplane_traction (2))', 'max(vinplane_traction (Magnitude))', 'max(vWSS (0))', 'max(vWSS (1))', 'max(vWSS (2))', 'max(vWSS (Magnitude))', 'max(X)', 'max(Y)', 'max(Z)', 'med(Area)', 'med(average_pressure)', 'med(average_speed)', 'med(GlobalElementID)', 'med(GlobalNodeID)', 'med(p_avg_left)', 'med(pressure)', 'med(timeDeriv (0))', 'med(timeDeriv (1))', 'med(timeDeriv (2))', 'med(timeDeriv (3))', 'med(timeDeriv (Magnitude))', 'med(velocity (0))', 'med(velocity (1))', 'med(velocity (2))', 'med(velocity (Magnitude))', 'med(vinplane_traction (0))', 'med(vinplane_traction (1))', 'med(vinplane_traction (2))', 'med(vinplane_traction (Magnitude))', 'med(vWSS (0))', 'med(vWSS (1))', 'med(vWSS (2))', 'med(vWSS (Magnitude))', 'med(X)', 'med(Y)', 'med(Z)', 'min(Area)', 'min(average_pressure)', 'min(average_speed)', 'min(GlobalElementID)', 'min(GlobalNodeID)', 'min(p_avg_left)', 'min(pressure)', 'min(timeDeriv (0))', 'min(timeDeriv (1))', 'min(timeDeriv (2))', 'min(timeDeriv (3))', 'min(timeDeriv (Magnitude))', 'min(velocity (0))', 'min(velocity (1))', 'min(velocity (2))', 'min(velocity (Magnitude))', 'min(vinplane_traction (0))', 'min(vinplane_traction (1))', 'min(vinplane_traction (2))', 'min(vinplane_traction (Magnitude))', 'min(vWSS (0))', 'min(vWSS (1))', 'min(vWSS (2))', 'min(vWSS (Magnitude))', 'min(X)', 'min(Y)', 'min(Z)', 'N', 'q1(Area)', 'q1(average_pressure)', 'q1(average_speed)', 'q1(GlobalElementID)', 'q1(GlobalNodeID)', 'q1(p_avg_left)', 'q1(pressure)', 'q1(timeDeriv (0))', 'q1(timeDeriv (1))', 'q1(timeDeriv (2))', 'q1(timeDeriv (3))', 'q1(timeDeriv (Magnitude))', 'q1(velocity (0))', 'q1(velocity (1))', 'q1(velocity (2))', 'q1(velocity (Magnitude))', 'q1(vinplane_traction (0))', 'q1(vinplane_traction (1))', 'q1(vinplane_traction (2))', 'q1(vinplane_traction (Magnitude))', 'q1(vWSS (0))', 'q1(vWSS (1))', 'q1(vWSS (2))', 'q1(vWSS (Magnitude))', 'q1(X)', 'q1(Y)', 'q1(Z)', 'q3(Area)', 'q3(average_pressure)', 'q3(average_speed)', 'q3(GlobalElementID)', 'q3(GlobalNodeID)', 'q3(p_avg_left)', 'q3(pressure)', 'q3(timeDeriv (0))', 'q3(timeDeriv (1))', 'q3(timeDeriv (2))', 'q3(timeDeriv (3))', 'q3(timeDeriv (Magnitude))', 'q3(velocity (0))', 'q3(velocity (1))', 'q3(velocity (2))', 'q3(velocity (Magnitude))', 'q3(vinplane_traction (0))', 'q3(vinplane_traction (1))', 'q3(vinplane_traction (2))', 'q3(vinplane_traction (Magnitude))', 'q3(vWSS (0))', 'q3(vWSS (1))', 'q3(vWSS (2))', 'q3(vWSS (Magnitude))', 'q3(X)', 'q3(Y)', 'q3(Z)', 'std(Area)', 'std(average_pressure)', 'std(average_speed)', 'std(GlobalElementID)', 'std(GlobalNodeID)', 'std(p_avg_left)', 'std(pressure)', 'std(timeDeriv (0))', 'std(timeDeriv (1))', 'std(timeDeriv (2))', 'std(timeDeriv (3))', 'std(timeDeriv (Magnitude))', 'std(velocity (0))', 'std(velocity (1))', 'std(velocity (2))', 'std(velocity (Magnitude))', 'std(vinplane_traction (0))', 'std(vinplane_traction (1))', 'std(vinplane_traction (2))', 'std(vinplane_traction (Magnitude))', 'std(vWSS (0))', 'std(vWSS (1))', 'std(vWSS (2))', 'std(vWSS (Magnitude))', 'std(X)', 'std(Y)', 'std(Z)', 'sum(Area)', 'sum(average_pressure)', 'sum(average_speed)', 'sum(GlobalElementID)', 'sum(GlobalNodeID)', 'sum(p_avg_left)', 'sum(pressure)', 'sum(timeDeriv (0))', 'sum(timeDeriv (1))', 'sum(timeDeriv (2))', 'sum(timeDeriv (3))', 'sum(timeDeriv (Magnitude))', 'sum(velocity (0))', 'sum(velocity (1))', 'sum(velocity (2))', 'sum(velocity (Magnitude))', 'sum(vinplane_traction (0))', 'sum(vinplane_traction (1))', 'sum(vinplane_traction (2))', 'sum(vinplane_traction (Magnitude))', 'sum(vWSS (0))', 'sum(vWSS (1))', 'sum(vWSS (2))', 'sum(vWSS (Magnitude))', 'sum(X)', 'sum(Y)', 'sum(Z)', 'Time', 'vtkValidPointMask', 'max(p_avg_right)', 'med(p_avg_right)', 'min(p_avg_right)', 'q1(p_avg_right)', 'q3(p_avg_right)', 'std(p_avg_right)', 'sum(p_avg_right)', 'max(Surface Flow)', 'med(Surface Flow)', 'min(Surface Flow)', 'q1(Surface Flow)', 'q3(Surface Flow)', 'std(Surface Flow)', 'sum(Surface Flow)', 'max(p_avg_aorta)', 'med(p_avg_aorta)', 'min(p_avg_aorta)', 'q1(p_avg_aorta)', 'q3(p_avg_aorta)', 'std(p_avg_aorta)', 'sum(p_avg_aorta)']

# Properties modified on spreadSheetView1
spreadSheetView1.HiddenColumnLabels = ['Block Name', 'Block Number', 'Row ID', 'avg(Area)', 'avg(average_pressure)', 'avg(average_speed)', 'avg(GlobalElementID)', 'avg(GlobalNodeID)', 'avg(pressure)', 'avg(timeDeriv (0))', 'avg(timeDeriv (1))', 'avg(timeDeriv (2))', 'avg(timeDeriv (3))', 'avg(timeDeriv (Magnitude))', 'avg(velocity (0))', 'avg(velocity (1))', 'avg(velocity (2))', 'avg(velocity (Magnitude))', 'avg(vinplane_traction (0))', 'avg(vinplane_traction (1))', 'avg(vinplane_traction (2))', 'avg(vinplane_traction (Magnitude))', 'avg(vWSS (0))', 'avg(vWSS (1))', 'avg(vWSS (2))', 'avg(vWSS (Magnitude))', 'avg(X)', 'avg(Y)', 'avg(Z)', 'max(Area)', 'max(average_pressure)', 'max(average_speed)', 'max(GlobalElementID)', 'max(GlobalNodeID)', 'max(p_avg_left)', 'max(pressure)', 'max(timeDeriv (0))', 'max(timeDeriv (1))', 'max(timeDeriv (2))', 'max(timeDeriv (3))', 'max(timeDeriv (Magnitude))', 'max(velocity (0))', 'max(velocity (1))', 'max(velocity (2))', 'max(velocity (Magnitude))', 'max(vinplane_traction (0))', 'max(vinplane_traction (1))', 'max(vinplane_traction (2))', 'max(vinplane_traction (Magnitude))', 'max(vWSS (0))', 'max(vWSS (1))', 'max(vWSS (2))', 'max(vWSS (Magnitude))', 'max(X)', 'max(Y)', 'max(Z)', 'med(Area)', 'med(average_pressure)', 'med(average_speed)', 'med(GlobalElementID)', 'med(GlobalNodeID)', 'med(p_avg_left)', 'med(pressure)', 'med(timeDeriv (0))', 'med(timeDeriv (1))', 'med(timeDeriv (2))', 'med(timeDeriv (3))', 'med(timeDeriv (Magnitude))', 'med(velocity (0))', 'med(velocity (1))', 'med(velocity (2))', 'med(velocity (Magnitude))', 'med(vinplane_traction (0))', 'med(vinplane_traction (1))', 'med(vinplane_traction (2))', 'med(vinplane_traction (Magnitude))', 'med(vWSS (0))', 'med(vWSS (1))', 'med(vWSS (2))', 'med(vWSS (Magnitude))', 'med(X)', 'med(Y)', 'med(Z)', 'min(Area)', 'min(average_pressure)', 'min(average_speed)', 'min(GlobalElementID)', 'min(GlobalNodeID)', 'min(p_avg_left)', 'min(pressure)', 'min(timeDeriv (0))', 'min(timeDeriv (1))', 'min(timeDeriv (2))', 'min(timeDeriv (3))', 'min(timeDeriv (Magnitude))', 'min(velocity (0))', 'min(velocity (1))', 'min(velocity (2))', 'min(velocity (Magnitude))', 'min(vinplane_traction (0))', 'min(vinplane_traction (1))', 'min(vinplane_traction (2))', 'min(vinplane_traction (Magnitude))', 'min(vWSS (0))', 'min(vWSS (1))', 'min(vWSS (2))', 'min(vWSS (Magnitude))', 'min(X)', 'min(Y)', 'min(Z)', 'N', 'q1(Area)', 'q1(average_pressure)', 'q1(average_speed)', 'q1(GlobalElementID)', 'q1(GlobalNodeID)', 'q1(p_avg_left)', 'q1(pressure)', 'q1(timeDeriv (0))', 'q1(timeDeriv (1))', 'q1(timeDeriv (2))', 'q1(timeDeriv (3))', 'q1(timeDeriv (Magnitude))', 'q1(velocity (0))', 'q1(velocity (1))', 'q1(velocity (2))', 'q1(velocity (Magnitude))', 'q1(vinplane_traction (0))', 'q1(vinplane_traction (1))', 'q1(vinplane_traction (2))', 'q1(vinplane_traction (Magnitude))', 'q1(vWSS (0))', 'q1(vWSS (1))', 'q1(vWSS (2))', 'q1(vWSS (Magnitude))', 'q1(X)', 'q1(Y)', 'q1(Z)', 'q3(Area)', 'q3(average_pressure)', 'q3(average_speed)', 'q3(GlobalElementID)', 'q3(GlobalNodeID)', 'q3(p_avg_left)', 'q3(pressure)', 'q3(timeDeriv (0))', 'q3(timeDeriv (1))', 'q3(timeDeriv (2))', 'q3(timeDeriv (3))', 'q3(timeDeriv (Magnitude))', 'q3(velocity (0))', 'q3(velocity (1))', 'q3(velocity (2))', 'q3(velocity (Magnitude))', 'q3(vinplane_traction (0))', 'q3(vinplane_traction (1))', 'q3(vinplane_traction (2))', 'q3(vinplane_traction (Magnitude))', 'q3(vWSS (0))', 'q3(vWSS (1))', 'q3(vWSS (2))', 'q3(vWSS (Magnitude))', 'q3(X)', 'q3(Y)', 'q3(Z)', 'std(Area)', 'std(average_pressure)', 'std(average_speed)', 'std(GlobalElementID)', 'std(GlobalNodeID)', 'std(p_avg_left)', 'std(pressure)', 'std(timeDeriv (0))', 'std(timeDeriv (1))', 'std(timeDeriv (2))', 'std(timeDeriv (3))', 'std(timeDeriv (Magnitude))', 'std(velocity (0))', 'std(velocity (1))', 'std(velocity (2))', 'std(velocity (Magnitude))', 'std(vinplane_traction (0))', 'std(vinplane_traction (1))', 'std(vinplane_traction (2))', 'std(vinplane_traction (Magnitude))', 'std(vWSS (0))', 'std(vWSS (1))', 'std(vWSS (2))', 'std(vWSS (Magnitude))', 'std(X)', 'std(Y)', 'std(Z)', 'sum(Area)', 'sum(average_pressure)', 'sum(average_speed)', 'sum(GlobalElementID)', 'sum(GlobalNodeID)', 'sum(p_avg_left)', 'sum(pressure)', 'sum(timeDeriv (0))', 'sum(timeDeriv (1))', 'sum(timeDeriv (2))', 'sum(timeDeriv (3))', 'sum(timeDeriv (Magnitude))', 'sum(velocity (0))', 'sum(velocity (1))', 'sum(velocity (2))', 'sum(velocity (Magnitude))', 'sum(vinplane_traction (0))', 'sum(vinplane_traction (1))', 'sum(vinplane_traction (2))', 'sum(vinplane_traction (Magnitude))', 'sum(vWSS (0))', 'sum(vWSS (1))', 'sum(vWSS (2))', 'sum(vWSS (Magnitude))', 'sum(X)', 'sum(Y)', 'sum(Z)', 'Time', 'vtkValidPointMask', 'max(p_avg_right)', 'med(p_avg_right)', 'min(p_avg_right)', 'q1(p_avg_right)', 'q3(p_avg_right)', 'std(p_avg_right)', 'sum(p_avg_right)', 'max(Surface Flow)', 'med(Surface Flow)', 'min(Surface Flow)', 'q1(Surface Flow)', 'q3(Surface Flow)', 'std(Surface Flow)', 'sum(Surface Flow)', 'max(p_avg_aorta)', 'med(p_avg_aorta)', 'min(p_avg_aorta)', 'q1(p_avg_aorta)', 'q3(p_avg_aorta)', 'std(p_avg_aorta)', 'sum(p_avg_aorta)']

# export view
ExportView(file_path+'p_avg_left.csv', view=spreadSheetView1)

# hide data in view
Hide(plotDataOverTime5, spreadSheetView1)

# set active source
SetActiveSource(plotDataOverTime6)

# show data in view
plotDataOverTime6Display_1 = Show(plotDataOverTime6, spreadSheetView1, 'SpreadSheetRepresentation')

# export view
ExportView(file_path+'surface_flow_left.csv', view=spreadSheetView1)

# clear all selections
ClearSelection()

#================================================================
# addendum: following script captures some of the application
# state to faithfully reproduce the visualization during playback
#================================================================

#--------------------------------
# saving layout sizes for layouts

# layout/tab size in pixels
layout1.SetSize(1885, 969)

#-----------------------------------
# saving camera placements for views

# current camera placement for renderView1
renderView1.Set(
    CameraPosition=[-30.87984938283176, 18.505485264915034, 149.40124287102455],
    CameraFocalPoint=[-8.546056362545748, -16.810419209381976, 84.33635264964154],
    CameraViewUp=[0.8920598312881091, -0.19069926725294972, 0.4097109308664082],
    CameraParallelScale=20.01367759079839,
)


##--------------------------------------------
## You may need to add some code at the end of this python script depending on your usage, eg:
#
## Render all views to see them appears
# RenderAllViews()
#
## Interact with the view, usefull when running from pvpython
# Interact()
#
## Save a screenshot of the active view
# SaveScreenshot("path/to/screenshot.png")
#
## Save a screenshot of a layout (multiple splitted view)
# SaveScreenshot("path/to/screenshot.png", GetLayout())
#
## Save all "Extractors" from the pipeline browser
# SaveExtracts()
#
## Save a animation of the current active view
# SaveAnimation()
#
## Please refer to the documentation of paraview.simple
## https://www.paraview.org/paraview-docs/latest/python/paraview.simple.html
##--------------------------------------------