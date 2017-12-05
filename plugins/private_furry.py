# RoboCop 2's furry.py, uses the RSS engine to grab random Furry art from DeviantArt

from cloudbot import hook
import feedparser
import random

@hook.command
def furry(text):
	d = feedparser.parse('http://backend.deviantart.com/rss.xml?type=deviation&q=furry')
	counter = len(d['entries'])
	value = random.randint(0, counter-1)
	if d.entries[value]['media_rating'] == 'adult':
		value = random.randint(0, counter-1)
	returnitem = "\x02{}\x02: {}".format(d.entries[value]['title'], d.entries[value]['link'])
	return str(returnitem)
