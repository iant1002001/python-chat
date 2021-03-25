import socket
import select

#Setting constants.
HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 3000

#Setting the server socket to allow multiple connections.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#Opening the server socket for connections.
server_socket.bind((IP, PORT))
server_socket.listen()

sockets_list = [server_socket]
#Storing connected clients in a dictionary.
#The client has a socket as its key with user information as its data.
clients = {}


def receive_message(client_socket):
    try:
        #Receives the message header from the client.
        message_header = client_socket.recv(HEADER_LENGTH)

        #This handles a client closing their connection.
        #The server receives no message data when a client disconnects.
        if not len(message_header):
            return False

        #Convert the message header into a length.
        message_length = int(message_header.decode('utf-8'))

        #Return the actual message data.
        return {'header': message_header, 
                'data': client_socket.recv(message_length)}

    except:
        # This exception occurs on empty messages or a client crashing.
        return False

