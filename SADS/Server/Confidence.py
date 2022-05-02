import numpy as np

'''
confidenceInterval() : 다음 Time Interval 예측에 사용될 수 있는 안정적인 데이터의 구간 계산
holtLower() : 예측값과 실제값의 표준오차를 사용하여 Tiem Interval의 하한값 계산
'''
class Confidence():
    def __init__(self, z, holt_z):
        self.z = z              # 2.58, 99.9%의 신뢰구간
        self.holt_z = holt_z    # 3.219, 99.99%의 신뢰구간

    def confidenceInterval(self, use_INT_arr):
        return np.mean(use_INT_arr) + ( self.z * (np.std(use_INT_arr) / np.sqrt(len(use_INT_arr))) )

    def holtLower(self, fcast, se):
        return fcast - ( self.holt_z * se )