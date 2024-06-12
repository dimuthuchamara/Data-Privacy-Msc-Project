import socket
import threading
from cryptography.fernet import Fernet
import binascii
import sys

# Constants for communication channel
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

# Generate a secret key for encryption
key = Fernet.generate_key()
print("Secret Key:", key.decode())  # Print the secret key for reference

# Create a server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# Start the server
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_clients, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

# Handle client connections and data encryption
def handle_clients(conn, addr):
    print(f"[NEW CONNECTION] {addr} Connected.")
    print("[STARTING] Server is starting...")

    print("*** WELCOME TO MEASURING PRIVACY LEVEL FOR DATA SHARING SYSTEM ***")
    while True:
        print("OPTIONS:")
        print("1. Receive File")
        print("2. Send File")
        print("3. Exit")
        user_choice = int(input("Enter your Choice: "))
        if user_choice == 1:
            print("*** CHOOSE ENCRYPTION METHOD ***")
            print("1. Weak Encryption (XOR Cipher)")
            print("2. Strong Encryption (AES128)")
            user_input = int(input("Choose Option (1/2): "))
            if user_input == 1:
                filename = input("Please enter the filename: ")
                f = Fernet(key)
                with open(filename, "rb") as file:
                    file_data = file.read(9000000)
                    # Weak encryption using XOR cipher
                    data = bytearray(file_data)
                    for index, value in enumerate(data):
                        data[index] = value ^ 20

                    conn.send(data)
                    print("YOUR FILE HAS BEEN SUCCESSFULLY SENT")

            elif user_input == 2:
                filename = input("Please enter the filename: ")
                f = Fernet(key)
                with open(filename, "rb") as file:
                    file_data = file.read(9000000)
                    # Strong encryption using AES128
                    if filename.endswith('.txt'):
                        data = bytearray(file_data)  # for text file
                    elif filename.endswith('.jpg'):
                        data = binascii.hexlify(file_data)  # for image file

                encrypted_data = f.encrypt(file_data)
                conn.send(encrypted_data)
                print("YOUR FILE HAS BEEN SUCCESSFULLY SENT")

            conn.close()

        elif user_choice == 2:
            print("*** CHOOSE ENCRYPTION METHOD ***")
            print("1. Weak Encryption (XOR Cipher)")
            print("2. Strong Encryption (AES128)")
            user_input = int(input("Choose Option (1/2): "))
            if user_input == 1:
                filename = input("Please enter the filename: ")
                f = Fernet(key)
                with open(filename, "rb") as file:
                    file_data = file.read(9000000)
                    data = bytearray(file_data)
                    for index, value in enumerate(data):
                        data[index] = value ^ 20

                    conn.send(data)
                    print("YOUR FILE HAS BEEN SUCCESSFULLY SENT")

            elif user_input == 2:
                filename = input("Please enter the filename: ")
                f = Fernet(key)
                with open(filename, "rb") as file:
                    file_data = file.read(9000000)
                    if filename.endswith('.txt'):
                        data = bytearray(file_data)  # for text file
                    elif filename.endswith('.jpg'):
                        data = binascii.hexlify(file_data)  # for image file

                encrypted_data = f.encrypt(file_data)
                conn.send(encrypted_data)
                print("YOUR FILE HAS BEEN SUCCESSFULLY SENT")

            conn.close()

        elif user_choice == 3:
            break

        else:
            print("Please enter a valid input!")

    print("[CLOSING CONNECTION] Connection to", addr, "is closed.")

print("[STARTING] Server is starting...")
start()
