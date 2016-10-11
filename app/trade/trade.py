from flask import jsonify

from app.survivor import SurvivorDb
from app.survivor.inventory import Inventory
from app.trade.points import Points


class TradeManager:

    def __init__(self, trade_json):
        trade_left_json = trade_json['trade'][0]
        trade_right_json = trade_json['trade'][1]
        self.items_left = Inventory(trade_left_json['itens'])
        self.items_right = Inventory(trade_right_json['itens'])
        db = SurvivorDb('survivors')
        self.traderLeft = db.searchById(trade_left_json['id'])
        self.traderRight = db.searchById(trade_right_json['id'])
        db.close()

    def calcPoints(self, items):
        points = Points()
        return (items.water * points.water) + (items.food * points.food) + (items.medication * points.medication) + (items.ammunition * points.ammunition)

    def equalPoints(self):
        if self.calcPoints(self.items_left) == self.calcPoints(self.items_right):
            return True
        return False

    def trade(self):
        if self.traderLeft is not None and  self.traderRight is not None:

            if self.equalPoints() and self.traderLeft.canTrade() and self.traderRight.canTrade():

                if self.traderLeft.canGiveItens(self.items_left) and self.traderRight.canGiveItens(self.items_right):

                    new_inventory_left = self.traderLeft.performTrade(self.items_left, self.items_right)
                    new_inventory_right = self.traderRight.performTrade(self.items_right,self.items_left)

                    db = SurvivorDb('survivors')
                    db.updateById( self.traderLeft._id, 'inventory', new_inventory_left)
                    db.updateById( self.traderRight._id, 'inventory', new_inventory_right)
                    db.close()

                    response_json = {
                        'trade':
                            [
                                self.traderLeft.survivorToDic(),
                                self.traderRight.survivorToDic()
                            ]
                    }
                    return jsonify(response_json), 200

                else:
                    json = {'error':'survivor is giving more itens then he can'}
                    return jsonify(json), 409
            else:
                json = {'error':'trade is only possible with same quantity of points and survivors isn\'t infected'}
                return jsonify(json), 409
        else:
            json = {'error':'survivor not found'}
            return jsonify(json), 404

def verifyTradeIntegrity(trade_request_json):
    if ('trade' in trade_request_json and len(trade_request_json['trade']) == 2):
        trade = trade_request_json['trade']
        if ('id' in trade[0]) and ('id' in trade[1]):
            if ('itens' in trade[0]) and ('itens' in trade[1]):
                return True
    return False