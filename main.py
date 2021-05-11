from flask import Flask, send_file, request, Response
import json
import os
import process
import pytest
from flask_cors import CORS
# import processor
import re

app = Flask(__name__)
CORS(app)

@app.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response

def getData(filename, updated):
  lastestFilename = ""
  if os.path.exists(updated):
    lastestFilename = updated
  else:
    lastestFilename = filename

  with open(lastestFilename) as file:
    data = json.load(file)
    return data

# todo: add call for requesting available datasets

# todo: add parameter for selecting dataset
@app.route('/data')
def dataEndpoint():
  data = getData('./data/V3136.json', './data/update.json')

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

  update = getData('./data/V3136.json', './data/update.json')
  for track in update['data']['tracks']:
    if track['events'][0]['uuid'] == update_data['varsConceptID']:
      track['varsConcept'] = update_data['varsConceptName']

      with open('./data/update.json', 'w') as outfile:
        json.dump(update, outfile)
      break

  return "pass"


# @app.route('/img')
# def getImage():
#     uuid = request.args.get('uuid')
#     frame = request.args.get('frame')

#     return send_file('exports/V3136/' + uuid + '/frame-' + frame + '.jpg')

@app.route('/video')
def getVideo():
  uuid = request.args.get('uuid')

  # return send_file('exports/V3136/' + uuid + '/source.mov')

  full_path = 'exports/V3136/' + uuid + '/source.webm'
  file_size = os.stat(full_path).st_size
  start = 0
  length = 10240  # can be any default length you want

  range_header = request.headers.get('Range', None)
  if range_header:
      m = re.search('([0-9]+)-([0-9]*)', range_header)  # example: 0-1000 or 1250-
      g = m.groups()
      byte1, byte2 = 0, None
      if g[0]:
          byte1 = int(g[0])
      if g[1]:
          byte2 = int(g[1])
      if byte1 < file_size:
          start = byte1
      if byte2:
          length = byte2 + 1 - byte1
      else:
          length = file_size - start

  with open(full_path, 'rb') as f:
      f.seek(start)
      chunk = f.read(length)

  rv = Response(chunk, 206, mimetype='video/webm', content_type='video/webm', direct_passthrough=True)
  rv.headers.add('Content-Range', 'bytes {0}-{1}/{2}'.format(start, start + length - 1, file_size))
  return rv

@app.route('/video2/<uuid>')
def getVideo2(uuid):
  print("hello there")
  full_path = 'exports/V3136/' + uuid + '/source.webm'
  # full_path = 'imports/V3136.mp4'
  return send_file(full_path, 'video/webm')

@app.route('/image')
def getImage():
  print("hello")
  uuid = request.args.get('uuid')
  full_path = 'exports/V3136/' + uuid + '/thumbnail.png'
  return send_file(full_path, 'image/png')

# @app.route('/init')
# def init():
#     processor.process('V3136')

#     return

if __name__ == '__main__':
  app.run(host='0.0.0.0')
  # app.run(debug=True)
