from pymongo import MongoClient
from survivor import Survivor
import pymongo

class SurvivorDb:
    def __init__(self,database):
        try:
            # self.connection = MongoClient(DATABASE_URI)
            # self.db = connection.get_default_database()[database]
            self.connection = MongoClient()
            self.db = self.connection.apilipse[database]
            self.db.find({})
        except pymongo.errors.ServerSelectionTimeoutError:
            print "Database is taking too long to responde\nIs it running?\n - ServerSelectionTimeoutError"
        except pymongo.errors.ConnectionFailure:
            print "Failed to connect to database"

    def dataToSurvivor(self, survData):
        return Survivor(
            survData['_id'],
            survData['name'],
            survData['age'],
            survData['gender'],
            survData['lastLocation']['x'],
            survData['lastLocation']['y'],
            survData['inventory'],
            survData['infectionReports']
        )

    def getAllSurvivors(self):
        return self.searchByQuery({})

    def searchById(self, _id):
        try:
            survivorData = self.db.find({'_id': int(_id)})[0]
        except:
            return None
        return self.dataToSurvivor(survivorData)

    def insert(self, objSurvivor):
        survivor = {
            '_id': self.maxid() + 1,
            'name': objSurvivor.name,
            'age': objSurvivor.age,
            'gender': objSurvivor.gender,
            'lastLocation':{
                'x':objSurvivor.lastLocation.x,
                'y':objSurvivor.lastLocation.y
            },
            'inventory': {
                'water': objSurvivor.inventory.water,
                'food': objSurvivor.inventory.food,
                'medication': objSurvivor.inventory.medication,
                'ammunition': objSurvivor.inventory.ammunition
            },
            'infectionReports': 0
        }

        try:
            _id = self.db.insert_one(survivor).inserted_id
        except ServerSelectionTimeoutError:
            return None
        objSurvivor._id = _id
        return objSurvivor

    def updateById(self, _id, field, value):
        # try:
        return self.db.update_one({'_id': _id},{"$set":{field: value}})
        # except:
        #     return None

    def canTrade(self, _id):
        if self.searchById(_id).infectionReports < 3:
            return True
        return False

    def searchByQuery(self, query):
        survivorsList = []
        cursor = self.db.find(query)
        for survivor in cursor:
            survivorsList.append(self.dataToSurvivor(survivor))
        return survivorsList

    def maxid(self):
        return self.db.find_one(sort=[("_id", -1)])['_id']

    def updateLocation(self, _id, lat, lon):
        # try:
        return self.updateById(_id,'lastLocation',{'x':lat,'y':lon})
            # self.updateById(_id,'lastLocation.x',lat)
            # self.updateById(_id,'lastLocation.y',lon)
        # except:
        #     return None

    def reportInfection(self,_id):
        try:
            return self.updateById(_id,'infectionReports',self.searchById(_id).infectionReports + 1).modified_count
        except:
            return -1

    def insertSurvivor(self, new_survivor_inf):
        if 'name' in new_survivor_inf and 'age' in new_survivor_inf and 'gender' in new_survivor_inf:
            if 'lastLocation' in new_survivor_inf and 'inventory' in new_survivor_inf:
                new_survivor_obj = Survivor(0, new_survivor_inf['name'],
                                            new_survivor_inf['age'],
                                            new_survivor_inf['gender'],
                                            new_survivor_inf['lastLocation']['x'],
                                            new_survivor_inf['lastLocation']['y'],
                                            new_survivor_inf['inventory'])
                new_survivor_obj = self.insert(new_survivor_obj)
                return new_survivor_obj
        return None

    def close(self):
        self.connection.close()
