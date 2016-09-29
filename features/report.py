import sys
sys.path.append('/database')
from survivorDb import SurvivorDb
db = SurvivorDb()

def reports():
    report = {}
    # get all survivors
    listAllSurvivors = db.getAllSurvivors()
    # count healthy survivors
    healthy = 0
    # count itens of health survivors
    itens = [0,0,0,0]
    # count itens of infected survivors
    lostItens = [0,0,0,0]

    for survivor in listAllSurvivors:
        survivor.inventory
        # is infected?
        if survivor.canTrade():
            healthy += 1
            itens[0],itens[1],itens[2],itens[3] = itens[0] + survivor.getWater(), itens[1] + survivor.getFood(), itens[2] + survivor.getMedication(), itens[3] + survivor.getAmmunition()
        else:
            lostItens[0],lostItens[1],lostItens[2],lostItens[3] = lostItens[0] + survivor.getWater(), lostItens[1] + survivor.getFood(), lostItens[2] + survivor.getMedication(), lostItens[3] + survivor.getAmmunition()

    avgItensPerSurvivor = {}
    pointsLost = {}
    names = ['water','food','medication','ammunition']
    points = 4
    # make dict of itens using names as key and a to iterate
    for a in range(0, 4):
        avgItensPerSurvivor[names[a]] = itens[a] / float(healthy)
        pointsLost[names[a]] = lostItens[a] * points
        points -= 1
    percentegeNonInfected = (healthy * 100) / len(listAllSurvivors)
    percentegeInfected = 100 - percentegeNonInfected
    return {'reports':{
            'itens':{
                'averageItensPerSurvivor':avgItensPerSurvivor,
                'pointsLostPerItem':pointsLost
            },
            'survivors':{
                'percentege':{
                    'infected':percentegeInfected,
                    'nonInfected':percentegeNonInfected
                },
                'absolut':{
                    'infected':len(listAllSurvivors),
                    'nonInfected':healthy
                }
            }
        }
    }
