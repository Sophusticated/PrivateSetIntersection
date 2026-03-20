import numpy as np
from scipy.interpolate import lagrange
import galois


def lagrange_basis_coeffs(x_points, j):
    """
    Returns the coefficients of the j-th Lagrange basis polynomial,
    from lowest degree to highest (numpy convention).
    """
    x_points = np.array(x_points, dtype=int)
    x_j = x_points[j]

    # Start with the polynomial "1"
    poly = np.array([1.0])

    for k, x_k in enumerate(x_points):
        if k != j:
            # Multiply by (x - x_k) / (x_j - x_k)
            # (x - x_k) as a polynomial is [-x_k, 1] in low-to-high convention
            linear_factor = np.array([-x_k, 1.0]) / (x_j - x_k) #deg 1 polynomial divided by scalar
            poly = np.polymul(poly, linear_factor)  # np.polymul uses high-to-low!

    return poly


def all_basis_coeffs(x_points):
    return [lagrange_basis_coeffs(x_points, j) for j in range(len(x_points))]

def lagrange_interpolate(x_points, y_points):
    """
    Returns the coefficients of the interpolating polynomial
    passing through all (x_j, y_j) pairs.
    """
    x_points = np.array(x_points, dtype=float)
    y_points = np.array(y_points, dtype=float)
    n = len(x_points)

    # Accumulate y_j * L_j into a single polynomial
    # degree is n-1
    result = np.zeros(n)  # n coefficients for a degree-(n-1) polynomial

    for j in range(n):
        L_j = lagrange_basis_coeffs(x_points, j)
        
        L_j_padded = np.zeros(n)
        L_j_padded[n - len(L_j):] = L_j
        result += y_points[j] * L_j_padded

    return result

x_points = [0, 1, 2]
y_points = [1, 3, 2]

print(lagrange_interpolate(x_points, y_points))
print( lagrange(x_points, y_points))

def interpolate(xvals, yvals, exp = 16):
    GF = galois.GF(2**exp)
    print(GF.properties)
    #makes a polynomial with coefficients in GF(2)

interpolate([1,2], [3,4])
