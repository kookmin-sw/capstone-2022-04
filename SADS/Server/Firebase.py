from firebase_admin import firestore
from firebase_admin import messaging

'''
getPublicKey() : 송신기 (Tag)의 공개키를 가져옴
setEncryptionData() : UUID 정보와 암호화된 정보 업로드
deleteEncryptionData() : UUID 정보와 암호화된 정보 삭제
'''
class Firebase():
    def __init__(self):
        self.db = firestore.client()
    
    def sendMessage(self, cnt):
        registration_token = 'cjCeV5oSRnuhyF8VljAEtZ:APA91bENgw7naurauGXZndZnei1xtss1mDepQd7_gmSBnzHCfu-m4qBkTKr8Cw-OsGoMtNUNrpOyIN9DqYPwadtN_UPgiDaJozT0gAiLSSAP1VMl78-S40Q9um58z-_Sj3fBvPwgjYZo'

        message = messaging.Message(
        notification=messaging.Notification(
            title='Detect Spoofing Attack',
            body=str(cnt),
        ),
        token=registration_token,
        )

        response = messaging.send(message)
        # Response is a Message ID String.
        print('Successfully sent message:', response)
    
    def getPublicKey(self):
        ref = self.db.collection(u'public').document(u'data')
        return ref.get()
        
    def setEncryptionData(self, uuid, en):
        doc_ref = self.db.collection(u'encry').document(u'data')
        doc_ref.set({
            u'uuid': uuid,
            u'y1': en[0],
            u'y2': en[1]
        })

    def setFlag(self):
        doc_ref = self.db.collection(u'flag').document(u'data')
        doc_ref.set({
            u'flag': True,
        })
    
    def deleteEncryptionData(self):
        self.db.collection(u'encry').document(u'data').delete()