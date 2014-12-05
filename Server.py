__author__ = 'paolobruzzo'

import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
SECRET_SHA512 = 'bd2b1aaf7ef4f09be9f52ce2d8d599674d81aa9d6a4421696dc4d93dd0619d682ce56b4d64a9ef097761ced99e0f67265b5f76085e5b0ee7ca4696b2ad6fe2b2'


def waitValidConnection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    conn, addr = s.accept()

    data = conn.recv(BUFFER_SIZE)
    password = ''
    while data:
        print 'Received data: ', data
        password += data
        data = conn.recv(BUFFER_SIZE)
    conn.close()

    if password == SECRET_SHA512:
        return True
    return False

if __name__ == '__main__':
    if waitValidConnection():
        print("Connection Accepted")
    else:
        print("Connection Refused")