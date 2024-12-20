from flask import request, jsonify, json, Blueprint #,render_template, request
from app import mysql
import json
from datetime import datetime
import app
# If you need socketio stuff maybe uncomment the below line.
# from flask_socketio import SocketIO, join_room, leave_room, send, emit

# Feel free to add more imports


PatientDashboardData = Blueprint('PatientDashboardData', __name__)

@PatientDashboardData.route("/getCurrentTherapist", methods=['POST'])
def getCurrentTherapistFunc():
    try:
        patientID = request.json.get('patientID')
        cursor = mysql.connection.cursor()
        cursor.execute('''
                SELECT mainTherapistID FROM patients WHERE patientID = %s
                ''', (patientID, ))
        therapistID = cursor.fetchone()[0]
        if therapistID:
            cursor.execute('''
                SELECT users.userID, users.userName, users.profileImg, therapists.therapistID
                FROM therapists
                INNER JOIN users ON therapists.userID = users.userID
                WHERE therapists.therapistID = %s            
            ''', (therapistID, ))
            data = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            results = [dict(zip(columns, row)) for row in data]

            response = jsonify(results)
            response.status_code = 200
            response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response
        else:
            response = jsonify({"message":"no main therapist found"})
            response.status_code = 404
            response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response

    except Exception as err:
        return {"error":  f"{err}"}

@PatientDashboardData.route("/getJournals", methods=['POST'])
def getJournalsFunc():
    """
    Fetch Patient Dashboard Data
    ---
    tags:
      - Patient Dashboard
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              patientId:
                type: integer
                example: 1
    responses:
      200:
        description: Patient dashboard data fetched successfully
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
      500:
        description: Internal server error
    """
    try:
        totalResults = []
        patientID = request.json.get('patientID')
        cursor = mysql.connection.cursor()
        cursor.execute('''
                SELECT journalID, journalEntry, timeDone FROM journals WHERE patientID = %s
                ''', (patientID, ))
        data = cursor.fetchall()
        if data:
            columns = [column[0] for column in cursor.description]
            results = [dict(zip(columns, row)) for row in data]
            response = jsonify(results)
            response.status_code = 200
            response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response
        else:
            response = jsonify({"message":"no journals found"})
            response.status_code = 404
            response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response

    except Exception as err:
        return {"error":  f"{err}"}
    
@PatientDashboardData.route("/getFeedback", methods=['POST'])
def getFeedbackFunc():
    try:
        patientID = request.json.get('patientID')
        cursor = mysql.connection.cursor()
        cursor.execute('''
                SELECT feedbackID, feedbackDate, feedback, users.userName FROM feedback
                INNER JOIN therapists ON feedback.therapistID = therapists.therapistID
                INNER JOIN users ON therapists.userID = users.userID
                WHERE patientID = %s
                ''', (patientID, ))
        feedback_data = cursor.fetchall()
        if feedback_data:
            feedback_columns = [column[0] for column in cursor.description]
            feedback_results = [dict(zip(feedback_columns, row)) for row in feedback_data]
            response = jsonify(feedback_results)
            response.status_code = 200
            response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response
        else:
            response = jsonify({"message":"no feedback found"})
            response.status_code = 404
            response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response

    except Exception as err:
        return {"error":  f"{err}"}
    
