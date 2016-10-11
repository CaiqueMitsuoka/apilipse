from app.survivor import SurvivorDb


class SurvivorsReport:
    def getAllSurvivors(self):

        db = SurvivorDb('survivors')
        listAllSurvivors = db.getAllSurvivors()
        db.close()
        return listAllSurvivors

    def report_survivor_quantity(self):
        list_all_survivors = self.getAllSurvivors()

        healthy = 0

        for survivor in list_all_survivors:
            # is infected?
            if survivor.canTrade():
                healthy += 1

        total_survivors = len(list_all_survivors)

        percentage_non_infected = (healthy * 100) / len(list_all_survivors)

        percentage_infected = 100 - percentage_non_infected

        return {
            'survivors':
            {
                'Total': total_survivors,
                'percentage': {
                    'infected': percentage_infected,
                    'nonInfected': percentage_non_infected
                },
                'absolute': {
                    'infected': total_survivors - healthy,
                    'nonInfected': healthy
                }
            }
        }

