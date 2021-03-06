from INT import INT
from RSSI import RSSI

'''
detectMode() : 현재 수집된 광고패킷을 기반으로 Time Interval 검사와 RSSI 검사 진행 (= Detection Phase)
'''
class DetectionModel():
    def __init__(self):
        self.pre_item = {}

        self.INT_c = INT()
        self.RSSI_c = RSSI()

    def detectMode(self, item):
        if self.INT_c.check_INT(curr_time = item['time']):
            if self.RSSI_c.check_rssi(rssi = float(item['rssi']), test=True):
                return 1
            else:
                return 2

        self.RSSI_c.check_rssi(rssi = float(item['rssi']), test=False)
        self.pre_item = item
        return False
    
    def checkFlag(self):
        self.INT_c.pre_time = 0
