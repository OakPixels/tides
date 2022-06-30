from flask import Flask, request

# Tides
import urllib3
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def tides():
    """Send tides"""
    http = urllib3.PoolManager()
    text = {"status":200,"callCount":1,"copyright":"Copyright","requestLat":54.597286,"requestLon":-5.93012,"responseLat":54.6,"responseLon":-5.9167,"atlas":"TPXO","station":"BELFAST",
    "extremes":[{"time":"","height":0,"type":"High"},{"time":"","height":0,"type":"Low"},{"time":"","height":0,"type":"High"},{"time":"","height":0,"type":"Low"}]}
    # Select Tide 1
    # print(text['extremes'][0])
    # Open data
    url = 'https://www.tidetimes.org.uk/belfast-tide-times'
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data, "html.parser")
    new_types = []
    new_times = []
    new_tides = []

    types = soup.find_all('td', attrs={'class' : 'tal'})
    types.pop(0)
    for num in range(0,4):
        type = types[num].text.strip()
        new_types.append(type)
    # Remove Header

    tides = soup.find_all('td', attrs={'class' : 'tar'})
    for tide in tides:
        tide = tide.text.strip()
        tide = tide[:-1]
        new_tides.append(tide)
    # Remove Header
    new_tides.pop(0)

    times = soup.find_all('td', attrs={'class' : 'tac'})
    # Remove non times depending on amount of tides
    if len(new_tides) == 3:
        cuttimes = times[1:4]
    else:
        cuttimes = times[1:5]
    print(cuttimes)
    for time in cuttimes:
        time = time.text.strip()
        new_times.append(time)

    # Edit Types
    for num in range(0,4):
        text['extremes'][num]['type'] = type

    # Edit Tides
    for num in range(0,4):
        text['extremes'][num]['height'] = tide

    # Edit Times
    for num in range(0,4):
        text['extremes'][num]['time'] = time

    return text
