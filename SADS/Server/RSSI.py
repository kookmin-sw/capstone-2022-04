import numpy as np
from KalmanFilter import KalmanFilter
from Confidence import Confidence
from HoltTech import HoltTech
from Server.HoltTech import HoltTech

class RSSI():
    def __init__(self):
        self.fcast = 0
        self.power_sum = 0
        self.se = 0
        self.idx = 2
        
        self.confi = Confidence(z=2.58, holt_z=3.219)
        self.holt = HoltTech(level = 0.9, trend = 0.4)
        self.KF = KalmanFilter(processNoise = 0.4, measurementNoise = 5)
        
        self.lower = 0
        self.upper = 0

    def check_rssi(self, rssi, test):
        pre_data = self.KF.applyFilter(rssi)
        
        if self.lower != 0 and self.upper != 0:
            if test:
                if pre_data < self.lower or pre_data > self.upper :
                    return True
                else:
                    return False
    
        if self.fcast == 0:     
            self.fcast = self.holt.holtForcast(pre_data)
            return
    
        self.power_sum += np.power(pre_data - self.fcast, 2)

        if self.se == 0:
            self.se = np.sqrt(self.power_sum / ( self.idx - 1 ))
            self.fcast = self.holt.holtForcast(pre_data)
            self.idx += 1
            return
    
        self.fcast = self.holt.holtForcast(pre_data)
        self.lower, self.upper = self.confi.holtCheck(self.fcast, self.se)
        self.se = np.sqrt(self.power_sum / ( self.idx - 1))
        self.idx += 1
        
        return False