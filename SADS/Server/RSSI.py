import numpy as np
from KalmanFilter import KalmanFilter

'''
full_arr() : 예측에 사용되는 데이터를 최대 10000개로 한정하기 위한 함수
check_val() : 현재 수신된 광고 패킷과 이전에 수신된 광고 패킷 중 어떤 것이 공격자의 것인지 특정
add_rssi() : 현재 수신된 RSSI를 평활화하고 사분범위 계산을 위한 데이터 수집
check_rssi() : 사분범위를 활용하여 스푸핑 공격 감지 및 공격자의 패킷 특정
'''
class RSSI():
    def __init__(self):
        self.rssi_arr = []
        self.kf = KalmanFilter(processNoise=1, measurementNoise=1)

    def full_arr(self):
        del self.rssi_arr[:len(self.rssi_arr) - 100]

    def check_val(self, min, max, val):
        if min < val < max:
            return 0
        else:
            if val < min:
                return min - val
            else:
                return val - max

    def add_rssi(self, rssi):
        if len(self.rssi_arr) > 10000:
            self.full_arr()

        self.rssi_arr.append(self.kf.applyFilter(rssi))

    def check_rssi(self, curr, prev):
        # 사분범위 계산
        Q1 = np.percentile(self.rssi_arr, 25)
        Q3 = np.percentile(self.rssi_arr, 75)
        IQR = (Q3 - Q1) * 1.5

        min = Q1 - IQR
        max = Q3 + IQR

        # 스푸핑 공격 여부 검증
        curr_val = self.check_val(min, max, self.kf.applyFilter(curr['rssi']))
        prev_val = self.check_val(min, max, self.kf.applyFilter(prev['rssi']))

        if curr_val == 0 and prev_val == 0:
            print("It's not a spoofing attack")
            return False
        else:
            if curr_val > prev_val:
                print(curr['uuid'] + ' attempted a spoofing attack.')
            else:
                print(prev['uuid'] + ' attempted a spoofing attack.')

            return True