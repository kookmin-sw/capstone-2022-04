import socket
import threading
import ScanUtility
import bluetooth._bluetooth as bluez
import random
import time

uuid = ''
client = None
start_flag = False
time_flag = True

def rcvdBeacon():
        dev_id = 0
        global uuid
        global client
        global start_flag
        global time_flag
        try:
            sock = bluez.hci_open_dev(dev_id)
            print ("\n *** Looking for BLE Beacons ***\n")
            print ("\n *** CTRL-C to Cancel ***\n")
        except:
            print ("Error accessing bluetooth")

        ScanUtility.hci_enable_le_scan(sock)
        index = 0
        flag = False
        
        try:
            while True:
                returnedList = ScanUtility.parse_events(sock, uuid, 100)
                if returnedList:
                    for item in returnedList:
                        if item == None:
                            pass
                        else:
                            # Start Section
                            if not start_flag:
                                # 광고 패킷을 처음 수신 받았을 때
                                timeTh = threading.Thread(target=setFlag, args=())
                                timeTh.start()
                                start_flag = True
                            
                            if start_flag and time_flag:
                                # Unicast Phase
                                # 광고 패킷을 수신받기 시작했고 (start_flag == True)
                                # Promise Time일 때 (time_flag == True)
                                # Server로 광고 패킷 송신
                                message = str(index) + ',' + str(item['time']) + ',' + item['uuid'] + ',' + str(item['rssi'])
                                print(message)
                                encodedMsg = message.encode(encoding="utf-8")
                                client.sendall(encodedMsg)
                                print("message sent!")
                                
                index += 1

        except KeyboardInterrupt:
            pass

def initSetting():
    global uuid
    global client

    serverHost = '192.168.219.104'
    PORT = 9999
   
    # Server로부터 UUID값과 Random Seed Value 값 수신
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((serverHost, PORT))
    client.sendall("AP".encode())

    data = client.recv(1024)
    decodedData = data.decode("utf-8")
    splitData = decodedData.split(' ')

    # UUID 설정
    uuid = splitData[0]
    
    # Random Seed Value에 따른 Seed 설정
    random.seed(splitData[1])
    return True

def setFlag():
    global time_flag
    
    while True:
        # Random Time List 요소 값 생성
        time.sleep(random.randint(2,5))
        
        # Promise Time : 광고 패킷을 수신받는 시간 (time_flag == True)
        # Non-promise Time : 광고 패킷을 수신받지 않는 시간 (time_flag == False)
        time_flag = not time_flag
        
if __name__ == '__main__':
    if initSetting():
        rcvdBeaconTh = threading.Thread(target=rcvdBeacon, args=())
        rcvdBeaconTh.start()
