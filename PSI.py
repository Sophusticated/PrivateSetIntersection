import random
import hashlib
from lagrangeinterpolation import interpolate
import galois
from itertools import permutations
import random

exp = 64
GF = galois.GF(2**exp)

#Sender set X:
X = {12, 14, 2, 4}
#Receiver set Y:
Y = {8, 10, 12, 14}

#Choose l1 and L2 from kappa and lambda and n
#TODO: There is no conway poly for 128?
L1 = 64
L2 = 64

#use SHA 256 and truncate output to become a field value
def H1(number):
    digest = hashlib.sha256(str(number).encode()).digest()
    bit_string = format(int.from_bytes(digest, byteorder='big'), '0256b')
    return bit_string[:L1]

def H2(number):
    digest = hashlib.sha256(str(number).encode()).digest()
    bit_string = format(int.from_bytes(digest, byteorder='big'), '0256b')
    return bit_string[L1:L1+L2] #eg. from 64 to 128



#Sender inputs random bit string of length l1
Snum = random.randint(0,2**L1)
Sinput = format(Snum, f'0{L1}b')
print(Snum, Sinput)
#receiver inputs D = Enc({(y, H1(y)) | y in Y}) here H1 maps from values to l1 amount of values


#Here we hash y, and since we truncate to L1 bits, we have {0,1}^* -> {0,1}^L1
RinputXVals = list(Y)
RinputYVals = [(int(H1(y), 2)) for y in Y]
#So here receiver is actually generating random values (y values in a coordinate) to put as points.
D = interpolate(RinputXVals, RinputYVals, exp)
#Now D is a polynomial, which acts as an OKVS

#Magical VOLE gives Q to sender, and R to receiver

def totallyLegitSuperObliviousVole(D: galois.Poly, s):
    sFieldElement = GF(int(s, 2))
    coeffList = D.coeffs
    Q = []
    R = []
    for i in range(0, len(coeffList)):
        ri = GF(i+1) #Here we choose a value for r. We do +1 because if 0 is included then R does not have enough coefficients for the checker
        #It is a little sketchy because it should also work for 0, but then we would have to change the volechecker so it's no big eal 
        R.append(ri)
        qi = ri + coeffList[i] * sFieldElement
        Q.append(qi)
    return galois.Poly(Q, field=GF), galois.Poly(R, field=GF)

Q, R = totallyLegitSuperObliviousVole(D, Sinput)


def Send(X, Q, s):
    sFieldElement = GF(int(s, 2))
    M = [] #using list instead of set bc of nice permute function from random
    for x in X:
        #TODO: should we change the hash function so it just returns an int? In the protocol it outputs bitstrings but we never use that anyway
        #TODO: does this stay true to the protocol? We are adding them instead of using strings.
        #previous bugged code was mi = int(Q(x) + GF(int(H1(x), 2) * sFieldElement)), where the right term became 0
        mi = H2(x + int(Q(x) + GF(int(H1(x), 2)) * sFieldElement)) 
        M.append(mi)
    return random.sample(M, len(M)) #gives permutation


M = Send(X, Q, Sinput)
print(M)

def receiverOutput(R, Y):
    outPutList = []
    for y in Y:
        test = H2(y + int(R(y)))
        if test in M:
            outPutList.append(y)
    return outPutList

print(f'The set intersection consists of elements: {receiverOutput(R,Y)}')

#So sender wants to find the "y" value of Q at a certain point, they can sum all the
#terms, which in a polynomial are sum(Qi*Ax,i) where 
#TODO: why do we write Ax,i instead of just x^i?


#TODO: Ok so I suppose GFs work so that in GF(2^n) there are n elements, and they have some ordering. So in 2^4, the highest element is 3, but it's not actually 3,
#because it's x^2 + x + 1. So we can't plot it so easily.

def voleChecker(Q, D, s, R):
    """
    Ri = Qi + s*Di
    """
    sFieldElement = GF(int(s, 2))
    Dcoeffs = D.coeffs
    Qcoeffs = Q.coeffs
    Rcoeffs = R.coeffs
    for i in range(len(Rcoeffs)):
        Ri = Rcoeffs[i]
        assert Qcoeffs[i] == Ri - Dcoeffs[i] * sFieldElement #Switched to minus here just for aura points
        assert Ri == Qcoeffs[i] - Dcoeffs[i] * sFieldElement #equivalent

voleChecker(Q, D, Sinput, R)

#TODO: Why does this work? Can the receiver not just spam different outputs and basically lie about it's input set?
