from flask import Flask, render_template
import random
from urllib.request import urlretrieve

app = Flask('app')

@app.route('/')
def index():
  urlretrieve("https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all", "./http_proxies.txt")
  with open('http_proxies.txt') as f:
    proxy = random.choice(list(f.readlines())).splitlines()[0]
  return render_template('index.html', proxy=proxy)

app.run(host='0.0.0.0', port=8080)