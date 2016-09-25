from survivor import Survivor
from survivorDb import SurvivorDb

class Trader:
    id = 0
    water = 0
    food = 0
    medication = 0
    ammunition = 0
    def __init__(self, data, id):
        self.id = id
        self.water, self.food, self.medication, self.ammunition = data

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


# def trade(data):
#     if verifyIntegrity():
#
#     else:
