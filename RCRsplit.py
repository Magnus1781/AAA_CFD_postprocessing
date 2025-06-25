def splitRCR(Rp, C, Rd, Ai, A_tot):
    """
    Function to calculate Rpi, Ci, and Rdi based on the given inputs.
    
    Args:
        Rp (float): Resistance Rp
        C (float): Capacitance C
        Rd (float): Resistance Rd
        Ai (float): Area Ai
        A_tot (float): Total area A_tot
    
    Returns:
        tuple: Rpi, Ci, Rdi
    """
    # Conversion factors for cgs units
    R_conv = 1e04
    C_conv = 1e-04

    # Calculate Rpi, Ci, and Rdi
    Rpi = ((A_tot / Ai) * Rp) * R_conv
    Ci = ((Ai / A_tot) * C) * C_conv
    Rdi = ((A_tot / Ai) * Rd) * R_conv

    return Rpi, Ci, Rdi


#left internal illiac = 0.235206
#right internal illiac = 0.199269
#left external illiac = 0.973772
#right external illiac = 0.939913
A_tot=1
A_half=0.5
print(A_tot)
print("left internal illiac =", splitRCR(0.03429281445153486, 5.108983915251614, 0.5773750266606054, 0.235206, A_tot))
print("right internal illiac =", splitRCR(0.03429281445153486, 5.108983915251614, 0.5773750266606054, 0.199269, A_tot))
print("left external illiac =", splitRCR(0.03429281445153486, 5.108983915251614, 0.5773750266606054, 0.973772, 2.34816))
print("right external illiac =", splitRCR(0.03429281445153486, 5.108983915251614, 0.5773750266606054, 0.939913, 2.34816))
