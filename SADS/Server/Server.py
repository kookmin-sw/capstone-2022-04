import socket
from CreateRandom import CreateRandom
from DetectionModel import DetectionModel

'''
serverSetting(): AP와 소켓 통신을 위한 연결 작업
receiveFromAP(): AP가 수신 받는 광고 패킷을 받아 스푸핑 공격 검증
'''
class Server():
    def __init__(self, HOST, PORT = 9999):
        self.HOST = HOST
        self.PORT = PORT
        
        self.cr = CreateRandom()
        self.d = DetectionModel()
        self.client_socket = None
        self.uuid = ''

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
        self.uuid = self.cr.createUUID()
        label = self.uuid
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
           