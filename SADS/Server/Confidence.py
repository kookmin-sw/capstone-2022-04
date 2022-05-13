import numpy as np

class Confidence():
    def __init__(self, z, holt_z):
        self.z = z  # 2.58
        self.holt_z = holt_z # 3.219

    def confidenceInterval(self, use_INT_arr):
        return np.mean(use_INT_arr) + ( self.z * (np.std(use_INT_arr) / np.sqrt(len(use_INT_arr))) )

    def holtLower(self, fcast, se):
        return fcast - ( self.holt_z * se )

    def holtCheck(self, fcast, se):
        MIN = fcast - ( self.holt_z * se )
        MAX = fcast + ( self.holt_z * se )
        return MIN, MAX