import random
import string

'''
createUUID(): 광고 패킷(비콘)의 UUID를 랜덤으로 생성
'''
class CreateRandom():
    def __init__(self):
        self.data = []

    def createUUID(self):
        uuid_candidate = string.ascii_lowercase[0:6] + string.digits
        new_uuid = ''

        # 8 4 4 4 12
        for i in range(32):
            if i == 8 or i == 12 or i == 16 or i == 20:
                new_uuid += '-'

            new_uuid += random.choice(uuid_candidate)

        return new_uuid