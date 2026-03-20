import numpy as np
from scipy.interpolate import lagrange
import galois
def interpolate(xvals, yvals, exp = 16):
    GF = galois.GF(2**exp)
    print(GF.properties)
    #makes a polynomial with coefficients in GF(2)

interpolate(1,2)
