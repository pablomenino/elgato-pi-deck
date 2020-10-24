#!/bin/bash

#----------------------------------------------------------------------------------------
# elgato-pi-deck
# Version: 0.9.2
# 
# WebSite:
# https://www.mfwlab.com
# 
# Copyright © 2020 - Pablo Meniño <pablo.menino@mfwlab.com>
#----------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------
# Uninstall elgato-pi-deck

if [ "$EUID" -ne 0 ]; then
    echo "This script must be run as root!!!"
    exit 1
fi

# Stop service
systemctl stop elgato-pi-deck.service
systemctl disable elgato-pi-deck.service

# remove udev rules
rm /etc/udev/rules.d/20-elgato-pi-deck.rules
# Reload udev rules
udevadm control --reload-rules
udevadm trigger

# remove systemd service
rm /etc/systemd/system/elgato-pi-deck.service

# reload systemd daemon
systemctl daemon-reload

#----------------------------------------------------------------------------------------
# Exit

exit 0
#----------------------------------------------------------------------------------------
