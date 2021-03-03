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

def Preprocess(data):
    return data