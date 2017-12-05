# RoboCop 3's meme.py - PRINT ALL THEM MEMES

from PIL import ImageFont, Image, ImageDraw, ImageFilter, ImageChops
from cloudbot import hook
import random
import base64
import requests
import json
import os
from io import BytesIO

# Impact.ttf is included with the meme.py package, but you can use any TrueType font.
meme_font = "data/fonts/Impact.ttf"

# Your imgur API key should go here.
api_key = "1ae994097d741ae"
# Comment up top and uncomment below if you already have a key in the config.
# @hook.onload()
# def addkey(bot):
#     global api_key
#     api_key = bot.config.get("api_keys", {}).get("imgur_client_id")

# Directory to your meme folder store.
# There should NOT be a trailing slash.
meme_directory = "data/memes"

# The format of your memes in the store, preferably JPG or PNG.
meme_format = "jpg"

@hook.command
def meme(text, notice):
    # Set args to whatever will be the input.
    args = text

    # Generate Meme List from store.
    meme_list = [f for f in os.listdir(meme_directory) if f.endswith('.{}'.format(meme_format))]
    meme_list = [m[:-4] for m in meme_list]

    if ";" in args:
        arguments = args.split(";")
        count = len(arguments)
        if count == 2:
            # Arguments with a specific meme, one line
            topString = ''
            bottomString = arguments[1]
            meme = arguments[0]
            if meme == "!random":
                meme = random.choice(meme_list)
            link = meme_generator(meme, bottomString, topString)
            return link
        elif count == 3:
            # Arguments with a specific meme, two lines
            topString = arguments[1]
            bottomString = arguments[2]
            meme = arguments[0]
            if meme == "!random":
                meme = random.choice(meme_list)
            link = meme_generator(meme, topString, bottomString)
            return link
        else:
            # So many args
            # What do they mean?
            # Too intense...
            return "You gave one too many arguments."
    else:
        if args == "!list":
            notice("Supported Memes: {}".format(", ".join(meme_list)))
        else:
            # Just text?, use a random meme!
            topString = ''
            bottomString = args
            meme = random.choice(meme_list)
            link = meme_generator(meme, topString, bottomString)
            return link

def meme_generator(meme, topString, bottomString):
    print(meme)
    try:
        img = Image.open("{}/{}.{}".format(meme_directory, str(meme), meme_format))
    except:
        return "Could not find such meme in the store."
    imageSize = img.size

    # Find the largest font size that works
    fontSize = imageSize[1]//5
    font = ImageFont.truetype(meme_font, fontSize)
    topTextSize = font.getsize(topString)
    bottomTextSize = font.getsize(bottomString)
    while topTextSize[0] > imageSize[0]-20 or bottomTextSize[0] > imageSize[0]-20:
        fontSize = fontSize - 1
        font = ImageFont.truetype(meme_font, fontSize)
        topTextSize = font.getsize(topString)
        bottomTextSize = font.getsize(bottomString)

    # Find the top centered position for top text
    topTextPositionX = (imageSize[0]//2) - (topTextSize[0]//2)
    topTextPositionY = 0
    topTextPosition = (topTextPositionX, topTextPositionY)

    # Find the bottom centered position for bottom text
    bottomTextPositionX = (imageSize[0]//2) - (bottomTextSize[0]//2)
    factor = bottomTextSize[1] * 0.27
    add = bottomTextSize[1] + factor
    bottomTextPositionY = imageSize[1] - add
    bottomTextPosition = (bottomTextPositionX, bottomTextPositionY)

    # Initialize the meme background
    ImageDraw.Draw(img)

    # Initialize Image Layers for Compositing
    # The Outline Mask layer, just gives the blurred "look" to the outline
    outline = Image.new('RGBA', img.size, (0, 0, 0, 0))
    # Shadow_Matte is just a backplane for the blur mask in the outlines, it's just black
    shadow_matte = Image.new('RGB', img.size, (0,0,0))
    # Text to draw on top of everything (the actual white text)
    top_text = Image.new('RGBA', img.size, (255, 255, 255, 0))

    # Draw the bare text outlines to the outlines mask layer
    # There may be a better way (antialised)
    outlineRange = fontSize//15
    for x in range(-outlineRange, outlineRange+1):
        for y in range(-outlineRange, outlineRange+1):
            ImageDraw.Draw(outline).text((topTextPosition[0]+x, topTextPosition[1]+y), topString, (0,0,0), font=font)
            ImageDraw.Draw(outline).text((bottomTextPosition[0]+x, bottomTextPosition[1]+y), bottomString, (0,0,0), font=font)

    # Define the custom kernel
    kernel = [
        0, 1, 2, 1, 0,
        1, 2, 4, 2, 1,
        2, 4, 8, 4, 1,
        1, 2, 4, 2, 1,
        0, 1, 2, 1, 0]
    # Create a PIL-friendly filter using the maths from the custom kernel
    custom_krnl = ImageFilter.Kernel((5, 5), kernel, scale = 0.3 * sum(kernel))

    # Apply the custom kernel filter to the existing outline mask (adds the blur)
    blurred_outline = outline.filter(custom_krnl)

    # Actually draw the changes by the filter
    ImageDraw.Draw(blurred_outline).text(topTextPosition, topString, font = font, fill = (0, 0, 0))

    # Compositing time - Apply the blurred mask to the pure-black shadow matte, then superimpose it on the meme background
    img = Image.composite(img, shadow_matte, ImageChops.invert(blurred_outline))

    # Draw the white text to be placed on top of the whole meme
    ImageDraw.Draw(top_text).text(topTextPosition, topString, (255,255,255), font=font)
    ImageDraw.Draw(top_text).text(bottomTextPosition, bottomString, (255,255,255), font=font)

    # Compositing time - Add the white text, superimposing it over the black outline and the meme background
    img = Image.composite(img, top_text, ImageChops.invert(top_text))

    # Initialize a variable to store our image
    image_meme = BytesIO()

    # Save the completed composition to a PNG in memory
    img.save(image_meme, format="PNG")
    link = sendtoimgur(image_meme, meme)
    return link

def sendtoimgur(file, meme_name):
    headers = {'Authorization': 'Client-ID ' + api_key}
    base64img = base64.b64encode(file.getvalue())
    url="https://api.imgur.com/3/upload.json"
    r = requests.post(url, data={'key': api_key, 'image':base64img,'title':'{} - {}'.format("RoboCop Meme", meme_name)},headers=headers,verify=False)
    print(r.text)
    val=json.loads(r.text)
    try:
        return val['data']['link']
    except KeyError:
        return val['data']['error']
