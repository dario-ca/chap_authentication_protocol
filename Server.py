import socket
import ssl

TCP_IP = '127.0.0.1'
TCP_PORT = 8181
BUFFER_SIZE = 1024
SECRET_SHA512 = 'bd2b1aaf7ef4f09be9f52ce2d8d599674d81aa9d6a4421696dc4d93dd0619d682ce56b4d64a9ef097761ced99e0f67265b5f76085e5b0ee7ca4696b2ad6fe2b2'


def setConnection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    sock, addr = s.accept()

    # Create a secure connection with SSL
    secure_sock = ssl.wrap_socket(sock, server_side=True, certfile='cert.pem', keyfile='cert.pem', ssl_version=ssl.PROTOCOL_TLSv1)

    data = secure_sock.recv(BUFFER_SIZE)

    # Read password sent by the client
    password = ''
    while data:
        password += data
        data = secure_sock.recv(BUFFER_SIZE)

    # Close connection (TODO: leave the connection open in case of successful connection)
    secure_sock.close()

    if password == SECRET_SHA512:
        return True
    return False

if __name__ == '__main__':

    valid = setConnection()

    # Wait for a valid connection
    while not valid:
        print "Connection Refused"
        valid = setConnection()

    print "Connection Accepted"
