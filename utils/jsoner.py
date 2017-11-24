import json


class Location:
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng

    def load_from_json(self):
        return "NotImplemented!Sorry!"

    def parse_to_json_parts(self):
        location = \
            {
                "lat": self.lat,
                "lng": self.lng
            }
        return location


class Clothes:
    """
    @param top1: color
    @param top2: color
    @param top3: color
    @param bottom: color
    """

    def __init__(self, top1, top2, top3, bottom):
        self.top1 = top1
        self.top2 = top2
        self.top3 = top3
        self.bottom = bottom

    def load_from_json(self):
        return "NotImplemented!Sorry!"

    def parse_to_json_parts(self):
        clothes = \
            {
                "tops": {
                    "top1": self.top1,
                    "top2": self.top2,
                    "top3": self.top3
                },
                "bottom": self.bottom
            }
        return clothes


class Handler:
    def __init__(self, username, location, clothes):
        """
        Before you call this method, you need to make `location` object and
        `clothes` object and to do `parse_to_json_parts()` in each instance.
        """
        self.username = username
        self.location = location
        self.clothes = clothes

        print("Before you call this method,you need to make `location` object and `clothes` object.")
        print("args:username, location, clothes")

    def load_from_json(self):
        pass

    def parse_to_json(self):
        user_data = \
            {
                "username": self.username,
                "location": self.location,
                "clothes": self.clothes
            }
        return json.dumps(user_data)


dummy_users = {'key1': {
    "username": "hashimoto",
    "location": {
        "lat": 35.0,
        "lng": 135.9
    },
    "clothes": {
        "tops": {
            "top1": "image_url1",
            "top2": "image_url2",
            "top3": "image_url3"
        },
        "bottom": {
            "bottom": "bottom_url"
        }
    }
}, 'key2': {
    "username": "shirata",
    "location": {
        "lat": 35.0,
        "lng": 135.0
    },
    "clothes": {
        "tops": {
            "top1": "image_url1",
            "top2": "image_url2",
            "top3": "image_url3"
        },
        "bottom": {
            "bottom": "bottom_url"
        }
    }
}}

#
# dummy = json.dumps(dummy_users)
#
# print dummy
#
# load_json = json.loads(dummy)
# print load_json['key1']
