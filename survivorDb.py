from pymongo import MongoClient
from survivor import Survivor
import pymongo
class SurvivorDb:

    def __init__(self, database):
        global db
        try:
            db = MongoClient().apilipse[database]
            db.find({})
        except pymongo.errors.ServerSelectionTimeoutError:
            print "Database is taking too long to responde\n - ServerSelectionTimeoutError"
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
            survivorData = db.find({'_id': int(_id)})[0]
            # print survivorData
        except:
            return None
        return self.dataToSurvivor(survivorData)

    def insert(self, name, age, gender, lastLocation , inventory):
        if(isinstance(name,str) and isinstance(age, int) and isinstance(gender,str) and isinstance(lastLocation, tuple) and
        isinstance(lastLocation[0], float) and isinstance(lastLocation[1], float) and isinstance(inventory, dict)):
            survivor = {
            '_id': self.maxid() + 1,
            'name': name,
            'age': age,
            'gender': gender,
            'lastLocation':{
            'x':lastLocation[0],
            'y':lastLocation[1]
            },
            'inventory': inventory,
            'infectionReports': 0
            }
        else:
            raise ValueError('Incorrect type')
        try:
            _id = db.insert_one(survivor).inserted_id
        except ServerSelectionTimeoutError:
            print 'eh isso ai bobs'
        return Survivor(_id, name, age, gender, lastLocation[0],lastLocation[1], inventory, 0)

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
