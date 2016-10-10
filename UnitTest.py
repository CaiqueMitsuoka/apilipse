import sys
import unittest
import requests
import json
import pdb
import random

from app.survivor import Survivor
from app.survivor import SurvivorDb
from app.trade.trade import verifyIntegrity, assignContent, trade


# uri = 'https://apilipse.herokuapp.com/api/v1/'
uri = 'http://localhost:5000/api/v1/'

class TestSurvivorClass(unittest.TestCase):
    inventory = {
        'water':1,
        'food':2,
        'medication':1,
        'ammunition': 20
    }
    survivorTest = Survivor(1,'paranaue', 21,'M', 15484.3, 22548.1,inventory)

    def test_survivorToDic(self):
        dict_expected_from_default_survivor = {
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
        }
        self.assertEqual(self.survivorTest.survivorToDic(), dict_expected_from_default_survivor)

    def test_canGiveItens(self):
        self.assertTrue(self.survivorTest.canGiveItens(self.inventory))

    def test_canGiveItensWaterWrong(self):
        inventory_with_more_water = {'water':2,'food':2,'medication':1,'ammunition':20}
        self.assertFalse(self.survivorTest.canGiveItens(inventory_with_more_water))

    def test_canGiveItensFoodWrong(self):
        inventory_with_more_food = {'water': 1, 'food': 3, 'medication': 1, 'ammunition': 20}
        self.assertFalse(self.survivorTest.canGiveItens(inventory_with_more_food))

    def test_canGiveItensMedicationWrong(self):
        inventory_with_more_medication = {'water': 1, 'food': 2, 'medication': 2, 'ammunition': 20}
        self.assertFalse(self.survivorTest.canGiveItens(inventory_with_more_medication))

    def test_canGiveItensAmmunitionWrong(self):
        inventory_with_more_ammunition = {'water': 1, 'food': 2, 'medication': 1, 'ammunition': 21}
        self.assertFalse(self.survivorTest.canGiveItens(inventory_with_more_ammunition))

    def test_canGiveZeroItens(self):
        inventory_with_no_itens = {'water': 0, 'food': 0, 'medication': 0, 'ammunition': 0}
        self.assertTrue(self.survivorTest.canGiveItens(inventory_with_no_itens))



class TestTrade(unittest.TestCase):
    def test_assignContent(self):
        correct_inventory = {'water':0,'food':0,'medication':5,'ammunition':2}
        inventory_missing_water_food = {'medication':5,'ammunition':2}

        self.assertEqual(correct_inventory, assignContent(correct_inventory))

        self.assertEqual(correct_inventory, assignContent(inventory_missing_water_food))


    def test_verifyIntegrity(self):
        trade_json = {'trade':[{'id':0,'itens':{}},{'id':0,'itens':{}}]}
        self.assertTrue(verifyIntegrity(trade_json))

        trade_json_wrong_key = {'trade':[{'id':0,'itens':{}},{'ideas':0,'itens':{}}]}
        self.assertFalse(verifyIntegrity(trade_json_wrong_key))

        trade_json_missing_keys = {'trade':[]}
        self.assertFalse(verifyIntegrity(trade_json_missing_keys))

    def test_trade(self):
        trade_good = {
                'trade':[
                    {
                        'id':12,
                        'itens':
                            {
                                'water':3
                            }
                    },
                    {
                        'id':24,
                        'itens':
                            {
                                'food':2,
                                'medication':2,
                                'ammunition':2
                            }
                    }
                ]
            }
        trade_good_reverse = {
                'trade':[
                    {
                        'id':24,
                        'itens':
                            {
                                'water':3
                            }
                    },
                    {
                        'id':12,
                        'itens':
                            {
                                'food':2,
                                'medication':2,
                                'ammunition':2
                            }
                    }
                ]
            }
        self.assertEqual(200,trade(trade_good))
        self.assertEqual(200,trade(trade_good_reverse))


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
        id = postRequest('survivors', surv)[0]['id']
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
        self.assertEqual(200, response_cod)


def postRequest(route, data):
    response = requests.post(uri + route,data=json.dumps(data),headers={'Content-Type':'application/json'})
    # print response
    # print response.json()
    return response.json(), response.status_code

def putRequest(route, data):
    response = requests.put(uri + route,data=json.dumps(data),headers={'Content-Type':'application/json'})
    return response.json(), response.status_code

if __name__ == '__main__':
    db = SurvivorDb('survivors')
    unittest.main()
