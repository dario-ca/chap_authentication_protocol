import socket
import random
import time
import string
import hashlib
import thread
import datetime
from Utils import *

SECRET = 'secret'
LAST_CHALLENGE_SENT = ''

# to set the global variable
def setLastChallenge(challenge):
    global LAST_CHALLENGE_SENT
    LAST_CHALLENGE_SENT = challenge

# creates a new challenge of letters and numbers
def createChallenge(lenght=30, chars=string.ascii_letters + string.digits):
    # generate a sequence of characters taken from the specified characters
    return ''.join(random.choice(chars) for _ in range(lenght))

# Returns a random number withing a given interval
def getRandomSec(from_sec, to_sec):
    # init seed with the current time in milliseconds
    random.seed(int(round(time.time() * 1000)))
    return random.uniform(from_sec, to_sec)

# To check if the user wants to exit
def isClosingMessage(message):
    return message == CLOSING_MESSAGE

# This runs on a separate thread, and sends every N seconds
# a challenge to the client
def startChallenges(sock):
    while 1:
        challenge = createChallenge()
        sendMessage(sock, MessageType.CHALLENGE, challenge)
        setLastChallenge(challenge)
        time.sleep(getRandomSec(10, 20))

# To check if the client response is OK
def isChallegeCorrect(clientResponse):
    return clientResponse == hashlib.sha512(LAST_CHALLENGE_SENT + SECRET).hexdigest()

# This runs on the main thread and listen to the client sock.send
def monitorIncomingMessages(sock):
    while 1:
        type, incoming = parseMessage(sock.recv(BUFFER_SIZE))
        # If i received a normal user message
        if type == MessageType.MESSAGE:
            if isClosingMessage(incoming):
                break
            else:
                print "Client said: " + incoming
        # if is a challenge packet response
        elif type == MessageType.CHALLENGE:
            if not isChallegeCorrect(incoming):
                sendMessage(sock, MessageType.NACK, "Trying to Hack me ?")
                break
            else:
                print "Client challenge response approved"
                now = datetime.datetime.now().strftime("%H:%M:%S")
                sendMessage(sock, MessageType.ACK, 'Your authentication has been approved at ' + now)


def setConnection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    sock, addr = s.accept()

    # Read password sent by the client
    password = sock.recv(BUFFER_SIZE)

    # If the password doesn't match, close immediately
    if password != hashlib.sha512(SECRET).hexdigest():
        print "Connection Refused"
        sendMessage(sock, MessageType.NACK, "Wrong password")
        sock.close()
        return False

    # Else
    print "Connection Accepted"
    sendMessage(sock, MessageType.ACK, "Password Correct")

    # Launch the handler of the challenges in a new thread
    # so that it does not interfere with the sock.recv on
    # the main thread
    thread.start_new_thread(startChallenges, (sock, ))

    # Launch the sock.recv on the main thread
    monitorIncomingMessages(sock)

    # You get here when the user enters the closing message,
    # or when the challenge message is incorrect
    sock.close()
    return True


if __name__ == '__main__':
    setConnection()
