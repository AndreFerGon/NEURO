import socket

<<<<<<< HEAD
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
=======
def main():
    host = 'localhost'
    port = 12345

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")

        while True:
            user_input = input("Enter a label (0 - 1 - 2 - 3 - 4): ")
            if user_input.isdigit() and int(user_input) in range(5):
                client_socket.sendall(user_input.encode())
                print(f"Sent: {user_input}")
            else:
                print("Invalid input! Please enter a number between 0 and 4.")

    except Exception as e:
        print(f"Error occurred: {e}")

    finally:
        client_socket.close()
        print("Connection closed.")

if __name__ == "__main__":
    main()
>>>>>>> cbcc04a0f60b4a6ae28dc0774c11d62abba3ae98
