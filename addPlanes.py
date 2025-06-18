from paraview.simple import *
import numpy as np
import os
import pandas as pd
import ast
import csv
import math
from collections import defaultdict




def compute_plane_points(center, normal, side_length=5):
    center = np.array(center)
    normal = np.array(normal)
    normal = normal / np.linalg.norm(normal)

    # Pick an arbitrary vector not parallel to the normal
    if np.allclose(normal, [0, 0, 1]):
        tangent = np.array([1, 0, 0])
    else:
        tangent = np.array([0, 0, 1])

    # First direction vector (u) is perpendicular to normal
    u = np.cross(normal, tangent)
    u = u / np.linalg.norm(u)

    # Second direction vector (v) is perpendicular to both normal and u
    v = np.cross(normal, u)

    # Scale to half side length
    half = side_length / 2
    u *= half
    v *= half

    # Plane corners
    origin = center - u - v
    point1 = center + u - v
    point2 = center - u + v

    return origin.tolist(), point1.tolist(), point2.tolist()

renderView1 = GetActiveViewOrCreate('RenderView')
planes = {}

# Loop over 3 slices
for i in range(1, 4):
    clip = FindSource(f"Clip{i}")
    slice = FindSource(f"Slice{i}")
    
    if not slice:
        print(f"Warning: Slice{i} not found. Skipping...")
        continue

    # Extract origin and normal
    clip_center = clip.ClipType.Origin
    clip_normal =clip.ClipType.Normal
    slice_center = slice.SliceType.Origin
    slice_normal = slice.SliceType.Normal

    if i == 2:
        origin, point1, point2 = compute_plane_points(slice_center, slice_normal, 5)
    else:
        origin, point1, point2 = compute_plane_points(slice_center, slice_normal, 4)
        
    plane_name = f'Slice_plane_{i}'
    plane = Plane(registrationName=plane_name)
    plane.Origin = origin
    plane.Point1 = point1
    plane.Point2 = point2
    plane.XResolution = 40
    plane.YResolution = 40
    planeDisplay = Show(plane, renderView1, 'GeometryRepresentation')
    planeDisplay.Representation = 'Surface'
    planeDisplay.Set(
    AmbientColor=[0.3333333432674408, 0.3333333432674408, 1.0],
    DiffuseColor=[0.3333333432674408, 0.3333333432674408, 1.0],
)
    plane.UpdatePipeline()


    origin, point1, point2 = compute_plane_points(clip_center, clip_normal, 4)
        
    plane_name = f'Clip_plane_{i}'
    plane = Plane(registrationName=plane_name)
    plane.Origin = origin
    plane.Point1 = point1
    plane.Point2 = point2
    plane.XResolution = 40
    plane.YResolution = 40
    planeDisplay = Show(plane, renderView1, 'GeometryRepresentation')
    planeDisplay.Representation = 'Surface'
    planeDisplay.Set(
    AmbientColor=[0.3333333432674408, 0.3333333432674408, 1.0],
    DiffuseColor=[0.3333333432674408, 0.3333333432674408, 1.0],
)
    plane.UpdatePipeline()


renderView1.Update()