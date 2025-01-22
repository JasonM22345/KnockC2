# KnockC2

**KnockC2** is a Command and Control (C2) system that simulates secure communication and remote command execution between a server and a client using a sophisticated port-knocking mechanism. This project demonstrates the use of sockets for establishing and managing secure connections, as well as executing commands in a controlled environment. The C2 server can be deployed on a Wide Area Network (WAN) while the clients operate on a Local Area Network (LAN).

---

## Features

1. **Port-Knock Sequence**

   - The system employs a three-phase port-knocking mechanism to authenticate clients before allowing communication.
   - Each phase involves the client sending hashed values based on a predetermined string and the current time. This ensures that only authorized clients can connect.

2. **Dynamic Port Configuration**

   - The C2 server initially listens on port `8007`.
   - Upon successful port-knock authentication, a new port (`8008`) is dynamically opened for secure communication.

3. **Command Execution**

   - After authentication, the server provides a command menu for interacting with the client:
     - **Get Machine Info**: Retrieve detailed information about the client VM.
     - **Upload File**: Transfer a file (e.g., `file.txt`) from the client to the server.
     - **Close Connection**: Terminate the communication session.
     - **Shutdown Client**: Shut down the client machine.

4. **Intrusion Detection System (IDS) Evasion**

   - Default IDS solutions like Snort and Suricata are not designed to detect this system without custom rules specifically targeting the port-knocking sequence.
   - Even with custom rules, detection is not guaranteed, particularly if the exfiltrated data is encrypted or not transmitted in clear text.

5. **Real-World Relevance**

   - The system’s stealthy design emphasizes the challenges of detecting advanced malware-like behavior.
   - Manual analysis and custom rule creation are often required to identify and mitigate such threats.

---

## Project Structure

- **`server.py`**: Implements the C2 server functionality, including socket management, port-knock sequence validation, and command execution.
- **`client.py`**: Simulates the malware client, which connects to the server, performs the port-knock sequence, and executes received commands.
- **`file.txt`**: A sample file used to demonstrate the file upload feature.
- **`README.md`**: Project documentation and usage instructions.

---

## How It Works

### `server.py` - The C2 Server

The server uses sockets to listen for incoming connections on port `8007`. It validates the client’s port-knocking sequence by checking the hashes sent in three phases. Upon successful validation, it dynamically opens port `8008` for secure command and control operations. The server allows the execution of predefined commands, leveraging sockets to send and receive data between the server and client.

### `client.py` - The Malware Implant

The client connects to the server using sockets and performs the three-phase port-knock sequence. The client sends hashed values of a predetermined string and the current time to authenticate with the server. After authentication, it listens for commands from the server and executes them accordingly. For example, it can gather machine information, upload files via sockets, or shut down the machine.

### `file.txt` - Sample File

The file serves as a demonstration of the file transfer functionality. The client reads the file in chunks and sends it to the server using sockets. The server reconstructs the file and saves it locally.

---

## Real-World Relevance

KnockC2 demonstrates the challenges of detecting advanced malware using traditional intrusion detection systems. The port-knocking mechanism evades general IDS detection by design. Systems like Snort and Suricata require manual intervention to craft custom rules targeting the specific behavior of the port-knocking sequence. Even with such rules, detection is not guaranteed, particularly if exfiltrated data is encrypted or obscured.

This project highlights the importance of proactive threat hunting and advanced detection strategies to counter stealthy malware in real-world scenarios.

---

## Usage Instructions

### Prerequisites

- Python 3.7 or higher
- Linux environment

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/JasonM22345/KnockC2.git
   cd KnockC2
   ```

2. Start the server on the WAN VM:

   ```bash
   python3 server.py
   ```

3. Start the client on the LAN VM:

   ```bash
   python3 client.py
   ```

4. Follow the prompts on the server to execute commands.

---



## Disclaimer

This project is for **educational purposes only**. It demonstrates advanced networking concepts and secure communication techniques in a simulated environment. Misuse of this system for malicious purposes is strictly prohibited.

