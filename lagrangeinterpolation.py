import galois

def galois_basis_coeffs(x_points, j, exp):
    GF = galois.GF(2**exp)
    x_points =  GF(x_points)
    x_j = GF(x_points[j])
    poly = galois.Poly([1], field=GF)
    for k, x_k in enumerate(x_points):
        if k != j:
            linear_factor = galois.Poly([1, x_k], field=GF) // (x_j + x_k) # Slightly sus to round down? idk but "true division not implemented"
            poly = poly * linear_factor
    return poly 

def interpolate(x_points, y_points, exp = 2):
    GF = galois.GF(2**exp)
    x_points = GF(x_points)
    y_points = GF(y_points)
    
    result = galois.Poly([0], field=GF) #result should be a poly with additive identity element.
    
    for j, y_j in enumerate(y_points):
        basis = galois_basis_coeffs(x_points, j, exp)
        result = result + basis * y_j

    for xi, yi in zip(x_points, y_points):
        assert result(xi) == yi, "ruh roh, it doesn't evaluate to the right value"
    return result

print("The polynomial is " + str(interpolate([0,1,2], [1,3,2])))

def check_basis_coeffs(x_points, ext_exp):
    GF = galois.GF(2**ext_exp)
    x_points = GF(x_points)
    for j in range(len(x_points)):
        poly = galois_basis_coeffs(x_points, j, ext_exp)
        for i, xi in enumerate(x_points):
            val = poly(xi)
            expected = GF(1) if i == j else GF(0)
            assert val == expected, f"L_{j}({xi}) = {val}, expected {expected}"
    print("All basis polynomials check out!")

check_basis_coeffs([1,2],2)
