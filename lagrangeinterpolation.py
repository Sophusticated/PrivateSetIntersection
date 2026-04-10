import galois

def galois_basis_coeffs(x_points, j, exp):
    GF = galois.GF(2**exp, irreducible_poly=galois.irreducible_poly(2, 128))
    x_points =  GF(x_points)
    x_j = GF(x_points[j])
    poly = galois.Poly([1], field=GF)
    for k, x_k in enumerate(x_points):
        if k != j:
            linear_factor = galois.Poly([1, x_k], field=GF) // (x_j + x_k) # Slightly sus to do floor division? idk but "true division not implemented"
            poly = poly * linear_factor
    return poly 

def interpolate(x_points, y_points, exp):
    GF = galois.GF(2**exp, irreducible_poly=galois.irreducible_poly(2, 128))
    x_points = GF(x_points)
    y_points = GF(y_points)
    
    result = galois.Poly([0], field=GF) #result should be a poly with additive identity element.
    
    for j, y_j in enumerate(y_points):
        basis = galois_basis_coeffs(x_points, j, exp)
        result = result + basis * y_j

    for xi, yi in zip(x_points, y_points):
        assert result(xi) == yi, "ruh roh, it doesn't evaluate to the right value"
    return result

