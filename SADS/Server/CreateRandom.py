from Firebase import Firebase
from UseData import UseData
from ElGamal import ElGamal
import random
import string

class CreateRandom():
    def __init__(self):
        self.useData = UseData()
        self.fireBase = Firebase()
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

    def createEncryptionData(self):
        doc = self.fireBase.getPublicKey()
        en = []

        if doc.exists:
            cs = ElGamal(p=32653, a=1, b=0, numpoints=32978, g=doc.to_dict()['g'], h=doc.to_dict()['h'])
            self.data = self.getData() 
            en = cs.encrypt(self.data)
            return self.data, en
        else:
            print('doc does not exist')
    
    def createTimeList(self, seed):
        random.seed(seed)

        # Random Time List 생성 (AP)
        timeList = []
        for i in range(1000):
            if i % 2 == 0:
                timeList.append(random.randint(2, 7) + 0.5)
            else:
                timeList.append(random.randint(3, 5) - 0.5)
        
        return timeList
        
    
    def getData(self):
        return self.useData.data[random.randrange(0, 32978)]