from flask import request, jsonify, json, Blueprint #,render_template, request
from app import mysql

TherapistDashboardData = Blueprint('TherapistDashboardData', __name__)
    
@TherapistDashboardData.route("/therapistDashboardData", methods=['POST'])
def theraDashFunc():
    """
    Fetch Therapist Dashboard Data
    ---
    tags:
      - Therapist Dashboard
    parameters:
      - name: userId
        in: body
        type: integer
        required: true
        description: Therapist ID
    responses:
      200:
        description: Returns the therapist's dashboard data
        schema:
          type: object
          properties:
            accepting:
              type: integer
              description: Whether the therapist is accepting new patients
            survey:
              type: object
              description: Survey content
      500:
        description: Internal server error
    """
    try:
        userId = request.json.get('userId')
        cursor = mysql.connection.cursor()
        cursor.execute(f'SELECT acceptingPatients FROM therapists WHERE therapistID = {userId}')
        data = cursor.fetchall()
        accepting = data[0][0]
        cursor.execute(f'SELECT content -> "$.survey" AS surveyData FROM therapists WHERE therapistID = {userId}')
        data = cursor.fetchall()
        cursor.close()
        response = jsonify({"accepting": int(accepting), "survey" : data[0]})
        response.status_code = 200
        response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    except Exception as err:
        return {"error":  f"{err}"}
    
@TherapistDashboardData.route("/therapistsPatientsList", methods=['POST'])
def theraPatListFunc():
    """
    Fetch Therapist's Patients List
    ---
    tags:
      - Therapist Dashboard
    parameters:
      - name: userId
        in: body
        type: integer
        required: true
        description: Therapist ID
    responses:
      200:
        description: Returns the list of patients and their feedback
        schema:
          type: object
          properties:
            patientData:
              type: array
              items:
                type: object
                properties:
                  patientName:
                    type: string
                    description: Name of the patient
                  feedback:
                    type: string
                    description: Feedback provided by the patient
                  patientID:
                    type: integer
                    description: Patient ID
      500:
        description: Internal server error
    """
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
        
        response = jsonify({"patientData" : returnArray})
        response.status_code = 200
        response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    except Exception as err:
        return {"error":  f"{err}"}

@TherapistDashboardData.route("/therapistsAcceptingStatus", methods=['POST'])
def theraAcceptFunc():
    """
    Update Therapist Accepting Status
    ---
    tags:
      - Therapist Dashboard
    parameters:
      - name: userId
        in: body
        type: integer
        required: true
        description: Therapist ID
      - name: acceptingStatus
        in: body
        type: integer
        required: true
        description: New accepting status
    responses:
      200:
        description: Updates the therapist's accepting status
        schema:
          type: object
          properties:
            inserted:
              type: integer
              description: Whether the update was successful (1 for success)
            accepting:
              type: integer
              description: The updated accepting status
      500:
        description: Internal server error
    """
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
                response = jsonify({"inserted": 1, "accepting" : 0})
                response.status_code = 200
                response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
                response.headers['Access-Control-Allow-Credentials'] = 'true'
                response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
                response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
                return response
            else:
                response = jsonify({"inserted": 1, "accepting" : 1})
                response.status_code = 200
                response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
                response.headers['Access-Control-Allow-Credentials'] = 'true'
                response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
                response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
                return response
        else:
            cursor.close()
            response = jsonify({"inserted": 0, "accepting" : 0})
            response.status_code = 200
            response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response
    except Exception as err:
        return {"error":  f"{err}"}
    
@TherapistDashboardData.route("/therapistUpdateSurvey", methods=['POST'])
def theraUpdSurveyFunc():
    """
    Update Therapist Survey Data
    ---
    tags:
      - Therapist Dashboard
    parameters:
      - name: surveyToSubmit
        in: body
        type: string
        required: true
        description: Survey data to be updated
      - name: therapistId
        in: body
        type: integer
        required: true
        description: Therapist ID
    responses:
      200:
        description: Updates the survey data of the therapist
        schema:
          type: object
          properties:
            inserted:
              type: boolean
              description: Whether the update was successful
      500:
        description: Internal server error
    """
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
            response = jsonify({"inserted": True})
            response.status_code = 200
            response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response
        else:
            cursor.close()
            response = jsonify({"inserted": False})
            response.status_code = 200
            response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response
    except Exception as err:
        return jsonify({"error":  f"{err}"})