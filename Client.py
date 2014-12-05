import socket
import hashlib
import getpass

TCP_IP = '127.0.0.1'
TCP_PORT = 8181
BUFFER_SIZE = 1024


def connect(password):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #secure_sock = ssl.wrap_socket(sock, ca_certs='cert.pem', cert_reqs=ssl.CERT_REQUIRED, ssl_version=ssl.PROTOCOL_TLSv1)

    # Try to connect to the server
    try:
        sock.connect((TCP_IP, TCP_PORT))
    except socket.error:
        print "Connection Refused"
        return False

    # send password
    sock.send(password)

    # print all the challenges responses
    message = sock.recv(BUFFER_SIZE)
    while message:
        print "Server message: " + message
        message = sock.recv(BUFFER_SIZE)

    sock.close()


if __name__ == '__main__':
    passPlain = getpass.getpass(prompt="Enter Password: ")
    passHash = hashlib.sha512(passPlain).hexdigest()
    connect(passHash)