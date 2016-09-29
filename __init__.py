# -*- coding: <UTF-8> -*-
from flask import Flask,jsonify,abort,make_response,request
from survivor import Survivor
from suvivorDb import SurvivorDb
from trade import trade
from report import reports
import json

# instanciate flask and connect database
app = Flask(__name__)
db = SurvivorDb('survivors')

@app.route('/', methods=['GET'])
def version():
    return jsonify({'Apilipse':'Api for the best zombie social network, always with you <3','version':'1.0'})

# get all the survivors
@app.route('/api/v1/survivors', methods=['GET'])
def getAllSurvivors():
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
    return jsonify(reports()), 200

# post update location
@app.route('/api/v1/update/location', methods=['PUT'])
def updateLocation():
    try:
        result = db.updateLocation(request.json['id'], request.json['lastLocation']['x'], request.json['lastLocation']['y'])
    except KeyError:
        # key missing
        abort(422)
    except:
        # parse error
        abort(400)
    if result < 1:
        # survivor not found
        abort(404)
    return jsonify({'updatedId':request.json['id']}), 200

# post new survivor
@app.route('/api/v1/survivors', methods=['POST'])
def postNewSurvivor():
    try:
        newSurvivor = db.insert(str(request.json['name']),int(request.json['age']),str(request.json['gender']),(float(request.json['lastLocation']['x']),float(request.json['lastLocation']['y'])),dict(request.json['inventory']))
    except:
        # parse error
        abort(422)
    if newSurvivor == None:
        # database error
        abort(500)
    return jsonify({'insertedCount': 1, 'insertedId': newSurvivor._id, 'path':'/survivors/' + str(newSurvivor._id)}), 201

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
    try:
        # try to parse
        reqData = request.json
    except:
        # parse error
        abort(400)
    try:
        # call trade
        if trade(reqData):
            return jsonify({'code':0, 'message':'Sucess!', 'tradeRight':reqData['trade'][0]['id'], 'tradeLeft':reqData['trade'][1]['id']}), 200
        else:
            return jsonify({'code':1,'message':'Survivor can\'t trade', 'tradeRight':reqData['trade'][0]['id'], 'tradeLeft':reqData['trade'][1]['id']}), 400
    except (KeyError, ValueError):
        abort(422)
    except:
        abort(404)

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
        survivorDic['name'],
        survivorDic['age'],
        survivorDic['gender'],
        survivorDic['lastLocation']['x'],
        survivorDic['lastLocation']['y'],
        survivorDic['inventory'],
        survivorDic['infectionReports']
    )



if __name__ == '__main__':
    app.run(host='0.0.0.0')
