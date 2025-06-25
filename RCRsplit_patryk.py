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
    R_conv = 1 #No conversion needed with Simvascular guidelines method
    C_conv = 1

    # Calculate Rpi, Ci, and Rdi
    Rpi = ((A_tot / Ai) * Rp) * R_conv
    Ci = ((Ai / A_tot) * C) * C_conv
    Rdi = ((A_tot / Ai) * Rd) * R_conv

    return Rpi, Ci, Rdi

Pmean=125000 #dyn/cm^2
Q=80 #ml/s

Rtot=Pmean/Q #=1562,5

Rd=0.91*Rtot
Rp=0.09*Rtot
C=0.001 #starting guess
left_illiac_area = 2
right_illiac_area = 2
left_renal_area = 1
right_renal_area = 1

A_tot=left_illiac_area+right_illiac_area+left_renal_area+right_renal_area   


print("left illiac =", splitRCR(Rp, C, Rd, left_illiac_area, A_tot))
print("right illiac =", splitRCR(Rp, C, Rd, right_illiac_area, A_tot))
print("left renal =", splitRCR(Rp, C, Rd, left_renal_area, A_tot))
print("right renal =", splitRCR(Rp, C, Rd, right_renal_area, A_tot))
