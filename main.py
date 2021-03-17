from flask import Flask
import json
import os
import process
from flask_cors import CORS

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

if __name__ == '__main__':
    app.run()