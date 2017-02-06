import array
import fcntl
import fileinput
import socket
import struct

INTERFACE = "wlan0"

PROFILEWIFI1 = "homewifi"
PROFILEWIFI2 = "workwifi"

TARGETFILE = "/etc/hosts"

SEARCHEXP = "#MYLOCALSERVERIP MYSERVERDOMAIN"
REPLACEEXP = "MYLOCALSERVERIP MYSERVERDOMAIN"

# hardware stuff with linux functions
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
maxLength = {"interface": 16, "essid": 32}
calls = {"SIOCGIWESSID": 0x8B1B} # get ESSID wireless.h - kernel stuff

def getESSID(interface):
    essid = array.array("c", "\0" * maxLength["essid"])
    essidPointer, essidLength = essid.buffer_info()
    request = array.array("c",
        interface.ljust(maxLength["interface"], "\0") +
        struct.pack("PHH", essidPointer, essidLength, 0)
    )
    fcntl.ioctl(sock.fileno(), calls["SIOCGIWESSID"], request)
    name = essid.tostring().rstrip("\0")
    if name:
        return name
    return None

ESSID = getESSID(INTERFACE)


if ESSID == PROFILEWIFI1:
    for line in fileinput.input(TARGETFILE, inplace=True):
        print line.replace(SEARCHEXP, REPLACEEXP),
if ESSID == PROFILEWIFI2:
    for line in fileinput.input(TARGETFILE, inplace=True):
        print line.replace(REPLACEEXP, SEARCHEXP),
