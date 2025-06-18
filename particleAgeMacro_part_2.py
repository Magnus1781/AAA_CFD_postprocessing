from paraview.simple import *
import numpy as np
import os
import pandas as pd
import ast
import csv
import math
from collections import defaultdict

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

####Change this only#############
model = AAA013
#################################

cwd = f"C:\\Users\\magnuswe\\OneDrive - SINTEF\\Simvascular\\results\\two_last_cycles\\{model}-two_last_cycles"

#Saving entry state#
SaveState(os.path.join(cwd, 'paraview_particle_age_part2_pre.pvsm'))
SaveState(os.path.join(cwd, 'paraview_valid_region.pvsm'))

##Logging setup##
log_file_path = os.path.join(cwd, "particle_log2.txt")
log_file = open(log_file_path, "w")

def log(msg):
    log_file.write(msg + "\n")
    log_file.flush()
log("Created log")


#################Load the centerline points and tangents##############
data = pd.read_csv(os.path.join(cwd, 'centerline_points_and_tangents_table.csv'))
points = dict()
tangents = dict()

for col in data.columns:
    if col.startswith('point_'):
        points[col] = ast.literal_eval(data[col].iloc[0])
        log(str(ast.literal_eval(data[col].iloc[0])))
    elif col.startswith('tangent_'):
        tangents[col] = ast.literal_eval(data[col].iloc[0])



# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# update the view to ensure updated data information
renderView1.Update()

temporalInterpolator1 = FindSource('TemporalInterpolator1')
temporalInterpolator1.DiscreteTimeStepInterval = 0.02
Hide(temporalInterpolator1, renderView1)


stlfile = FindSource(f"{model[:6]}.stl")
Hide(stlfile, renderView1)

transform1=FindSource("TransformSTL")
Hide(transform1, renderView1)

clip3 = FindSource('Clip3')
clip3Display = Show(clip3, renderView1, 'UnstructuredGridRepresentation')
clip3Display.Opacity = 0.3

# update the view to ensure updated data information
renderView1.Update()

####Alternative section with line cretion of tangents. To check tangents.
"""
for i in range(5):
    log(str(points[f"point_{i}"]))
    log(str(tangents[f"tangent_{i}"]))
    origin = np.array(points[f"point_{i}"])
    tangent = np.array(tangents[f"tangent_{i}"])
    log("here i am no2")
    tip = origin + tangent * 5  # Scale the tangent if needed

    line1 = Line(registrationName=f'Line{i}')
    log(str(origin.tolist()))
    log(str(tip.tolist()))

    line1.Set(
        Point1=origin.tolist(),
        Point2=tip.tolist(),
    )
    line1.UpdatePipeline()
    line1Display = Show(line1, renderView1, 'GeometryRepresentation')
    line1Display.Representation = 'Surface'
renderView1.Update()
"""



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



planes = {}

#Creating planes based on the points and tangents
for i in range(5):
    log(f'length of data: {len(data)}')
    plane_name = f'Plane_{i}'
    origin, point1, point2 = compute_plane_points(points[f"point_{i}"], tangents[f"tangent_{i}"])
    plane = Plane(registrationName=plane_name)
    plane.Origin = origin
    plane.Point1 = point1
    plane.Point2 = point2
    plane.XResolution = 40
    plane.YResolution = 40
    planes[plane_name] = plane
    #planes[plane_name] = create_seed_plane(plane_name, points[f'point_{i}'], tangents[f'tangent_{i}'], 10, 30)
    planeDisplay = Show(planes[plane_name], renderView1)  # Show the correct object
    planes[plane_name].UpdatePipeline()
    planeDisplay.Representation = 'Surface'
    Hide(plane, renderView1)
    log(f"Plane {i} created with center {points[f'point_{i}']} and normal {tangents[f'tangent_{i}']}")

renderView1.ResetCamera()

renderView1.Update()
log("Camera reset and rendered")
particle_tracers = {}
log("particle_tracers dictionary created")

