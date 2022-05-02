from statsmodels.tsa.api import Holt

'''
holtForcast() : 홀트의 선형 추세 기법을 활용한 다음 Time Interval 예측
'''
class HoltTech():
    def __init__(self, a):
        self.a = a # 0.1
    
    def holtForcast(self, use_INT_arr):
        fit = Holt(use_INT_arr, initialization_method="estimated").fit(smoothing_level=self.a)
        return fit.forecast(1)[0]