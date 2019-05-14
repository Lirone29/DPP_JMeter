import pandas as pd
from datetime import datetime
import json
from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for, jsonify, json, abort, Flask
)

app = Flask(__name__)

#url_prefix='/doodle'
#bp = Blueprint('doodle', __name__)

dateVar = [['29.05.2019',"9:00"], ['29.05.2018', "14:00"], ['06.05.2018', "10:00"]]
#columns = ['Date','Time']
dataFrameVar = pd.DataFrame(dateVar, columns=['Date', 'Time'])


class Option(object):
    def __init__(self, column=[], table=[]):
        column.append('Date')
        column.append('Time')
        table.append(column)

app.Date=[
    {
        'id': '1',
        'date': '29.05.2019',
        'time': '9:00'
    },
    {
        'id': '1',
        'date': '05.05.2019',
        'time': '12:00'
    }
]


app.Survey=[
    {
        'id': '1',
        'title': 'Survey Name',
        'name': 'Eliza',
        #'options': Option
    },
    {
        'id': '2',
        'title': 'Survey Name 2',
        'name': 'Fiona',
        #'options': Option
    }
]

name='test1'
@app.route('/')
def index():
    return jsonify({'APP/DOODLE': "DPP-JMETER DOODLE"})

@app.route('/surveys/save', methods=['GET'])
def saveSurvey():
    file = open(name+".txt", "w")
    json.dump(app.Survey, file)
    file.close()
    return jsonify({'Result': "Saved"})

@app.route('/surveys/load', methods=['POST'])
def loadSurvey():
    try:
        file = open(name+".txt", "r")
    except FileNotFoundError:
        return jsonify({'Result': "Error (No file found to load)"})
    app.Survey = json.load(file,cls=JSONObjectEncoder)
    file.close()
    return jsonify({'Result': "Loaded"})

#@app.route('/doodle/survey/addTime', methods=('POST'))
#def addDateSurvey(date, time):
#    df2 = pd.DataFrame([date, time], columns = ['Date','Time'])
#    bp.Survey.dataFrameVar.append(df2)
#    return jsonify({'Result': "Time added"})


@app.route('/surveys', methods=['GET'])
def showSurveys():
    return jsonify({'surveys': app.Survey})


@app.route('/survey/<surveyID>', methods=['GET'])
def getSurvey(surveyID):
    sur = [Survey for Survey in app.Survey if (Survey['id'] == surveyID)]

    d = [Date for Date in app.Date if (Date['id'] == surveyID)]

    return jsonify({'_survey': sur, 'date': d})


@app.route('/survey/date/<surveyID>', methods=['GET'])
def getSurveyDates(surveyID):
    d = [Date for Date in app.Date if (Date['id'] == surveyID)]

    return jsonify({'survey': d})

@app.route('/survey/date', methods=['POST'])
def createDate(surveyID):
    d = [Date for Date in app.Date if (Date['id'] == surveyID)]

    if len(d) != 0:
        return jsonify({'Error': 'User with this id exists'})

    dat = {

        'id': request.json['id'],

        'date': request.json['date'],

        'time': request.json['time'],
    }

    app.Date.append(dat)

    return jsonify(dat)

@app.route('/survey/date/<surveyID>', methods=['POST'])
def addDate(surveyID):
    d = [Date for Date in app.Date if (Date['id'] == surveyID)]

    if len(d) == 0:
        return jsonify({'Error': 'User with this id doesnt exists'})

    dat = {

        'id': surveyID,

        'date': request.json['date'],

        'time': request.json['time'],
    }

    app.Date.append(dat)

    return jsonify(dat)

@app.route('/survey', methods=['POST'])
def createSurvey():
    sur = [Survey for Survey in app.Survey if (Survey['id'] == request.json['id'])]

    if len(sur) != 0:
        return jsonify({'Error': 'Survey with this id exists'})

    dat = {

        'id': request.json['id'],

        'name': request.json['name'],

        'title': request.json['title'],

        'options': request.json['options'],

       # 'dsc': request.json['dsc']
    }

    app.Survey.append(dat)

    return jsonify(dat)

if __name__ == '__main__':
    app.run(host = 'localhost', port = 5000, debug = True)