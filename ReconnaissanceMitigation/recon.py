import random
import subprocess


def main():
    # Change mac address which will lead to a change in the IP address
    subprocess.Popen("ifconfig eth0 down", shell=True, stdin=subprocess.PIPE)

    # The prefix is needed by nmap to identify the Processor and OS on the device
    # By changing it to a random other prefix that exists we can obfuscate the attacker (Intel, Apple) prefix
    prefix = random.choice(["C8:86:29", "F0:9C:D7", "EC:D6:8A", "EC:23:68", "E0:61:B2", "DC:15:DB", "D4:EC:86",
                            "CC:8C:DA", "CC:2A:80", "C0:8B:6F", "68:3C:7D",
                            "94:0C:98", "90:FD:61", "90:E1:7B", "90:DD:5D", "90:C1:C6", "90:B9:31", "90:B2:1F"])
    newMACAddress = ":%02x:%02x:%02x" % (random.randint(0, 255),
                                         random.randint(0, 255),
                                         random.randint(0, 255))
    newMACAddress = prefix.lower() + newMACAddress
    subprocess.Popen("ifconfig eth0 hw ether " + newMACAddress, shell=True, stdin=subprocess.PIPE)
    subprocess.Popen("ifconfig eth0 up", shell=True, stdin=subprocess.PIPE)


if __name__ == "__main__":
    main()
