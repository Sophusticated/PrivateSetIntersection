import random
import hashlib
from lagrangeinterpolation import interpolate
import galois
import random

exp = 128
print(galois.irreducible_poly(2, exp))
GF = galois.GF(2**exp, irreducible_poly=galois.irreducible_poly(2, exp)) #fix?
#TODO Choose l1 and L2 from kappa and lambda and n
L1 = exp
L2 = L1

#use SHA 256 and truncate output to become a field value
def H1(number):
    digest = hashlib.sha256(str(number).encode()).digest()
    bit_string = format(int.from_bytes(digest, byteorder='big'), '0256b')
    return bit_string[:L1]

def H2(number):
    digest = hashlib.sha256(str(number).encode()).digest()
    bit_string = format(int.from_bytes(digest, byteorder='big'), '0256b')
    return bit_string[L1:L1+L2] #eg. from 64 to 128

def notVeryObliviousVole(D: galois.Poly, s):
    sFieldElement = GF(int(s, 2))
    coeffList = D.coeffs
    Q = []
    R = []
    for i in range(0, len(coeffList)):
        ri = GF(random.randint(1,2**L1-1)) #Is this right? If it already exists should we generate again until it doesn't?
        R.append(ri)
        qi = ri + coeffList[i] * sFieldElement
        Q.append(qi)
    return galois.Poly(Q, field=GF), galois.Poly(R, field=GF)


def Send(X, Q, s):
    sFieldElement = GF(int(s, 2))
    M = [] #using list instead of set bc of nice permute function from random
    for x in X:
        #TODO: does this stay true to the protocol? We are adding them instead of using strings.
        mi = H2(x + int(Q(x) + GF(int(H1(x), 2)) * sFieldElement)) 
        M.append(mi)
    return random.sample(M, len(M)) #gives permutation


def receiverOutput(R, Y, M):
    outPutList = []
    for y in Y:
        test = H2(y + int(R(y)))
        if test in M:
            outPutList.append(y)
    return outPutList


#So sender wants to find the "y" value of Q at a certain point, they can sum all the
#terms, which in a polynomial are sum(Qi*Ax,i) where 
#TODO: why do we write Ax,i instead of just x^i?
#TODO: Ok so I suppose GFs work so that in GF(2^n) there are n elements, and they have some ordering. So in 2^4, the highest element is 3, but it's not actually 3,
#because it's x^2 + x + 1. So we can't plot it so easily.


#Main program:

if __name__=="__main__":

    X = {12, 14, 2, 4}
    Y = {8, 10, 12, 14}

    #Sender inputs random bit string of length l1
    Snum = random.randint(0,2**L1)
    Sinput = format(Snum, f'0{L1}b')

    #receiver inputs D = Enc({(y, H1(y)) | y in Y})
    RinputXVals = list(Y)
    RinputYVals = [(int(H1(y), 2)) for y in Y]
    D = interpolate(RinputXVals, RinputYVals, exp) #D is a polynomial, which acts as an OKVS

    #VOLE gives Q to sender, and R to receiver
    Q, R = notVeryObliviousVole(D, Sinput)
    #Sender computes M and sends a random permutation which is used to generate the final receiver output
    M = Send(X, Q, Sinput)

    print(f'The set intersection consists of elements: {receiverOutput(R,Y,M)}')




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

#voleChecker(Q, D, Sinput, R)


