from cloudbot import hook
import os
import pickle

@hook.command('debugwelcome')
@hook.irc_raw('JOIN')
def remindme(chan, nick, message):
	userdata = readnicks()
	user = str(nick)
	print(chan)
	if user in userdata:
		comment = userdata.get(user);
		channel = userdata.get('channel')
		userdata.pop(user, None)
		message(comment + ": " + user + " has logged back in.", channel);
		storenicks(userdata)

@hook.command('remindme')
def remindmestore(text, nick, chan):
	try:
		userdata = readnicks()
	except EOFError:
		userdata = None		
	if userdata is None:
		user = text
		print(chan)
		userdata = {user: nick, 'channel': chan}
		storenicks(userdata)
		return "OK, will remind you when " + user + " logs back in."
	else:
		user = text
		userdata[user] = nick
		userdata['channel'] = chan
		storenicks(userdata);
		return "OK, will remind you when " + user + " logs back in."

def storenicks(userdata):
        try:
                # This tries to open an existing file but creates a new file if necessary.
                with open('rmnicks.pkl', 'wb') as output:
                        pickle.dump(userdata, output, pickle.HIGHEST_PROTOCOL)
        except IOError:
                pass

def readnicks():
        # This tries to open an existing file but creates a new file if necessary.
        with open('rmnicks.pkl', 'rb') as textut:
                userdata = pickle.load(textut)
                return userdata;
