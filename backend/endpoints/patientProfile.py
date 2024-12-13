from flask import request, jsonify, Blueprint
from app import mysql


PatientProfileData = Blueprint('PatientProfileData', __name__)

# Fetch patient overview details
@PatientProfileData.route('/patient-overview/<int:userID>', methods=['GET'])
def get_patient_overview(userID):
    try:
        cursor = mysql.connection.cursor()

        # Fetch patient basic details
        cursor.execute('''
            SELECT u.userName, u.profileImg, p.allRecordsViewable, p.mainTherapistID
            FROM users u
            INNER JOIN patients p ON u.userID = p.userID
            WHERE u.userID = %s
        ''', (userID,))
        patient_data = cursor.fetchone()

        if not patient_data:
            return jsonify({"error": "Patient not found"}), 404

        # Extract basic patient info
        userName, profileImg, allRecordsViewable, mainTherapistID = patient_data

        # Fetch completed daily surveys
        cursor.execute('''
            SELECT cds.completionID, ds.dateCreated, cds.weight, cds.height, 
                   cds.calories, cds.water, cds.exercise, cds.sleep, cds.energy, cds.stress
            FROM dailySurveys ds
            LEFT JOIN completedDailySurveys cds ON ds.dailySurveyID = cds.dailySurveyID
            WHERE cds.patientID = (
                SELECT patientID FROM patients WHERE userID = %s
            )
            ORDER BY cds.completionID DESC
        ''', (userID,))
        daily_surveys = cursor.fetchall()

        daily_surveys_data = [
            {
                "completionID": survey[0],
                "surveyDate": survey[1].strftime("%Y-%m-%d") if survey[1] else None,
                "weight": survey[2],
                "height": survey[3],
                "calories": survey[4],
                "water": survey[5],
                "exercise": survey[6],
                "sleep": survey[7],
                "energy": survey[8],
                "stress": survey[9],
            }
            for survey in daily_surveys
        ]

        # Fetch feedback
        cursor.execute('''
            SELECT feedbackID, feedbackDate, feedback
            FROM feedback
            WHERE patientID = (
                SELECT patientID FROM patients WHERE userID = %s
            )
            ORDER BY feedbackDate DESC
        ''', (userID,))
        feedback = cursor.fetchall()

        feedback_data = [
            {
                "feedbackID": fb[0],
                "feedbackDate": fb[1].strftime("%Y-%m-%d") if fb[1] else None,
                "feedback": fb[2],
            }
            for fb in feedback
        ]

        # Fetch journal entries
        cursor.execute('''
            SELECT journalID, journalEntry, timeDone
            FROM journals
            WHERE patientID = (
                SELECT patientID FROM patients WHERE userID = %s
            )
            ORDER BY timeDone DESC
        ''', (userID,))
        journals = cursor.fetchall()

        journals_data = [
            {
                "journalID": journal[0],
                "journalEntry": journal[1],
                "timeDone": journal[2].strftime("%Y-%m-%d %H:%M:%S") if journal[2] else None,
            }
            for journal in journals
        ]

        cursor.close()

        response = {
            "userName": userName,
            "profileImg": profileImg,
            "allRecordsViewable": bool(allRecordsViewable),
            "mainTherapistID": mainTherapistID,
            "dailySurveys": daily_surveys_data,
            "feedback": feedback_data,
            "journals": journals_data,
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Fetch detailed daily survey responses
@PatientProfileData.route('/daily-survey-details/<int:completionID>', methods=['GET'])
def get_daily_survey_details(completionID):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''
            SELECT cds.completionID, cds.weight, cds.height, cds.calories, cds.water, 
                   cds.exercise, cds.sleep, cds.energy, cds.stress, ds.dateCreated
            FROM completedDailySurveys cds
            INNER JOIN dailySurveys ds ON cds.dailySurveyID = ds.dailySurveyID
            WHERE cds.completionID = %s
        ''', (completionID,))
        survey = cursor.fetchone()

        if not survey:
            return jsonify({"error": "Survey not found"}), 404

        survey_data = {
            "completionID": survey[0],
            "weight": survey[1],
            "height": survey[2],
            "calories": survey[3],
            "water": survey[4],
            "exercise": survey[5],
            "sleep": survey[6],
            "energy": survey[7],
            "stress": survey[8],
            "surveyDate": survey[9].strftime("%Y-%m-%d") if survey[9] else None,
        }

        cursor.close()
        return jsonify(survey_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Add new feedback
@PatientProfileData.route('/add-feedback', methods=['POST'])
def add_feedback():
    try:
        data = request.json
        userID = data.get('userID')
        feedback = data.get('feedback')

        cursor = mysql.connection.cursor()
        cursor.execute('''
            INSERT INTO feedback (therapistID, patientID, feedbackDate, feedback)
            VALUES (%s, (SELECT patientID FROM patients WHERE userID = %s), CURDATE(), %s)
        ''', (userID, userID, feedback))
        mysql.connection.commit()
        cursor.close()

        return jsonify({"message": "Feedback added successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Add a new journal entry
@PatientProfileData.route('/add-journal', methods=['POST'])
def add_journal():
    try:
        data = request.json
        userID = data.get('userID')
        journalEntry = data.get('journalEntry')

        cursor = mysql.connection.cursor()
        cursor.execute('''
            INSERT INTO journals (patientID, journalEntry, timeDone)
            VALUES ((SELECT patientID FROM patients WHERE userID = %s), %s, NOW())
        ''', (userID, journalEntry))
        mysql.connection.commit()
        cursor.close()

        return jsonify({"message": "Journal added successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



