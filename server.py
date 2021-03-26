import socket
import select

# Setting constants.
HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 3000

# Setting the server socket to allow multiple connections.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Opening the server socket for connections.
server_socket.bind((IP, PORT))
server_socket.listen()

sockets_list = [server_socket]
# Storing connected clients in a dictionary.
# The client has a socket as its key with user information as its data.
clients = {}


def receive_message(client_socket):
    try:
        # Receives the message header from a client.
        message_header = client_socket.recv(HEADER_LENGTH)

        # This handles a client closing their connection.
        # The server receives no message data when a client exits.
        if not len(message_header):
            return False

        # Convert the message header into a length.
        message_length = int(message_header.decode('utf-8'))

        # Return the actual message data.
        return {'header': message_header,
                'data': client_socket.recv(message_length)}

    except:
        # This exception occurs on empty messages or a client crashing.
        return False


# Continuously receive and send messages to/from all client sockets.
while True:
    # Using select.select to use OS level I/O for the sockets.
    # select.select takes in read list, write list, and exception list.
    # We don't need to access the write list, so I left it unnamed.
    read_sockets, _, exception_sockets = select.select(
        sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket is server_socket:
            # A new client is accepted into the server
            client_socket, client_address = server_socket.accept()
            # Receive a username from the client
            user = receive_message(client_socket)
            # If no username is received, 
            # the client disconnected and we continue on.
            if user is False:
                continue
            # Adds the accepted socket to the select.select() list.
            sockets_list.append(client_socket)
            # Saves the username and username header
            # to the client dictionary with client_socket as its key.
            clients[client_socket] = user
            # Prints out client information for debugging.
            print(
                f"Accepted a new connection from {client_address[0]}:"
                f"{client_address[1]}, "
                f"username:{user['data'].decode('utf-8')}")
        else:
            # If the notified socket is not the server,
            # it means that a client has sent a message.
            message = receive_message(notified_socket)
            # If the message is empty, handle for client disconnecting.
            if message is False:
                print(
                    "Closed the connection from "
                    f"{clients[notified_socket]['data'].decode('utf-8')}")
                # Remove the client from our list and dictionary.
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            # Get the user that sent a message.
            user = clients[notified_socket]
            # Print the message for debugging.
            print(
                f"Received a message from {user['data'].decode('utf-8')}: "
                f"{message['data'].decode('utf-8')}")

            # Iterate through connected clients to broadcast to.
            for client_socket in clients:
                # Broadcast the message to everybody but the sender.
                if client_socket is not notified_socket:
                    client_socket.send(
                        user['header']
                        + user['data']
                        + message['header']
                        + message['data'])

    # If a client causes an exception, remove them from the server.
    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
        