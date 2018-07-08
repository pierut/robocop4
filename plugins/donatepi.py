from decimal import *
from cloudbot import hook
import urllib, json

@hook.command("dtp", "donatetopi", autohelp=False)
def donate():
	return str("DOGE: ") + str("DLG5tHXKbJtNLGhijPwrFVrt18vzagwAVG");
