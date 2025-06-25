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
#A_tot=0.235206+0.199269+0.973772+0.939913
#A_tot=0.939913+0.720489+0.973772+0.686628 
A_tot=1
A_half=0.5
#PC-MRI RCR verdier
#print("left internal illiac =", splitRCR(0.03429282733222398, 5.108978119022028, 0.5773753496227657, 0.686628, A_tot))
#print("right internal illiac =", splitRCR(0.03429282733222398, 5.108978119022028, 0.5773753496227657, 0.720489, A_tot))
#print("left external illiac =", splitRCR(0.03429282733222398, 5.108978119022028, 0.5773753496227657, 0.973772, A_tot))
#print("right external illiac =", splitRCR(0.03429282733222398, 5.108978119022028, 0.5773753496227657, 0.939913, A_tot))

#Metode 2 RCR verdier
#print("left internal illiac =", splitRCR(0.053995125013154295, 4.062573166369919, 0.438606486782754, 0.686628, A_tot))
##print("right internal illiac =", splitRCR(0.053995125013154295, 4.062573166369919, 0.438606486782754, 0.720489, A_tot))
#print("left external illiac =", splitRCR(0.053995125013154295, 4.062573166369919, 0.438606486782754, 0.973772, A_tot))
#print("right external illiac =", splitRCR(0.053995125013154295, 4.062573166369919, 0.438606486782754, 0.939913, A_tot))
print("iliac =", splitRCR(0.055265723911421434, 3.9741762385005903, 0.7024630073429903, A_half, A_tot))