# -*- coding: <UTF-8> -*-
import json
class Survivor:
    _id = None
    name = ''
    age = 0
    gender = ''
    lastLocation = {'x':.0,'y':.0}
    inventory = {}
    infectionReports = 0

    def __init__(self, _id , name, age, gender, lat, lon, invent, infectRep=0):
        # TODO:missing handler
        self._id = int(_id)
        self.name = str(name)
        self.age = int(age)
        self.gender = str(gender)
        self.lastLocation['x'] = float(lat)
        self.lastLocation['y'] = float(lon)
        self.inventory = dict(invent)
        self.infectionReports = infectRep


    def canTrade(self):
        if self.infectionReports < 3:
            return True
        return False

    def survivorToDic(self):
        dictSurvivor = {"id":self._id
            , "path": '/survivor/' + str(self._id)
            , "name": self.name
            , "age": self.age
            , "gender": self.gender
            , "infectionReports": self.infectionReports
            , "canTrade": self.canTrade()
            , "lastLocation": {
                "x": self.lastLocation['x']
                ,"y": self.lastLocation['y']
            }
            , "inventory": {
                "water": self.inventory['water']
                ,"food": self.inventory['food']
                ,"medication":self.inventory['medication']
                ,"ammunition": self.inventory['ammunition']
            }
        }
        return dictSurvivor
