import socket
import threading
import ScanUtility
import bluetooth._bluetooth as bluez

uuid = ''
client = None

def rcvdBeacon():
        dev_id = 0
        global uuid
        global time_flag
        global client
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
                        message = str(index) + ',' + str(item['time']) + ',' + item['uuid'] + ',' + item['macAddress'] + ',' + str(item['rssi'])
                        print(message)
                        encodedMsg = message.encode(encoding="utf-8")
                        client.sendall(encodedMsg)
                        print("message sent!")
                                
                index += 1
                if flag:
                    break

        except KeyboardInterrupt:
            pass

def initSetting():
    global uuid
    global client

    serverHost = '192.168.219.104'
    PORT = 9999
   
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((serverHost, PORT))
    client.sendall("AP".encode())

    data = client.recv(1024)
    decodedData = data.decode("utf-8")

    splitData = decodedData.split(' ')

    # Set UUID
    uuid = splitData[0]

    return True

if __name__ == '__main__':
    if initSetting():
        rcvdBeaconTh = threading.Thread(target=rcvdBeacon, args=())
        rcvdBeaconTh.start()


