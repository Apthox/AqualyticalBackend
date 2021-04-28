from flask import Flask, send_file, request
import json
import os
import process
import pytest
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

# ./data
# ./data/V3136/ -> create folder for data
# ./data/V3136/Summary.json
# ./data/V3136/V3136.json // READ ONLY
# ./data/V3136/t*/*.png
# @Shawn TODO: complete this functional POST request to update the data
# Receiving object { varsConceptID, varsConceptName } 

@app.route('/update', methods=["POST"])
def updateTrack():
  update_data = request.get_json()
  print(update_data)

  update = getData('./data/V3136.json')
  for track in update['data']['tracks']:
    if track['events'][0]['uuid'] == update_data['varsConcaptID']:
      track['varsConcept'] = update_data['varsConceptName']

      with open('./data/update.json', 'w') as outfile:
        json.dump(update, outfile)
      break

  return "pass"


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
