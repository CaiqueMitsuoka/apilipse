# -*- coding: <UTF-8> -*-
from flask import Flask,jsonify
from survivor import Survivor
from suvivorDb import SurvivorDb
import json

app = Flask(__name__)
db = SurvivorDb('survivors')

@app.route('/api/v1/survivors', methods=['GET'])
def getAllSurvivors():
    listSurv = db.getAllSurvivors()
    survivorList = []
    for people in listSurv:
        survivorList.append(people.survivorToDic())
    return jsonify({'Suvivors':survivorList})



if __name__ == '__main__':
    app.run(debug=True)
