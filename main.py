from flask import Flask, send_file, request
import json
import os
import process
from flask_cors import CORS
import processor

app = Flask(__name__)
CORS(app)

def getData(filename):
    with open(filename) as file:
        data = json.load(file)
        return data

# todo: add call for requesting available datasets

# todo: add parameter for selecting dataset
@app.route('/data')
def dataEndpoint():
    data = getData('./data/V3136.json')

    # Preprocess
    data = process.Preprocess(data)

    return json.dumps(data)

@app.route('/img')
def getImage():
    uuid = request.args.get('uuid')
    frame = request.args.get('frame')

    return send_file('exports/V3136/' + uuid + '/frame-' + frame + '.jpg')

@app.route('/init')
def init():
    processor.process('V3136')

    return

if __name__ == '__main__':
    app.run()