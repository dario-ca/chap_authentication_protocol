__author__ = 'paolobruzzo'

import socket
import hashlib
import getpass

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024


def connect(password):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Try to connect to the server
    try:
        s.connect((TCP_IP, TCP_PORT))
    except socket.error:
        print "Connection Refused"
        return False

    s.send(password)
    s.close()


if __name__ == '__main__':
    passPlain = getpass.getpass(prompt="Enter Password: ")
    passHash = hashlib.sha512(passPlain).hexdigest()
    connect(passHash)