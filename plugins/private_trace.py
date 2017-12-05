# RoboCop 2's trace.py - Runs a traceroute on the local system, based upon ping.py
import subprocess
import os
from pastebin_python import PastebinPython

from cloudbot import hook


@hook.command()
def traceroute(text, reply):
    """<host> [-i|-p] - runs a traceroute of <host> with UDP, IMCP, or TCP disabled or enabled."""

    if os.name == "nt":
        return "Windows will probably never get support for this."

    args = text.split(' ')
    host = args[0]

    icmp = None
    tcp = None

    # Check flags, and turn on the protocol modes accordingly
    if len(args) > 1:
        if args[0] == "-i":
            icmp = True
            host = args[1]
        elif args[0] == "-p":
            tcp = True
            host = args[1]

    if icmp is True:
        mesg = "with ICMP ECHO enabled."
        flags = ["traceroute", "-P", "ICMP", "-w", "3", "-q", "1", "-m", "16", host]
    elif tcp is True:
        mesg = "with TCP enabled."
        flags = ["traceroute", "-P", "TCP", "-w", "3", "-q", "1", "-m", "16", host]
    else:
        mesg = "with UDP datagrams enabled."
        flags = ["traceroute", "-w", "3", "-q", "1", "-m", "16", host]

    reply("Running traceroute of {} {} ".format(host, mesg))
    
    try:
        tcrcmd = subprocess.check_output(flags).decode("utf-8")
    except subprocess.CalledProcessError:
        return "Error: Host not found or could not complete traceroute."
    if "request timed out" in tcrcmd or "unknown host" in tcrcmd:
        return "Error: could not complete traceroute"
    else:
        title = "Traceroute Output".encode('utf-8')
        key = "cea50129bea8b85d06d4e5342f1575d8".encode('utf-8')
        pbin = PastebinPython(api_dev_key=key)
        link = pbin.createPaste(tcrcmd, title)
        return str(link);
