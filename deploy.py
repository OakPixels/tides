from flask import Flask, request

# Tides
import urllib3
from bs4 import BeautifulSoup

app = Flask(__name__)

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
    for type in types:
        type = type.text.strip()
        type = type[:-5]
        new_types.append(type)
    # Remove Header
    new_types.pop(0)

    tides = soup.find_all('td', attrs={'class' : 'tar'})
    for tide in tides:
        tide = tide.text.strip()
        tide = tide[:-1]
        new_tides.append(tide)
    # Remove Header
    new_tides.pop(0)

    times = soup.find_all('td', attrs={'class' : 'tac'})
    for time in times:
        time = time.text.strip()
        new_times.append(time)
    # Remove Header
    new_times.pop(0)

    # Edit Types
    for index, type in enumerate(new_types, start=0):
        text['extremes'][index]['type'] = type

    # Edit Tides
    for index, tide in enumerate(new_tides, start=0):
        text['extremes'][index]['height'] = tide

    # Edit Times
    for index, time in enumerate(new_times, start=0):
        text['extremes'][index]['time'] = time

    return text