#Creatig particle tracers for each plane
reinjection_nth_step = 50
for i in range(5):
    particle_tracer_name = f'ParticleTracer_{i}'
    particle_tracer = ParticleTracer(registrationName=particle_tracer_name, Input=clip3,
        SeedSource=planes[f'Plane_{i}'])
    log(f"ParticleTracer_{i} created with seed source Plane_{i}")
    particle_tracer.ForceReinjectionEveryNSteps = reinjection_nth_step
    particle_tracer.SelectInputVectors = ['POINTS', 'velocity']
    
    # trace defaults for the display properties.

    # show data in view
    particle_tracerDisplay = Show(particle_tracer, renderView1, 'GeometryRepresentation')
    particle_tracerDisplay.Representation = 'Surface'
    particle_tracer.StaticSeeds=1
    particle_tracer.MeshOverTime='Static'
    particle_tracer.UpdatePipeline()
    particle_tracers[particle_tracer_name] = particle_tracer  # store in dictionary
    renderView1.Update()



log("particle_tracers dictionary populated")

#Creating temporal particles to pathlines for particle visualization
tempParToPathLinesDict = {}
for i in range(5):
    temporalParticlesToPathlines_name = f'TemporalParticlesToPathlines_{i}'
    obj = TemporalParticlesToPathlines(registrationName=temporalParticlesToPathlines_name, Input=particle_tracers[f'ParticleTracer_{i}'], Selection=None)
    obj.MaskPoints = 0
    tempParToPathLinesDict[temporalParticlesToPathlines_name] = obj
    log(f"TemporalParticlesToPathlines {i} created with input ParticleTracer_{i}")
    objDisplay = Show(OutputPort(obj, 1), renderView1, 'GeometryRepresentation')
    objDisplay.Representation = 'Surface'
    renderView1.Update()

log("tempParToPathLinesDict populated")

######################Rendering#######################






# get layout
layout1 = GetLayout()

#--------------------------------
# saving layout sizes for layouts

# layout/tab size in pixels
layout1.SetSize(1923, 990)

#-----------------------------------
# saving camera placements for views

# current camera placement for renderView1
camera1 = renderView1.GetActiveCamera()

renderView1.Set(
    CameraPosition=camera1.GetPosition(),
    CameraFocalPoint=camera1.GetFocalPoint(),
    CameraViewUp=camera1.GetViewUp(),
    CameraParallelScale=renderView1.CameraParallelScale,
)

renderView1.Update()
#################Particle tracking####################
# Get time range from the animation scene
scene = GetAnimationScene()
t0 = scene.TimeKeeper.TimestepValues[0]  # Start time
t1 = scene.TimeKeeper.TimestepValues[-1] # End time

# Set fine time resolution
dt = 0.02
fine_timesteps = np.arange(t0, t1 + dt, dt)
log(f"Timestep is set to {dt}")
log(f"First timestep: {t0}, Last timestep: {t1}")


ignored_ids = defaultdict(set)
vmag_threshold = 0.2
#active_particles = defaultdict(lambda: defaultdict(int))
exit_records = defaultdict(list)

previous_counts = defaultdict(lambda: defaultdict(int))
first_time_step = defaultdict(lambda: True)
total_current_count = defaultdict(int)
end_simulation = False
remaining_particles = defaultdict(lambda: defaultdict(int))

