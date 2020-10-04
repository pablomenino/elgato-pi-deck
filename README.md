<h3 align="center">elgato-pi-deck</h3>
<h3 align="center">Version: 0.8</h3>
<p align="center">elgato-pi-deck - Is a puthon script to control Elgato Stream Deck and send actions to elgato-pi-deck-server.</p>

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

Yo can assign new butons editing the python script.

And I have to write the documentation to edit the script and make a configuration file to be more simple.

In case to unisntall:

```
sudo ./uninstall.sh
```

## <a name="To-Do">To-Do

* Write documentation to edit script
* Generate a config file to add actions/buttons more simple
* Create a configuration GUI
