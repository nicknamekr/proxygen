import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse 
from fastapi.templating import Jinja2Templates 
import random
from urllib.request import urlretrieve

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def download():
  urlretrieve("https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all", "./http_proxies.txt")
  urlretrieve("https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all", "./socks4_proxies.txt")
  urlretrieve("https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all", "./socks5_proxies.txt")
  threading.Timer(500, download).start()

download()

@app.get('/', response_class=HTMLResponse)
async def root(request:Request):
  print('HTTP Proxy loaded.')
  urlretrieve("https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all", "./http_proxies.txt")
  with open('http_proxies.txt') as f:
    proxy = random.choice(list(f.readlines())).splitlines()[0]
  return templates.TemplateResponse('index.html', {"request": request, "proxy":proxy, "name":"HTTP"})

@app.get('/socks4', response_class=HTMLResponse)
async def socks4(request:Request):
  print('SOCKS4 Proxy loaded.')
  urlretrieve("https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all&ssl=all&anonymity=all", "./socks4_proxies.txt")
  with open('socks4_proxies.txt') as f:
    proxy = random.choice(list(f.readlines())).splitlines()[0]
  return templates.TemplateResponse('index.html', {"request": request, "proxy":proxy, "name":"SOCKS4"})

@app.get('/socks5', response_class=HTMLResponse)
async def socks5(request:Request):
  print('SOCKS5 Proxy loaded.')
  urlretrieve("https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all&ssl=all&anonymity=all", "./socks5_proxies.txt")
  with open('socks5_proxies.txt') as f:
    proxy = random.choice(list(f.readlines())).splitlines()[0]
  return templates.TemplateResponse('index.html', {"request": request, "proxy":proxy, "name":"SOCKS5"})

uvicorn.run(app,host="0.0.0.0",port="8080")
