import random
from ECC import ECC

class ElGamal():
    rand = random.SystemRandom()
    def __init__(self, p, a, b, numpoints, g, h):
        self.e = ECC(p=p, a=a, b=b)
        self.numpoints = numpoints
        self.g = g
        self.h = h

    def multiply(self,x,y):
        return self.e.addPoints(x,y)
   

    def exponentiate(self,x,n):
        if n < 0:
            x = self.e.inversePoint(x)
        return self.e.multiplumOfPoint(x,n)

    def encrypt(self, m):
        t = self.rand.randrange(0,self.numpoints)
        c1 = self.exponentiate(self.g,t)
        c2 = self.multiply(self.exponentiate(self.h,t),m)
        return [c1,c2]