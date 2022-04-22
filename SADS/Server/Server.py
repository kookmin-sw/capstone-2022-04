from firebase_admin import credentials
import firebase_admin
import socket
import time
from CreateRandom import CreateRandom
from Firebase import Firebase
from DetectionModel import DetectionModel

'''
serverSetting(): AP와 소켓 통신을 위한 연결 작업
receiveFromAP(): AP가 수신 받는 광고 패킷을 받아 스푸핑 공격 검증
'''
class Server():
    def __init__(self, HOST, PORT = 9999):
        self.HOST = HOST
        self.PORT = PORT
        cred = credentials.Certificate('beacon-bbd26-firebase-adminsdk-wsvjj-82e61b4482.json')
        firebase_admin.initialize_app(cred)

        self.d = DetectionModel()
        self.cr = CreateRandom()
        self.fr = Firebase()
        self.client_socket = None
        self.uuid = ''
        self.data = []
        self.flag = False

    def serverSetting(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # For 'WinError 10048 Error'
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server_socket.bind((self.HOST, self.PORT))
        server_socket.listen()

        print('Ready for connect with AP')

        # Wating client access & return new socket
        self.client_socket, addr = server_socket.accept()

        # Print client address
        print('Connected by: ', addr)


        while True:
            msg = self.client_socket.recv(1024)

            if not msg:
                print("/// Connection Failed")

            if msg.decode("utf-8") == "AP":
                print("/// Connection Success")
                break
            
        print("-------------------------------------")

        # 광고 패킷을 송신하는 기기의 UUID 랜덤 생성 후 AP에게 송신
        # Major, Minor value
        label = self.uuid + ' ' + str(self.data[0]) + ' ' + str(self.data[1])
        encodeLabel = label.encode(encoding="utf-8")
        self.client_socket.sendall(encodeLabel)
        print("/// Send Label")
        print("encry : ", label)
        print("-------------------------------------")

        # 스푸핑 공격 감지 시작
        self.receiveFromAP()

        
    def receiveFromAP(self):
        while True:
            ackMsg = self.client_socket.recv(1024)
            decodeMsg = ackMsg.decode("utf-8")
            splitedData = decodeMsg.split(',')
            item = {"time": float(splitedData[1]), "uuid": splitedData[2], "rssi": int(splitedData[3])}

            if ackMsg != None:
                # 광고 패킷 검사
                res = self.d.detectMode(item=item)

                # 스푸핑 공격 감지
                if res:
                    print("****************************************")
                    print("Detect Spoofing Attack!")
                    print(decodeMsg)
                    print("****************************************")
    
    def listenFirebase(self):
        doc_public = self.fr.db.collection(u'public').document(u'data')
        doc_updatePublic = self.fr.db.collection(u'public').document(u'data')

        def on_snapshot(on_snapshot, changes, read_time):
            for change in changes:
                if change.type.name == 'ADDED':
                    self.uuid = self.cr.createUUID()
                    self.data, en = self.cr.createEncryptionData()
                    self.fr.setEncryptionData(uuid=self.uuid, en=en)
                    self.serverSetting()
                
        
        def on_snapshot2(on_snapshot, changes, read_time):
            for change in changes:
                if change.type.name == 'MODIFIED':
                    self.fr.deleteEncryptionData()
                    self.uuid = self.cr.createUUID()
                    self.data, en = self.cr.createEncryptionData()
                    self.fr.setEncryptionData(uuid=self.uuid, en=en)
            
                    updateData = self.uuid + ' ' + str(self.data[0]) + ' ' + str(self.data[1])
                    encodeLabel = updateData.encode(encoding="utf-8")
                    self.client_socket.sendall(encodeLabel)
            
        doc_public.on_snapshot(on_snapshot)
        doc_updatePublic.on_snapshot(on_snapshot2)
        
        while True:
            if not self.flag:
                time.sleep(1)
            else:
                break
    

           