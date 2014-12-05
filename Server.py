import socket
import ssl
import random
import time
import string
import hashlib

TCP_IP = '127.0.0.1'
TCP_PORT = 8181
BUFFER_SIZE = 1024
SECRET = 'secret'


def getChallengeMessage(lenght=20, chars=string.ascii_letters + string.digits):
    # generate a sequence of characters taken from the specified characters
    return ''.join(random.choice(chars) for _ in range(lenght))


def getRandomMillSec():
    from_sec = 5
    to_sec = 15
    # init seed with the current time in milliseconds
    random.seed(int(round(time.time() * 1000)))
    return random.uniform(from_sec, to_sec) * 1000

# sends a challenge every 2 seconds
def sendChallenges(sock):
    for _ in range(0,5):
        sock.send(getChallengeMessage())
        time.sleep(2)


def setConnection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    sock, addr = s.accept()

    # Create a secure connection with SSL
    secure_sock = ssl.wrap_socket(sock, server_side=True, certfile='cert.pem', keyfile='cert.pem',
                                  ssl_version=ssl.PROTOCOL_TLSv1)

    # Read password sent by the client
    password = secure_sock.recv(BUFFER_SIZE)

    # Check it
    if password != hashlib.sha512(SECRET).hexdigest():
        print "Connection Refused"
        secure_sock.send("Authentication Failed")
        secure_sock.close()
        return False

    # Else
    print "Connection Accepted"
    sendChallenges(secure_sock)
    secure_sock.close()
    return True


if __name__ == '__main__':
    setConnection()
