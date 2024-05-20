import socket

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
