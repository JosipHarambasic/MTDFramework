#!/bin/sh
### Script is for stopping Portscan and increase the time for a portscan

### first flush all the iptables Rules
iptables -F
iptables -X


### INPUT iptables Rules
### Accept loopback input
iptables -A INPUT -i lo -p all -j ACCEPT

### add a rule to explicitly allow all traffic related to an existing connection
### in our case it is the already established connection to the ElectroSense platform
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

### DROP spoofing packets
iptables -A INPUT -s 10.0.0.0/8 -j DROP
iptables -A INPUT -s 169.254.0.0/16 -j DROP
iptables -A INPUT -s 172.16.0.0/12 -j DROP
iptables -A INPUT -s 127.0.0.0/8 -j DROP
# iptables -A INPUT -s 192.168.0.0/24 -j DROP

iptables -A INPUT -s 224.0.0.0/4 -j DROP
iptables -A INPUT -d 224.0.0.0/4 -j DROP
iptables -A INPUT -s 240.0.0.0/5 -j DROP
iptables -A INPUT -d 240.0.0.0/5 -j DROP
iptables -A INPUT -s 0.0.0.0/8 -j DROP
iptables -A INPUT -d 0.0.0.0/8 -j DROP
iptables -A INPUT -d 239.255.255.0/24 -j DROP
iptables -A INPUT -d 255.255.255.255 -j DROP

### Dropping all invalid packets, since those are reconnaissance attack packets
iptables -A INPUT -m state --state INVALID -j DROP

### if we allow this then information about the OS are shown else not
iptables -A FORWARD -m state --state INVALID -j DROP

### We can also drop the state but this will cause that we can't detect the IP address, this is
### unfortunate since we would like to get IP address to be able to connect to it
# iptables -A OUTPUT -m state --state INVALID -j DROP

### flooding of RST packets, smurf attack Rejection
iptables -A INPUT -p tcp -m tcp --tcp-flags RST RST -m limit --limit 2/second --limit-burst 2 -j ACCEPT

### Protecting against portscans
### Attacking IP will be locked for 24 hours (3600 x 24 = 86400 Seconds)
iptables -A INPUT -m recent --name portscan --rcheck --seconds 500 -j DROP
iptables -A FORWARD -m recent --name portscan --rcheck --seconds 500 -j DROP

### Remove attacking IP after 24 hours
iptables -A INPUT -m recent --name portscan --remove
iptables -A FORWARD -m recent --name portscan --remove

iptables -A INPUT -p tcp -i eth0 -m state --state NEW -m recent --set
iptables -A INPUT -p tcp -i eth0 -m state --state NEW -m recent --update --seconds 30 --hitcount 5 -j DROP
iptables -A FORWARD -p tcp -i eth0 -m state --state NEW -m recent --set
iptables -A FORWARD -p tcp -i eth0 -m state --state NEW -m recent --update --seconds 30 --hitcount 5 -j DROP
### Allow the following ports through from outside
### SMTP mail sender = 25
### DNS =53
### HTTP = 80
### HTTPS = 443
### SSH = 22

### Keep the following ports through open to the public
iptables -A INPUT -p tcp -m tcp --dport 25 -j ACCEPT
iptables -A INPUT -p tcp -m tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp -m tcp --dport 443 -j ACCEPT
iptables -A INPUT -p tcp -m tcp --dport 22 -j ACCEPT

### Allow ping means ICMP port is open (If you do not want ping replace ACCEPT with REJECT)
iptables -A INPUT -p icmp -m icmp --icmp-type 8 -j ACCEPT

### Lastly reject All INPUT traffic
iptables -A INPUT -j REJECT

################# Below are for OUTPUT iptables rules #############################################

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
