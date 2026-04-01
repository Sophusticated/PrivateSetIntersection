import random
import hashlib
from lagrangeinterpolation import interpolate
import galois
from itertools import permutations
#Sender set X:
X = {12, 14, 2, 4}
#Receiver set Y:
Y = {8, 10, 12, 14}

#Choose l1 and L2 from kappa and lambda and n
#TODO: There is no conway poly for 128?
L1 = 64
L2 = 64

#use SHA 256 and truncate output to become a field value
def Hl1(number, l):
    digest = hashlib.sha256(str(number).encode()).digest()
    bit_string = format(int.from_bytes(digest, byteorder='big'), '0256b')
    return bit_string[:l]

def Hl2(number, l2):
    digest = hashlib.sha256(str(number).encode()).digest()
    bit_string = format(int.from_bytes(digest, byteorder='big'), '0256b')
    return bit_string[l2:]


#Sender inputs random bit string of length l1
Snum = random.randint(0,2**L1)
Sinput = format(Snum, f'0{L1}b')
print(Snum, Sinput)
#receiver inputs D = Enc({(y, H1(y)) | y in Y}) here H1 maps from values to l1 amount of values


#Here we hash y, and since we truncate to L1 bits, we have {0,1}^* -> {0,1}^L1
RinputXVals = list(Y)
RinputYVals = [(int(Hl1(y,L1), 2)) for y in Y]
#So here receiver is actually generating random values (y values in a coordinate) to put as points.
D = interpolate(RinputXVals, RinputYVals, exp=L1)
#Now D is a polynomial, which acts as an OKVS

#Magical VOLE gives Q to sender, and R to receiver

def totallyLegitSuperObliviousVole(D: galois.Poly, s, exp = 64):
    GF = galois.GF(2**exp)
    sFieldElement = GF(int(s, 2))
    coeffList = D.coeffs
    Q = []
    R = []
    for i in range(len(coeffList)):
        ri = GF(i) #just renaming for clarity that I am just choosing ri
        R.append(ri)
        qi = ri + coeffList[i] * sFieldElement
        Q.append(qi)
    return galois.Poly(Q, field=GF), galois.Poly(R, field=GF)

Q, R = totallyLegitSuperObliviousVole(D, Sinput)


def voleChecker(Q, D, s, R, exp = 64):
    GF = galois.GF(2**exp)
    sFieldElement = GF(int(s, 2))
    Dcoeffs = D.coeffs
    Qcoeffs = Q.coeffs
    Rcoeffs = R.coeffs
    for i in range(len(Rcoeffs)):
        Ri = GF(Rcoeffs[i])
        assert Qcoeffs[i] == Ri - Dcoeffs[i] * sFieldElement #Switched to minus here just for aura points

#R = [i for i in range(len(Q.coeffs))] #create an R just so my volechecker also works if I get real vole one day
voleChecker(Q, D, Sinput, R)


#Here both Q and R are binary strings, and each element is a coefficient
#Q = R xor D*s  
#So Ri = Qi + s*Di
#So sender wants to find the "y" value of Q at a certain point, they can sum all the
#terms, which in a polynomial are sum(Qi*Ax,i) where 
#TODO: why do we write Ax,i instead of just x^i?

#So the process is:
#S finds Dec(Q,x) for a given x by summing over Q*x^i
#S xors that with s* the hashed value of x, using the same hash function, it cancels out
#.. if they give the same value
#Now s compares that mod2 sum with 
#TODO: aren't we just comparing Dec(Q,x) xor something with Dec(Q,x) xor same thing?
#answer: R has to send some additional info directly to S so that S can compare

#Simple case:
#I think R sends the polynomial which does not contain any info except that you can evaluate it at different points
#So I can evalueate it at x, then XOR that from the Value, and if that gives me the same as when i
#XOR the s value times the hashed x value, then it means that I hit the same X value.
#Still not safe to spam attacks where I try everything

#More complicated case:
 

#Either pad to get H2 or just choose different digits


#TODO: Ok so I suppose GFs work so that in GF(2^n) there are n elements, and they have some ordering. So in 2^4, the highest element is 3, but it's not actually 3,
#because it's x^2 + x + 1. So we can't plot it so easily.