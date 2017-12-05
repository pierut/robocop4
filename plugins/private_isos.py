# RoboCop 4's isos.py [PRIVATE] - Returns a link from the repository based on your input.
# THIS MODULE HAS NOT BEEN MARKED FOR RELEASE

from cloudbot import hook
import json
from fuzzywuzzy import process

@hook.command("isos", permissions=["rulesuser"], autohelp=False)
def isos(text, message):
    with open('data/isos.json') as data_file:    
        terms = json.load(data_file)
        terms = terms['product']
        data_file.close()

    text,ratio = process.extractOne(text.lower(), terms.keys())
    print(text)
    return terms.get(text, "Tip not found.")