@PatientDashboardData.route("/getDailySurveys", methods=['POST'])
def getDailySurveysFunc():
    try:
        patientID = request.json.get('patientID')
        cursor = mysql.connection.cursor()

        #   Create a daily survey if one doesn't exist
        cursor.execute('''
            SELECT dateCreated FROM dailySurveys
            ORDER BY dateCreated DESC
            LIMIT 1
        ''')
        data = cursor.fetchone()
        if data:
            latestDailySurvey = data[0].date()
            if datetime.today().date() != latestDailySurvey:
                cursor.execute('''
                    INSERT INTO dailySurveys (dateCreated) VALUES (NOW())
                ''')
                mysql.connection.commit()
        else:
            cursor.execute('''
                    INSERT INTO dailySurveys (dateCreated) VALUES (NOW())
            ''')
            mysql.connection.commit()

        #   Extract incomplete + complete daily surveys        
        cursor.execute('''
                SELECT
                    ds.dailySurveyID,
                    ds.dateCreated,
                    cds.completionID,
                    IFNULL(cds.weight, NULL) AS weight,
                    IFNULL(cds.height, NULL) AS height,
                    IFNULL(cds.calories, NULL) AS calories,
                    IFNULL(cds.water, NULL) AS water,
                    IFNULL(cds.exercise, NULL) AS exercise,
                    IFNULL(cds.sleep, NULL) AS sleep,
                    IFNULL(cds.energy, NULL) AS energy,
                    IFNULL(cds.stress, NULL) AS stress
                FROM dailySurveys ds
                LEFT JOIN completedDailySurveys cds
                    ON ds.dailySurveyID = cds.dailySurveyID AND cds.patientID = %s
                WHERE (DATE(ds.dateCreated) = CURDATE())
                    OR (cds.dailySurveyID IS NOT NULL)
                ''', (patientID, ))
        daily_survey_data = cursor.fetchall()
        if daily_survey_data:
            daily_survey_columns = [column[0] for column in cursor.description]
            daily_survey_results = [dict(zip(daily_survey_columns, row)) for row in daily_survey_data]
            response = jsonify(daily_survey_results)
            response.status_code = 200
            response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response
        else:
            response = jsonify({"message":"no daily surveys found"})
            response.status_code = 404
            response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response

    except Exception as err:
        return {"error":  f"{err}"}
    
@PatientDashboardData.route("/getIncompleteTherapistSurveys", methods=['POST'])
def getIncompleteTherapistSurveysFunc():
    try:
        patientID = request.json.get('patientID')
        cursor = mysql.connection.cursor()
        cursor.execute('''
                SELECT users.userName, JSON_EXTRACT(surveys.content, '$.survey') AS survey, surveys.dateCreated, surveys.surveyID FROM surveys
                INNER JOIN patients ON surveys.patientID = patients.patientID
                INNER JOIN therapists ON surveys.therapistID = therapists.therapistID
                INNER JOIN users ON therapists.userID = users.userID
                WHERE patients.patientID = %s AND surveys.therapistID = patients.mainTherapistID;
            ''', (patientID, ))
        incomp_surveys_data = cursor.fetchall()
        if (incomp_surveys_data):
            incomp_surveys_columns = [column[0] for column in cursor.description]
            incomp_surveys_results = [dict(zip(incomp_surveys_columns, row)) for row in incomp_surveys_data]
            response = jsonify(incomp_surveys_results)
            response.status_code = 200
            response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response
        else:
            response = jsonify({"message":"no incomplete therapist surveys found"})
            response.status_code = 404
            response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response
    except Exception as err:
        return {"error":  f"{err}"}
    
@PatientDashboardData.route("/getCompleteTherapistSurveys", methods=['POST'])
def getCompleteTherapistSurveysFunc():
    try:
        patientID = request.json.get('patientID')
        cursor = mysql.connection.cursor()
        cursor.execute('''
                    SELECT users.userName, JSON_EXTRACT(completedSurveys.questions, '$.survey') AS questions,
                    JSON_EXTRACT(completedSurveys.answers, '$.answers') AS answers, completedSurveys.dateDone , completedSurveys.completionID,
                    completedSurveys.dateDone
                    FROM completedSurveys
                    INNER JOIN patients ON completedSurveys.patientID = patients.patientID
                    INNER JOIN therapists ON completedSurveys.therapistID = therapists.therapistID
                    INNER JOIN users ON therapists.userID = users.userID
                    WHERE completedSurveys.patientID = %s;
                    ''', (patientID, ))
        comp_surveys_data = cursor.fetchall()
        if comp_surveys_data:
            comp_surveys_columns = [column[0] for column in cursor.description]
            comp_surveys_results = [dict(zip(comp_surveys_columns, row)) for row in comp_surveys_data]
            response = jsonify(comp_surveys_results)
            response.status_code = 200
            response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response
        else:
            response = jsonify({"message":"no complete therapist surveys found"})
            response.status_code = 404
            response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response
    except Exception as err:
        return {"error":  f"{err}"}

