# RoboCop 3's comic.py - based on WeedBotRefresh's comic.py

from cloudbot import hook
import os
from random import shuffle
from PIL import Image, ImageDraw, ImageFont
import base64
import requests
import json
from datetime import datetime
from io import BytesIO

from cloudbot.event import EventType

mcache = dict()


@hook.on_start()
def load_key(bot):
    global api_key
    global background_file
    global font_file
    global font_size
    global buffer_size
    api_key = bot.config.get("api_keys", {}).get("imgur_client_id")
    background_file = bot.config.get("resources", {}).get("background")
    font_file = bot.config.get("resources", {}).get("font")
    font_size = bot.config.get("resources", {}).get("font_size")
    buffer_size = bot.config.get("resources", {}).get("buffer_size")


@hook.event([EventType.message, EventType.action], ignorebots=False, singlethread=True)
def track(event, conn):
    key = (event.chan, conn.name)
    if key not in mcache:
        mcache[key] = []

    value = (datetime.now(), event.nick, str(event.content))
    mcache[key].append(value)
    mcache[key] = mcache[key][-1*buffer_size:]


@hook.command("comic")
def comic(conn, chan):
    text = chan
    try:
        msgs = mcache[(text, conn.name)]
    except KeyError:
        return "Not Enough Messages."
    sp = 0
    chars = set()

    for i in range(len(msgs)-1, 0, -1):
        sp += 1
        diff = msgs[i][0] - msgs[i-1][0]
        chars.add(msgs[i][1])
        if sp > 10 or diff.total_seconds() > 120 or len(chars) > 3:
            break

    msgs = msgs[-1*sp:]

    panels = []
    panel = []

    for (d, char, msg) in msgs:
        if len(panel) == 2 or len(panel) == 1 and panel[0][0] == char:
            panels.append(panel)
            panel = []
        if msg.count('\x01') >= 2:
            ctcp = msg.split('\x01', 2)[1].split(' ', 1)
            if len(ctcp) == 1:
                ctcp += ['']
            if ctcp[0] == 'ACTION':
                msg = '*'+ctcp[1]+'*'
        panel.append((char, msg))

    panels.append(panel)

    print(repr(chars))
    print(repr(panels))

    # Initialize a variable to store our image
    image_comic = BytesIO()

    # Save the completed composition to a JPEG in memory
    make_comic(chars, panels).save(image_comic, format="JPEG", quality=85)

    # Get API Key, upload the comic to imgur
    headers = {'Authorization': 'Client-ID ' + api_key}
    base64img = base64.b64encode(image_comic.getvalue())
    url = "https://api.imgur.com/3/upload.json"
    r = requests.post(url, data={'key': api_key, 'image': base64img, 'title': 'Weedbot Comic'}, headers=headers, verify=False)
    val = json.loads(r.text)
    try:
        return val['data']['link']
    except KeyError:
        return val['data']['error']


def wrap(st, font, draw, width):
    st = st.split()
    mw = 0
    mh = 0
    ret = []

    while len(st) > 0:
        s = 1
        while True and s < len(st):
            w, h = draw.textsize(" ".join(st[:s]), font=font)
            if w > width:
                s -= 1
                break
            else:
                s += 1

        if s == 0 and len(st) > 0:  # we've hit a case where the current line is wider than the screen
            s = 1

        w, h = draw.textsize(" ".join(st[:s]), font=font)
        mw = max(mw, w)
        mh += h
        ret.append(" ".join(st[:s]))
        st = st[s:]

    return ret, (mw, mh)


def rendertext(st, font, draw, pos):
    ch = pos[1]
    for s in st:
        w, h = draw.textsize(s, font=font)
        draw.text((pos[0], ch), s, font=font, fill=(0xff, 0xff, 0xff, 0xff))
        ch += h


def fitimg(img, width, height):
    scale1 = float(width) / img.size[0]
    scale2 = float(height) / img.size[1]

    l1 = (img.size[0] * scale1, img.size[1] * scale1)
    l2 = (img.size[0] * scale2, img.size[1] * scale2)

    if l1[0] > width or l1[1] > height:
        l = l2
    else:
        l = l1

    return img.resize((int(l[0]), int(l[1])), Image.ANTIALIAS)


def make_comic(chars, panels):
    panelheight = 300
    panelwidth = 480

    filenames = os.listdir('data/chars/')
    shuffle(filenames)
    filenames = map(lambda x: os.path.join('data/chars', x), filenames[:len(chars)])
    chars = list(chars)
    chars = zip(chars, filenames)
    charmap = dict()
    for ch, f in chars:
        charmap[ch] = Image.open(f)

    imgwidth = panelwidth
    imgheight = panelheight * len(panels)

    bg = Image.open(background_file)

    im = Image.new("RGBA", (imgwidth, imgheight), (0xff, 0xff, 0xff, 0xff))
    font = ImageFont.truetype(font_file, font_size)

    for i in range(len(panels)):
        pim = Image.new("RGBA", (panelwidth, panelheight), (0xff, 0xff, 0xff, 0xff))
        pim.paste(bg, (0, 0))
        draw = ImageDraw.Draw(pim)

        st1w = 0; st1h = 0; st2w = 0; st2h = 0
        (st1, (st1w, st1h)) = wrap(panels[i][0][1], font, draw, 2*panelwidth/3.0)
        rendertext(st1, font, draw, (10, 10))
        if len(panels[i]) == 2:
            (st2, (st2w, st2h)) = wrap(panels[i][1][1], font, draw, 2*panelwidth/3.0)
            rendertext(st2, font, draw, (panelwidth-10-st2w, st1h + 10))

        texth = st1h + 10
        if st2h > 0:
            texth += st2h + 10 + 5

        maxch = panelheight - texth
        im1 = fitimg(charmap[panels[i][0][0]], 2*panelwidth/5.0-10, maxch)
        pim.paste(im1, (10, panelheight-im1.size[1]), im1)

        if len(panels[i]) == 2:
            im2 = fitimg(charmap[panels[i][1][0]], 2*panelwidth/5.0-10, maxch)
            im2 = im2.transpose(Image.FLIP_LEFT_RIGHT)
            pim.paste(im2, (panelwidth-im2.size[0]-10, panelheight-im2.size[1]), im2)

        draw.line([(0, 0), (0, panelheight-1), (panelwidth-1, panelheight-1), (panelwidth-1, 0), (0, 0)], (0, 0, 0, 0xff))
        del draw
        im.paste(pim, (0, panelheight * i))

    return im
