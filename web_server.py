from socket import *
import sys

# Create an IPv4-TCP socket
server_socket = socket(AF_INET, SOCK_STREAM)
port_num = 6789
# Bind socket to a port and have it listen there
server_socket.bind(('', port_num))     # Bind a port to socket
server_socket.listen(1)                # Accepts only 1 client at a time

# Continously do the following:
while True:
    # Establish the connection
    print('Server is ready to serve...')
    connectionSocket, addr = server_socket.accept()     # If there is a request, accept and open a new data socket

    try:
        http_message = connectionSocket.recv(1024).decode()
        print(http_message)
        filename = http_message.split()[1]   # Gets the filename from HTTP request message
        f = open(filename[1:])               # Shave off '/' from filename, and open file

        # Send HTTP response message
        outputdata = "HTTP/1.1 200 OK\r\n\r\n" + f.read()   # HTTP header appended to data
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())   # Ex: 'C' -> '01101100' ASCII
        connectionSocket.send("\r\n".encode())

        connectionSocket.close()
    except IOError:
        print("File Not Found")

        # Send response message for file not found
        outputdata = "HTTP/1.1 404 Not Found\r\n\r\n" + "File Not FOOOOOD"
        connectionSocket.send(outputdata.encode())
        connectionSocket.send("\r\n".encode())
        # Close client socket
        # Fill in start
        connectionSocket.close()
        # Fill in end

    server_socket.close()
    sys.exit()  # Terminate the program after sending the corresponding data
