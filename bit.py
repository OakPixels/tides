from flask import Flask, request

# Tides
import urllib3
from bs4 import BeautifulSoup
# from flask_cors import CORS

app = Flask(__name__)
# CORS(app)
print('working away at something...')

# @app.route("/")
def bitprice():
    """Get Bitcoin Price"""
    http = urllib3.PoolManager()
    url = 'https://google.com/search?q=bitcoinprice'
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data, "html.parser")
    types = soup.find('div', attrs={'class' : 'BNeawe iBp4i AP7Wnd'})
    print(types)
    print('decode')
    type = types.text.strip().split()
    print(type[0])
    return soup

bitprice()
