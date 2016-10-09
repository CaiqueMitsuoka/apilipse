from app.survivor import SurvivorDb

from survivorsReports import report_survivor_quantity



def get_reports():
    db = SurvivorDb('survivors')
    report = {}
    # get all survivors
    listAllSurvivors = db.getAllSurvivors()
    # count healthy survivors
    healthy = 0
    # count items of health survivors
    items = [0, 0, 0, 0]
    # count items of infected survivors
    lost_itens = [0, 0, 0, 0]

    for survivor in listAllSurvivors:
        # is infected?
        if survivor.canTrade():
            healthy += 1
            items[0] = items[0] + survivor.inventory.water
            items[1] = items[1] + survivor.inventory.food
            items[2] = items[2] + survivor.inventory.medication
            items[3] = items[3] + survivor.inventory.ammunition

        else:
            lost_itens[0] = lost_itens[0] + survivor.inventory.water
            lost_itens[1] = lost_itens[1] + survivor.inventory.food
            lost_itens[2] = lost_itens[2] + survivor.inventory.medication
            lost_itens[3] = lost_itens[3] + survivor.inventory.ammunition

    avg_items_per_survivor = {}
    points_lost = {}
    names = ['water', 'food', 'medication', 'ammunition']
    points = 4
    # make dict of items using names as key and a to iterate
    for a in range(0, 4):
        avg_items_per_survivor[names[a]] = items[a] / float(healthy)
        points_lost[names[a]] = lost_itens[a] * points
        points -= 1
    return {
        'reports':
            {
                'itens': {
                    'averageItensPerSurvivor': avg_items_per_survivor,
                        'pointsLostPerItem': points_lost
                    },
                'survivors': report_survivor_quantity()
            }
    }