@PatientDashboardData.route("/getInvoices", methods=['POST'])
def getInvoicesFunc():
    try:
        patientID = request.json.get('patientID')
        cursor = mysql.connection.cursor()
        cursor.execute('''
                SELECT users.userName, invoices.invoiceID, invoices.amountDue, invoices.dateCreated FROM invoices
                INNER JOIN therapists ON invoices.therapistID = therapists.therapistID
                INNER JOIN users ON therapists.userID = users.userID
                WHERE invoices.patientID = %s;
                ''', (patientID, ))
        invoices_data = cursor.fetchall()
        if invoices_data:
            invoices_columns = [column[0] for column in cursor.description]
            invoices_results = [dict(zip(invoices_columns, row)) for row in invoices_data]
            response = jsonify(invoices_results)
            response.status_code = 200
            response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response
        else:
            response = jsonify({"message":"no complete therapist surveys found"})
            response.status_code = 404
            response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response
    except Exception as err:
        return {"error":  f"{err}"}
    
@PatientDashboardData.route("/saveJournal", methods=['POST'])
def save():
    """
    Save Journal Entry
    ---
    tags:
      - Patient Dashboard
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              patientId:
                type: integer
                example: 1
              journalId:
                type: integer
                example: 101
              journalEntry:
                type: string
                example: "This is a journal entry."
    responses:
      200:
        description: Journal entry saved successfully
      500:
        description: Internal server error
    """
    try:
        journalEntry = request.json.get('journalEntry')
        patientId = request.json.get('patientId')
        journalId = request.json.get('journalId') if request.json.get('journalId') else "null"
        # print("Journal ID: " + journalId + "\n")
        cursor = mysql.connection.cursor()
        if journalId == "null":
            currentDate = datetime.now()
            # print(currentDate)
            cursor.execute('''
                    INSERT INTO journals (patientID, journalEntry, timeDone)
                    VALUES (%s, %s, %s)
                    ''', (patientId, journalEntry, currentDate))
        else:
            cursor.execute('''
                    UPDATE journals
                    SET journalEntry = %s
                    WHERE patientID = %s AND journalID = %s
                    ''', (journalEntry, patientId, journalId))
        mysql.connection.commit()
        cursor.close()
        response = jsonify({"message" : "Journal saved successfully"})
        response.status_code = 200
        response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    except Exception as err:
        return {"error":  f"{err}"}
    
@PatientDashboardData.route("/sendFeedback", methods=['POST'])
def sendFeedbackFunc():
    """
    Send Feedback to a Therapist
    ---
    tags:
      - Patient Dashboard
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              patientId:
                type: integer
                example: 1
              feedback:
                type: string
                example: "Great session with the therapist."
    responses:
      200:
        description: Feedback sent successfully
      500:
        description: Internal server error
    """
    try:
        # print("GOT HERE")
        therapistID = request.json.get('therapistID')
        patientID = request.json.get('patientID')
        feedback = request.json.get('feedback')

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT userID FROM patients WHERE patientID = %s", (patientID, ))
        realUserID = cursor.fetchone()[0]

        cursor.execute("INSERT INTO feedback (therapistID, patientID, feedbackDate, feedback) VALUES (%s, %s, NOW(), %s)", (therapistID, patientID, feedback))
        mysql.connection.commit()

        # Emit the event to the connected socket clients
        if str(realUserID) in app.sockets:
            app.socketio.emit('new-feedback', {
                'feedback': feedback
            }, room=app.sockets[str(realUserID)])

        response = jsonify({"message": "Success"})
        response.status_code = 200
        response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    
