# RoboCop 3's rules.py - A rules command designed specifically for #techsupport on Snoonet (IRC)

from cloudbot import hook

rules_base = "1) Don't ask for help or specific skills, just state your issue. 2) Use Pastebin.com or /r/techsupport for long descriptions. 3) Be patient and don't spam."
rules_spam = "{}: Your issue was too long. Go to http://pastebin.com and link your issue from there."
rules_nick = "{}: Please change your nick by typing /nick my_nickname"
rules_nocoop = "{}: You've been helped on the matter and will receive no further help or advice. Thank you for your cooperation.";
rules_abuse = "{}: Abusing the bot might cause you to be kicked from the channel, please refrain from it."

coding_base = "1) Don't ask for help or specific skills, just state your issue. 2) Use Pastebin.com or equivalent for long descriptions. 3) Be patient and don't spam. 4) We don't make miracles."

@hook.command("rules", permissions=["rulesuser"], autohelp=False)
def rules(text, message, chan):
    """[spam|nick|nocoop|abuse|none] <user> - rules command for #techsupport."""
    user = text
    if " " in text:
        command,user = text.split(" ")
        if command == "spam":
            message(rules_spam.format(user))
        elif command == "nick":
            message(rules_nick.format(user))
        elif command == "nocoop":
            message(rules_nocoop.format(user))
        elif command == "abuse":
            message(rules_abuse.format(user))
    else:
        if text == "debug":
            return "This is a debug message. Thank you for listening."
        else:
            if text == "":
                if chan == "#coding":
                    return coding_base
                else:
                    return rules_base
            else:
                if chan == "#coding":
                    message("{}: ".format(text) + rules_base)
                else:
                    message("{}: ".format(text) + rules_base)
