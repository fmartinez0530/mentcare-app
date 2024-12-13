from flask import request, jsonify, json, Blueprint #,render_template, request
from app import mysql
import json
from datetime import datetime
import app
# If you need socketio stuff maybe uncomment the below line.
# from flask_socketio import SocketIO, join_room, leave_room, send, emit

# Feel free to add more imports


PatientDashboardData = Blueprint('PatientDashboardData', __name__)

@PatientDashboardData.route("/patientDashboardData", methods=['POST'])
def patientDashFunc():
    try:
        totalResults = []
        patientId = request.json.get('patientId')
        cursor = mysql.connection.cursor()
        cursor.execute('''
                SELECT journalID, journalEntry, timeDone FROM journals WHERE patientID = %s
                ''', (patientId, ))
        data = cursor.fetchall()
        if data:
            #print("DATA: ", data)
            columns = [column[0] for column in cursor.description]
            results = [dict(zip(columns, row)) for row in data]
            #print("RESULTS: ", results)
            print("JOURNALS SUCCESSFUL")
            totalResults.append(results)
        else:
            totalResults.append("Nothing")

        cursor.execute('''
                SELECT feedbackID, feedbackDate, feedback, users.userName FROM feedback
                INNER JOIN therapists ON feedback.therapistID = therapists.therapistID
                INNER JOIN users ON therapists.userID = users.userID
                WHERE patientID = %s
                ''', (patientId, ))
        feedback_data = cursor.fetchall()
        if feedback_data:
            feedback_columns = [column[0] for column in cursor.description]
            feedback_results = [dict(zip(feedback_columns, row)) for row in feedback_data]
            #print("Feedback RESULTS: ", feedback_results)
            print("FEEDBACK SUCCESSFUL")
            totalResults.append(feedback_results)
        else:
            totalResults.append("Nothing")

        #   Create new daily survey if one doesn't exist
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
                    ON ds.dailySurveyID = cds.dailySurveyID
                WHERE (DATE(ds.dateCreated) = CURDATE())
                    OR (cds.dailySurveyID IS NOT NULL AND cds.patientID = %s)
                ''', (patientId, ))
        daily_survey_data = cursor.fetchall()
        if daily_survey_data:
            daily_survey_columns = [column[0] for column in cursor.description]
            daily_survey_results = [dict(zip(daily_survey_columns, row)) for row in daily_survey_data]
            # print("Daily Survey RESULTS: ", daily_survey_results)
            print("DAILY SURVEYS SUCCESSFUL")
            totalResults.append(daily_survey_results)
        else:
            print("NO DAILY SURVEYS FOUND")
            totalResults.append("Nothing")
        
        #   Extract incomplete therapist survey (if exists)
        cursor.execute('''
                SELECT therapistID FROM therapistPatientsList WHERE patientID = %s AND status = 'Active';
                ''', (patientId, ))
        therapistId = 0
        if(cursor.rowcount > 0):
            therapistId = cursor.fetchone()[0]
        if (therapistId != 0):
            cursor.execute('''
                    SELECT users.userName, JSON_EXTRACT(surveys.content, '$.survey') AS survey, surveys.dateCreated, surveys.surveyID FROM surveys
                    INNER JOIN therapists ON surveys.therapistID = therapists.therapistID
                    INNER JOIN users ON therapists.userID = users.userID
                    WHERE surveys.therapistID = %s AND surveys.patientID = %s;
                ''', (therapistId, patientId ))
            incomp_surveys_data = cursor.fetchall()
            if (incomp_surveys_data):
                incomp_surveys_columns = [column[0] for column in cursor.description]
                incomp_surveys_results = [dict(zip(incomp_surveys_columns, row)) for row in incomp_surveys_data]
                #print("Incomplete Survey RESULTS: ", incomp_surveys_results)
                print("INCOMPLETE THERAPIST SURVEYS SUCCESSFUL")
                totalResults.append(incomp_surveys_results)
            else:
                totalResults.append("Nothing")
        else:
            totalResults.append("Nothing")

        
        #   Extract complete therapist surveys (if exists)
        if therapistId != 0:
            cursor.execute('''
                    SELECT users.userName, JSON_EXTRACT(completedSurveys.questions, '$.survey') AS questions,
                    JSON_EXTRACT(completedSurveys.answers, '$.answers') AS answers, completedSurveys.dateDone , completedSurveys.completionID,
                    completedSurveys.dateDone
                    FROM completedSurveys
                    INNER JOIN therapists ON completedSurveys.therapistID = therapists.therapistID
                    INNER JOIN users ON therapists.userID = users.userID
                    WHERE completedSurveys.patientID = %s and therapists.therapistID = %s;
                    ''', (patientId, therapistId))
            comp_surveys_data = cursor.fetchall()
            if comp_surveys_data:
                comp_surveys_columns = [column[0] for column in cursor.description]
                comp_surveys_results = [dict(zip(comp_surveys_columns, row)) for row in comp_surveys_data]
                print("COMPLETE THERAPIST SURVEYS SUCCESSFUL")
                totalResults.append(comp_surveys_results)
            else:
                totalResults.append("Nothing")
        else:
            totalResults.append("Nothing")

        #   Extract invoices (if exists):
        cursor.execute('''
                SELECT users.userName, invoices.invoiceID, invoices.amountDue, invoices.dateCreated FROM invoices
                INNER JOIN therapists ON invoices.therapistID = therapists.therapistID
                INNER JOIN users ON therapists.userID = users.userID
                WHERE invoices.patientID = %s;
                ''', (patientId, ))
        invoices_data = cursor.fetchall()
        if invoices_data:
            invoices_columns = [column[0] for column in cursor.description]
            invoices_results = [dict(zip(invoices_columns, row)) for row in invoices_data]
            #print("Invoices RESULTS: ", invoices_results)
            print("INVOICES SUCCESSFUL")
            totalResults.append(invoices_results)
        else:
            totalResults.append("Nothing")

        cursor.close()
        return jsonify(totalResults)
    except Exception as err:
        return {"error":  f"{err}"}
    
@PatientDashboardData.route("/saveJournal", methods=['POST'])
def save():
    try:
        journalEntry = request.json.get('journalEntry')
        patientId = request.json.get('patientId')
        journalId = request.json.get('journalId') if request.json.get('journalId') else "null"
        print("Journal ID: " + journalId + "\n")
        cursor = mysql.connection.cursor()
        if journalId == "null":
            currentDate = datetime.now()
            print(currentDate)
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
        return jsonify({"message" : "Journal saved successfully"}), 200
    except Exception as err:
        return {"error":  f"{err}"}
    
@PatientDashboardData.route("/sendFeedback", methods=['POST'])
def sendFeedbackFunc():
    try:
        print("GOT HERE")
        patientID = request.json.get('patientId')
        feedback = request.json.get('feedback')
        # Emit the event to the connected socket clients
        app.socketio.emit('new-feedback', {
            'feedback': feedback
        }, room=app.sockets[patientID])

        return jsonify({"message": "Success"}), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    
#   Send the newly completed therapist survey to patient & therapist (therapist is WIP)
@PatientDashboardData.route("/completeTherapistSurvey", methods=['POST'])
def sendTherapistSurveyFunc():
    try:
        userID = request.json.get('userID')
        patientID = request.json.get('patientID')
        surveyID = request.json.get('surveyID')

        questions = request.json.get('questions')
        surveyQuestions= json.dumps({"survey": questions})
        answers = request.json.get('answers')
        surveyAnswers = json.dumps({"answers" : answers})
        currentDate = datetime.now()

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT therapistID FROM surveys WHERE surveyID = %s', (surveyID, ))
        therapistID = cursor.fetchone()
        
        if therapistID is None:
            print("TherapistID not found for surveyID:", surveyID)
            return jsonify({"error": "Therapist not found for this survey."}), 404
        
        therapistID = therapistID[0]

        cursor.execute('''
            INSERT INTO completedSurveys (patientID, therapistID, questions, answers, dateDone)
            VALUES (%s, %s, %s, %s, %s)
        ''', (patientID, therapistID, surveyQuestions, surveyAnswers, currentDate))
        mysql.connection.commit()

        # Log success after inserting
        print("Survey inserted successfully.")
        
        cursor.execute('''
                DELETE FROM surveys WHERE surveyID = %s    
                ''', (surveyID, ))
        mysql.connection.commit()

        cursor.close()
        if str(userID) in app.sockets:
            app.socketio.emit('submit-therapist-survey', room=app.sockets[str(userID)])
        # Return a success response
        return jsonify({"message": "Success"}), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    
@PatientDashboardData.route("/completeDailySurvey", methods=['POST'])
def sendDailySurveyFunc():
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

        return jsonify({"message": "Survey data submitted successfully!"}), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500
