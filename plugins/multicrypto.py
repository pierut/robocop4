from decimal import *
from cloudbot import hook
import urllib, json

url = "https://api.coinmarketcap.com/v1/ticker/?limit=9999"

@hook.command("c", "crypto", autohelp=False)
def crypto(text="btc"):
    text, amount = text.split()
    text = text.upper()
    response = urllib.request.urlopen(url)
    data = response.read()
    encoding = response.info().get_content_charset('utf-8')
    data = json.loads(data.decode(encoding))
    x = 0
    while x < len(data):
        #print(x)
        if data[x]['symbol'] == text:
            print(data[x]['symbol'])
            seday = float(data[x]['percent_change_7d'])
            ohour = float(data[x]['percent_change_1h'])
            tfhour = float(data[x]['percent_change_24h'])
            print(str(seday) + str(ohour) + str(tfhour))
            if seday > 0:
                sevday = str("\x0303") + str(seday) + str("\x03")
            elif seday < 0:
                sevday = str("\x0304") + str(seday) + str("\x03")
            else:
                seday = str("ERRAR: 7d was neither > or < 0. WTF??")

            if tfhour > 0:
                tfhour = str("\x0303") + str(tfhour) + str("\x03")
            elif tfhour < 0:
                tfhour = str("\x0304") + str(tfhour) + str("\x03")
            else:
                tfhour = str("ERRAR: 24h was neither > or < 0. WTF??")

            if ohour > 0:
                ohour = str("\x0303") + str(ohour) + str("\x03")
            elif ohour < 0:
                ohour = str("\x0304") + str(ohour) + str("\x03")
            else:
                ohour = str("ERRAR: 1h was neither > or < 0. WTF??")

            pfloat = float(data[x]['price_usd'])
            afloat = float(amount)
            bfloat = float(data[x]['price_btc'])
            utotal = pfloat * afloat
            btotal = bfloat * afloat
            utotal = Decimal(utotal)
            btotal = Decimal(btotal)
            utotal = Decimal(utotal.quantize(Decimal('.00000001'), rounding=ROUND_DOWN))
            btotal = Decimal(btotal.quantize(Decimal('.00000001'), rounding=ROUND_DOWN))
            return data[x]['name'] + str(" : rank: ") + data[x]['rank'] + str(": $") + data[x]['price_usd'] + str(" : 1H: ") + str(ohour) + str(" 24H: ") + str(tfhour) + str(" 7D: ") + str(sevday) + str(' : B') + data[x]['price_btc'] + str(' : arg: $') + str(utotal) + str(' : B') + str(btotal)
        x = x + 1
