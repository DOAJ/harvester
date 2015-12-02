from copy import deepcopy

class HarvestStateFactory(object):

    @classmethod
    def harvest_state(cls):
        return deepcopy(STATE)

STATE = {
    "issn" : "1234-5678",
    "account" : "123456789",
    "status" : "active",
    "last_harvest" : [
        {
            "plugin" : "epmc",
            "date" : "1970-01-01T00:00:00Z"
        }
    ]
}