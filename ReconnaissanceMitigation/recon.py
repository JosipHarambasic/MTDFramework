import random
import subprocess


def main():
    # Change mac address which will lead to a change in the IP address
    subprocess.Popen("ifconfig eth0 down", shell=True, stdin=subprocess.PIPE)
    newMACAddress = "02:00:00:%02x:%02x:%02x" % (random.randint(0, 255),
                                                 random.randint(0, 255),
                                                 random.randint(0, 255))
    subprocess.Popen("ifconfig eth0 hw ether " + newMACAddress, shell=True, stdin=subprocess.PIPE)
    subprocess.Popen("ifconfig eth0 up", shell=True, stdin=subprocess.PIPE)


if __name__ == "__main__":
    main()
