import socket

def send_message(host, port, message):
    try:
        # Create a socket connection to the server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        # Send the message to the server
        client_socket.sendall(message.encode())

        # Close the socket connection
        client_socket.close()
        print(f"Message '{message}' sent successfully to {host}:{port}")
    except Exception as e:
        print(f"Error occurred while sending message: {e}")

if __name__ == "__main__":
    host = "localhost"  # Set the host where the server is running
    port = 12345        # Set the port on which the server is listening

    while True:
        # Get user input for the message to send
        message = input("Enter message to send ('q' to quit): ")
        if message.lower() == "q":
            break  # Exit the loop if 'q' is entered

        # Send the message to the server
        send_message(host, port, message)
