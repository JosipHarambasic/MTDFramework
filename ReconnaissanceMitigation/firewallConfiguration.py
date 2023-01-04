import subprocess


def main():
    # Clean iptables before adding actual rules
    subprocess.Popen("iptables -F", shell=True, stdin=subprocess.PIPE)
    subprocess.Popen("iptables -X", shell=True, stdin=subprocess.PIPE)

    # adding actual rules
    firewallConfiguration = [" -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT",
                             " -A INPUT -m recent --name portscan --rcheck --seconds 86400 -j DROP",
                             " -A FORWARD -m recent --name portscan --rcheck --seconds 86400 -j DROP",
                             " -A INPUT -m recent --name portscan --remove",
                             " -A FORWARD -m recent --name portscan --remove",
                             " -A INPUT -p tcp -i eth0 -m state --state NEW -m recent --set",
                             " -A INPUT -p tcp -i eth0 -m state --state NEW -m recent --update --seconds 60 --hitcount "
                             "3 -j DROP",
                             " -A FORWARD -p tcp -i eth0 -m state --state NEW -m recent --set",
                             " -A FORWARD -p tcp -i eth0 -m state --state NEW -m recent --update --seconds 60 "
                             "--hitcount 3 -j DROP",
                             " -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT",
                             ]
    print("Adding rules to iptables")
    counter = 0
    for i in firewallConfiguration:
        try:
            subprocess.Popen("iptables" + i, shell=True, stdin=subprocess.PIPE)
            counter += 1
        except:
            continue

    print(str(counter) + "/" + str(len(firewallConfiguration)) + " rules were added")


if __name__ == "__main__":
    main()
