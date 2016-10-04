# -*- coding: <UTF-8> -*-
import json
class Survivor:
    _id = None
    name = ''
    age = 0
    gender = ''
    lastLocation = {'x':.0,'y':.0}
    infectionReports = 0
    water = 0
    food = 0
    medication = 0
    ammunition = 0
    def __init__(self, _id, data, infectRep=0):
        self._id = int(_id)
        self.name = str(data['name'])
        self.age = int(data['age'])
        self.gender = str(data['gender'])
        self.lastLocation['x'] = float(data['lastLocation']['x'])
        self.lastLocation['y'] = float(data['lastLocation']['y'])
        self.setInventory(data['inventory'])
        self.infectionReports = infectRep

    def setInventory(self, invent):
        self.water = self.food = self.medication = self.ammunition = 0
        if 'water' in invent:
            self.water = invent['water']
        if 'food' in invent:
            self.food = invent['food']
        if 'medication' in invent:
            self.medication = invent['medication']
        if 'ammunition' in invent:
            self.ammunition = invent['ammunition']

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
                "water": self.water
                ,"food": self.food
                ,"medication":self.medication
                ,"ammunition": self.ammunition
            }
        }
        return dictSurvivor

    def getTotalPoints(self):
        return self.water * 4 + self.food * 3 + self.medication * 2 + self.ammunition

    def canGiveItens(self, givingItens):
        if self.canTrade():
            # giving more than his have
            if (givingItens['water'] <= self.water) and (givingItens['food'] <= self.food) and (givingItens['medication'] <= self.medication) and (givingItens['ammunition'] <= self.ammunition):
                return True
        return False

    def setId(self,_id):
        self._id = _id
    def getId(self):
        return self._id
    def getName(self):
        return self.name
    def getAge(self):
        return self.age
    def getGender(self):
        return self.gender
    def getLastLocationX(self):
        return self.lastLocation['x']
    def getLastLocationY(self):
        return self.lastLocation['y']
    def getWater(self):
        return self.water
    def getFood(self):
        return self.food
    def getMedication(self):
        return self.medication
    def getAmmunition(self):
        return self.ammunition

    def getListInventory(self):
        return {'water':self.getWater(),'food':self.getFood(),'medication':self.getMedication(),'ammunition':self.getAmmunition()}

    def performTrade(self, give, receive):
        self.water = self.water - give['water'] + receive['water']
        self.food = self.food - give['food'] + receive['food']
        self.medication = self.medication - give['medication'] + receive['medication']
        self.ammunition = self.ammunition - give['ammunition'] + receive['ammunition']
        return self.getListInventory()