#   Send the newly completed therapist survey to patient & therapist (therapist is WIP)
@PatientDashboardData.route("/completeTherapistSurvey", methods=['POST'])
def sendTherapistSurveyFunc():
    """
    Complete Therapist Survey
    ---
    tags:
      - Patient Dashboard
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              userID:
                type: integer
                example: 1
              patientID:
                type: integer
                example: 2
              surveyID:
                type: integer
                example: 101
              questions:
                type: array
                items:
                  type: string
                example: ["How was your day?", "How do you feel?"]
              answers:
                type: array
                items:
                  type: string
                example: ["Good", "Happy"]
    responses:
      200:
        description: Survey submitted successfully
      404:
        description: Therapist not found
      500:
        description: Internal server error
    """
    try:
        userID = request.json.get('userID')
        patientID = request.json.get('patientID')
        surveyID = request.json.get('surveyID')

        questions = request.json.get('questions')
        surveyQuestions = json.dumps({"survey": questions}, ensure_ascii=False)
        answers = request.json.get('answers')
        surveyAnswers = json.dumps({"answers" : answers})
        currentDate = datetime.now()

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT therapistID FROM surveys WHERE surveyID = %s', (surveyID, ))
        therapistID = cursor.fetchone()
        
        if therapistID is None:
            # print("TherapistID not found for surveyID:", surveyID)
            response = jsonify({"error": "Therapist not found for this survey."})
            response.status_code = 404
            response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response
        
        therapistID = therapistID[0]

        cursor.execute('''
            INSERT INTO completedSurveys (patientID, therapistID, questions, answers, dateDone)
            VALUES (%s, %s, %s, %s, %s)
        ''', (patientID, therapistID, surveyQuestions, surveyAnswers, currentDate))
        mysql.connection.commit()

        # Log success after inserting
        # print("Survey inserted successfully.")
        
        cursor.execute('''
                DELETE FROM surveys WHERE surveyID = %s    
                ''', (surveyID, ))
        mysql.connection.commit()

        cursor.close()
        if str(userID) in app.sockets:
            app.socketio.emit('submit-therapist-survey', room=app.sockets[str(userID)])
        # Return a success response
        response = jsonify({"message": "Success"})
        response.status_code = 200
        response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    
@PatientDashboardData.route("/completeDailySurvey", methods=['POST'])
def sendDailySurveyFunc():
    """
    Complete Daily Survey
    ---
    tags:
      - Patient Dashboard
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              patientId:
                type: integer
                example: 1
              dailySurveyID:
                type: integer
                example: 102
              weight:
                type: number
                example: 70.5
              height:
                type: number
                example: 175
              calories:
                type: integer
                example: 1500
              water:
                type: integer
                example: 8
              exercise:
                type: integer
                example: 60
              sleep:
                type: number
                example: 7.5
              energy:
                type: integer
                example: 8
              stress:
                type: integer
                example: 2
    responses:
      200:
        description: Daily survey completed successfully
      500:
        description: Internal server error
    """
    try:
        data = request.get_json()
        
        fakeUserID = data.get('patientID')
        realUserID = data.get('userID')
        dailySurveyID = data.get('dailySurveyID')
        weight = data.get('weight')
        height = data.get('height')
        calories = data.get('calories')
        water = data.get('water')
        exercise = data.get('exercise')
        sleep = data.get('sleep')
        energy = data.get('energy')
        stress = data.get('stress')

        cursor = mysql.connection.cursor()
        cursor.execute('''
                INSERT INTO completedDailySurveys (dailySurveyID, patientID, weight, height, calories, water, exercise, sleep, energy, stress)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ''', (dailySurveyID, fakeUserID, weight, height, calories, water, exercise, sleep, energy, stress))
        mysql.connection.commit()
        cursor.close()

        # Emit the event to the connected socket clients
        if str(realUserID) in app.sockets:
            app.socketio.emit('submit-daily-survey', {
                'patientID': fakeUserID,
                'dailySurveyID': dailySurveyID,
                'weight': weight,
                'height': height,
                'calories': calories,
                'water': water,
                'exercise': exercise,
                'sleep': sleep,
                'energy': energy,
                'stress': stress
            }, room=app.sockets[realUserID])

        response = jsonify({"message": "Survey data submitted successfully!"})
        response.status_code = 200
        response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    except Exception as err:
        return jsonify({"error": str(err)}), 500

@PatientDashboardData.route('/checkInsurance', methods=['POST'])
def checkInsFunc():
    try:
        patientID = request.json.get('patientID')
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT insuranceCompany, insuranceID, insuranceTier FROM patients WHERE patientID = %s", (patientID, ))
        data = cursor.fetchone()
        if data[0] is None or data[1] is None or data[2] is None:
           return jsonify({'message' : 'success'}), 404
        else:
            return jsonify({'message' : 'success'}), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    
@PatientDashboardData.route('/payInvoiceInsurance', methods=['POST'])
def payInvoiceInsFunc():
    try:
        invoiceID = request.json.get('invoiceID')
        cursor = mysql.connection.cursor()
        cursor.execute('''DELETE FROM invoices WHERE invoiceID = %s;''', (invoiceID,))
        mysql.connection.commit()
        return jsonify({'message' : 'success'}), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    
