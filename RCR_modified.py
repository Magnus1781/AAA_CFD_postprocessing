import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy as sp

#inflow_data = pd.read_csv("scaled_inlet_cgs.csv", delim_whitespace=True) # i added a time 0.21 which was missing. It's value is the same as 0.2; did the same for 0.57

#inflow_data = pd.read_csv("scaled_inlet_cgs.csv", sep='\s+')

# scaled_inlet_cgs_2 belongs to aortafemoral 2 (latest version in cgs units, scaled by -1!!!! for SV)
inflow_data = pd.read_csv("negative_IR_flow_average_data.txt", delim_whitespace=True)
# Tester ut i originale enheter !!!
flow_rate = inflow_data.flow_rate.values*(-1000) # convert to mm^3/sec
print(inflow_data)
#0.05526570261478228, 3.974149567713768, 0.7024640806759403, 268.13143354512073 For negative_IR_flow_average_data.txt
0.055265723911421434, 3.9741762385005903, 0.7024630073429903, 268.13349740496096

# creating Q(t) for 0 <= t <= T based on inflow profile -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# The .loc method in Pandas allows you to access rows and columns by labels or index positions.
# [112, 'time'] specifies that you want to access the cell in row 112 (the 113th row, as indexing starts from 0) of the column 'time'.
n_rows=24

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
p0=[84.4*133.22] #units in Pa
t = np.linspace(time_extended[0], T, int(1e4 + 1))



A = 1

# Pressure values 
p_to_dyne= 1333.22
p_to_pascal=133.22  # Convert to original values in the script 
p_dia=84.4 * p_to_pascal #78
p_syst=143 * p_to_pascal #117

# solving the DE and Z, C, R --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def minimisation_function(params, T, Q, dQ, A):

    # In dyne/cm^2 
    ideal_mean = (p_dia*2 + p_syst)/3 
    
    Z, C, R, offset = params
    
    p0 = [p_dia + offset] # initial condition, in pascal = gr/mm/s^2
    t = np.linspace(time_extended[0], T, int(1e4 + 1))
    p = sp.integrate.odeint(system, p0, t, args = (Z, C, R, Q, dQ, A, ))
    
   
    t = t[int(len(p)*(T-T)/(T)):]#int(len(p)*(T-1)/(T-1))] # take only part of the solution where we have nice periodicity
    p = p[int(len(p)*(T-T)/(T)):]#int(len(p)*(T-1)/(T-1))] # take only part of the solution where we have nice periodicity
    

    error = np.sqrt((min(p) - p_dia)**2 
                    + (np.mean(p) - ideal_mean)**2
                    + (max(p) - min(p) - (p_syst - p_dia))**2 # fix distance between diastole and systole 
                    #and let offset figure out the exact height
                    + (p[0] - p[-1])**2) # this last one makes sure the cycle is periodic because the pressure at
                    # the end should be the same as at the beginning of a cycle. maybe by using this we can get 
                    # away with solving the DE for less cycles
    print(f'error : {error}')
    return error 

# for usual operation for stents ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Using parameters from Eirini, converting to CGS (multiply R by 10000 and devide C by 10000)
#initial_guess = [13000, 0.000015 , 130000, 120] # parameters from Eirini
#initial_guess = [1502.5086473910784, 0.0009999985377034724, 29464.261198606496, 100] # parameters from Eirini
#initial_guess = [15025.089, 0.00009999985377034724, 150000, 110] --> 4821 final error 
#initial_guess = [32300000, 0.0000000743, 327000000, 110]  
R_scale=1e04
C_scale=1e-04

# Trying Karens parameters, convert to cgs
#initial_guess = [0.03795357217738048, 4.742737432896731, 1.240740022234062, 149.55477703519804]
#initial_guess = [0.03795357217738048, 4.742737432896731, 1.240740022234062, 150.55477703519804]    
initial_guess = [12, 13, 30, 300] 

# Assuming initial guess is in the order: Rp, C, Rd. spm: hva faen burde offset være 
print(p0)
res = sp.optimize.minimize(minimisation_function, initial_guess, args = (T, Q, dQ, A, ),
                            bounds = [(0.01, 30000), (0.0000001, 10), (0.1, 300000), (-10*133.322, 10*133.322)],
                            tol = 1e-12,
                            options = {'disp' : False, 'maxiter' : 1e6},
                            method = 'Powell'
                            )
print(p0)
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



def split(Ai, A_tot, Z,C,R):
    Zi = (A_tot/Ai)*Z
    Ci = (Ai/A_tot)*C
    Ri = (A_tot/Ai)*R
    return Zi, Ci, Ri

A_scale=100
#Patient 1.1:
A_r_ext_iliac= 1 #0.939913*A_scale
A_r_int_iliac= 1 # 0.720489*A_scale
A_l_ext_iliac= 1 #0.973772*A_scale
A_l_int_iliac= 1 #0.686628*A_scale

A_tot = 1 #A_r_ext_iliac + A_r_int_iliac + A_l_ext_iliac + A_l_int_iliac

# RCR, right external iliac 
RCR_extIlR = split(A_r_ext_iliac, A_tot, res.x[0], res.x[1],res.x[2])

# RCR left external iliac 
RCR_extIlL = split(A_l_ext_iliac, A_tot, res.x[0], res.x[1],res.x[2])

# RCR right internal iliac 
RCR_intIlR = split(A_r_int_iliac, A_tot, res.x[0], res.x[1],res.x[2])

# RCR left internal 
RCR_intIlL = split(A_l_int_iliac, A_tot, res.x[0], res.x[1],res.x[2])
#p_dia = p_dia

print(f'aorta parameters: {res.x[0]}, {res.x[1]}, {res.x[2]}, {offset}')
print(f'iliac ext right parameters: {RCR_extIlR}')
print(f'iliac ext left parameters: {RCR_extIlL}')
print(f'iliac int right parameters: {RCR_intIlR}')
print(f'iliac int left parameters: {RCR_intIlL}')
print('starting pressure:', p_dia + offset)



# plotting --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

p0 = [p_dia + offset] # initial condition, in pascal = gr/mm/s^2
t = np.linspace(time_extended[0], T, int(1e4 + 1))
p = sp.integrate.odeint(system, p0, t, args = (Z, C, R, Q, dQ, A, ))

plt.figure()
plt.xlabel("time (s)")
plt.ylabel("Pressure (mmHg)")
plt.plot(t, p)
plt.show()

