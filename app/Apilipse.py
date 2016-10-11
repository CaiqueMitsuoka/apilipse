# -*- coding: <UTF-8> -*-
from flask import Flask,jsonify,abort,make_response,request

import json

from app.trade import TradeManager
from app.trade import verifyTradeIntegrity
from config import VERSION_STRING, VERSION
from .reports import get_reports
from .survivor import SurvivorDb


# instanciate flask and connect database
app = Flask(__name__)

@app.route('/', methods=['GET'])
def version():
    return jsonify({'Apilipse':'Api for the best zombie social network, always with you <3','version': VERSION})



@app.route('/api/%s/survivors' %(VERSION_STRING), methods=['GET'])
def get_all_survivors():
    db = SurvivorDb('survivors')

    listSurv = db.getAllSurvivors()

    db.close()

    if len(listSurv) == 0:
        abort(404)

    survivorList = []
    for people in listSurv:
        survivorList.append(people.survivorToDic())

    return jsonify({'Suvivors':survivorList}), 200



@app.route('/api/%s/survivors/<int:survivor_id>' %(VERSION_STRING), methods=['GET'])
def getSurvivorById(survivor_id):
    db = SurvivorDb('survivors')

    survivor = db.searchById(survivor_id)
    db.close()

    if survivor == None:
        abort(404)

    return make_response(jsonify(survivor.survivorToDic()),200)



@app.route('/api/%s/reports' %(VERSION_STRING), methods=['GET'])
def getReports():
    return jsonify(get_reports()), 200



@app.route('/api/%s/update/location' %(VERSION_STRING), methods=['PUT'])
def updateLocation():

    db = SurvivorDb('survivors')
    result = db.updateLocation(request.json['id'], request.json['lastLocation']['x'], request.json['lastLocation']['y'])
    db.close()

    if result == None:
        # survivor not found
        abort(404)

    return jsonify(db.searchById(request.json['id']).survivorToDic()), 200



@app.route('/api/%s/survivors' %(VERSION_STRING), methods=['POST'])
def postNewSurvivor():

    db = SurvivorDb('survivors')
    new_survivor = db.insertSurvivor(request.json)
    db.close()

    if new_survivor == None:
        abort(422)

    return jsonify(new_survivor.survivorToDic()), 201

@app.route('/api/%s/update/infected' %(VERSION_STRING), methods=['PUT'])
def reportInfected():
    try:
        _id = request.json['id']

    except:
        # parse error
        abort(400)

    db = SurvivorDb('survivors')
    result = db.reportInfection(_id)
    db.close()

    if result > 0:
        return jsonify({'reported':result})

    # database error
    abort(500)



@app.route('/api/%s/update/trade' %(VERSION_STRING), methods=['PUT'])
def postTrade():

    if verifyTradeIntegrity(request.json):
        tradeManaged = TradeManager(request.json)
        return tradeManaged.trade()

    abort(422)




@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def coulnt_parse(error):
    return make_response(jsonify({'error': 'Couldn\'t parse JSON'}), 400)

@app.errorhandler(422)
def coulnt_parse(error):
    return make_response(jsonify({'error': 'Missing key or in correct value'}), 422)

@app.errorhandler(500)
def coulnt_parse(error):
    return make_response(jsonify({'error': 'Internal error'}), 500)

