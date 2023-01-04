#!/bin/bash
iptables -F
iptables -X
iptables -N portscan
iptables -A portscan -j LOG --log-level 4 --log-prefix 'Blocked_scans '
iptables -A portscan -j DROP
iptables -N UDP
iptables -A UDP -j LOG --log-level 4 --log-prefix 'UDP_FLOOD '
iptables -A UDP -p udp -m state --state NEW -m recent --set --name UDP_FLOOD
iptables -A UDP -j DROP
iptables -N domainscan
iptables -A domainscan -j LOG --log-level 4 --log-prefix 'Blocked_domain_scans '
iptables -A domainscan -p tcp -m state --state NEW -m recent --set --name Webscanners
iptables -A domainscan -j DROP
iptables -A INPUT -s 10.0.0.0/24 -j ACCEPT
iptables -A INPUT -p tcp -m tcp --destination-port 32768:61000 -j ACCEPT
iptables -A INPUT -m state --state ESTABLISHED -j ACCEPT
iptables -I INPUT -i lo -j ACCEPT
iptables -I INPUT -m recent --name whitelist --rcheck -j ACCEPT
iptables -A INPUT -m recent --name portscan --rcheck --seconds 86400 -j portscan
iptables -A INPUT -m recent --name UDP_FLOOD --rcheck --seconds 86400 -j portscan
iptables -A INPUT -m recent --name portscan --remove
iptables -A INPUT -m recent --name UDP_FLOOD --remove
iptables -A INPUT -p tcp -m tcp --destination-port 443 -j ACCEPT
iptables -A INPUT -p tcp -m tcp --destination-port 22 -j ACCEPT
iptables -A INPUT -p tcp -m tcp -m recent -m state --state NEW --name portscan --set -j portscan
iptables -A INPUT -p udp -m state --state NEW -m recent --set --name Domainscans
iptables -A INPUT -p udp -m state --state NEW -m recent --rcheck --seconds 5 --hitcount 5 --name Domainscans -j UDP