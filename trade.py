from survivor import Survivor
from survivorDb import SurvivorDb

class Trader:
    id = 0
    water = 0
    food = 0
    medication = 0
    ammunition = 0
    inventory = {}
    def __init__(self, data, id):
        self.id = id
        self.water, self.food, self.medication, self.ammunition = data

    def getTotalPoints(self):
        return self.water * 4 + self.food * 3 + self.medication * 2 + self.ammunition

    def canGiveItens(self,db):
        survivor = db.searchById(self.id)
        if not (survivor == None) and survivor.canTrade():
            self.inventory = survivor.inventory
            if (self.inventory['water'] >= self.water) and (self.inventory['food'] >= self.food) and (self.inventory['medication'] >= self.medication) and (self.inventory['ammunition'] >= self.ammunition):
                return True
        return False

    def listItens(self):
        return [self.water,self.food,self.medication,self.ammunition]

    def prepareTrade(self, receive):
        # self.inventory = db.searchById(self.id).inventory
        self.inventory['water'] = (self.inventory['water'] - self.water) + receive[0]
        self.inventory['food'] = (self.inventory['food'] - self.food) + receive[1]
        self.inventory['medication'] = (self.inventory['medication'] - self.medication) + receive[2]
        self.inventory['ammunition'] = (self.inventory['ammunition'] - self.ammunition) + receive[3]
        qtt = 0
        for item in self.inventory:
            if item >= 0:
                qtt += 1
        if qtt == len(self.inventory):
            return True
        return False

    def commitTrade(self,db):
        r = db.updateById(self.id,'inventory',self.inventory)
        return r

def assignContent(itens):
    typeItens = ['water','food','medication','ammunition']
    listItens = []
    for a in range(len(typeItens)):
        if typeItens[a] in itens:
            listItens.append(itens[typeItens[a]])
        else:
            listItens.append(0)
    return listItens

# aqui soh entra dict ja parseado
def getTraders(data):
    try:
        # vetorizar po
        p1 = data['trade'][0]
        p2 = data['trade'][1]
        tradeRight = Trader(assignContent(p1['itens']),p1['id'] )
        tradeLeft = Trader(assignContent(p2['itens']), p2['id'] )
        return [tradeRight,tradeLeft]
    except (KeyError, ValueError, IndexError ):
        return []

def verifyIntegrity(data):
    if ('trade' in data and len(data['trade']) == 2):
        trade = data['trade']
        if ('id' in trade[0]) and ('id' in trade[1]):
            if ('itens' in trade[0]) and ('itens' in trade[1]):
                return True
    return False

def trade(data):
    if verifyIntegrity(data):
        tradeRight, tradeLeft = getTraders(data)
        db = SurvivorDb('survivors')
        if tradeLeft.canGiveItens(db) and tradeRight.canGiveItens(db):
            if tradeRight.prepareTrade(tradeLeft.listItens()) and tradeLeft.prepareTrade(tradeRight.listItens()):
                tradeLeft.commitTrade(db)
                tradeRight.commitTrade(db)
                return True
            else:
                raise ValueError('Give more itens than have')
        else:
            return False
    else:
        raise KeyError('Missing key in JSON request')
