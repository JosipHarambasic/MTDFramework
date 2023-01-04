import subprocess


def main():
    firewallConfiguration = [" -A INPUT -m recent --name portscan --rcheck --seconds 86400 -j DROP",
                             " -A FORWARD -m recent --name portscan --rcheck --seconds 86400 -j DROP",
                             " -A INPUT -m recent --name portscan --remove",
                             " -A FORWARD -m recent --name portscan --remove",
                             " -A INPUT -p tcp -i eth0 -m state --state NEW -m recent --set",
                             " -A INPUT -p tcp -i eth0 -m state --state NEW -m recent --update --seconds 30 --hitcount "
                             "5 -j DROP",
                             " -A FORWARD -p tcp -i eth0 -m state --state NEW -m recent --set",
                             " -A FORWARD -p tcp -i eth0 -m state --state NEW -m recent --update --seconds 30 "
                             "--hitcount 5 -j DROP "
                             ]
    for i in firewallConfiguration:
        subprocess.Popen("iptables" + i, shell=True, stdin=subprocess.PIPE)
        print("Added " + i + "Rule to iptables")


if __name__ == "__main__":
    main()
