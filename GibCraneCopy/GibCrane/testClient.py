"""
File not needed - can be deleted

"""

import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# give server address (ip, port) suggested port from 10000 to 65535
server_address = ('192.168.0.96', 10000)
print('connecting to %s port %s' % server_address)

# connect socket to the server
sock.connect(server_address)
print('connected to %s port %s' % server_address)

while True:
    # prepare message
    message = "xdddddddd"
    print('sending "%s"' % message)

    # sending encoded messege
    sock.sendall(message.encode())

    # Look for the response
    amount_received = 0
#  amount_expected = len(message)

#  while amount_received < amount_expected:  # while full message is not confirmed
#     data = sock.recv(16)  # getting echo message in 16 bit packege
#    amount_received += len(data)  # amount of recived bits
#   print('received "%s"' % data)  # print echo message

# finally:
#   print('closing socket')
# sock.close() # closing socket connection