for t in fine_timesteps:
    scene.AnimationTime = float(t)
    t = round(t, 3)
    renderView1.Update()
    current_counts = defaultdict(lambda: defaultdict(int))

    if t == 0.00:
        SaveState(os.path.join(cwd, 'paraview_particle_age_part2_post.pvsm'))
        log("Saved state at t=0")
    if t > 95.00 and all(cnt == 0 for cnt in total_current_count.values()):
        break

    # Iteration over each particle tracer
    for name, obj in particle_tracers.items():
        
        renderView1.Update()

        data = servermanager.Fetch(obj)
        points = data.GetPoints()
        numPts = points.GetNumberOfPoints()

        injections = data.GetPointData().GetArray("InjectionStepId")
        inj_point_id_dataset = data.GetPointData().GetArray("InjectedPointId")
        log(f"number of points for {name}: {numPts}")

            
        if t == 0.00:
            v_array = data.GetPointData().GetArray("velocity")
            for i in range(numPts):
                v = v_array.GetTuple(i)
                vmag = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
                inj_point_id = inj_point_id_dataset.GetValue(i)
                if vmag < vmag_threshold:
                    ignored_ids[name].add(inj_point_id)
        
        
        total_current_count[name] = 0
        for i in range(numPts):
            inj_id = injections.GetValue(i)
            inj_point_id = inj_point_id_dataset.GetValue(i)
            if inj_id > 94*reinjection_nth_step or inj_point_id in ignored_ids[name]: # for force injection every 10th step: inj_id @ t=94 is 94*10=940. every 50th step is 94*50=4700 
                continue  # Skip tracking this injection ID
        
            #age = round(ages.GetValue(i), 3)
            current_counts[name][(inj_id, inj_point_id)] += 1
            total_current_count[name] +=1
        
        
        log(f"Total particles from {name} at t={t}: {total_current_count[name]}")
        added_particles = 0
        if t == 0.00:
            previous_counts[name] = current_counts[name].copy()
            continue
        elif t == 190.00:
            remaining_particles[name] = current_counts[name]
        else:
            for (inj_id, inj_point_id), prev_count in previous_counts[name].items():
                curr_count = current_counts[name].get((inj_id, inj_point_id), 0)
                exited = prev_count - curr_count
                if exited > 0:
                    exit_records[name].append((round(t-dt,3), inj_id, inj_point_id, exited))  # InjectionStepId, time, num exited

                # Detect newly injected particles (not present in guess_count)
            for (inj_id, inj_point_id), curr_count in current_counts[name].items():
                if (inj_id, inj_point_id) not in previous_counts[name]:
                    # New particles injected
                    added_particles += curr_count
        if t % 1 == 0:
            log(f"At t={t}, {added_particles} new particles injected from {name}")
        # Update previous_counts for the next timestep

            
        previous_counts[name] = current_counts[name].copy()

log(f"Remaining particles: {remaining_particles}")

# Save results to CSV

for i in range(5):
    output_file = os.path.join(cwd, f"particle_age_stats_{i}.csv")
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["Current time", "Time of Injection","Particle age", "Injection Point ID", "Count"])
        for time, inj_id, inj_point_id, count in exit_records[f'ParticleTracer_{i}']:
            injection_time = round(inj_id * 0.01/reinjection_nth_step, 4)
            current_time = round(time * 0.01, 4)
            particle_age = round(current_time - injection_time, 4)
            writer.writerow([current_time, injection_time, particle_age, inj_point_id, count])
        for (inj_id, inj_point_id), count in remaining_particles[f'ParticleTracer_{i}'].items():
            injection_time = round(inj_id * 0.01/reinjection_nth_step, 4)
            # For remaining, use the last time step
            current_time = round(t1 * 0.01, 4)
            particle_age = round(current_time - injection_time, 4)
            writer.writerow([current_time, injection_time, particle_age, inj_point_id, count])
    log(f"CSV saved at: {os.path.abspath(output_file)}")


injection_zero_counts = {}
particle_tracer_count = {}

# Loop through each particle tracer
for i in range(5):
    injection_zero_counts[i] = 0
    particle_tracer_count[i] = 0
    for time, inj_id, inj_point_id, count in exit_records[f'ParticleTracer_{i}']:
        particle_tracer_count[i] += count
        if inj_id == 0:
            injection_zero_counts[i] += count

for i in range(5):
    for (inj_id, inj_point_id), count in remaining_particles[f'ParticleTracer_{i}'].items():
        particle_tracer_count[i] += count

# Multiply each count by 95
scaled_injection_zero_counts = {k: v * 95 for k, v in injection_zero_counts.items()}

# Compute total sums (optional, for summary logging)
sum_scaled_zero_counts = sum(scaled_injection_zero_counts.values())
total_exit_count = sum(particle_tracer_count.values())

# Log full summary
log(f"Scaled injection step 0 counts per tracer (×95): {scaled_injection_zero_counts}")
log(f"Total particle exit count per tracer: {particle_tracer_count}")
log(f"Sum of scaled injection 0 counts: {sum_scaled_zero_counts}")
log(f"Total particle exit count (all tracers): {total_exit_count}")

# Per-tracer comparison
for i in range(5):
    scaled = scaled_injection_zero_counts[i]
    total = particle_tracer_count[i]
    if total == scaled:
        log(f"✅ Tracer {i}: Scaled step 0 count ({scaled}) matches total exit count ({total}).")
    else:
        log(f"❌ Tracer {i} mismatch:")
        log(f"    Scaled step 0 count: {scaled}")
        log(f"    Actual exit count:   {total}")
        log(f"    Difference:          {total - scaled}")




log_file.close()
