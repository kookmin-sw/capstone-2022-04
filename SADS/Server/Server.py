from firebase_admin import credentials
import firebase_admin
import socket
import time
import threading
from CreateRandom import CreateRandom
from Firebase import Firebase
from DetectionModel import DetectionModel

'''
serverSetting() : AP와 소켓 통신을 위한 연결 작업
receiveFromAP() : AP가 수신 받는 광고 패킷을 받아 스푸핑 공격 검증
'''
class Server():
    def __init__(self, HOST, PORT = 9999):
        self.HOST = HOST
        self.PORT = PORT
        cred = credentials.Certificate('beacon-bbd26-firebase-adminsdk-wsvjj-82e61b4482.json')
        firebase_admin.initialize_app(cred)
        
        self.cr = CreateRandom()
        self.fr = Firebase()
        self.d = DetectionModel()
        self.client_socket = None
        self.uuid = ''
        self.data = []
        self.flag = False
        self.timeList = []
        self.idx = 0

        self.dummyFlag = False
        self.timeFlag = True
        self.startFlag = False
        

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

        # Make Random Seed

        self.timeList = self.cr.createTimeList(str(self.data[0]))
        label = self.uuid
        encodeLabel = label.encode(encoding="utf-8")
        self.client_socket.sendall(encodeLabel)
        print("/// Send Label")
        print("encry : ", label)
        print("timeList: \n", self.timeList)
        print("-------------------------------------")

        self.receiveFromAP()

        
    def receiveFromAP(self):
        flag = False
        while True:
            ackMsg = self.client_socket.recv(1024)
            decodeMsg = ackMsg.decode("utf-8")
            splitedData = decodeMsg.split(',')
            item = {"time": float(splitedData[1]), "uuid": splitedData[2], "mac": splitedData[3], "rssi": int(splitedData[4])}

            if ackMsg != None:
                if self.timeFlag and not self.dummyFlag:
                    print("---------------------------------------------------------------------")
                    print(decodeMsg)
                    res = self.d.detectMode(item=item)

                    if res == 1:
                        flag = True
                    elif res == 2 and self.startFlag == False:
                        self.fr.setFlag()
                        timeTh = threading.Thread(target=self.setNonPromise, args=())
                        timeTh.start()  
                        self.startFlag = True
                elif not self.timeFlag and self.dummyFlag:
                    flag = True
                
                if flag:
                    print("!!! Detect Spoofing Attack !!!")
                    print("Attacker's Packet: " + decodeMsg)
                    print("---------------------------------------------------------------------")
                    break


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
    
    def setNonPromise(self):
        self.dummyFlag = True
        print("***************************************************************")
        print("!!! Start Delay Time !!!")

        for _ in range(2):
            if not self.timeFlag:
                print("!!! Non-promise time ON !!!")

            if(self.timeFlag == False):
                self.d.checkFlag()
       
            time.sleep(self.timeList[self.idx])

            if self.idx % 2 == 1:
                self.startFlag = False
                self.dummyFlag = False
            else:
                print("!!! End Delay Time !!!")
                print("***************************************************************")

            if not self.timeFlag:
                print("!!! Non-promise time OFF !!!")

            self.timeFlag = not self.timeFlag
            self.idx += 1
           