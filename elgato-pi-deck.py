#!/usr/bin/env python3

#  elgato-pi-deck
# 
#  LICENSE: GPL 3.0
# 
#  @package    elgato-pi-deck
#  @author     Pablo Meniño
#  @copyright  Pablo Meniño (pablo.menino@mfwlab.com)
#  @license    http://www.gnu.org/licenses/gpl-3.0.html
#  @version    0.9.2
# 
#  @email      pablo.menino@mfwlab.com
#  @website    https://www.mfwlab.com
#
#  Based on StreamDeck Python Library example

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Load Modules
import os
import threading
import requests
# Load WakeOnLan Support
from wakeonlan import send_magic_packet
from PIL import Image, ImageDraw, ImageFont
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper
# Load JSON Support
import json
import os

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Load config from file

CONFIGDIR = os.path.dirname(os.path.realpath(__file__))

with open(CONFIGDIR + '/config.json') as json_file:
    config = json.load(json_file)

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# General config

# Folder location of image assets and fonts
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "Assets")
FONT_SRC = config['FONT_SRC']
# Default Panel to Display
PANEL_SELECT = int(config['PANEL_SELECT'])
# Default Brightness Configuration
PANEL_BRIGHTNESS = int(config['PANEL_BRIGHTNESS'])
PANEL_BRIGHTNESS_STEP = int(config['PANEL_BRIGHTNESS_STEP'])

# Deck is powered On by default (Screen is On)/Load state from config file
deck_poweron = bool(config['deck_poweron'])

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Check if host is alive

def check_ping(ip):
    hostname = ip
    response = os.system("ping -c 1 " + hostname)
    # Check the response.
    if response == 0:
        pingstatus = True
    else:
        pingstatus = False
    return pingstatus

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Generates a custom tile with run-time generated text and custom image via the
# PIL module.

