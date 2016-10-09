import sys, os

from app.survivor import SurvivorDb

sys.path.append(os.path.abspath('..'))


def report_survivor_quantity():
    db = SurvivorDb('survivors')
    # get all survivors
    list_all_survivors = db.getAllSurvivors()
    # count healthy survivors
    healthy = 0

    for survivor in list_all_survivors:
        # is infected?
        if survivor.canTrade():
            healthy += 1

    percentage_non_infected = (healthy * 100) / len(list_all_survivors)
    percentage_infected = 100 - percentage_non_infected
    db.close()
    return {
        'Total': len(list_all_survivors),
        'percentage': {
            'infected': percentage_infected,
            'nonInfected': percentage_non_infected
        },
        'absolute': {
            'infected': len(list_all_survivors) - healthy,
            'nonInfected': healthy
        }
    }
