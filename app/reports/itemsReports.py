from app.survivor import SurvivorDb
from app.survivor.inventory import Inventory
from app.trade.points import Points


class ItemsReports:

    def getAllSurvivors(self):

        db = SurvivorDb('survivors')
        listAllSurvivors = db.getAllSurvivors()
        db.close()
        return listAllSurvivors

    def items_report(self):
        total_items = Inventory()
        valid_items = Inventory()

        list_all_survivors = self.getAllSurvivors()

        total_non_infected = 0

        for survivor in list_all_survivors:

            total_items.water += survivor.inventory.water
            total_items.food += survivor.inventory.food
            total_items.medication += survivor.inventory.medication
            total_items.ammunition += survivor.inventory.ammunition
            # is infected?
            if survivor.canTrade():
                # if infected
                total_non_infected += 1
                valid_items.water += survivor.inventory.water
                valid_items.food += survivor.inventory.food
                valid_items.medication += survivor.inventory.medication
                valid_items.ammunition += survivor.inventory.ammunition

        total_survivors = len(list_all_survivors)
        points = Points()
        items = {
            'items':{
                'total':{
                    'water':total_items.water,
                    'food':total_items.food,
                    'medication':total_items.medication,
                    'ammunition':total_items.ammunition
                },
                'average': {
                    'total':{
                        'water': total_items.water / total_survivors,
                        'food': total_items.food / total_survivors,
                        'medication': total_items.medication / total_survivors,
                        'ammunition': total_items.ammunition / total_survivors
                    },
                    'non-infected':{
                        'water': valid_items.water / total_survivors,
                        'food': valid_items.food / total_survivors,
                        'medication': valid_items.medication / total_survivors,
                        'ammunition': valid_items.ammunition / total_survivors
                    }
                }
            },
            'points':{
                'total': total_items.calcPoints(),
                'non-infected': valid_items.calcPoints(),
                'per item':{
                    'water':points.pointsWater(total_items.water),
                    'food':points.pointsFood(total_items.food),
                    'medication':points.pointsMedication(total_items.medication),
                    'ammunition':points.pointsAmmunition(total_items.ammunition)
                },
                'lost for infection':{
                    'water': points.pointsWater(total_items.water - valid_items.water),
                    'food': points.pointsFood(total_items.food - valid_items.food),
                    'medication': points.pointsMedication(total_items.medication - valid_items.medication),
                    'ammunition': points.pointsAmmunition(total_items.ammunition - valid_items.ammunition)
                }
            }
        }
        return items
