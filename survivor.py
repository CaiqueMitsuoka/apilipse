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
            , "path": '/survivors/' + str(self._id)
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
    def getWater(self):
        return self.inventory['water']
    def getFood(self):
        return self.inventory['food']
    def getMedication(self):
        return self.inventory['medication']
    def getAmmunition(self):
        return self.inventory['ammunition']

    def getListInventory(self):
        return [self.getWater(),self.getFood(),self.getMedication(),self.getAmmunition()]
