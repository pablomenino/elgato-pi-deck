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
# Stop

kill $(ps aux | grep '/usr/bin/python3 /opt/elgato-pi-deck/elgato-pi-deck.py' | awk '{print $2}')
