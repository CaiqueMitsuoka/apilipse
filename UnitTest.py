import sys
import unittest
import requests
import json
import pdb
import random
sys.path.append('modules')
from survivor import Survivor
from survivorDb import SurvivorDb
from trade import assignContent, Trader, getTraders, verifyIntegrity, trade

# uri = 'https://apilipse.herokuapp.com/api/v1/'
uri = 'http://localhost:5000/api/v1/'

class TestSurvivorClass(unittest.TestCase):
    def test_init(self):
        survivorTest = Survivor(1,{'name':'paranaue','age': 21,'gender': 'M','lastLocation':{'x': 15484.3,'y': 22548.1},'inventory': {'water':1,'food':2,'medication':1,'ammunition': 20}})
        self.assertEqual(survivorTest.name , 'paranaue')
        self.assertEqual(survivorTest.getAge() , 21)
        self.assertEqual(survivorTest.getGender() , 'M')
        self.assertEqual(survivorTest.getLastLocationX() , 15484.3)
        self.assertEqual(survivorTest.getLastLocationY() , 22548.1)
        self.assertEqual(survivorTest.getWater() , 1)
        self.assertEqual(survivorTest.getFood() , 2)
        self.assertEqual(survivorTest.getMedication() , 1)
        self.assertEqual(survivorTest.getAmmunition() , 20)
        self.assertEqual(survivorTest.infectionReports, 0)
        self.assertTrue(survivorTest.canTrade())
        self.assertEqual(survivorTest.survivorToDic(), {
            "id": 1,
            "name": "paranaue",
            "path": "/survivors/1",
            "age": 21,
            "gender": "M",
            "canTrade": True,
            "infectionReports": 0,
            "lastLocation": {
                "x": 15484.3,
                "y": 22548.1
            },
            "inventory": {
                "water": 1,
                "food": 2,
                "medication": 1,
                "ammunition": 20
            }
        })
    # def test_setInventory(self):
    #     survivorTest = Survivor(1,{'name':'paranaue','age': 21,'gender': 'M','lastLocation':{'x': 15484.3,'y': 22548.1},'inventory': {'water':1,'food':2,'medication':1,'ammunition': 20}})


class TestTrade(unittest.TestCase):
    def test_assignContent(self):
        self.assertEqual([1,3,5,2], assignContent({'water':1,'food':3,'medication':5,'ammunition':2}))
        self.assertEqual([0,3,0,0], assignContent({'food':3}))
        self.assertEqual([0,0,1,1], assignContent({'medication':1,'ammunition':1}))
        self.assertEqual([0,0,0,0], assignContent({}))

    def test_getTraders(self):
        self.assertEqual([], getTraders({'trade':[{'id':3,'itens':{'water':2}}]}))
        self.assertEqual([], getTraders({}))
        goodIntegrity = getTraders({'trade':[{'id':12,'itens':{'water':3}},{'id':24,'itens':{'food':2,'medication':2,'ammunition':2}}]})
        self.assertEqual(2,len(goodIntegrity))
        self.assertEqual(12,goodIntegrity[0].id)
        self.assertEqual(12,goodIntegrity[0].getTotalPoints())
        self.assertTrue(goodIntegrity[0].canGiveItens(db))
        self.assertEqual(12,goodIntegrity[1].getTotalPoints())
        self.assertTrue(goodIntegrity[1].canGiveItens(db))
        self.assertEqual(24,goodIntegrity[1].id)

    def test_verifyIntegrity(self):
        self.assertTrue(verifyIntegrity({'trade':[{'id':0,'itens':{}},{'id':0,'itens':{}}]}))
        self.assertFalse(verifyIntegrity({'trade':[{'id':0,'itens':{}},{'ideas':0,'itens':{}}]}))
        self.assertFalse(verifyIntegrity({'trade':[{'id':0,'itens':{}},{'id':0,'itensasd':{}}]}))
        self.assertFalse(verifyIntegrity({'trade':[{'id':0,'itens':{}},{'id':0}]}))
        self.assertFalse(verifyIntegrity({'trade':[{'itens':{}},{'id':0,'itens':{}}]}))
        self.assertFalse(verifyIntegrity({'trade':[]}))
        self.assertFalse(verifyIntegrity({}))

    def test_trade(self):
        self.assertTrue(trade({'trade':[{'id':12,'itens':{'water':3}},{'id':24,'itens':{'food':2,'medication':2,'ammunition':2}}]}))
        self.assertTrue(trade({'trade':[{'id':24,'itens':{'water':3}},{'id':12,'itens':{'food':2,'medication':2,'ammunition':2}}]}))


