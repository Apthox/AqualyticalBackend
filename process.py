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

        dict = {"Duration": duration, "Start": start, "End": end, "Predicted": predicted, "VarsConcept": track['varsConcept'], "EventCount": eventCount, "UUID": track['events'][0]['uuid']}
        new_list.append(dict)

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
