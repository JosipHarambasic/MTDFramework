#!/bin/sh
### Script is for stopping Portscan and increase the time for a portscan

### first flush all the iptables Rules
iptables -F
iptables -X

############## INPUT iptables Rules ##############
### Accept loopback interface
iptables -A INPUT -i lo -p all -j ACCEPT

### add a rule to explicitly allow all traffic related to an existing connection
### in our case it is the already established connection to the ElectroSense platform
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

### Dropping all invalid packets, since those are reconnaissance attack packets
iptables -A INPUT -m state --state INVALID -j DROP
iptables -A FORWARD -m state --state INVALID -j DROP

### Protecting against port scans
### Attacking IP will be blocked for all connections for 24 hours (3600 x 24 = 86400 Seconds)
### port scans are still possible, because of stealth scan --> already changed MAC address
iptables -A INPUT -m recent --name portscan --rcheck --seconds 86400 -j DROP
iptables -A FORWARD -m recent --name portscan --rcheck --seconds 86400 -j DROP

### Remove attacking IP after 24 hours
iptables -A INPUT -m recent --name portscan --remove
iptables -A FORWARD -m recent --name portscan --remove

iptables -A INPUT -p tcp -m tcp --dport 139 -m recent --name portscan --set -j LOG --log-prefix "portscan:"
iptables -A INPUT -p tcp -m tcp --dport 139 -m recent --name portscan --set -j DROP

iptables -A FORWARD -p tcp -m tcp --dport 139 -m recent --name portscan --set -j LOG --log-prefix "portscan:"
iptables -A FORWARD -p tcp -m tcp --dport 139 -m recent --name portscan --set -j DROP

iptables -A INPUT -p tcp --dport 80 -i eth0 -m state --state NEW -m recent --set
iptables -A INPUT -p tcp --dport 80 -i eth0 -m state --state NEW -m recent --update --seconds 30 --hitcount 2 -j DROP

iptables -A INPUT -p tcp --dport 443 -i eth0 -m state --state NEW -m recent --set
iptables -A INPUT -p tcp --dport 443 -i eth0 -m state --state NEW -m recent --update --seconds 30 --hitcount 2 -j DROP

### Keep the following ports through open to the public
iptables -A INPUT -p tcp -m tcp --dport 25 -j ACCEPT
iptables -A INPUT -p tcp -m tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp -m tcp --dport 443 -j ACCEPT
iptables -A INPUT -p tcp -m tcp --dport 22 -j ACCEPT

### Allow ping means ICMP port is open (If you do not want ping replace ACCEPT with REJECT)
iptables -A INPUT -p icmp -m icmp --icmp-type 8 -j ACCEPT

### Lastly reject All INPUT traffic
iptables -A INPUT -j REJECT

################# Below are for OUTPUT iptables rules #####################

### Allow loopback OUTPUT
iptables -A OUTPUT -o lo -j ACCEPT
iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

iptables -A OUTPUT -p tcp -m tcp --dport 25 -j ACCEPT
iptables -A OUTPUT -p udp -m udp --dport 53 -j ACCEPT
iptables -A OUTPUT -p tcp -m tcp --dport 80 -j ACCEPT
iptables -A OUTPUT -p tcp -m tcp --dport 443 -j ACCEPT
iptables -A OUTPUT -p tcp -m tcp --dport 22 -j ACCEPT

### Allow pings
iptables -A OUTPUT -p icmp -m icmp --icmp-type 8 -j ACCEPT

### Lastly Reject all Output traffic
iptables -A OUTPUT -j REJECT

### Reject Forwarding  traffic
iptables -A FORWARD -j REJECT
