#!/bin/bash

### Protecting against portscans
### Attacking IP will be locked for 24 hours (3600 x 24 = 86400 Seconds)
iptables -A INPUT -m recent --name portscan --rcheck --seconds 86400 -j DROP
iptables -A FORWARD -m recent --name portscan --rcheck --seconds 86400 -j DROP

### Remove attacking IP after 24 hours
iptables -A INPUT -m recent --name portscan --remove
iptables -A FORWARD -m recent --name portscan --remove

iptables -A INPUT -p tcp -i eth0 -m state --state NEW -m recent --set
iptables -A INPUT -p tcp -i eth0 -m state --state NEW -m recent --update --seconds 30 --hitcount 5 -j DROP
iptables -A FORWARD -p tcp -i eth0 -m state --state NEW -m recent --set
iptables -A FORWARD -p tcp -i eth0 -m state --state NEW -m recent --update --seconds 30 --hitcount 5 -j DROP