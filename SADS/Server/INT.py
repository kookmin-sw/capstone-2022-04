from operator import le
from HoltTech import HoltTech
from Confidence import Confidence
import numpy as np

'''
full_arr() : 예측에 사용되는 데이터를 최대 10000개로 한정하기 위한 함수
check_INT() : 현재 입력값을 기준으로 Time Interval 검사 진행
'''
'''
full_arr() : 예측에 사용되는 데이터를 최대 10000개로 한정하기 위한 함수
check_INT() : 현재 입력값을 기준으로 Time Interval 검사 진행
'''
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

        # 이전에 들어온 패킷을 사용하여 Time Interval 계산
        INT = curr_time - self.pre_time
        print('/// Current INT: ', INT)
        
        # 스푸핑 공격 검사
        if self.lower != 0:
            if INT < self.lower:
                self.fcast = self.fcast_pre
                self.se = self.se_pre
                self.power_sum -= np.power(INT - self.fcast_pre, 2)
                self.idx -= 1
                return True

        # 신뢰 구간을 계산하기 위한 데이터의 최소 개수를 맞추기 위한 작업
        if len(self.use_INT_arr) < 3 and INT < 0.3:
            self.use_INT_arr.append(INT)
            self.pre_time = curr_time
            return False

        # 정밀한 예측을 위해 99%의 신뢰구간을 활용하여 데이터 필터링
        if INT < self.confi.confidenceInterval(self.use_INT_arr):
            if len(self.use_INT_arr) > 10:

                if self.fcast == 0:
                    self.fcast = self.holt.holtForcast(INT)
                    self.use_INT_arr.append(INT)
                    self.pre_time = curr_time
                    return False
                
                # 표준 오차 계산을 위한 실제값과 예측값 차이 누적
                self.power_sum += np.power(INT - self.fcast, 2)

                if self.se == 0:
                    self.se = np.sqrt(self.power_sum / ( self.idx - 1))
                    self.fcast = self.holt.holtForcast(INT)
                    self.use_INT_arr.append(INT)
                    self.pre_time = curr_time
                    self.idx += 1
                    return False

                # 다음 Time Interval 예측
                self.fcast_pre = self.fcast
                self.se_pre = self.se

                self.fcast = self.holt.holtForcast(INT)
                # 예측값과 표준 오차를 활용한 Time Interval의 하한값 계산
                self.lower = self.confi.holtLower(self.fcast, self.se)
                # 표준 오차 계산
                self.se = np.sqrt(self.power_sum / ( self.idx - 1))
                self.idx += 1
                print('Prediction Next INT: ', self.fcast)
                print('Calculated Next Lower INT: ', self.lower)
            
          
            self.use_INT_arr.append(INT)
                
        self.pre_time = curr_time
        return False
