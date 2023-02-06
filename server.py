import os
import socket
import logging
import subprocess
import time

log = logging.getLogger("main")
logging.basicConfig(level=logging.INFO)

# Standard loopback interface address (localhost) else specify one, also needs to be specified on client
HOST = ""

# listen on Port (non-privileged ports are > 1023)
PORT = 1235
workingDir = os.getcwd()


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if HOST == "":
        s.bind((socket.gethostname(), PORT))
    else:
        s.bind((HOST, PORT))

    # Allow 5 connections at same time
    s.listen(5)

    # wait 5 secs before start on boot, to allow ElectroSense Sensor
    time.sleep(5)
    currentPath = os.getcwd() + "/ReconnaissanceMitigation"
    os.chdir(currentPath)
    if os.path.exists(currentPath + "/recon.sh"):
        print("Setup firewall")
        subprocess.Popen("sh recon.sh", shell=True, stdin=subprocess.PIPE)
    os.chdir(workingDir)

    # start MTD solution deployer in background
    while True:
        clientSocket, address = s.accept()
        print("Connection form " + address)
        attack = clientSocket.recv(1024).decode('utf-8')
        if attack == "recon":
            currentPath = os.getcwd() + "/ReconnaissanceMitigation"
            os.chdir(currentPath)
            if os.path.exists(currentPath + "/recon.py"):
                print("Executing Reconnaissance mitigation")
                subprocess.Popen("python3 recon.py", shell=True, stdin=subprocess.PIPE)

        elif attack == "cj":
            currentPath = os.getcwd() + "/CryptojackerMitigation"
            os.chdir(currentPath)
            if os.path.exists(currentPath + "/main.py"):
                print("Executing Cryptojacker mitigation")
                subprocess.Popen("python3 main.py", shell=True, stdin=subprocess.PIPE)
        os.chdir(workingDir)


if __name__ == '__main__':
    main()
