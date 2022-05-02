class GaloisField():
    def __init__(self, p):
        self.p = p
        pass

    def range(self):
        point = []

        for i in range(1, self.p):
            a = self.cal(i)

            for item in a:
                point.append([i, item])
        
        return point
        
    def cal(self, x):
        val = []
        res = ( x**3 + x ) % self.p

        for i in range(0, self.p):
            if ( i ** 2 ) % self.p == res:
                val.append(i)
        
        return val