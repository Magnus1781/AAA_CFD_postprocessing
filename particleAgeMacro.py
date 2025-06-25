# Import necessary ParaView and Python modules
from paraview.simple import *
import csv
import os
import numpy as np
from collections import defaultdict

import matplotlib.pyplot as plt

# Load the particle tracer output
particle_tracer = FindSource("ParticleTracer1")


################Logging setup####################
# Get the directory where the particle tracer's data is stored
cwd = r"C:\Users\magnuswe\OneDrive - SINTEF\Simvascular\results\two_last_cycles\AAA004_sim_0-15_1-3mill-two_last_cycles"

# Create the new log file in cwd
particle_creation_log_file_path = os.path.join(cwd, "particle_creation_log.txt")
particle_creation_log_file = open(particle_creation_log_file_path, "w")

# Set up the output file and log file paths
output_file = os.path.join(cwd, "particle_age_stats.csv")
log_file_path = os.path.join(cwd, "particle_log.txt")
log_file = open(log_file_path, "w")

def log(msg):
    log_file.write(msg + "\n")
    log_file.flush()


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



# Track active particles per (injectionId, age) at each timestep
active_particles = defaultdict(int)  # {(injectionId, age): count}
exit_records = []

total_previous_count = 0  # Total number of particles at the previous timestep
# Initialize the active particles counter
previous_counts = defaultdict(int)  # {(injectionId, age): count}
first_time_step = True  # Flag to skip exit comparison on the first timestep with particles
for t in fine_timesteps:
    scene.AnimationTime = float(t)
    Render()
    log(f"Fetching data at t={t:.3f}")
    data = servermanager.Fetch(particle_tracer)
    

    # Get arrays
    points = data.GetPoints()
    numPts = points.GetNumberOfPoints()
    ages = data.GetPointData().GetArray("ParticleAge")
    injections = data.GetPointData().GetArray("InjectionStepId")
    
    if points is None or points.GetNumberOfPoints() == 0:
        continue


    # Track particles by (InjectionStepId, Age) as key
    current_counts = defaultdict(int)
    total_current_count = 0  # Total number of particles at the current timestep

    for i in range(numPts):
        inj_id = injections.GetValue(i)
        if inj_id > 940:
            continue  # Skip tracking this injection ID
        age = round(ages.GetValue(i), 3) # Round to 3 decimal places to avoid floating point issues
        current_counts[(inj_id, age)] += 1
        total_current_count +=1
    log(f"Total particles at t={t:.3f}: {total_current_count}")

    if first_time_step:
        # On the first frame with particles, initialize previous_counts with current_counts
        previous_counts = current_counts.copy()
        first_time_step = False
        particles_added = total_current_count
    
    
    # Compare with previous timestep to detect disappearances
    else:
        injected_particles = 0  # Reset particles added for this timestep
        if int(t / dt) % 10 == 0:
            log(f"Particles added at t={t:.3f}: {particles_added}")
            injected_particles = particles_added
        
        guess_count = defaultdict(int)  # {(injectionId, age): count}
        for (inj_id, age), count in previous_counts.items():
            new_age = round(age + dt, 2)  # Increment age by dt
            guess_count[(inj_id, new_age)] += count
        
        for (inj_id, age), prev_count in guess_count.items():
            curr_counts = current_counts.get((inj_id, age), 0)
            if curr_counts == 0:
                # Particles from (inj_id, age) disappeared
                disappeared_count = prev_count
                exit_records.append((t, inj_id, round(age-dt, 2), disappeared_count))
                log(f"At t={round(t-dt,2)}, {disappeared_count} particles from InjectionStepId {inj_id} with age {round(age-dt,2)} exited.")

            elif curr_counts < prev_count:
                # Particles from (inj_id, age) exited
                lost_count = prev_count - curr_counts
                lost_age = round(age - dt, 2) # Decrement age by dt
                lost_time = round(t - dt,2)  # Time of loss
                exit_records.append((round(t, 2), inj_id, lost_age, lost_count))
                log(f"At t={lost_time}, {lost_count} particles from InjectionStepId {inj_id} with age {lost_age:.3f} exited.")


        # Detect newly injected particles (not present in guess_count)
        for (inj_id, age), curr_count in current_counts.items():
            if (inj_id, age) not in guess_count:
                # New particles injected
                log(f"At t={t:.3f}, {curr_count} new particles injected with InjectionStepId {inj_id}, age {age:.3f}")



    # Update previous_counts for the next timestep
    previous_counts = current_counts.copy()
log(f"exit_records: {exit_records}")
# Save results to CSV
with open(output_file, "w", newline="") as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerow(["Current time", "Time of Injection", "Particle age", "# of exited particles"])
    for time, inj_id, age, count in exit_records:
        injection_time = round(inj_id * 0.001, 3)
        current_time = round(time * 0.01, 3)
        particle_age = round(age * 0.01, 3)
        writer.writerow([current_time, injection_time, particle_age, count])


log(f"CSV saved at: {os.path.abspath(output_file)}")
log_file.close()
