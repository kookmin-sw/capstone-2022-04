from operator import le
from HoltTech import HoltTech
from Confidence import Confidence
import numpy as np

class INT():
    def __init__(self):
        self.use_INT_arr = []
        self.pre_time = 0
        self.fcast = 0
        self.power_sum = 0
        self.se = 0
        self.idx = 2

        self.confi = Confidence(z = 2.58, holt_z= 3.219)
        self.holt = HoltTech(level=0.1, trend=0.0001)
        self.lower = 0
        
        self.fcast_pre = 0
        self.se_pre = 0

    def full_arr(self):
        del self.use_INT_arr[:len(self.use_INT_arr) - 100]

    def check_INT(self, curr_time):
        if len(self.use_INT_arr) > 10000:
            self.full_arr()

        if self.pre_time == 0:
            self.pre_time = curr_time
            return False

        INT = curr_time - self.pre_time
#         print('Current INT: ', INT)
        
        if self.lower != 0:
            if INT < self.lower:
                self.fcast = self.fcast_pre
                self.se = self.se_pre
                self.power_sum -= np.power(INT - self.fcast_pre, 2)
                self.idx -= 1
                return True

        if len(self.use_INT_arr) < 3 and INT < 0.3:
            self.use_INT_arr.append(INT)
            self.pre_time = curr_time
            return False

        if INT < self.confi.confidenceInterval(self.use_INT_arr):
            print('Current INT: ', INT)
            if len(self.use_INT_arr) > 10:

                if self.fcast == 0:
                    self.fcast = self.holt.holtForcast(INT)
                    self.use_INT_arr.append(INT)
                    self.pre_time = curr_time
                    return False
                
                self.power_sum += np.power(INT - self.fcast, 2)

                if self.se == 0:
                    self.se = np.sqrt(self.power_sum / ( self.idx - 1))
                    self.fcast = self.holt.holtForcast(INT)
                    self.use_INT_arr.append(INT)
                    self.pre_time = curr_time
                    self.idx += 1
                    return False

                self.fcast_pre = self.fcast
                self.se_pre = self.se

                self.fcast = self.holt.holtForcast(INT)
                print('fcast: ', self.fcast)
                self.lower = self.confi.holtLower(self.fcast, self.se)
                self.se = np.sqrt(self.power_sum / ( self.idx - 1))
                print('se: ', self.se)
                self.idx += 1
                print('lower: ', self.lower)
            
          
            self.use_INT_arr.append(INT)
                
        self.pre_time = curr_time
        return False
