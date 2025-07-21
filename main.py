import json, unittest, datetime

with open("./data-1.json","r") as f:
    jsonData1 = json.load(f)
with open("./data-2.json","r") as f:
    jsonData2 = json.load(f)
with open("./data-result.json","r") as f:
    jsonExpectedResult = json.load(f)


def convertFromFormat1 (jsonObject):
    # Convert location string to nested object
    location_parts = jsonObject["location"].split("/")
    location = {
        "country": location_parts[0],
        "city": location_parts[1], 
        "area": location_parts[2],
        "factory": location_parts[3],
        "section": location_parts[4]
    }
    
    # Build the result object
    result = {
        "deviceID": jsonObject["deviceID"],
        "deviceType": jsonObject["deviceType"],
        "timestamp": jsonObject["timestamp"],
        "location": location,
        "data": {
            "status": jsonObject["operationStatus"],
            "temperature": jsonObject["temp"]
        }
    }
    
    return result


def convertFromFormat2 (jsonObject):
    # Convert ISO timestamp to Unix timestamp
    iso_timestamp = jsonObject["timestamp"]
    dt = datetime.datetime.fromisoformat(iso_timestamp.replace('Z', '+00:00'))
    unix_timestamp = int(dt.timestamp() * 1000)
    
    # Build location object from separate fields
    location = {
        "country": jsonObject["country"],
        "city": jsonObject["city"],
        "area": jsonObject["area"], 
        "factory": jsonObject["factory"],
        "section": jsonObject["section"]
    }
    
    # Build the result object
    result = {
        "deviceID": jsonObject["device"]["id"],
        "deviceType": jsonObject["device"]["type"],
        "timestamp": unix_timestamp,
        "location": location,
        "data": jsonObject["data"]
    }
    
    return result


def main (jsonObject):

    result = {}

    if (jsonObject.get('device') == None):
        result = convertFromFormat1(jsonObject)
    else:
        result = convertFromFormat2(jsonObject)

    return result


class TestSolution(unittest.TestCase):

    def test_sanity(self):

        result = json.loads(json.dumps(jsonExpectedResult))
        self.assertEqual(
            result,
            jsonExpectedResult
        )

    def test_dataType1(self):

        result = main (jsonData1)
        self.assertEqual(
            result,
            jsonExpectedResult,
            'Converting from Type 1 failed'
        )

    def test_dataType2(self):

        result = main (jsonData2)
        self.assertEqual(
            result,
            jsonExpectedResult,
            'Converting from Type 2 failed'
        )

if __name__ == '__main__':
    unittest.main()
