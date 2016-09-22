# -*- coding: <UTF-8> -*-
from flask import Flask,jsonify,abort,make_response,request
from survivor import Survivor
from suvivorDb import SurvivorDb
import json

app = Flask(__name__)
db = SurvivorDb('survivors')

@app.route('/api/v1/survivors', methods=['GET'])
def getAllSurvivors():
    listSurv = db.getAllSurvivors()
    survivorList = []
    if len(listSurv) == 0:
        abort(404)
    for people in listSurv:
        survivorList.append(people.survivorToDic())
    return jsonify({'Suvivors':survivorList}), 201

@app.route('/api/v1/survivors/<int:survivor_id>')
def getSurvivorById(survivor_id):
    survivor = db.searchById(survivor_id)
    if survivor == None:
        abort(404)
    return jsonify(survivor.survivorToDic())

@app.route('/api/v1/update/location', methods=['POST'])
def updateLocation():
    try:
        result = db.updateLocation(request.json['id'], request.json['lastLocation']['x'], request.json['lastLocation']['y'])
    except:
        abort(422)
    if result > 0:
        return jsonify({'updatedId':request.json['id']})
    abort(404)


@app.route('/api/v1/survivors', methods=['POST'])
def postNewSurvivor():
    try:
        newSurvivor = db.insert(str(request.json['name']),int(request.json['age']),str(request.json['gender']),(float(request.json['lastLocation']['x']),float(request.json['lastLocation']['y'])),dict(request.json['inventory']))
    except:
        abort(422)
    if newSurvivor == None:
        # database error
        abort(422)
    return jsonify({'insertedCount': 1, 'insertedId': newSurvivor._id})

@app.route('/api/v1/update/infected', methods=['POST'])
def reportInfected():
    try:
        _id = request.json['id']
    except:
        # vamo ve
        abort(422)
    try:
        result = db.reportInfection(_id)
    except:
        abort(404)

    if result > 0:
        return jsonify({'reported':result})
    # database error
    abort(404)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(422)
def coulnt_parse(error):
    return make_response(jsonify({'error': 'Could\'t parse JSON'}), 422)

if __name__ == '__main__':
    app.run(debug=True)

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