def render_key_image(deck, icon_filename, font_filename, label_text):
    # Create new key image of the correct dimensions, black background.
    image = PILHelper.create_image(deck)

    # Resize the source image asset to best-fit the dimensions of a single key,
    # and paste it onto our blank frame centered as closely as possible.
    icon = Image.open(icon_filename).convert("RGBA")
    icon.thumbnail((image.width, image.height - 20), Image.LANCZOS)
    icon_pos = ((image.width - icon.width) // 2, 0)
    image.paste(icon, icon_pos, icon)

    # Load a custom TrueType font and use it to overlay the key index, draw key
    # label onto the image.
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_filename, int(config['FONT_SIZE']))
    label_w, label_h = draw.textsize(label_text, font=font)
    label_pos = ((image.width - label_w) // 2, image.height - 20)
    draw.text(label_pos, text=label_text, font=font, fill="white")

    return PILHelper.to_native_format(deck, image)

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Returns styling information for a key based on its position and state.

def get_key_style(deck, key, state):
    # Last button in panel0 is reserved, turn display On/Off
    display_key_off = deck.key_count() - 1
    # Get/Set Panel selection
    global PANEL_SELECT
    global config

    # Load panel config -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

    # How many buttons this panel have
    button_count = len(config['panel'+str(PANEL_SELECT)]) - 1
    print("Panel: " + str(PANEL_SELECT))
    if key <= button_count:
        print("Load Key: " + "key_" + str(key))
        name = "key_" + str(key)
        keypos = str(key)
        icon = "{}".format(config['panel'+str(PANEL_SELECT)][key]['image_pressed'] if state else config['panel'+str(PANEL_SELECT)][key]['image'])
        font = "fonts/" + FONT_SRC
        label = "Pressed!" if state else config['panel'+str(PANEL_SELECT)][key]['name']
    elif key == display_key_off and PANEL_SELECT == 0:
        # Turn Display On/Off
        name = "key_turn_on_off"
        keypos = str(key)
        icon = "{}".format("icons/menu/shutdown-pressed.png" if state else "icons/menu/shutdown.png")
        font = "fonts/" + FONT_SRC
        label = "Pressed!" if state else "Turn On/Of"
    else:
        # Button not assigned
        name = "key_none"
        keypos = str(key)
        icon = "{}".format("icons/menu/unavailable.png" if state else "icons/menu/unavailable-pressed.png")
        font = "fonts/" + FONT_SRC
        label = "Pressed!" if state else ""

    return {
        "name": name,
        "keypos": keypos,
        "icon": os.path.join(ASSETS_PATH, icon),
        "font": os.path.join(ASSETS_PATH, font),
        "label": label
    }

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Creates a new key image based on the key index, style and current key state
# and updates the image on the StreamDeck.

def update_key_image(deck, key, state):
    # Determine what icon and label to use on the generated key.
    key_style = get_key_style(deck, key, state)

    # Generate the custom key with the requested image and label.
    image = render_key_image(deck, key_style["icon"], key_style["font"], key_style["label"])

    # Use a scoped-with on the deck to ensure we're the only thread using it
    # right now.
    with deck:
        # Update requested key with the generated image.
        deck.set_key_image(key, image)

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Prints key state change information, updates rhe key image and performs any
# associated actions when a key is pressed.

def key_change_callback(deck, key, state):
    # Print new key state
    print("Deck {} Key {} = {}".format(deck.id(), key, state), flush=True)

    # Last button in panel0 is reserved, turn display On/Off
    display_key_off = deck.key_count() - 1

    global PANEL_SELECT
    global PANEL_BRIGHTNESS
    global PANEL_BRIGHTNESS_STEP
    global deck_poweron

    # How many buttons this panel have
    button_count = len(config['panel'+str(PANEL_SELECT)]) - 1

    # Update the key image based on the new key state.
    update_key_image(deck, key, state)

    # Check if the key is changing to the pressed state.
    if state:
        key_style = get_key_style(deck, key, state)

        # Get button actions from config file -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

        if key == display_key_off and PANEL_SELECT == 0:
            print("press Power On/Off\n")

            if deck_poweron:
                print("Turning Off Deck")
                deck.set_brightness(0)
                deck_poweron = False
            else:
                print("Turning On Deck")
                deck.set_brightness(PANEL_BRIGHTNESS)
                deck_poweron = True

        elif key <= button_count and config['panel'+str(PANEL_SELECT)][int(key_style["keypos"])]['type'] == "wakeonlan" and deck_poweron:
            print("wakeonlan Pressed: " + config['panel'+str(PANEL_SELECT)][int(key_style["keypos"])]['name'])
            if check_ping(config['panel'+str(PANEL_SELECT)][int(key_style["keypos"])]['nodeip']):
                print("Node Is OK, no action")
            else:
                print("Node is powered off, Wake Up")
                send_magic_packet(config['panel'+str(PANEL_SELECT)][int(key_style["keypos"])]['nodemac'])

        elif key <= button_count and config['panel'+str(PANEL_SELECT)][int(key_style["keypos"])]['type'] == "gotopanel" and deck_poweron:
            print("gotopanel Pressed: " + config['panel'+str(PANEL_SELECT)][int(key_style["keypos"])]['gotopanelid'])
            PANEL_SELECT = int(config['panel'+str(PANEL_SELECT)][int(key_style["keypos"])]['gotopanelid'])
            deck.reset()
            for key in range(deck.key_count()):
                update_key_image(deck, key, False)

        elif key <= button_count and config['panel'+str(PANEL_SELECT)][int(key_style["keypos"])]['type'] == "action" and deck_poweron:
            print("action Pressed: " + config['panel'+str(PANEL_SELECT)][int(key_style["keypos"])]['name'])

            # Check if elgato-pi-server is alive (Ping)
            if check_ping(config['panel'+str(PANEL_SELECT)][int(key_style["keypos"])]['serverip']):
                print("Node OK, Send action to elgato-pi-server")
                try:
                    actionreq = ""
                    actionreq = actionreq + "http://"
                    actionreq = actionreq + config['panel'+str(PANEL_SELECT)][int(key_style["keypos"])]['serverip']
                    actionreq = actionreq + ":"
                    actionreq = actionreq + config['panel'+str(PANEL_SELECT)][int(key_style["keypos"])]['serverport']
                    actionreq = actionreq + "/?launch=elgato-pi-deck&conn="
                    actionreq = actionreq + config['panel'+str(PANEL_SELECT)][int(key_style["keypos"])]['action']
                    r = requests.get(actionreq,timeout=3)
                    print(r.content)
                    r.raise_for_status()
                except requests.exceptions.HTTPError as errh:
                    print ("Http Error:",errh)
                except requests.exceptions.ConnectionError as errc:
                    print ("Error Connecting:",errc)
                except requests.exceptions.Timeout as errt:
                    print ("Timeout Error:",errt)
                except requests.exceptions.RequestException as err:
                    print ("Ops: Something Else",err)

        elif key <= button_count and config['panel'+str(PANEL_SELECT)][int(key_style["keypos"])]['type'] == "webhook" and deck_poweron:
            print("webhook Pressed: " + config['panel'+str(PANEL_SELECT)][int(key_style["keypos"])]['name'])

            try:
                actionreq = ""
                actionreq = actionreq + config['panel'+str(PANEL_SELECT)][int(key_style["keypos"])]['webhookurl']
                r = requests.post(actionreq,timeout=3)
                print(r.content)
                r.raise_for_status()
            except requests.exceptions.HTTPError as errh:
                print ("Http Error:",errh)
            except requests.exceptions.ConnectionError as errc:
                print ("Error Connecting:",errc)
            except requests.exceptions.Timeout as errt:
                print ("Timeout Error:",errt)
            except requests.exceptions.RequestException as err:
                print ("Ops: Something Else",err)

        elif key <= button_count and config['panel'+str(PANEL_SELECT)][int(key_style["keypos"])]['type'] == "blank" and deck_poweron:
            print("Blank Pressed.")

        elif key <= button_count and config['panel'+str(PANEL_SELECT)][int(key_style["keypos"])]['type'] == "bright0" and deck_poweron:
            print("press Brightness 0\n")
            PANEL_BRIGHTNESS = 0
            deck.set_brightness(PANEL_BRIGHTNESS)

        elif key <= button_count and config['panel'+str(PANEL_SELECT)][int(key_style["keypos"])]['type'] == "brightless" and deck_poweron:
            print("press Brightness <=\n")
            if PANEL_BRIGHTNESS > 10:
                PANEL_BRIGHTNESS = PANEL_BRIGHTNESS - PANEL_BRIGHTNESS_STEP
                deck.set_brightness(PANEL_BRIGHTNESS)

        elif key <= button_count and config['panel'+str(PANEL_SELECT)][int(key_style["keypos"])]['type'] == "brightmore" and deck_poweron:
            print("press Brightness =>\n")
            if PANEL_BRIGHTNESS < 100:
                PANEL_BRIGHTNESS = PANEL_BRIGHTNESS + PANEL_BRIGHTNESS_STEP
                deck.set_brightness(PANEL_BRIGHTNESS)

        elif key <= button_count and config['panel'+str(PANEL_SELECT)][int(key_style["keypos"])]['type'] == "bright100" and deck_poweron:
            print("press Brightness 100\n")
            PANEL_BRIGHTNESS = 100
            deck.set_brightness(PANEL_BRIGHTNESS)

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Main

if __name__ == "__main__":
    streamdecks = DeviceManager().enumerate()

    print("elgato-pi-deck - Start")
    print("")

    print("Found {} Stream Deck(s).\n".format(len(streamdecks)))

    for index, deck in enumerate(streamdecks):
        deck.open()
        deck.reset()

        print("Opened '{}' device (serial number: '{}')".format(deck.deck_type(), deck.get_serial_number()))

        # Set initial screen brightness to PANEL_BRIGHTNESS in config file
        deck.set_brightness(PANEL_BRIGHTNESS)

        # Set initial key images.
        for key in range(deck.key_count()):
            update_key_image(deck, key, False)

        # Register callback function for when a key state changes.
        deck.set_key_callback(key_change_callback)

        # Wait until all application threads have terminated.
        for t in threading.enumerate():
            if t is threading.currentThread():
                continue

            if t.is_alive():
                t.join()
