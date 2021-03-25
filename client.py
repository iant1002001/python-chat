import socket
import select
import errno
import sys

# Set constants
HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 3000

#Set username, setup client for connection to the server
my_username = input("Username: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

# Encode the username input to prepare it for the server, then send it.
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

# Loop through sending messages on the client
while True:
    message = input(f"{my_username} > ")

    # If message isn't blank, encode it and send it
    if message:
        message = message.encode('utf-8')
        message_header = f"{len(message) :< {HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)

    try:
        # Loop through receiving messages
        while True:
            # Receive username and message information 
            # being broadcast by the server and decode it
            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                print("Connection closed by the server.")
                sys.exit()
            username_length = int(username_header.decode('utf-8'))
            username = client_socket.recv(username_length).decode('utf-8')

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8'))
            message = client_socket.recv(message_length).decode('utf-8')

            print(f"{username} > {message}")

    except IOError as e:
        if e.errno is not errno.EAGAIN and e.errno is not errno.EWOULDBLOCK:
            print('Read error', str(e))
            sys.exit()
        continue

    except Exception as e:
        print('General error',str(e))
        sys.exit()