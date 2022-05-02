class ECC():
    def __init__(self, p, a, b):
        self.id = "Point at infinity"
        self.p = p
        self.a = a
        self.b = b

    def checkPoint(self,p):
        if p != self.id:
            ls = (p[1]*p[1])%self.p
            hs = ((p[0]**3)+(self.a*p[0]) + self.b)%self.p
            if ls == hs:
                return True
            else: 
                return False
        else:
            return True

	# Find n*p, Where n is the Number and p the Point
    def multiplumOfPoint(self,p,n):
        if self.checkPoint(p):
            binrep = bin(n)[2:]
            res = self.id
		
            for bit in binrep:
                res = self.addPoints(res,res)
                if bit == "1":
                    res = self.addPoints(res,p)
            return res
        else:
            print("Must have a point on the curve as input")

    def addPoints(self,p1,p2):
        if self.checkPoint(p1) and self.checkPoint(p2):
            if p1 == self.id:
                return p2
            elif p2 == self.id:
                return p1
            elif (p1[0] == p2[0]) and (p1[1] == ((-p2[1])%self.p)):
                return self.id
            elif (p1[0] == p2[0]) and (p1[1] == p2[1]):
                return self.calcPoint(p1,p2,self.lambdaEqual(p1))
            else:
                return self.calcPoint(p1,p2,self.lambdaDiff(p1,p2))
        else:
            print("Both points must be on the curve.")

    def inversePoint(self,p):
        if self.checkPoint(p) and (not p == self.id):
            return [p[0],((-p[1])%self.p)]
        elif p == self.id:
            return p
        else: 
            print("Must have point on curve to find inverse")

    def lambdaEqual(self,p1):
        l = ((3*p1[0]*p1[0])+self.a)*(self.modinv((2*p1[1]),self.p))%self.p
        return l

    def lambdaDiff(self,p1,p2):
        l = (p2[1]-p1[1])*(self.modinv(((p2[0]-p1[0])%self.p),self.p))%self.p
        return l

    def calcPoint(self,p1,p2,l):
        x = ((l*l) - p1[0] - p2[0])%self.p
        y = ((l*(p1[0]-x))-p1[1])%self.p
        return [x,y]

    def egcd(self,a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = self.egcd(b % a, a)
            return (g, x - (b // a) * y, y)

    def modinv(self, a, m):
        g, x, y = self.egcd(a, m)
        if g != 1:
            raise Exception('modular inverse does not exist')
        else:
            return x % m