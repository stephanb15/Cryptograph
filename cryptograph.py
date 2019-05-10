import math


def extndEuclid(x1,x):
    ...
    



class Keys:
    def RSA(prime1,prime2):
        #find the keys for RSA encryption decryption
        n=prime1*prime2
        phin=(prime1-1)(prime2-1)
        enorm=2**16+1
        #a usual vale for the encryption exponent (performance)
        e=enorm
        if enorm > phin:
            print("Error: choose greater prime numbers")
            # or in case calculate a e <phin with gcd(e,phin)=1
            #which might either be a performacne issue or a security issue
        #find a "d" with d*e kongurent 1 module phin
        public=(e,n)
        private=d
        return (public,private)



class Encrypt:
    def __init__(self,x):
        #input is to be the data you like to encrypt
        if isinstance(x,float):
            self.float=x
        elif isinstance(x,int):
            self.int=x
        elif isinstance(x,str):
            self.str=x
        else:
            print("Your input",x,"is not understood by this class")
            print("    try a different data type")

    def RSA(self, pubkey):

        #input the RSA public key tupel "pubkey" 
        return self.int


x=Encrypt(11341)
print(x.RSA(11))