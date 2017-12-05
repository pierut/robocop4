import re
import random

import requests

from cloudbot import hook
from cloudbot.util import timeformat, formatting

headers = {'User-Agent': 'CloudBot/dev 1.0 - CloudBot Refresh by lukeroge'}

reddit_re = re.compile(r'.*(((www\.)?reddit\.com/r|redd\.it)[^ ]+)', re.I)

base_url = "http://reddit.com/r/{}/.json"
short_url = "http://redd.it/{}"

@hook.command
def rquote(text, bot):
    url = "http://reddit.com/user/{}/comments/.json".format(text)

    # the reddit API gets grumpy if we don't include headers
    r = requests.get(url, headers=headers)
    data = r.json()
    try:
        size = len(data["data"]["children"]) - 1
        print(size)
    except:
        return "That user doesn't exist."

    try:
        comment_num = random.randint(0, size)
        print(comment_num)
    except ValueError:
        return "{} has no comments on reddit.".format(text)

    item = data["data"]["children"][comment_num]["data"]["body"]

    id = data["data"]["children"][comment_num]["data"]["id"]
    linkid = data["data"]["children"][comment_num]["data"]["link_id"]

    link = "http://reddit.com/comments/{}//{}".format(linkid[3:], id)

    item = str(item).replace('\n', ' ')
    item = formatting.truncate_str(item, 150)

    return "{} - {}".format(item, str(link))
