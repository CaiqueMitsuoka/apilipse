# -*- coding: <UTF-8> -*-
from flask import Flask,jsonify,abort,make_response,request

import json
from app.trade import trade
from .reports import get_reports
from .survivor import Survivor
from .survivor import SurvivorDb
# instanciate flask and connect database
app = Flask(__name__)

@app.route('/', methods=['GET'])
def version():
    return jsonify({'Apilipse':'Api for the best zombie social network, always with you <3','version':'1.0'})

# get all the survivors
@app.route('/api/v1/survivors', methods=['GET'])
def get_all_survivors():
    listSurv = db.getAllSurvivors()
    if len(listSurv) == 0:
        abort(404)
    survivorList = []
    for people in listSurv:
        survivorList.append(people.survivorToDic())
    return jsonify({'Suvivors':survivorList}), 200

# get survivor by id
@app.route('/api/v1/survivors/<int:survivor_id>', methods=['GET'])
def getSurvivorById(survivor_id):
    survivor = db.searchById(survivor_id)
    if survivor == None:
        abort(404)
    return make_response(jsonify(survivor.survivorToDic()),200)

# get reports
@app.route('/api/v1/reports', methods=['GET'])
def getReports():
    return jsonify(get_reports()), 200

# post update location
@app.route('/api/v1/update/location', methods=['PUT'])
def updateLocation():
    # try:
    result = db.updateLocation(request.json['id'], request.json['lastLocation']['x'], request.json['lastLocation']['y'])
    print result
    # except KeyError:
    #     # key missing
    #     print 'aqui mesmo'
    #     abort(422)
    # except:
    #     # parse error
    #     abort(400)
    if result < 1:
        # survivor not found
        abort(404)
    return jsonify({'updatedId':request.json['id']}), 200

# post new survivor
@app.route('/api/v1/survivors', methods=['POST'])
def postNewSurvivor():
    new_survivor = db.insertSurvivor(request.json)
    if new_survivor == None:
        abort(422)
    return jsonify(new_survivor.survivorToDic()), 201

@app.route('/api/v1/update/infected', methods=['PUT'])
def reportInfected():
    try:
        _id = request.json['id']
    except:
        # parse error
        abort(400)
    result = db.reportInfection(_id)
    if result > 0:
        return jsonify({'reported':result})
    # database error
    abort(500)

# post a trade
@app.route('/api/v1/update/trade', methods=['PUT'])
def postTrade():
    return trade(request.json)

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

def jsonToSuvivor(s):
    survivorDic = json.loads(s)
    return Survivor(
        survivorDic['id'],
        survivorDic,
        survivorDic['infectionReports']
    )

db = SurvivorDb('survivors')
