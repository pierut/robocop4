from cloudbot import hook

@hook.command(autohelp=False)
def defcon(text, notice):
    if "debug" in text:
        notice("Defcon debug service requires an admin.")
    notice("Defcon is inactive.")
