# -*- coding: <UTF-8> -*-

from app.survivor.inventory import Inventory
from app.survivor.lastLocation import LastLocation


class Survivor:
    def __init__(self, _id, name, age, gender, last_location_x, last_location_y, inventory, infectRep=0):
        self._id = int(_id)
        self.name = str(name)
        self.age = int(age)
        self.gender = str(gender)
        self.lastLocation = LastLocation(last_location_x,last_location_y)
        self.inventory = Inventory(inventory)
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
                "x": self.lastLocation.x,
                "y": self.lastLocation.y
            }
            , "inventory": {
                "water": self.inventory.water
                ,"food": self.inventory.food
                ,"medication":self.inventory.medication
                ,"ammunition": self.inventory.ammunition
            }
        }
        return dictSurvivor

    def canGiveItens(self, givingItens):
        if self.canTrade() and (givingItens.water <= self.inventory.water) and (
                givingItens.food <= self.inventory.food) and (
                givingItens.medication <= self.inventory.medication) and (
                givingItens.ammunition <= self.inventory.ammunition):
            return True
        return False

    def getListInventory(self):
        return {
            'water':self.inventory.water,
            'food':self.inventory.food,
            'medication':self.inventory.medication,
            'ammunition':self.inventory.ammunition
        }

    def performTrade(self, give, receive):
        self.inventory.water = self.inventory.water - give.water + receive.water
        self.inventory.food = self.inventory.food - give.food + receive.food
        self.inventory.medication = self.inventory.medication - give.medication + receive.medication
        self.inventory.ammunition = self.inventory.ammunition - give.ammunition + receive.ammunition
        return self.getListInventory()
