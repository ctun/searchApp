from flask import Flask, Response, request, jsonify

from json import dumps, load
from os.path import dirname, realpath
from os import environ
import os.path
import sys
from search import findLoc, Location

path =  dirname(realpath(__file__))
path =  dirname(path)    # move up one-level
sys.path.append(path)

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Flask Dockerized'

@app.route('/__health')
def health_check():
    return "ok", 200

@app.route('/search', methods= ['POST'] )
def search():
    result = {}
    content = request.json
    latitude = float(content['latitude'])
    longitude = float(content['longitude'])
    distance = float(content['distance'])
    querytext = content['query']

    # return Response('initiating ' + latitude)
    city = Location(None, None, latitude, longitude)
    found = findLoc(city, distance)

    return jsonify({'total': len(found), 'locations':found})


def main():

    app.run(host='0.0.0.0')
    app.run()

if __name__ == '__main__':
    # app.debug = True
    main()
