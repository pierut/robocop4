# RoboCop 2's NODE.js Interpreter, designed to imitate pyexec.py. Also as reference for creating JavaScript-based RoboCop modules.
from cloudbot import hook
import sys
import urllib.parse, urllib.request
from pastebin_python import PastebinPython

@hook.command
def js(text):
	"""- Runs JavaScript code and returns the results. Requires a running JavaScript engine"""
	remote = "http://parser.secretalgorithm.com/"
	eval = urllib.parse.quote(text)
	address = remote + eval
	data = urllib.request.Request(address, None, {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57'})
	try:
		urlfile = urllib.request.urlopen(data)
	except:
		return "The remote service is currently down."
	page = urlfile.read()	
	
	contents = page.decode("utf-8");
	if '\n' in contents:
		return str(address);
	else:
		return contents;

@hook.command
def jsp(text):
	"""- Runs JavaScript code and returns multiline results as a Pastebin."""
	remote = "http://parser.secretalgorithm.com/"
	eval = urllib.parse.quote(text)
	address = remote + eval
	data = urllib.request.Request(address, None, {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57'})
	try:
		urlfile = urllib.request.urlopen(data)
	except:
		return "Server is down."
	page = urlfile.read()
	title = "Javascript Output".encode('utf-8')
	key = "cea50129bea8b85d06d4e5342f1575d8".encode('utf-8') 
	pbin = PastebinPython(api_dev_key=key)
	link = pbin.createPaste(page, title)
	return str(link);
