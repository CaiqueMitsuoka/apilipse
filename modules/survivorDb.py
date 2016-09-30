from pymongo import MongoClient
from survivor import Survivor
import pymongo

class SurvivorDb:

    def __init__(self,database):
        global db
        try:
            db = MongoClient('mongodb://serverv1:adb123@ds029837.mlab.com:29837/heroku_5l2fpwrs').get_default_database()['survivors']
            db.find({})
        except pymongo.errors.ServerSelectionTimeoutError:
            print "Database is taking too long to responde\nIs it running?\n - ServerSelectionTimeoutError"
        except pymongo.errors.ConnectionFailure:
            print "Failed to connect to database"

    def dataToSurvivor(self, survData):
        return Survivor(
            survData['_id'],
            survData,
            survData['infectionReports']
        )

    def getAllSurvivors(self):
        return self.searchByQuery({})

    def searchById(self, _id):
        try:
            survivorData = db.find({'_id': int(_id)})[0]
        except:
            return None
        return self.dataToSurvivor(survivorData)

    def insert(self, objSurvivor):
        survivor = {
            '_id': self.maxid() + 1,
            'name': objSurvivor.getName(),
            'age': objSurvivor.getAge(),
            'gender': objSurvivor.getGender(),
            'lastLocation':{
                'x':objSurvivor.getLastLocationY(),
                'y':objSurvivor.getLastLocationX()
            },
            'inventory': {
                'water': objSurvivor.getWater(),
                'food': objSurvivor.getFood(),
                'medication': objSurvivor.getMedication(),
                'ammunition': objSurvivor.getAmmunition()
            },
            'infectionReports': 0
        }

        try:
            _id = db.insert_one(survivor).inserted_id
        except ServerSelectionTimeoutError:
            return None
        objSurvivor.setId(_id)
        return objSurvivor

    def updateById(self, _id, field, value):
        try:
            return db.update_one({'_id': _id},{"$set":{field: value}})
        except:
            return None

    def canTrade(self, _id):
        if self.searchById(_id).infectionReports < 3:
            return True
        return False

    def searchByQuery(self, query):
        survivorsList = []
        cursor = db.find(query)
        for survivor in cursor:
            survivorsList.append(self.dataToSurvivor(survivor))
        return survivorsList

    def maxid(self):
        return db.find_one(sort=[("_id", -1)])['_id']

    def updateLocation(self, _id, lat, lon):
        try:
            return self.updateById(_id,'lastLocation',{'x':lat,'y':lon}).modified_count
            # self.updateById(_id,'lastLocation.x',lat)
            # self.updateById(_id,'lastLocation.y',lon)
        except:
            return -1

    def reportInfection(self,_id):
        try:
            return self.updateById(_id,'infectionReports',self.searchById(_id).infectionReports + 1).modified_count
        except:
            return -1
