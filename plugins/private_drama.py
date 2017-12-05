# RoboCop 4's drama.py - Meant as an even better joke.

from cloudbot import hook
import random

@hook.command
def dramaaltert(text, message, conn=None, chan=None, action=None, nick=None):
    value = random.randint(0, 3)
    if value == 2:
        action("*BANG*")
        conn.cmd("KICK {} {} Sorry, bad trigger!".format(chan, nick))
    else:
        if text == nick:
            action("*BANG*")
            conn.cmd("KICK {} {} No drama for you!".format(chan, nick))
        elif text == "":
            return "You need a nick."
        else:
            message("Paging {} for drama.".format(text))
