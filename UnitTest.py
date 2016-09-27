import unittest
import requests
import json
import pdb;
from survivor import Survivor
from survivorDb import SurvivorDb
from trade import assignContent, Trader, getTraders, verifyIntegrity, trade

class TestSurvivorClass(unittest.TestCase):
    def test_init(self):
        survivorTest = Survivor(1,'paranaue', 21, 'M', 15484.3, 22548.1, {'water':1,'food':2,'medication':1,'ammunition': 20},0)
        self.assertEqual(survivorTest.name , 'paranaue')
        self.assertEqual(survivorTest.age , 21)
        self.assertEqual(survivorTest.gender , 'M')
        self.assertEqual(survivorTest.lastLocation['x'] , 15484.3)
        self.assertEqual(survivorTest.lastLocation['y'] , 22548.1)
        self.assertEqual(survivorTest.inventory['water'] , 1)
        self.assertEqual(survivorTest.inventory['food'] , 2)
        self.assertEqual(survivorTest.inventory['medication'] , 1)
        self.assertEqual(survivorTest.inventory['ammunition'] , 20)
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
class TestTrade(unittest.TestCase):
    def test_assignContent(self):
        self.assertEqual([1,3,5,2], assignContent({'water':1,'food':3,'medication':5,'ammunition':2}))
        self.assertEqual([0,3,0,0], assignContent({'food':3}))
        self.assertEqual([0,0,1,1], assignContent({'medication':1,'ammunition':1}))
        self.assertEqual([0,0,0,0], assignContent({}))
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
        self.assertTrue(verifyIntegrity({'trade':[{'id':0,'itens':{}},{'id':0,'itens':{}}]}))
        self.assertFalse(verifyIntegrity({'trade':[{'id':0,'itens':{}},{'ideas':0,'itens':{}}]}))
        self.assertFalse(verifyIntegrity({'trade':[{'id':0,'itens':{}},{'id':0,'itensasd':{}}]}))
        self.assertFalse(verifyIntegrity({'trade':[{'id':0,'itens':{}},{'id':0}]}))
        self.assertFalse(verifyIntegrity({'trade':[{'itens':{}},{'id':0,'itens':{}}]}))
        self.assertFalse(verifyIntegrity({'trade':[]}))
        self.assertFalse(verifyIntegrity({}))
        self.assertTrue(trade({'trade':[{'id':12,'itens':{'water':3}},{'id':24,'itens':{'food':2,'medication':2,'ammunition':2}}]}))
        self.assertTrue(trade({'trade':[{'id':24,'itens':{'water':3}},{'id':12,'itens':{'food':2,'medication':2,'ammunition':2}}]}))


class TestApp(unittest.TestCase):
    # this is not a unit test, but for convenience reasons and not finding a good framework to do that,
    # I made my own test
    # I did TDD but with curl, but now all cases are imported here.
    # There is also a Postman test
    def test_app(self):
        response = postRequest('/api/v1/survivors', {"name":"Douglas Adams","age":42,"gender":"M","lastLocation":{"x":21545.2,"y":12654.1},"inventory":{"water":1,"food":2,"medication":4,"ammunition":10}})
        self.assertEqual(response[1],201)
        id = response[0]['insertedId']

        self.assertEqual(200,requests.get('http://localhost:5000/api/v1/survivors').status_code)

        response = postRequest('/api/v1/update/location',{"id":id,"lastLocation":{"x":12345.1,"y":64521.1}})
        self.assertEqual(response[1],200)
        self.assertEqual(response[0]['updatedId'], id)

        response = postRequest('/api/v1/update/trade',{"trade":
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

        response = postRequest('/api/v1/update/trade',{"trade":
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

        response = postRequest('/api/v1/update/trade',{"trade":
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

        response = postRequest('/api/v1/update/trade',{"trade":
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


        response = requests.get('http://localhost:5000/api/v1/survivors/' + str(id)).json()
        self.assertTrue(bool(response['canTrade']))
        # pdb.set_trace()

        self.assertTrue(1 == postRequest('/api/v1/update/infected',{'id':id})[0]['reported'])


        response = requests.get('http://localhost:5000/api/v1/survivors/' + str(id)).json()
        self.assertTrue(bool(response['canTrade']))
        self.assertTrue(1 == postRequest('/api/v1/update/infected',{'id':id})[0]['reported'])
        response = requests.get('http://localhost:5000/api/v1/survivors/' + str(id)).json()
        self.assertTrue(bool(response['canTrade']))
        self.assertTrue(1 == postRequest('/api/v1/update/infected',{'id':id})[0]['reported'])
        response = requests.get('http://localhost:5000/api/v1/survivors/' + str(id)).json()
        self.assertFalse(bool(response['canTrade']))
        # (field 'name' spelled wrong)                 \/
        response = postRequest('/api/v1/survivors', {"nami":"Douglas Adams","age":42,"gender":"M","lastLocation":{"x":21545.2,"y":12654.1},"inventory":{"water":1,"food":2,"medication":4,"ammunition":10}})
        self.assertEqual(response[1],400)


def postRequest(route, data):
    response = requests.post('http://localhost:5000' + route,data=json.dumps(data),headers={'Content-Type':'application/json'})
    # print response
    # print response.json()
    return (response.json(), response.status_code)

if __name__ == '__main__':
    db = SurvivorDb('survivors')
    unittest.main()
