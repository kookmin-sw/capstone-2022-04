import sys
import struct
import bluetooth._bluetooth as bluez
import time
import threading

OGF_LE_CTL=0x08
OCF_LE_SET_SCAN_ENABLE=0x000C

def hci_enable_le_scan(sock):
    hci_toggle_le_scan(sock, 0x01)

def hci_disable_le_scan(sock):
    hci_toggle_le_scan(sock, 0x00)

def hci_toggle_le_scan(sock, enable):
    cmd_pkt = struct.pack("<BB", enable, 0x00)
    bluez.hci_send_cmd(sock, OGF_LE_CTL, OCF_LE_SET_SCAN_ENABLE, cmd_pkt)

def packetToString(packet):
    """
    Returns the string representation of a raw HCI packet.
    """
    if sys.version_info > (3, 0):
        return ''.join('%02x' % struct.unpack("B", bytes([x]))[0] for x in packet)
    else:
        return ''.join('%02x' % struct.unpack("B", x)[0] for x in packet)

def parse_events(sock, g_uuid, loop_count = 100):
    old_filter = sock.getsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, 14)
    flt = bluez.hci_filter_new()
    bluez.hci_filter_all_events(flt)
    bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, flt)

    for i in range(0, loop_count):
        packet = sock.recv(255)
        dataString = packetToString(packet)

        if len(dataString) > 83:
            uuid = dataString[40:48] + "-" + dataString[48:52] + "-" + dataString[52:56] + "-" + dataString[56:60] + "-" + dataString[60:72]
            major = dataString[72:76]
            minor = dataString[76:80]

            majorVal = int("".join(major.split()[::-1]), 16)
            minorVal = int("".join(minor.split()[::-1]), 16)

            if uuid == g_uuid:
                
                type = "iBeacon"

                scrambledAddress = dataString[14:26]
                fixStructure = iter("".join(reversed([scrambledAddress[x:x+2] for x in range(0, len(scrambledAddress), 2)])))
                macAddress = ':'.join(a+b for a, b in zip(fixStructure, fixStructure))
                
                rssi, = struct.unpack("b", packet[len(packet)-1:])
                
                resultsArray = [{"type": type, "time": time.time(), "uuid": uuid, "rssi": rssi, "macAddress": macAddress}]
                return resultsArray