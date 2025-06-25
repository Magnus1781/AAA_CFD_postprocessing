from paraview.simple import *
import numpy as np
import os
import pandas as pd
import ast
import csv
import math
from collections import defaultdict
cwd = 'C:\\Users\\magnuswe\\OneDrive - SINTEF\\Simvascular\\results\\two_last_cycles\\AAA001_sim_0-19_1-1mill-two_last_cycles'


#################Logging setup####################
log_file_path = os.path.join(cwd, "particle_log2.txt")
log_file = open(log_file_path, "w")

def log(msg):
    log_file.write(msg + "\n")
    log_file.flush()


#################Load the centerline points and tangents##############
data = pd.read_csv(os.path.join(cwd, 'centerline_points_and_tangents_table.csv'))

points = dict()
tangents = dict()


for col in data.columns:
    if col.startswith('point_'):
        points[col] = ast.literal_eval(data[col].iloc[0])
    elif col.startswith('tangent_'):
        tangents[col] = ast.literal_eval(data[col].iloc[0])



# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

############Introduce Brownian motion in low velocity areas##############
# Get the programmable filter by name
pf = FindSource("ProgrammableFilter1")

pf.Set(
Script="""
import numpy as np
from vtkmodules.util import numpy_support

# Copy input to output to retain geometry and all original arrays
input0 = inputs[0]


# Get the input velocity array as a NumPy array
vel_array = input0.PointData["velocity"]
vel_np = numpy_support.vtk_to_numpy(vel_array)

# Parameters
#threshold = 0.05
#kT = 0.01
threshold = 0.2
kT = 0.1
# Compute new velocity array
new_vel_np = np.copy(vel_np)
for i, v in enumerate(vel_np):
    mag = np.linalg.norm(v)
    if mag == 0.0:
        continue  # Leave velocity_brownian as zero
    elif mag < threshold:
        noise = np.random.normal(loc=0.0, scale=kT, size=3)
        new_vel_np[i] = v + noise
    # else: keep original velocity

# Convert back to VTK array
new_vel_vtk = numpy_support.numpy_to_vtk(new_vel_np)
new_vel_vtk.SetName("velocity_brownian")

# Add to output without replacing the original velocity
output.PointData.AddArray(new_vel_vtk)

# Optional: set the new array as the active vector field (for glyphs, streamlines, etc.)
output.PointData.SetActiveVectors("velocity_brownian")""",
RequestInformationScript='',
RequestUpdateExtentScript='',
CopyArrays=1,
PythonPath='',
)

# update the view to ensure updated data information
renderView1.Update()

# hide data in view
Hide(pf, renderView1)

all_results_03820vtu= FindSource('all_results_03820.vtu*')

temporalInterpolator1 = FindSource('TemporalInterpolator1')

temporalInterpolator1.DiscreteTimeStepInterval = 0.1

# hide data in view
Hide(temporalInterpolator1, renderView1)

clip2 = FindSource('Clip2')

clip4 = FindSource('Clip4')

clip4Display = Show(clip4, renderView1, 'UnstructuredGridRepresentation')

clip4Display.Opacity = 0.3

# update the view to ensure updated data information
renderView1.Update()

planes = {}




def create_seed_plane(name, center, normal, plane_size, resolution):
    """
    Creates a uniformly sampled plane at `center` with `normal` as normal vector.
    Returns a transform-filtered plane that can be used as a ParticleTracer seed.
    """
    # Normalize the normal vector
    norm_len = math.sqrt(sum(n**2 for n in normal))
    normal = [n / norm_len for n in normal]

    # Create base plane aligned with Z-axis
    base_plane = Plane(registrationName=name)
    base_plane.Origin = [-plane_size / 2, -plane_size / 2, 0.0]
    base_plane.Point1 = [ plane_size / 2, -plane_size / 2, 0.0]
    base_plane.Point2 = [-plane_size / 2,  plane_size / 2, 0.0]
    base_plane.XResolution = resolution
    base_plane.YResolution = resolution

    # Calculate rotation axis and angle from Z-axis to the desired normal
    z_axis = [0.0, 0.0, 1.0]
    rot_axis = [
        z_axis[1]*normal[2] - z_axis[2]*normal[1],
        z_axis[2]*normal[0] - z_axis[0]*normal[2],
        z_axis[0]*normal[1] - z_axis[1]*normal[0],
    ]
    rot_axis_len = math.sqrt(sum(r**2 for r in rot_axis))

    if rot_axis_len < 1e-6:
        angle_deg = 0.0  # Vectors are aligned
        rot_axis = [0.0, 0.0, 1.0]  # arbitrary
    else:
        rot_axis = [r / rot_axis_len for r in rot_axis]
        dot = sum(z_axis[i]*normal[i] for i in range(3))
        angle_rad = math.acos(dot)
        angle_deg = math.degrees(angle_rad)

    # Apply rotation and translation to align and place the plane
    transform = Transform(Input=base_plane)
    transform.Transform = 'Transform'
    transform.Transform.Rotate = [angle_deg * a for a in rot_axis]
    transform.Transform.Translate = center

    return transform

