from cloudbot import hook
import random
import time
import os

@hook.command
def timer(text, conn=None, chan=None, action=None, nick=None):
	"""<seconds> - Starts a timer for the designated amount in seconds."""
	if os.path.isfile("timer.lock"):
		return "A timer session is already running."
	else:
		with open("timer.lock","a+") as f:
			f.write("lock")
	if text.isdigit():
		if int(text) > 1200:
			os.remove("timer.lock")
			return "Value too large."
		else:
			conn.cmd("PRIVMSG " + chan + " Starting a timer for " + text + " seconds.")
			count = int(text)
			time.sleep(count)
			os.remove("timer.lock")
			return "Your timer has ended."
	else:
		os.remove("timer.lock")
		return "The input must be in seconds."
