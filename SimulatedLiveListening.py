import socket

# Define the host and port to listen on
host = 'localhost'
port = 12345

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the host and port
server_socket.bind((host, port))

# Listen for incoming connections (maximum of 1 pending connection)
server_socket.listen(1)
print(f"Listening on {host}:{port}...")

try:
    # Accept a connection
    client_socket, addr = server_socket.accept()
    print(f"Connection established from {addr}")

    while True:
        # Receive data from the client
        data = client_socket.recv(1024)  # Adjust buffer size as needed
        
        if not data:
            break
        
        # Decode the received message (assuming UTF-8 encoding)
        received_message = data.decode().strip()  # Convert bytes to string and strip whitespace
        
        # Convert the received message (string) to an integer
        received_integer = float(received_message)

        # Process the received integer (e.g., print it)
        print(f"Received integer: {received_integer}")
        
except Exception as e:
    print(f"Error occurred: {e}")

finally:
    # Close the client socket
    client_socket.close()

    # Close the server socket
    server_socket.close()
