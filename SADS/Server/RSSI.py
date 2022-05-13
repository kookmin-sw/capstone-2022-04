import numpy as np
from KalmanFilter import KalmanFilter
from Confidence import Confidence
from HoltTech import HoltTech

'''
full_arr() : 예측에 사용되는 데이터를 최대 10000개로 한정하기 위한 함수
check_val() : 현재 수신된 광고 패킷과 이전에 수신된 광고 패킷 중 어떤 것이 공격자의 것인지 특정
add_rssi() : 현재 수신된 RSSI를 평활화하고 사분범위 계산을 위한 데이터 수집
check_rssi() : 사분범위를 활용하여 스푸핑 공격 감지 및 공격자의 패킷 특정
'''
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