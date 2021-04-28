"""
Desired Output = [
    {
        duration: 10, // end - start
        start: 7, // earliest event timestamp
        end: 17, // latest event timestamp
        predicted: 'crab', // predictedVar variable
        eventCount: 5 // length of events array
    },
    ...
]
"""
import json

def Preprocess(data):
    new_list = []
    trackNum = 0

    with open('./data/update.json', 'w') as outfile:
        json.dump(data, outfile)

    for track in data['data']['tracks']:
        start = min(x['time'] for x in track['events'])
        end = max(x['time'] for x in track['events'])
        duration = end - start
        predicted = track['predictedVarsConcept']
        eventCount = len(track['events'])
        
        frames = []
        for event in track['events']:
            frames.append(int(event['time'] * 30))
        dict = {"Duration": duration, "Start": start, "End": end, "Predicted": predicted, "EventCount": eventCount, "UUID": track['events'][0]['uuid'], "Frames": frames}
        new_list.append(dict)

        if track['varsConcept'] == "Unknown":
          color = "#FFFFFF"
        elif predicted == track['varsConcept']:
          color = "#90EE90"
        elif track['varsConcept'] == "":
          color = "#FF0000"
        else:
          color = "#ffcccb"

        dict = {"Duration": duration, "Start": start, "End": end, "Predicted": predicted, "EventCount": eventCount, "Track": trackNum, "Visual": color}
        new_list.append(dict)
        trackNum += 1
    return new_list

# update_data = {'varsConcaptID': '4d54c131-dc23-47d5-a257-147c516eff41',
#                 'varsConceptName': 'Testing'}

# with open('./data/V3136.json') as f:
#   update = json.load(f)

# for track in update['data']['tracks']:
#     if track['events'][0]['uuid'] == update_data['varsConcaptID']:
#         print("TEST")
#         track['varsConcept'] = update_data['varsConceptName']

#         with open('./data/update.json', 'w') as outfile:
#             json.dump(update, outfile)

# new_list = []

# for track in data['data']['tracks']:
#     start = min(x['time'] for x in track['events'])
#     end = max(x['time'] for x in track['events'])
#     duration = end - start
#     predicted = track['predictedVarsConcept']
#     eventCount = len(track['events'])
#     dict = {"Duration": duration, "Start": start, "End": end, "Predicted": predicted, "EventCount": eventCount}
#     new_list.append(dict)

# print(new_list[0])
