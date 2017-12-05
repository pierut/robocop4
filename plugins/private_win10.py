from cloudbot import hook
import json
from fuzzywuzzy import process

@hook.command("win10", permissions=["rulesuser"], autohelp=False)
def win10(text, message):
    with open('data/win10.json') as data_file:    
        terms = json.load(data_file)
        terms = terms['issues']
        data_file.close()

    text,ratio = process.extractOne(text.lower(), terms.keys())
    print(text)
    return terms.get(text, "Tip not found.")