log("create_seed_plane function defined")

for i in range(5):
    log(f'length of data: {len(data)}')
    plane_name = f'Plane_{i}'
    planes[plane_name] = create_seed_plane(plane_name, points[f'point_{i}'], tangents[f'tangent_{i}'], 10, 6)
    planeDisplay = Show(planes[plane_name], renderView1)  # Show the correct object
    planes[plane_name].UpdatePipeline()
    planeDisplay.Representation = 'Surface'
    log(f"Plane {i} created with center {points[f'point_{i}']} and normal {tangents[f'tangent_{i}']}")

renderView1.ResetCamera()
# update the view to ensure updated data information
renderView1.Update()
log("Camera reset and rendered")
particle_tracers = {}
log("particle_tracers dictionary created")

for i in range(5):
    particle_tracer_name = f'ParticleTracer_{i}'
    particle_tracer = ParticleTracer(registrationName=particle_tracer_name, Input=clip4,
        SeedSource=planes[f'Plane_{i}'])
    log(f"ParticleTracer_{i} created with seed source Plane_{i}")
    particle_tracer.ForceReinjectionEveryNSteps = 10
    particle_tracer.SelectInputVectors = ['POINTS', 'velocity_brownian']
    
    # trace defaults for the display properties.

    # show data in view
    particle_tracerDisplay = Show(particle_tracer, renderView1, 'GeometryRepresentation')
    particle_tracerDisplay.Representation = 'Surface'
    particle_tracer.UpdatePipeline()
    particle_tracers[particle_tracer_name] = particle_tracer  # store in dictionary
    renderView1.Update()

log("particle_tracers dictionary populated")

tempParToPathLinesDict = {}
for i in range(5):
    temporalParticlesToPathlines_name = f'TemporalParticlesToPathlines_{i}'
    obj = TemporalParticlesToPathlines(registrationName=temporalParticlesToPathlines_name, Input=particle_tracers[f'ParticleTracer_{i}'], Selection=None)
    obj.MaskPoints = 1
    tempParToPathLinesDict[temporalParticlesToPathlines_name] = obj
    log(f"TemporalParticlesToPathlines {i} created with input ParticleTracer_{i}")
    objDisplay = Show(OutputPort(obj, 1), renderView1, 'GeometryRepresentation')
    objDisplay.Representation = 'Surface'
    renderView1.Update()

log("tempParToPathLinesDict populated")

######################Rendering#######################



# hide data in view
Hide(temporalInterpolator1, renderView1)

# find source
transform2 = FindSource('Transform2')

# hide data in view
Hide(transform2, renderView1)

# find source
transform3 = FindSource('Transform3')

# hide data in view
Hide(transform3, renderView1)

# find source
transform4 = FindSource('Transform4')

# hide data in view
Hide(transform4, renderView1)

# find source
transform5 = FindSource('Transform5')

# hide data in view
Hide(transform5, renderView1)

# find source
transform6 = FindSource('Transform6')

# hide data in view
Hide(transform6, renderView1)


# get layout
layout1 = GetLayout()

#--------------------------------
# saving layout sizes for layouts

# layout/tab size in pixels
layout1.SetSize(1923, 990)

#-----------------------------------
# saving camera placements for views

# current camera placement for renderView1
renderView1.Set(
    CameraPosition=[10.507632759296303, 25.535154110721816, 93.83651110674131],
    CameraFocalPoint=[-11.283719055378347, -50.68664116286929, 92.29848164759251],
    CameraViewUp=[0.19907769209350992, -0.07662901228029555, 0.9769831457029686],
    CameraParallelScale=20.521903300643487,
)

renderView1.Update()
#################Particle tracking####################
# Get time range from the animation scene
scene = GetAnimationScene()
t0 = scene.TimeKeeper.TimestepValues[0]  # Start time
t1 = scene.TimeKeeper.TimestepValues[-1] # End time

# Set fine time resolution
dt = 0.1
fine_timesteps = np.arange(t0, t1 + dt, dt)
log(f"Timestep is set to {dt}")
log(f"First timestep: {t0}, Last timestep: {t1}")



#active_particles = defaultdict(lambda: defaultdict(int))
exit_records = defaultdict(list)

previous_counts = defaultdict(lambda: defaultdict(int))
first_time_step = defaultdict(lambda: True)
particles_added = defaultdict(int)
for name in particle_tracers.keys():
    first_time_step[name] = True  # Initialize the first_time_step flag for each tracer

