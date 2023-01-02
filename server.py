import os
import socket
import logging
import subprocess

log = logging.getLogger("main")
logging.basicConfig(level=logging.INFO)

# Standard loopback interface address (localhost) else specify one, also needs to be specified on client
HOST = ""

# Port to listen on (non-privileged ports are > 1023)
PORT = 1234

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if HOST == "":
        s.bind((socket.gethostname(), PORT))
    else:
        s.bind((HOST, PORT))

    # Allow 5 connections at same time
    s.listen(5)
    while True:
        clientSocket, address = s.accept()
        print(f"Connection form {address}")
        attack = clientSocket.recv(1024).decode('utf-8')
        if attack == "recon":
            currentPath = os.getcwd() + "/ReconnaissanceMitigation"
            os.chdir(currentPath)
            if os.path.exists(currentPath + "/recon.sh"):
                print("Executing Reconnaissance itigation")
                subprocess.Popen("sh recon.sh", shell=True, stdin=subprocess.PIPE)
        elif attack == "cj":
            currentPath = os.getcwd() + "/CryptojackerMitigation"
            os.chdir(currentPath)
            if os.path.exists(currentPath + "/main.py"):
                print("Executing Cryptojacker mitigation")
                subprocess.Popen("python3 main.py", shell=True, stdin=subprocess.PIPE)


if __name__ == '__main__':
    main()
