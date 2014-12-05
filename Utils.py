TCP_IP = '127.0.0.1'
TCP_PORT = 8181
BUFFER_SIZE = 1024
SECRET = 'secret'
CLOSING_MESSAGE = 'quit'

class MessageType:
    CHALLENGE = 'CHA'
    MESSAGE = 'MSG'
    ACK = 'ACK'
    NACK = 'NAC'

def sendMessage(sock, messType, message):
    sock.send(messType + message)

def parseMessage(text):
    if text[0: len(MessageType.CHALLENGE)] == MessageType.CHALLENGE:
        return MessageType.CHALLENGE, text[len(MessageType.CHALLENGE):]
    elif text[0: len(MessageType.MESSAGE)] == MessageType.MESSAGE:
        return MessageType.MESSAGE, text[len(MessageType.MESSAGE):]
    elif text[0: len(MessageType.ACK)] == MessageType.ACK:
        return MessageType.ACK, text[len(MessageType.ACK):]
    else:
        return MessageType.NACK, text[len(MessageType.NACK):]