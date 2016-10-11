# -*- coding: <UTF-8> -*-
from app.trade.points import Points


class Inventory:
    def __init__(self, inventory_json = {}):
        self.water = 0
        self.food = 0
        self.medication = 0
        self.ammunition = 0
        if 'water' in inventory_json:
            self.water = inventory_json['water']
        if 'food' in inventory_json:
            self.food = inventory_json['food']
        if 'medication' in inventory_json:
            self.medication = inventory_json['medication']
        if 'ammunition' in inventory_json:
            self.ammunition = inventory_json['ammunition']

    def calcPoints(self):
        return Points().totalPoints(self)