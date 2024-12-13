from flask import request, jsonify, json, Blueprint #,render_template, request
from app import mysql

TherapistDashboardData = Blueprint('TherapistDashboardData', __name__)
    
@TherapistDashboardData.route("/therapistDashboardData", methods=['POST'])
def theraDashFunc():
    try:
        userId = request.json.get('userId')
        cursor = mysql.connection.cursor()
        cursor.execute(f'SELECT acceptingPatients FROM therapists WHERE therapistID = {userId}')
        data = cursor.fetchall()
        accepting = data[0][0]
        cursor.execute(f'SELECT content -> "$.survey" AS surveyData FROM therapists WHERE therapistID = {userId}')
        data = cursor.fetchall()
        cursor.close()
        return jsonify({"accepting": int(accepting), "survey" : data[0]}), 200
    except Exception as err:
        return {"error":  f"{err}"}
    
@TherapistDashboardData.route("/therapistsPatientsList", methods=['POST'])
def theraPatListFunc():
    try:
        userId = request.json.get('userId')
        cursor = mysql.connection.cursor()
        cursor.execute(f'''
                SELECT users.userName, users.userID
                FROM patients, users
                WHERE users.userID = patients.userID AND patients.mainTherapistID = {userId}
                ''')
        patientsInfo = cursor.fetchall()
        cursor.execute(f'''
                SELECT feedback.feedback, users.userID
                FROM feedback, patients, users
                WHERE users.userID = patients.userID AND patients.patientID = feedback.patientID
                AND patients.mainTherapistID = {userId}
                ORDER BY feedbackDate DESC
                ''')
        feedbackInfo = cursor.fetchall()
        cursor.close()

        feedbackDict = {}
        for thing in feedbackInfo:
            feedbackDict[thing[1]] = thing[0]

        returnArray = []
        for thing in patientsInfo:
            print(returnArray)
            if(thing[1] in feedbackDict):
                returnArray.append((thing[0], feedbackDict[thing[1]], thing[1]))
            else:
                returnArray.append((thing[0], "No Feedback Sent", thing[1]))
            print(returnArray)
        
        return jsonify({"patientData" : returnArray}), 200
    except Exception as err:
        return {"error":  f"{err}"}

@TherapistDashboardData.route("/therapistsAcceptingStatus", methods=['POST'])
def theraAcceptFunc():
    try:
        userId = request.json.get('userId')
        accepting = True if request.json.get('acceptingStatus') == 1 else False # "accepting" mirrors the value of "acceptingStatus" from the frontend
        cursor = mysql.connection.cursor()
        cursor.execute(f'''UPDATE therapists
                       SET acceptingPatients = {not accepting}
                       WHERE therapistID = {userId}''') # We flip the value of "accepting" in the MySQL query
        mysql.connection.commit()
        if(cursor.rowcount > 0): # We ensure the table was modified
            cursor.close()
            if(accepting): # If "accepting" was 1, we tell the frontend it is now 0; Vice versa
                return jsonify({"inserted": 1, "accepting" : 0}), 200
            else:
                return jsonify({"inserted": 1, "accepting" : 1}), 200
        else:
            cursor.close()
            return jsonify({"inserted": 0, "accepting" : 0}), 200
    except Exception as err:
        return {"error":  f"{err}"}
    
@TherapistDashboardData.route("/therapistUpdateSurvey", methods=['POST'])
def theraUpdSurveyFunc():
    try:
        surveyData = str(request.json.get('surveyToSubmit'))
        therapistId = request.json.get('therapistId')

        surveyData = '{"survey": ' + surveyData + '}'
        surveyData = surveyData.replace("'", '\"')

        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE therapists SET content = %s WHERE therapistID = %s', (surveyData, therapistId))
        mysql.connection.commit()
        if(cursor.rowcount > 0): # We ensure the table was modified
            cursor.close()
            return jsonify({"inserted": True}), 200
        else:
            cursor.close()
            return jsonify({"inserted": False}), 200
    except Exception as err:
        return jsonify({"error":  f"{err}"})