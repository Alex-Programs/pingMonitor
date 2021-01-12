from ping3 import ping
import time
from flask import *
from threading import *
import csv
import datetime


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
    webpage = """<!doctype html>
<title>Download Statistics</title>

<head>
    <style>
        button {
            box-shadow: none;
            border-width: 2px solid;
            border-color: black;
            background-color: white;
            color: black;
            border-radius: 0px;
            font-family: sans-serif;
        }
    </style>
</head>

<body>
<button onclick="document.location.href = '/download'"> Download </button>
</body>
"""
    return webpage

@app.route("/download")
def download():
    return send_file("export.csv", as_attachment=True)

app.run(port=4242, host="0.0.0.0")