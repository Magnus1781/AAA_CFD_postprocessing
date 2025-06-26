"""

@authors: Menno

@Note:
Magnus Wennemo implemented for-loops for iterating the initial guesses

"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy as sp

# Parameters
file_name = "inlet_velocity_profile_half.csv" 
n_rows = 51  # Number of rows in the flow file
p_dia_mmHg = 80  # Diastolic blood pressure in mmHg
p_syst_mmHg = 120  # Systolic blood pressure in mmHg

#Initial guesses
Z_guesses = np.array([0.04, 0.06, 0.08, 0.1])
C_guesses = np.array([7, 8, 9, 10]) # [3, 3.5, 4, 4.5]
R_guesses = np.array([0.2, 0.3, 0.4, 0.5])
#offset_guesses = np.array([200, 400, 600, 800]) Denne er valgfri, sparer tid med konstant offset
offset_guesses = np.array([700])

#parameters: 0.052823509215410354, 9.999983214198243, 257513.48840526844, 1333.2175838037901
#Havner på 3725 med alle andre med cgs flow fila

#parameters: 0.03032481870250859, 9.999975709090924, 299235.13456480857, 1333.2192927203519
#Havner på 5863 med IR average data fila





# scaled_inlet_cgs_2 belongs to aortafemoral 2 (latest version in cgs units, scaled by -1!!!! for SV)
inflow_data = pd.read_csv(file_name, delim_whitespace=True)

flow_rate = inflow_data.flow_rate.values*(-1) # convert from cm^3/sec to mm^3/sec and make positive
print(flow_rate)


# creating Q(t) for 0 <= t <= T based on inflow profile -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# The .loc method in Pandas allows you to access rows and columns by labels or index positions.
# [112, 'time'] specifies that you want to access the cell in row 112 (the 113th row, as indexing starts from 0) of the column 'time'.


T=inflow_data.loc[n_rows-1, 'time'] # final time 
time_base = inflow_data.time.values[:-1] # remove final value because we will chain many time cycles together
print(T)
time = time_base
time = np.append(time, time_base + T)
time_extended = np.append(time, T+T)


flow_rate_extended = np.append(np.tile(flow_rate[:-1], 2), flow_rate[-1]) # T+1 same as for extended time

print(inflow_data.columns)

# create the continuous function for Q ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Q = sp.interpolate.interp1d(time_extended, flow_rate_extended, kind = "cubic", bounds_error = True)

# determine derivative of Q 
x, dx = np.linspace(time_extended[0], T+T, 100001, retstep = True) # just a big number for smooth data for interp1d. T+1 same as for extended time

# create discrete but very fine function for the gradient of Q
dQarray = np.gradient(Q(x), dx, edge_order=2)

# create the continuous function for the derivative of Q
dQ = sp.interpolate.interp1d(x, dQarray, kind = "cubic", bounds_error = True)

# solving the DE --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# system of equations
def system(p, t, Z, C, R, Q, dQ, A):
    # pressure, time, resistance p, capacitance, resistance d, flow rate, flow rate derivative, relative area of leg
    
    dpdt = -p/(R*C) + A*Q(t)/C *(1 + Z/R) + A*Z*dQ(t)
    
    # # if distal pressure pd is not 0. Not sure if it matters
    # pd = 50*133.322 # 10 mmHg
    # dpdt = (pd-p)/(R*C) + A*Q(t)/C *(1 + Z/R) + A*Z*dQ(t)
    
    return dpdt

# initial pressure, time array


# må endre her til cgs enheter, diastolisk trykk  
#p0 = [78*1333.22] # initial condition, in DYNE/CM^2
p0=[p_dia_mmHg*133.322] #units in Pa
t = np.linspace(time_extended[0], T, int(1e4 + 1))



A = 1
# Pressure values 
p_to_dyne= 1333.22
p_to_pascal=133.322  # Convert to original values in the script 
p_dia_pascal=p_dia_mmHg * p_to_pascal
p_syst_pascal=p_syst_mmHg * p_to_pascal
iteration=0
error=999
# solving the DE and Z, C, R --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def minimisation_function(params, T, Q, dQ, A):
    global iteration, error
    iteration+=1
    # In dyne/cm^2 
    ideal_mean = (p_dia_pascal*2 + p_syst_pascal)/3 
    
    Z, C, R, offset = params
    
    p0 = [p_dia_pascal + offset] # initial condition, in pascal = gr/mm/s^2
    t = np.linspace(time_extended[0], T, int(1e4 + 1))
    p = sp.integrate.odeint(system, p0, t, args = (Z, C, R, Q, dQ, A, ))
    
   
    t = t[int(len(p)*(T-T)/(T)):]#int(len(p)*(T-1)/(T-1))] # take only part of the solution where we have nice periodicity
    p = p[int(len(p)*(T-T)/(T)):]#int(len(p)*(T-1)/(T-1))] # take only part of the solution where we have nice periodicity
    

    error = np.sqrt((min(p) - p_dia_pascal)**2 
                    + (np.mean(p) - ideal_mean)**2
                    + (max(p) - min(p) - (p_syst_pascal - p_dia_pascal))**2 # fix distance between diastole and systole 
                    #and let offset figure out the exact height
                    + (p[0] - p[-1])**2) # this last one makes sure the cycle is periodic because the pressure at
                    # the end should be the same as at the beginning of a cycle. maybe by using this we can get 
                    # away with solving the DE for less cycles
    print(f'error : {error} iteration: {iteration}')
    return error 

# for usual operation for stents ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
   
try_number=0
results_dict = {}
# Assuming initial guess is in the order: Rp, C, Rd. spm: hva faen burde offset være 

res = None
for i in Z_guesses:
    for j in C_guesses:
        for k in R_guesses:
            for l in offset_guesses:
                initial_guess=[i, j, k, l]
                try_number+=1
                iteration=0
                res = sp.optimize.minimize(minimisation_function, initial_guess, args = (T, Q, dQ, A, ),
                            bounds = [(0.01, 30000), (0.0000001, 10), (0.1, 300000), (-10*133.322, 10*133.322)],
                            tol = 1e-12,
                            options = {'disp' : False, 'maxiter' : 1e6},
                            method = 'Powell'
                            )
                print(f'Z: {i}, C: {j}, R: {k}, offset: {l}, try number: {try_number}')
                print(f'error: {error}')
                print(f'parameters: {res.x[0]}, {res.x[1]}, {res.x[2]}, {res.x[3]}')
                print('starting pressure:', p_dia_pascal + res.x[3])
                print('---------------------------------------------------------------------------------------------------------------------------')
                
                # Create a dictionary to store the results
                
                results_dict[try_number] = {
                    'Z': i,
                    'C': j,
                    'R': k,
                    'offset': l,
                    'error': error,
                    'iteration': iteration
                }

                print(results_dict)
                if error < 1:
                    break
            if error < 1:
                break
        if error < 1:
            break
    if error < 1:
        break

"""
#initial_guess = [0.15, 1.02, 3.4, 50]
#initial_guess = [0.06, 2.7, 1.3, 84]
res = sp.optimize.minimize(minimisation_function, initial_guess, args = (T, Q, dQ, A, ),
                           bounds = [(0, 50), (0, 10), (0, 500), (-10*133.322, 10*133.322)],
                           tol = 1e-12,
                           options = {'disp' : False, 'maxiter' : 1e10},
                           method = 'Powell'
                           )
"""
Z, C, R, offset = res.x




print(f'aorta parameters: {res.x[0]}, {res.x[1]}, {res.x[2]}, {offset}')
print('starting pressure:', p_dia_pascal + offset)



# plotting --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

p0 = [p_dia_pascal + offset] # initial condition, in pascal = gr/mm/s^2
t = np.linspace(time_extended[0], T, int(1e4 + 1))
p = sp.integrate.odeint(system, p0, t, args = (Z, C, R, Q, dQ, A, ))

plt.figure()
plt.xlabel("time (s)")
plt.ylabel("Pressure (mmHg)")
plt.plot(t, p)
plt.show()

