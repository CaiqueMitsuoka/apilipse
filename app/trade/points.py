class Points:
    def __init__(self):
        self.water = 4
        self.food = 3
        self.medication = 2
        self.ammunition = 1

    def pointsWater(self, qtd):
        return qtd * self.water

    def pointsFood(self, qtd):
        return qtd * self.food

    def pointsMedication(self, qtd):
        return qtd * self.medication

    def pointsAmmunition(self, qtd):
        return qtd * self.ammunition

    def totalPoints(self, inventory):
        points = self
        return inventory.water * points.water + inventory.food * points.food + inventory.medication * points.medication + inventory.ammunition * points.ammunition