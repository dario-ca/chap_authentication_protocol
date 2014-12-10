import socket
import getpass
import thread
import os
from Utils import *

LAST_CHALLENGE_RECEIVED = ''


# to set the global variable
def setLastChallenge(challenge):
    global LAST_CHALLENGE_RECEIVED
    LAST_CHALLENGE_RECEIVED = challenge


# Handles the challenge messages
def handleChallenges(sock, password):
    while 1:
        # Get the challenge
        type, challenge = parseMessage(sock.recv(BUFFER_SIZE))

        # Hash the challenge and the password together
        hashedChallenge = encode(challenge + password)

        # Send it back
        sendMessage(sock, MessageType.CHALLENGE, hashedChallenge)

        # Remember it
        setLastChallenge(challenge)

        # Receive back the response from the server (Accepted / Denied)
        type, response = parseMessage(sock.recv(BUFFER_SIZE))
        print response

        if type != MessageType.ACK:
            sock.close()
            os._exit(0)


# Handles the interaction with the user
def talkToServer(sock):
    print "Type anything to write to the server, type '"+CLOSING_MESSAGE+"' to exit"
    input = raw_input()
    while input != CLOSING_MESSAGE:
        sendMessage(sock, MessageType.MESSAGE, input)
        input = raw_input()

    #Gets here when the user wants to close the connection
    sendMessage(sock, MessageType.MESSAGE, CLOSING_MESSAGE)
    sock.close()
    os._exit(0)


# Initiate the connection
def connect(password):
    passHash = encode(password)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Try to connect to the server
    try:
        sock.connect((TCP_IP, TCP_PORT))
    except socket.error:
        print "Connection Refused"
        return False

    # send hashed password
    sock.send(passHash)

    # Wait for the server response
    type, response = parseMessage(sock.recv(BUFFER_SIZE))

    # If the password is wrong
    if type == MessageType.NACK:
        print response
        sock.close()
    # If the password is correct
    elif type == MessageType.ACK:
        thread.start_new_thread(handleChallenges, (sock, password, ))
        talkToServer(sock)
        sock.close()


if __name__ == '__main__':
    password = getpass.getpass(prompt="Enter Password: ")
    connect(password)
