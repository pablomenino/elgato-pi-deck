#!/bin/bash

#----------------------------------------------------------------------------------------
# elgato-pi-deck
# Version: 0.8
# 
# WebSite:
# https://www.mfwlab.com
# 
# Copyright © 2020 - Pablo Meniño <pablo.menino@mfwlab.com>
#----------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------
# Install elgato-pi-deck

if [ "$EUID" -ne 0 ]; then
    echo "This script must be run as root!!!"
    exit 1
fi

# copy udev rules
cp 20-elgato-pi-deck.rules /etc/udev/rules.d/
# Reload udev rules
udevadm control --reload-rules
udevadm trigger

# copy systemd service
cp elgato-pi-deck.service /etc/systemd/system/

# reload systemd daemon
systemctl daemon-reload

# Start service
systemctl enable elgato-pi-deck.service
systemctl start elgato-pi-deck.service

#----------------------------------------------------------------------------------------
# Exit

exit 0
#----------------------------------------------------------------------------------------
