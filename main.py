import json
import unittest
import datetime
import logging

# Setup basic logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s — %(levelname)s — %(message)s')
logger = logging.getLogger(__name__)

# Load data files
with open("./data-1.json", "r") as f:
    json_data_1 = json.load(f)

with open("./data-2.json", "r") as f:
    json_data_2 = json.load(f)

with open("./data-result.json", "r") as f:
    json_expected_result = json.load(f)

def convert_from_format_1(payload):
    """
    Converts Format 1 data with location as slash-delimited string and UNIX timestamp.
    """
    try:
        location_parts = payload["location"].split("/")
        location = {
            "country": location_parts[0],
            "city": location_parts[1],
            "area": location_parts[2],
            "factory": location_parts[3],
            "section": location_parts[4],
        }

        result = {
            "deviceID": payload["deviceID"],
            "deviceType": payload["deviceType"],
            "timestamp": payload["timestamp"],
            "location": location,
            "data": {
                "status": payload["operationStatus"],
                "temperature": payload["temp"]
            }
        }

        logger.info("Successfully converted Format 1 for deviceID: %s", payload["deviceID"])
        return result
    except (KeyError, IndexError) as e:
        logger.error("Format 1 conversion failed: %s", str(e))
        raise

def convert_from_format_2(payload):
    """
    Converts Format 2 data with ISO timestamp and structured location.
    """
    try:
        # Convert ISO to UNIX timestamp in milliseconds
        iso_timestamp = payload["timestamp"]
        dt = datetime.datetime.fromisoformat(iso_timestamp.replace("Z", "+00:00"))
        unix_timestamp = int(dt.timestamp() * 1000)

        location = {
            "country": payload["country"],
            "city": payload["city"],
            "area": payload["area"],
            "factory": payload["factory"],
            "section": payload["section"]
        }

        result = {
            "deviceID": payload["device"]["id"],
            "deviceType": payload["device"]["type"],
            "timestamp": unix_timestamp,
            "location": location,
            "data": payload["data"]
        }

        logger.info("Successfully converted Format 2 for deviceID: %s", payload["device"]["id"])
        return result
    except (KeyError, ValueError) as e:
        logger.error("Format 2 conversion failed: %s", str(e))
        raise

def normalize_payload(payload):
    """
    Routes payload to correct converter based on schema type.
    """
    if "device" in payload:
        return convert_from_format_2(payload)
    return convert_from_format_1(payload)

class TestPayloadNormalization(unittest.TestCase):
    def test_format_1_conversion(self):
        result = normalize_payload(json_data_1)
        self.assertEqual(result, json_expected_result, "Format 1 conversion failed")

    def test_format_2_conversion(self):
        result = normalize_payload(json_data_2)
        self.assertEqual(result, json_expected_result, "Format 2 conversion failed")

    def test_timestamp_failure(self):
        with self.assertRaises(ValueError):
            bad_payload = json_data_2.copy()
            bad_payload["timestamp"] = "INVALID"
            normalize_payload(bad_payload)

    def test_missing_fields(self):
        with self.assertRaises(KeyError):
            broken_payload = {
                "deviceID": "broken",
                "timestamp": 12345
                # Missing fields
            }
            normalize_payload(broken_payload)

if __name__ == '__main__':
    unittest.main()
