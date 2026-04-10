"""
R.<X> = GF(2)[]

for p in R.polynomials(of_degree=256):
    if p.is_irreducible():
        print('\u0007')
        print(p)
        if p.is_primitive():
            print("Primitive.")
            break
        else:
            print("Not primitive")
    print('.', end='')
"""
