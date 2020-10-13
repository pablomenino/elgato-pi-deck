<h3 align="center">elgato-pi-deck</h3>
<h3 align="center">Version: 0.9</h3>
<p align="center">elgato-pi-deck - Is a python script to control Elgato Stream Deck and send actions to elgato-pi-deck-server.</p>

<p align="center">
<a href="https://github.com/pablomenino/elgato-pi-deck/releases"><img src="https://img.shields.io/github/release/pablomenino/elgato-pi-deck.svg"></a>
<a href="./LICENSE"><img src="https://img.shields.io/github/license/pablomenino/elgato-pi-deck.svg"></a>
</p>

**This is the client part of [elgato-pi-deck](https://github.com/pablomenino/elgato-pi-deck/) and works with [elgato-pi-deck-server](https://github.com/pablomenino/elgato-pi-deck-server/)**

**This is a basic script to be used like a template or idea of something more complex that you need**

## Table of contents

* [How to Use](#how-to-use)
* [To-Do](#To-Do)

## <a name="how-to-use">How to Use

#### Requirements

* Python 3
* Raspbian or Raspberry PI OS
* python3-pip
* python3-setuptools
* libudev-dev
* libusb-1.0-0-dev
* libhidapi-libusb0
* libjpeg-dev
* zlib1g-dev
* Pillow => 7.1.2
* streamdeck => 0.8.1
* wakeonlan => 1.1.6
* wheel => 0.32.3

**Install packages:**

```
sudo apt install -y python3-pip python3-setuptools
sudo apt install -y libudev-dev libusb-1.0-0-dev libhidapi-libusb0
sudo apt install -y libjpeg-dev zlib1g-dev
```

**Install Python packages:**

```
sudo pip3 install wheel
sudo pip3 install pillow
sudo pip3 install streamdeck
sudo pip3 install wakeonlan
```

#### Usage

<a href="https://raw.githubusercontent.com/pablomenino/elgato-pi-deck-server/master/Assets/diagam.png"><img src="https://raw.githubusercontent.com/pablomenino/elgato-pi-deck-server/master/Assets/diagam.png" width="380"></a>

In this case you are on Raspberry PI:

Clone this repo in /opt

```
cd /opt
sudo git clone https://github.com/pablomenino/elgato-pi-deck/
cd /opt/elgato-pi-deck/
```

Install:

```
sudo ./install.sh
```

Yo can assign new butons editing the configuration file.

Example config:

```
{
    "info": "elgato-pi-deck",
    "version": "0.9",
    "FONT_SRC": "Roboto-Regular.ttf",
    "FONT_SIZE": "16",
    "PANEL_SELECT": "0",
    "PANEL_BRIGHTNESS": "30",
    "PANEL_BRIGHTNESS_STEP": "10",
    "deck_poweron": "True",
    "panel0":
    [
        {
            "type": "gotopanel",
            "name": "Apps",
            "gotopanelid": "1",
            "image": "icons/utilities.png",
            "image_pressed": "icons/utilities-pressed.png"
        },
        {
            "type": "gotopanel",
            "name": "IoT",
            "gotopanelid": "2",
            "image": "icons/iot.png",
            "image_pressed": "icons/iot.png"
        },
        {
            "type": "wakeonlan",
            "name": "NAS",
            "image": "icons/1618plus.png",
            "image_pressed": "icons/1618plus.png",
            "nodename": "NAS",
            "nodeip": "192.168.0.22",
            "nodemac": "00:FF:AA:FF:AA:BB"
        },
        {
            "type": "bright0",
            "name": "Bright 0%",
            "image": "icons/brightness-0.png",
            "image_pressed": "icons/brightness-0.png"
        },
        {
            "type": "brightless",
            "name": "Bright -",
            "image": "icons/brightness-less.png",
            "image_pressed": "icons/brightness-less.png"
        },
        {
            "type": "brightmore",
            "name": "Bright +",
            "image": "icons/brightness-more.png",
            "image_pressed": "icons/brightness-more.png"
        },
        {
            "type": "bright100",
            "name": "Bright 100%",
            "image": "icons/brightness-100.png",
            "image_pressed": "icons/brightness-100.png"
        }
    ],
    "panel1":
    [
        {
            "type": "gotopanel",
            "name": "Back To Main Panel",
            "gotopanelid": "0",
            "image": "icons/back.png",
            "image_pressed": "icons/back-pressed.png"
        },
        {
            "type": "action",
            "name": "Firefox",
            "image": "icons/firefox.png",
            "image_pressed": "icons/firefox.png",
            "action": "firefox",
            "serverip": "192.168.0.10",
            "serverport": "8889"
        }
    ],
    "panel2":
    [
        {
            "type": "gotopanel",
            "name": "Back To Main",
            "gotopanelid": "0",
            "image": "icons/back.png",
            "image_pressed": "icons/back-pressed.png"
        },
        {
            "type": "webhook",
            "name": "Ligth CPU",
            "image": "icons/ligth.png",
            "image_pressed": "icons/ligth.png",
            "webhookurl": "http://192.168.0.48/api/webhook/200"
        }
    ]
}
```

## **Config info:**

You can change the font and size (edit config.json):

```
    "FONT_SRC": "Roboto-Regular.ttf",
    "FONT_SIZE": "16",
```

You can select wath panel to load at start up:

```
    "PANEL_SELECT": "0",
```

Set the initial screen brightness:

```
    "PANEL_BRIGHTNESS": "30",
```

Set display on/off in start up:

```
    "deck_poweron": "True",
```

By default the script assign the last key in panel (panel0) to power on/power off display.

You have severals type of buttons:

* gotopanel (select this to change the selected panel)

```
            "type": "gotopanel",
            "name": "Apps",
            "gotopanelid": "1",
            "image": "icons/utilities.png",
            "image_pressed": "icons/utilities-pressed.png"
```

**name:** name to display.

**gotopanelid:** is the panel id  to change.

Images path is in the Assets folder

* wakeonlan (To send wake on lan packet to node)

```
            "type": "wakeonlan",
            "name": "NAS",
            "image": "icons/1618plus.png",
            "image_pressed": "icons/1618plus.png",
            "nodename": "NAS",
            "nodeip": "192.168.0.22",
            "nodemac": "00:FF:AA:FF:AA:BB"
```

**name:** node name

**nodeip:** device ip address to check if alive

**nodemac:** device mac address

Images path is in the Assets folder

* bright0 (Set brightness to 0%)

```
            "type": "bright0",
            "name": "Bright 0%",
            "image": "icons/brightness-0.png",
            "image_pressed": "icons/brightness-0.png"
```

* brightless (Lower brightness level)

```
            "type": "brightless",
            "name": "Bright -",
            "image": "icons/brightness-less.png",
            "image_pressed": "icons/brightness-less.png"
```

* brightmore (Up brightness level)

```
            "type": "brightmore",
            "name": "Bright +",
            "image": "icons/brightness-more.png",
            "image_pressed": "icons/brightness-more.png"
```

* bright100 (Set brightness to 100%)

```
            "type": "bright100",
            "name": "Bright 100%",
            "image": "icons/brightness-100.png",
            "image_pressed": "icons/brightness-100.png"
```

* action (To send an action to server)

```
            "type": "action",
            "name": "Firefox",
            "image": "icons/firefox.png",
            "image_pressed": "icons/firefox.png",
            "action": "firefox",
            "serverip": "192.168.0.10",
            "serverport": "8889"
```

**name:** name to display

**action:** action to be executed on remote server

**serverip:** server ip address

**serverport:** server port

* webhook (post action to execute a webhook)

```
            "type": "webhook",
            "name": "Ligth CPU",
            "image": "icons/ligth.png",
            "image_pressed": "icons/ligth.png",
            "webhookurl": "http://192.168.0.48/api/webhook/200"
```

**name**: name to display
**webhookurl**: webhook address

## In case to unisntall:

```
sudo ./uninstall.sh
```

## <a name="To-Do">To-Do

* Write documentation to edit script
* Generate a config file to add actions/buttons more simple
* Create a configuration GUI
