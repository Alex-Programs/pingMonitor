from ping3 import ping
import time
from flask import *
from threading import *
import csv
import datetime
from os.path import getsize

class vars():
    cloudflarePing = 0

def monitor():
    while True:
        print("loop")
        router = ping("192.168.1.1")
        cloudflare = ping("1.1.1.1")

        timeData = datetime.datetime.now().replace(microsecond=0).isoformat()

        if router == None:
            routerSuccess = "False"
            router = 10000
        else:
            routerSuccess = "True"

        if cloudflare == None:
            cloudflareSuccess = "False"
            cloudflare = 10000
        else:
            cloudflareSuccess = "True"
            vars.cloudflarePing = cloudflare * 1000

        data = [str(timeData), routerSuccess, router * 1000, cloudflareSuccess, cloudflare * 1000]

        try:
            with open("export.csv", "a") as csvfile:
                csvwriter = csv.writer(csvfile)

                csvwriter.writerow(data)

            time.sleep(5)
        except:
            pass


Thread(target=monitor).start()

app = Flask(__name__)

@app.route("/")
def menu():
    file = open("webpage.html", mode="r")
    text = file.read()
    file.close()

    size = str(round(getsize("export.csv") / 1024, 2)) + "kb (UNIX)"

    text = text.replace("{{ cloudflarePingReplaceMe }}", str(round(vars.cloudflarePing))).replace("{{ FileSizeReplaceMe }}", size)
    return text

@app.route("/download")
def download():
    return send_file("export.csv", as_attachment=True)

app.run(port=4242, host="0.0.0.0")