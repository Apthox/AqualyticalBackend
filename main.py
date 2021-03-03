from flask import Flask
import json
import os
import process

app = Flask(__name__)

def getData(filename):
    with open(filename) as file:
        data = json.load(file)
        return data

@app.route('/data')
def dataEndpoint():
    data = getData('./data/V3136.json')

    # Preprocess
    data = process.Preprocess(data)

    return data

if __name__ == '__main__':
    app.run()