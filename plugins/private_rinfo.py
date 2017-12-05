from cloudbot import hook
from cloudbot.util import formatting, timeformat

from datetime import datetime
import requests

API_URL = "http://reddit.com"
INFO_MOD = "{}/r/{}/about/moderators.json"
INFO_SUB = "{}/r/{}/about.json"
INFO_USER = "{}/user/{}/about.json"
TIME_FORMAT = "%d %B, %Y"

HEADERS = {'User-Agent': 'RoboCop/2.0 - A bot by Foxlet'}

def find_moderators(subreddit):
    parsed = requests.get(INFO_MOD.format(API_URL, subreddit), headers=HEADERS).json()
    data = parsed['data']['children']
    userlist = []
    for x in data:
        userlist.append(x['name'])
    return userlist

def find_sub_data(subreddit):
    parsed = requests.get(INFO_SUB.format(API_URL, subreddit), headers=HEADERS).json()
    data = parsed['data']
    raw_time = datetime.fromtimestamp(int(data['created_utc']))
    date = "\x02{}\x02 ({} ago)".format(raw_time.strftime(TIME_FORMAT), timeformat.timesince(raw_time))
    return {'subs': data['subscribers'], 'date': date, 'active': data['accounts_active'], 'title': data['title']}

@hook.command()
def rinfo(text):
    args = text.split(" ")
    if args[0] == "mods":
        userlist = find_moderators(args[1])
        naming = formatting.pluralize(len(userlist), "moderator")
        return "\x02/r/{}\x02 has {}: {}".format(args[1], naming, ", ".join(userlist))
    elif args[0] == "sub":
        metadata = find_sub_data(args[1])
        return "\x02/r/{}\x02: Created {} | \x02{}\x02 subscriber(s) | \x02{}\x02 online | '{}'.".format(args[1], metadata['date'], metadata['subs'], metadata['active'], metadata['title'])
