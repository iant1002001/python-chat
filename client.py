import socket
import errno
from threading import Thread


HEADER_LENGTH = 10
client_socket = None


# Connects to the server
def connect(ip, port, my_username, error_message):

    global client_socket

    # Create a socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to a given ip and port
        client_socket.connect((ip, port))
    except Exception as e:
        # Connection error
        error_message(f"Connection error: {str(e)}")
        return False

    # Encode the username input to prepare it for
    # the server, then send it.
    username = my_username.encode('utf-8')
    username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(username_header + username)

    return True

# Sends a message to the server
def send(message):
    # Encode message information and send it
    message = message.encode('utf-8')
    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(message_header + message)

# Starts the listen function in a thread
def start_listening(incoming_message, error_message):
    Thread(target=listen, args=(incoming_message, error_message), daemon=True).start()

# Listens for incoming messages
def listen(incoming_message, error_message):
    while True:

        try:
            # Loop through received messages and print them
            while True:

                # Receive username and message information 
                # being broadcast by the server and decode it
                username_header = client_socket.recv(HEADER_LENGTH)
                # If we received no data,
                # the server closed a client connection.
                if not len(username_header):
                    error_message('Connection closed by the server')

                username_length = int(username_header.decode('utf-8'))
                username = client_socket.recv(username_length).decode('utf-8')

                message_header = client_socket.recv(HEADER_LENGTH)
                message_length = int(message_header.decode('utf-8'))
                message = client_socket.recv(message_length).decode('utf-8')

                # Package the username and message together
                # for ease of use later on.
                incoming_message(username, message)

        except Exception as e:
            error_message(f"Read error: {str(e)}")