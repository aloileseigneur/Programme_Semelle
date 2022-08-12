import bluetooth
import socket
import winreg as reg
from itertools import count

def scan():

    print("Scanning for bluetooth devices:")

    devices = bluetooth.discover_devices(lookup_names = True, lookup_class = True)

    number_of_devices = len(devices)

    print(number_of_devices,"devices found")

    for addr, name, device_class in devices:

        print("\n")

        print("Device:")

        print("Device Name: %s" % (name))

        print("Device MAC Address: %s" % (addr))

        print("Device Class: %s" % (device_class))

        print("\n")

    return



hostMACAddress = '2C:10:C1:41:9E:A5' # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
backlog = 1
size = 1024
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)






#############[('2C:10:C1:41:9E:A5', 'Nintendo RVL-WBC-01'), ('AC:FD:CE:5D:01:28', 'MECANIX')]##########3