class TestApp(unittest.TestCase):
    # this is not a unit test, but for convenience reasons and not finding a good framework to do that,
    # I made my own test
    # I did TDD but with curl, but now all cases are imported here.
    # There is also a Postman test

    def test_getAll(self):
        self.assertEqual(200,requests.get(uri + 'survivors').status_code)

    def test_insertPost(self):
        response = postRequest('survivors', {"name":"Douglas Adams","age":42,"gender":"M","lastLocation":{"x":21545.2,"y":12654.1},"inventory":{"water":1,"food":2,"medication":4,"ammunition":10}})
        self.assertEqual(response[1],201)

        # (field 'name' spelled wrong)                 \/
        # response = postRequest('survivors', {"nami":"Douglas Adams","age":42,"gender":"M","lastLocation":{"x":21545.2,"y":12654.1},"inventory":{"water":1,"food":2,"medication":4,"ammunition":10}})
        # self.assertEqual(response[1],422)

    def randm(self):
        return random.random() * 10000

    def test_apiUpdateLocation(self):
        response = putRequest('update/location',{"id":6,"lastLocation":{"x":self.randm(),"y":self.randm()}})
        self.assertEqual(response[1],200)

    def test_apiTrade(self):
        response = putRequest('update/trade',{"trade":
            [
                {
                    "id":4,
                    "itens":{
                        "water":1,
                        "food":2
                    }
                },
                {
                    "id":2,
                    "itens":{
                        "medication":2,
                        "ammunition":6
                    }
                }
            ]
        })
        self.assertEqual(response[1],200)
        # same trade, but oposite, for persistance of the test
        response = putRequest('update/trade',{"trade":
            [
                {
                    "id":2,
                    "itens":{
                        "water":1,
                        "food":2
                    }
                },
                {
                    "id":4,
                    "itens":{
                        "medication":2,
                        "ammunition":6
                    }
                }
            ]
        })
        self.assertEqual(response[1],200)

        response = putRequest('update/trade',{"trade":
            [
                {
                    "id":12,
                    "itens":{
                        "water":2,
                        "food":1,
                        "medication":3,
                        "ammunition":3
                    }
                },
                {
                    "id":18,
                    "itens":{
                        "water":3,
                        "food":1,
                        "medication":1,
                        "ammunition":3
                    }
                }
            ]
        })
        self.assertEqual(response[1],400)

        response = putRequest('update/trade',{"trade":
            [
                { #id misspelled
                    "di":6,
                    "itens":{
                        "water":1,
                        "food":2
                    }
                },
                {
                    "id":2,
                    "itens":{
                        "medication":2,
                        "ammunition":6
                    }
                }
            ]
        })
        self.assertEqual(response[1],422)

    def test_apiReportInfected(self):
        # check if survivor can trade
        surv = {"name":"Douglas Adams","age":42,"gender":"M","lastLocation":{"x":21545.2,"y":12654.1},"inventory":{"water":1,"food":2,"medication":4,"ammunition":10}}
        id = postRequest('survivors', surv)[0]['insertedId']
        uriSurv = uri + 'survivors/' + str(id)
        sendJson = {'id':id}
        response = requests.get(uriSurv).json()
        self.assertTrue(bool(response['canTrade']))
        # pdb.set_trace()

        self.assertTrue(1 == putRequest('update/infected',sendJson)[0]['reported'])


        response = requests.get(uriSurv).json()
        self.assertTrue(bool(response['canTrade']))
        self.assertTrue(1 == putRequest('update/infected',sendJson)[0]['reported'])
        response = requests.get(uriSurv).json()
        self.assertTrue(bool(response['canTrade']))
        self.assertTrue(1 == putRequest('update/infected',sendJson)[0]['reported'])
        response = requests.get(uriSurv).json()
        self.assertFalse(bool(response['canTrade']))

    def apiResports(self):
        response_cod = requests.get(uri + '/reports').status_code
        self.assertEqual(200,response_cod)


def postRequest(route, data):
    response = requests.post(uri + route,data=json.dumps(data),headers={'Content-Type':'application/json'})
    # print response
    # print response.json()
    return (response.json(), response.status_code)

def putRequest(route, data):
    response = requests.put(uri + route,data=json.dumps(data),headers={'Content-Type':'application/json'})
    return (response.json(), response.status_code)

if __name__ == '__main__':
    db = SurvivorDb('survivors')
    unittest.main()
