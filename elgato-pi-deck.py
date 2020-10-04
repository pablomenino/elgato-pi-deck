#!/usr/bin/env python3

#  elgato-pi-deck
# 
#  LICENSE: GPL 3.0
# 
#  @package    elgato-pi-deck
#  @author     Pablo Meniño
#  @copyright  Pablo Meniño (pablo.menino@mfwlab.com)
#  @license    http://www.gnu.org/licenses/gpl-3.0.html
#  @version    0.8
# 
#  @email      pablo.menino@mfwlab.com
#  @website    https://www.mfwlab.com
#
#  Based on StreamDeck Python Library example

import os
import threading

import requests

from wakeonlan import send_magic_packet

from PIL import Image, ImageDraw, ImageFont
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper

# Folder location of image assets and fonts
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "files")
FONT_SRC = "Roboto-Regular.ttf"
PANNEL_SELECT = 0
PANNEL_BRIGHTNESS = 30
PANNEL_BRIGHTNESS_STEP = 10

# Computers
synology = "192.168.0.11"
synology_mac1 = "00:11:44:AA:BB:CC"

# Deck screen is powered ON at start up
deck_poweron = True

# Check host is alive
def check_ping(ip):
    hostname = ip
    response = os.system("ping -c 1 " + hostname)
    # and then check the response...
    if response == 0:
        pingstatus = True
    else:
        pingstatus = False

    return pingstatus

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
    font = ImageFont.truetype(font_filename, 12)
    label_w, label_h = draw.textsize(label_text, font=font)
    label_pos = ((image.width - label_w) // 2, image.height - 20)
    draw.text(label_pos, text=label_text, font=font, fill="white")

    return PILHelper.to_native_format(deck, image)


# Returns styling information for a key based on its position and state.
def get_key_style(deck, key, state):
    # Last button in the example application is the exit button.
    exit_key_index = deck.key_count() - 1
    global PANNEL_SELECT

# Pannel 0 / *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* /

    if key == 0 and PANNEL_SELECT == 0:
        name = "key_1"
        icon = "{}.png".format("utilities-pressed" if state else "utilities")
        font = FONT_SRC
        label = "Pressed!" if state else "Apps"
    elif key == 1 and PANNEL_SELECT == 0:
        name = "key_2"
        icon = "{}.png".format("iot" if state else "iot")
        font = FONT_SRC
        label = "Pressed!" if state else "IoT"
    elif key == 2 and PANNEL_SELECT == 0:
        name = "key_3"
        icon = "{}.png".format("1618plus" if state else "1618plus")
        font = FONT_SRC
        label = "Pressed!" if state else "Synology 1618+"
    elif key == 10 and PANNEL_SELECT == 0:
        name = "key_11"
        icon = "{}.png".format("brightness-0" if state else "brightness-0")
        font = FONT_SRC
        label = "Pressed!" if state else "Brightness 0"
    elif key == 11 and PANNEL_SELECT == 0:
        name = "key_12"
        icon = "{}.png".format("brightness-less" if state else "brightness-less")
        font = FONT_SRC
        label = "Pressed!" if state else "Brightness <="
    elif key == 12 and PANNEL_SELECT == 0:
        name = "key_13"
        icon = "{}.png".format("brightness-more" if state else "brightness-more")
        font = FONT_SRC
        label = "Pressed!" if state else "Brightness =>"
    elif key == 13 and PANNEL_SELECT == 0:
        name = "key_14"
        icon = "{}.png".format("brightness-100" if state else "brightness-100")
        font = FONT_SRC
        label = "Pressed!" if state else "Brightness 100"
    elif key == 14 and PANNEL_SELECT == 0:
        name = "key_15"
        icon = "{}.png".format("shutdown-pressed" if state else "shutdown")
        font = FONT_SRC
        label = "Pressed!" if state else "Turn On/Of"
    elif PANNEL_SELECT == 0:
        name = "key_none"
        icon = "{}.png".format("unavailable" if state else "unavailable-pressed")
        font = FONT_SRC
        label = "Pressed!" if state else ""

# Pannel 1 / *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* /

    elif key == 0 and PANNEL_SELECT == 1:
        name = "key_1"
        icon = "{}.png".format("back-pressed" if state else "back")
        font = FONT_SRC
        label = "Pressed!" if state else "Return"
    elif key == 1 and PANNEL_SELECT == 1:
        name = "key_2"
        icon = "{}.png".format("firefox" if state else "firefox")
        font = FONT_SRC
        label = "Pressed!" if state else "Firefox"
    elif PANNEL_SELECT == 1:
        name = "key_none"
        icon = "{}.png".format("unavailable" if state else "unavailable-pressed")
        font = FONT_SRC
        label = "Pressed!" if state else ""

# Pannel 2 / *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* /

    elif key == 0 and PANNEL_SELECT == 2:
        name = "key_1"
        icon = "{}.png".format("back-pressed" if state else "back")
        font = FONT_SRC
        label = "Pressed!" if state else "Return"
    elif key == 1 and PANNEL_SELECT == 2:
        name = "key_2"
        icon = "{}.png".format("ligth" if state else "ligth")
        font = FONT_SRC
        label = "Pressed!" if state else "Ligth CPU"
    elif PANNEL_SELECT == 2:
        name = "key_none"
        icon = "{}.png".format("unavailable" if state else "unavailable-pressed")
        font = FONT_SRC
        label = "Pressed!" if state else ""

# Pannel END / *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* /

    return {
        "name": name,
        "icon": os.path.join(ASSETS_PATH, icon),
        "font": os.path.join(ASSETS_PATH, font),
        "label": label
    }

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

# Prints key state change information, updates rhe key image and performs any
# associated actions when a key is pressed.
def key_change_callback(deck, key, state):
    # Print new key state
    print("Deck {} Key {} = {}".format(deck.id(), key, state), flush=True)
    global PANNEL_SELECT
    global PANNEL_BRIGHTNESS
    global PANNEL_BRIGHTNESS_STEP
    global norc
    global norc_mac
    global deck_poweron

    # Update the key image based on the new key state.
    update_key_image(deck, key, state)

    # Check if the key is changing to the pressed state.
    if state:
        key_style = get_key_style(deck, key, state)

# Pannel 0 / *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* /

        if key_style["name"] == "key_1" and PANNEL_SELECT == 0 and deck_poweron:
            PANNEL_SELECT = 1
            print("press Apps\n")
            deck.reset()
            for key in range(deck.key_count()):
                update_key_image(deck, key, False)

        elif key_style["name"] == "key_2" and PANNEL_SELECT == 0 and deck_poweron:
            PANNEL_SELECT = 2
            print("press IoT\n")
            deck.reset()
            for key in range(deck.key_count()):
                update_key_image(deck, key, False)

        elif key_style["name"] == "key_11" and PANNEL_SELECT == 0 and deck_poweron:
            print("press Brightness 0\n")
            PANNEL_BRIGHTNESS = 0
            deck.set_brightness(PANNEL_BRIGHTNESS)

        elif key_style["name"] == "key_12" and PANNEL_SELECT == 0 and deck_poweron:
            print("press Brightness <=\n")
            if PANNEL_BRIGHTNESS > 10:
                PANNEL_BRIGHTNESS = PANNEL_BRIGHTNESS - PANNEL_BRIGHTNESS_STEP
                deck.set_brightness(PANNEL_BRIGHTNESS)

        elif key_style["name"] == "key_13" and PANNEL_SELECT == 0 and deck_poweron:
            print("press Brightness =>\n")
            if PANNEL_BRIGHTNESS < 100:
                PANNEL_BRIGHTNESS = PANNEL_BRIGHTNESS + PANNEL_BRIGHTNESS_STEP
                deck.set_brightness(PANNEL_BRIGHTNESS)

        elif key_style["name"] == "key_14" and PANNEL_SELECT == 0 and deck_poweron:
            print("press Brightness 100\n")
            PANNEL_BRIGHTNESS = 100
            deck.set_brightness(PANNEL_BRIGHTNESS)

        elif key_style["name"] == "key_7" and PANNEL_SELECT == 0 and deck_poweron:
            print("press Synology\n")
            if check_ping(synology):
                print("Synology Is OK")
            else:
                print("Synology is powered off, Wake Up")
                send_magic_packet(Synology_mac1)

        elif key_style["name"] == "key_15" and PANNEL_SELECT == 0:
            print("press Power On/Off\n")

            if deck_poweron:
                print("Turning Off Deck")
                deck.set_brightness(0)
                deck_poweron = False
            else:
                print("Turning On Deck")
                deck.set_brightness(PANNEL_BRIGHTNESS)
                deck_poweron = True

# Pannel Back - Global / *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* /

        elif key_style["name"] == "key_1" and PANNEL_SELECT != 0 and deck_poweron:
            PANNEL_SELECT = 0
            print("press Back\n")
            deck.reset()
            for key in range(deck.key_count()):
                update_key_image(deck, key, False)

# Pannel 1 / *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* /

        elif key_style["name"] == "key_2" and PANNEL_SELECT == 1 and deck_poweron:
            print("press firefox\n")
            try:
                r = requests.get("http://192.168.0.10:8889/?launch=elgato-pi-deck&conn=firefox",timeout=3)
                print(r.content)
                r.raise_for_status()
            except requests.exceptions.HTTPError as errh:
                print ("Http Error:",errh)
            except requests.exceptions.ConnectionError as errc:
                print ("Error Connecting:",errc)
            except requests.exceptions.Timeout as errt:
                print ("Timeout Error:",errt)
            except requests.exceptions.RequestException as err:
                print ("OOps: Something Else",err)



# Pannel 2 / *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* /

        elif key_style["name"] == "key_2" and PANNEL_SELECT == 2 and deck_poweron:
            print("press ligth cpu\n")
            try:
                r = requests.post("http://192.168.0.22/api/webhook/1",timeout=3)
                print(r.content)
                r.raise_for_status()
            except requests.exceptions.HTTPError as errh:
                print ("Http Error:",errh)
            except requests.exceptions.ConnectionError as errc:
                print ("Error Connecting:",errc)
            except requests.exceptions.Timeout as errt:
                print ("Timeout Error:",errt)
            except requests.exceptions.RequestException as err:
                print ("OOps: Something Else",err)

# Pannel END / *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* /

if __name__ == "__main__":
    streamdecks = DeviceManager().enumerate()

    print("Found {} Stream Deck(s).\n".format(len(streamdecks)))

    for index, deck in enumerate(streamdecks):
        deck.open()
        deck.reset()

        print("Opened '{}' device (serial number: '{}')".format(deck.deck_type(), deck.get_serial_number()))

        # Set initial screen brightness to 30%.
        deck.set_brightness(PANNEL_BRIGHTNESS)
        #deck.set_brightness(100)

        # Set initial key images.
        for key in range(deck.key_count()):
            update_key_image(deck, key, False)

        # Register callback function for when a key state changes.
        deck.set_key_callback(key_change_callback)

        # Wait until all application threads have terminated (for this example,
        # this is when all deck handles are closed).
        for t in threading.enumerate():
            if t is threading.currentThread():
                continue

            if t.is_alive():
                t.join()
