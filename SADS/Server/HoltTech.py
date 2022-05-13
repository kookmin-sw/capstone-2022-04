class HoltTech():
    def __init__(self, level, trend):
        self.level = level
        self.trend = trend

        self.preL = 0
        self.preB = 0

    def holtForcast(self, x):
        
        if self.preL == 0:
            self.preL = x
            self.preB = 0
            return x
        
        l = (self.level * x) + (1 - self.level) * (self.preL + self.preB)
        b = self.trend * (l - self.preL) + (1 - self.trend) * self.preB

        res = l + b

        self.preL = l
        self.preB = b

        return res
