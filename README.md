## Setup
### 1. Clone Repository
1. Clone github Repository into your /root folder ```git clone https://github.com/JosipHarambasic/MTDFramework.git```

### 2. Setup Service
1. Copy the mtd.service into the folder /etc/systemd/system/
2. Or just create new file with name <name>.service and add code from mtd.service into it

### 3. Start service
If you did not change the filename of the provided mtd.service than you can use this commands, otherwise use the name you specified
1. run command ```systemctl enable mtd.service```
2. run command ```systemctl start mtd.service```
3. check the status if active ```systemctl status mtd.service```
If the status shows active --> then everything is set up

### 4. Execute MTD solution
1. on default the firewall will be set up after 5 seconds as soon as the mtd.service is start
2. navigate into the MTDFramework and then execute either ```python3 client.py --attack cj``` or ```python3 client.py --attack recon```