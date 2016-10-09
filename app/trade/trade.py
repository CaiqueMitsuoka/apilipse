from app.survivor import SurvivorDb


def assignContent(itens):
    typeItens = ['water','food','medication','ammunition']
    listItens = {}
    for a in range(len(typeItens)):
        if typeItens[a] in itens:
            listItens[typeItens[a]] = itens[typeItens[a]]
        else:
            listItens[typeItens[a]] = 0
    return listItens

def verifyIntegrity(data):
    if ('trade' in data and len(data['trade']) == 2):
        trade = data['trade']
        if ('id' in trade[0]) and ('id' in trade[1]):
            if ('itens' in trade[0]) and ('itens' in trade[1]):
                return True
    return False

def calcPoints(itens):
    return itens['water'] * 4 + itens['food'] * 3 + itens['medication'] * 2 + itens['ammunition']

def equalPoints(itensLeft,itensRight):
    if calcPoints(itensLeft) == calcPoints(itensRight):
        return True
    return False

def trade(data):
    data = data['trade']
    if verifyIntegrity(data):
        db = SurvivorDb('survivors')
        trade = data['trade']
        tradeLeft = db.searchById(trade[0]['id'])
        itensLeft = assignContent(trade[0]['itens'])
        tradeRight = db.searchById(trade[1]['id'])
        itensRight = assignContent(trade[1]['itens'])
        if tradeLeft.canGiveItens(itensLeft) and tradeRight.canGiveItens(itensRight) and equalPoints(itensLeft,itensRight):
            db.updateById(tradeLeft.getId(), 'inventory', tradeLeft.performTrade(itensLeft,itensRight))
            db.updateById(tradeRight.getId(), 'inventory', tradeRight.performTrade(itensRight,itensLeft))
            result = (tradeLeft.survivorToDic() , 200)
        else:
            result = 422
        db.close()
    else:
        result = 404
    return result
