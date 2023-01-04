import subprocess


def main():
    # Clean iptables before adding actual rules
    subprocess.Popen("iptables -F", shell=True, stdin=subprocess.PIPE)
    subprocess.Popen("iptables -X", shell=True, stdin=subprocess.PIPE)

    # adding actual rules
    firewallConfiguration = [" -A INPUT -m recent --name portscan --rcheck --seconds 86400 -j DROP",
                             " -A FORWARD -m recent --name portscan --rcheck --seconds 86400 -j DROP",
                             " -A INPUT -m recent --name portscan --remove",
                             " -A FORWARD -m recent --name portscan --remove",
                             " -A INPUT -p tcp -i eth0 -m state --state NEW -m recent --set",
                             " -A INPUT -p tcp -i eth0 -m state --state NEW -m recent --update --seconds 60 --hitcount "
                             "3 -j DROP",
                             " -A FORWARD -p tcp -i eth0 -m state --state NEW -m recent --set",
                             " -A FORWARD -p tcp -i eth0 -m state --state NEW -m recent --update --seconds 60 "
                             "--hitcount 3 -j DROP",
                             " -A INPUT -p udp -m udp --dport 53 -j ACCEPT",
                             " -A INPUT -p tcp -m tcp --dport 80 -j ACCEPT",
                             " -A INPUT -p tcp -m tcp --dport 443 -j ACCEPT",
                             " -A INPUT -p tcp -m tcp --dport 22 -j ACCEPT",
                             " -A INPUT -p icmp -m icmp --icmp -type 8 -j ACCEPT",
                             " -A INPUT -j REJECT",
                             " -A OUTPUT -o lo -j ACCEPT",
                             " -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT",
                             " -A OUTPUT -p udp -m udp --dport 53 -j ACCEPT",
                             " -A OUTPUT -p tcp -m tcp --dport 80 -j ACCEPT",
                             " -A OUTPUT -p tcp -m tcp --dport 443 -j ACCEPT",
                             " -A OUTPUT -p tcp -m tcp --dport 22 -j ACCEPT",
                             " -A OUTPUT -p icmp -m icmp --icmp -type 8 -j ACCEPT",
                             " -A OUTPUT -j REJECT",
                             " -A FORWARD -j REJECT"
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
