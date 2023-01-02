#!/bin/bash
apt-get install python3-venv
mkdir /opt/MTDFramework
python3 -m venv /opt/MTDFramework/venv3
source /opt/MTDFramework/venv3/bin/activate
deactivate

systemctl daemon-reload
systemctl enable MTDFramework
systemctl start MTDFramework