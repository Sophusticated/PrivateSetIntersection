import random
import hashlib
#Sender set X:
X = {12, 14, 2, 4}
#Receiver set Y:
Y = {8, 10, 12, 14}

#Choose l1 and L2 from kappa and lambda and n
L1 = 128
L2 = 128

#use SHA 256 and truncate output to become a field value
def hash_first_l_bits(number, l):
    digest = hashlib.sha256(str(number).encode()).digest()
    bit_string = format(int.from_bytes(digest, byteorder='big'), '0256b')
    return bit_string[:l]

#Sender inputs random bit string of length l1
Snum = random.randint(0,2**L1)
Sinput = format(Snum, f'0{L1}b')
print(Snum, Sinput)
#receiver inputs D = Enc({(y, H1(y)) | y in Y}) here H1 maps from values to l1 amount of values


#Here we hash y, and since we truncate to L1 bits, we have {0,1}^* -> {0,1}^L1
Rinput = [(y, int(hash_first_l_bits(y,L1))) for y in Y]
print(Rinput)
#So here receiver is actually generating random values (y values in a coordinate) to put as points.

#Now d is a bitstring which encodes the coefficients for an interpolated equation
#TODO: Each coefficient is a field element, so should it not be a list of field elements? or a list of bitstrings?
#TODO: implement lagrange interpolation:

#Magical VOLE gives Q to sender, and R to receiver
#TODO: how tf do we fake vole?? 
# Maybe we can just hardcode a few of them and skip everything before here?

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