end_simulation = False

for t in fine_timesteps:
    scene.AnimationTime = float(t)
    t= round(t, 2)
    # update the view to ensure updated data information
    renderView1.Update()
    current_counts = defaultdict(lambda: defaultdict(int))

    # --- Exit condition block here ---
    if t > 5:
        if end_simulation:
            log("All particles with InjectionStepId < 95 have exited, breaking time loop")
            break


    # Iteration over each particle tracer
    for name, obj in particle_tracers.items():
        renderView1.Update()

        data = servermanager.Fetch(obj)
        points = data.GetPoints()

        numPts = points.GetNumberOfPoints()

        ages = data.GetPointData().GetArray("ParticleAge")

        injections = data.GetPointData().GetArray("InjectionStepId")
        log(f"number of points for {name}: {numPts}")
        
            

        
        
        total_current_count = 0  # Total number of particles at the current timestep

        for i in range(numPts):
            inj_id = injections.GetValue(i)
            if inj_id > 940:
                continue  # Skip tracking this injection ID
            age = round(ages.GetValue(i), 3) # Round to 3 decimal places to avoid floating point issues
            current_counts[name][(inj_id, age)] += 1
            total_current_count +=1
        if t > 95 and total_current_count == 0:
                end_simulation = True
                break
        log(f"Total particles from {name} at t={t:.3f}: {total_current_count}")

        if first_time_step[name]:
            # On the first frame with particles, initialize previous_counts with current_counts
            first_time_step[name] = False
            particles_added[name] = total_current_count
        
        # Compare with previous timestep to detect disappearances
        else:
            #injected_particles = 0  # Reset particles added for this timestep
            #if int(t / dt) % 10 == 0:
            #    log(f"Particles added at t={t}: {particles_added[name]} for {name}")
            #    injected_particles = particles_added[name]
            
            #guessing that all the particles from the previous timestep are still there, but are just older
            """
            guess_count = defaultdict(int)  # {(injectionId, age): count}
            for (inj_id, age), count in previous_counts[name].items():
                new_age = round(age + dt, 3)  # Increment age by dt
                #guess_count[(inj_id, new_age)] += count
                guess_count[(inj_id, new_age)] = count
            
            for (inj_id, age), prev_count in guess_count.items():
                curr_counts = current_counts[name].get((inj_id, age), 0)
                if curr_counts == 0:
                    # Particles from (inj_id, age) disappeared
                    disappeared_count = prev_count
                    exit_records[name].append((round(t-dt,3), inj_id, round(age-dt, 3), disappeared_count))
                    log(f"At t={round(t-dt,3)}, {disappeared_count} particles from {name} with InjectionStepId {inj_id} and age {round(age-dt,2)} exited.")

                elif curr_counts < prev_count:
                    # Particles from (inj_id, age) exited
                    lost_count = prev_count - curr_counts
                    lost_age = round(age - dt, 3) # Decrement age by dt
                    lost_time = round(t - dt,3)  # Time of loss
                    exit_records[name].append((lost_time, inj_id, lost_age, lost_count))
                    log(f"At t={lost_time}, {lost_count} particles from {name} with InjectionStepId {inj_id} and age {lost_age:.3f} went out of the domain.")

            """

            guess_count = defaultdict(int)
            for (inj_id, age), count in previous_counts[name].items():
                new_age = round(age + dt, 3)
                guess_count[(inj_id, new_age)] = count

            for (inj_id, age), expected_count in guess_count.items():
                actual_count = current_counts[name].get((inj_id, age), 0)
                exited = expected_count - actual_count
                if exited > 0:
                    exit_records[name].append((round(t-dt,3), inj_id, round(age-dt,3), exited))  # InjectionStepId, time, num exited



                # Detect newly injected particles (not present in guess_count)
            for (inj_id, age), curr_count in current_counts[name].items():
                if (inj_id, age) not in guess_count:
                    # New particles injected
                    log(f"At t={t}, {curr_count} new particles injected from {name} with InjectionStepId {inj_id}, age {age:.3f}")



        # Update previous_counts for the next timestep
        previous_counts[name] = current_counts[name].copy()
log(f"exit_records: {exit_records}")
# Save results to CSV

for i in range(5):
    output_file = os.path.join(cwd, f"particle_age_stats_{i}.csv")
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["Current time", "Time of Injection", "Particle age", "# of exited particles"])
        for time, inj_id, age, count in exit_records[f'ParticleTracer_{i}']:
            injection_time = round(inj_id * 0.001, 4)
            current_time = round(time * 0.01, 4)
            particle_age = round(age * 0.01, 4)
            writer.writerow([current_time, injection_time, particle_age, count])
    log(f"CSV saved at: {os.path.abspath(output_file)}")


log_file.close()
