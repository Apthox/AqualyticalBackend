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

    return new_list



# with open('/Users/shawn/Desktop/CST 499/AqualyticalBackend/data/V3136.json') as json_file:
#     data = json.load(json_file)

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
