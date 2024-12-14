from flask import request, jsonify, json, Blueprint, send_file #,render_template, request
from app import mysql
import app
from io import BytesIO
import os
from werkzeug.utils import secure_filename

settingsPageData = Blueprint('settingsPageData', __name__)

@settingsPageData.route('/settingsAccountData', methods=['POST'])
def settingsPageDataFunc():
    """
    Fetch User Account Data
    ---
    tags:
      - Settings
    parameters:
      - name: realUserID
        in: body
        type: integer
        required: true
        description: Real User ID
      - name: userID
        in: body
        type: integer
        required: true
        description: User ID
      - name: userType
        in: body
        type: string
        required: true
        description: User Type (Patient or Therapist)
    responses:
      200:
        description: Returns user account details
        schema:
          type: object
          properties:
            userName:
              type: string
            email:
              type: string
            patientPrivacy:
              type: boolean
            insComp:
              type: string
            insID:
              type: string
            insTier:
              type: string
            isActive:
              type: boolean
      500:
        description: Internal server error
    """
    try:
        realUserId = int(request.json.get('realUserID'))
        userId = request.json.get('userID')
        userType = request.json.get('userType')

        cursor = mysql.connection.cursor()

        cursor.execute(f'''
            SELECT userName, email
            FROM users
            WHERE users.userID = {realUserId}
            ''')
        data1 = cursor.fetchall()

        data2 = [[[],[],[],[]]]
        isActive = 0  # <-------- Using this for Deactivation/Activation of Therapist Account
        if(userType == "Patient"):
            cursor.execute(f'''
                SELECT allRecordsViewable, insuranceCompany, insuranceID, insuranceTier
                FROM patients
                WHERE patients.patientID = {userId};
                ''')
            data2 = cursor.fetchall()
        elif userType == "Therapist":
            cursor.execute(f'''
                SELECT isActive FROM therapists WHERE therapistID = {userId};''')
            data3 = cursor.fetchall()
            isActive = int(data3[0][0])
        cursor.close()
        print({"userName" : data1[0][0], "email" : data1[0][1], "patientPrivacy" : data2[0][0], "insuranceCompany" : data2[0][1], "insuranceID" : data2[0][2], "insuranceTier" : data2[0][3], "isActive" : isActive })
        
        response = jsonify({"userName" : data1[0][0], "email" : data1[0][1], "patientPrivacy" : data2[0][0], "insComp" : data2[0][1], "insID" : data2[0][2], "insTier" : data2[0][3], "isActive" : isActive })
        response.status_code = 200
        response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    
    except Exception as err:
        return {"error":  f"{err}"}

@settingsPageData.route('/settingsUpdAccDetails', methods=['POST'])
def settingsUpdAccDetailsFunc():
    """
    Update Account Details
    ---
    tags:
      - Settings
    parameters:
      - name: realUserID
        in: formData
        type: integer
        required: true
        description: Real User ID
      - name: userID
        in: formData
        type: integer
        required: true
        description: User ID
      - name: userType
        in: formData
        type: string
        required: true
        description: User Type (Patient or Therapist)
      - name: userNameUpd
        in: formData
        type: string
        required: true
        description: New User Name
      - name: emailUpd
        in: formData
        type: string
        required: true
        description: New Email Address
      - name: pfpFile
        in: formData
        type: file
        required: false
        description: New Profile Picture
    responses:
      200:
        description: Successfully updated user account details
        schema:
          type: object
          properties:
            inserted:
              type: integer
              description: Indicates success (1 for success)
            userName:
              type: string
            email:
              type: string
            profileImg:
              type: string
      404:
        description: User not found
      500:
        description: Internal server error
    """
    try:
        realUserId = request.form.get('realUserID')
        userId = request.form.get('userID')
        userType = request.form.get('userType')
        newName = request.form.get('userNameUpd')
        newEmail = request.form.get('emailUpd')
        print("New Name: ", newName)
        print("New Email: ", newEmail)

        cursor = mysql.connection.cursor()
        
        #   Updated profile picture (if it exists)
        if 'pfpFile' in request.files:
            profileImg = request.files['pfpFile']
            extension = profileImg.filename.rsplit('.', 1)[1].lower()
            UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'frontend', 'public', 'assets', 'profile-pics')
            filename = f'user-{realUserId}.{extension}'
            filename = secure_filename(filename)
            print(filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            profileImg.save(file_path)
            cursor.execute('''
                UPDATE users
                SET profileImg = %s
                WHERE userID = %s
            ''', (filename, realUserId))
            mysql.connection.commit()

        cursor.execute('''
            UPDATE users
            SET userName = %s, email = %s
            WHERE userID = %s            
        ''', (newName, newEmail, realUserId))
        mysql.connection.commit()
        
        cursor.execute(f'''
                SELECT userName, email, profileImg FROM users
                WHERE users.userID = {realUserId}
                ''')
        data = cursor.fetchone()
        if data:
            userName = data[0]
            email = data[1]
            profileImg = data[2]
            cursor.close()
            print(app.socketsNavbar)
            print(realUserId)
            if str(realUserId) in app.socketsNavbar:
                app.socketio.emit('update-navbar', room=app.socketsNavbar[str(realUserId)])
            print("SUCCESSFULLY UPDATED ACCOUNT DETAILS")
            response = jsonify({"inserted" : 1, "userName" : userName, "email" : email, "profileImg" : profileImg})
            response.status_code = 200
            response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response
        else:
            cursor.close()
            response = jsonify({"inserted" : 0})
            response.status_code = 404
            response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response
    except Exception as err:
        return {"error":  f"{err}"}
    
@settingsPageData.route('/settingsUpdInsDetails', methods=['POST'])
def settingsUpdInsDetailsFunc():
    """
    Update Insurance Details
    ---
    tags:
      - Settings
    parameters:
      - name: userId
        in: body
        type: integer
        required: true
        description: Patient ID
      - name: userType
        in: body
        type: string
        required: true
        description: User Type (Patient)
      - name: insCompUpd
        in: body
        type: string
        required: true
        description: New Insurance Company
      - name: insIDUpd
        in: body
        type: string
        required: true
        description: New Insurance ID
      - name: insTierUpd
        in: body
        type: string
        required: true
        description: New Insurance Tier
    responses:
      200:
        description: Successfully updated insurance details
        schema:
          type: object
          properties:
            inserted:
              type: integer
              description: Indicates success (1 for success)
            insComp:
              type: string
            insID:
              type: string
            insTier:
              type: string
      500:
        description: Internal server error
    """
    try:
        userId = request.json.get('userId')
        # userType = request.json.get('userType')
        newInsComp = request.json.get('insCompUpd')
        newInsID = request.json.get('insIDUpd')
        newInsTier = request.json.get('insTierUpd')
        
        cursor = mysql.connection.cursor()
        
        cursor.execute(f'''
                UPDATE patients
                SET insuranceCompany = "{newInsComp}", insuranceID = "{newInsID}", insuranceTier = "{newInsTier}"
                WHERE patientID = {userId};
                ''')
        mysql.connection.commit()

        cursor.execute(f'''
                SELECT insuranceCompany, insuranceID, insuranceTier
                FROM patients
                WHERE patientID = {userId};
                ''')
        data = cursor.fetchone()
        if data:
            insComp = data[0]
            insID = data[1]
            insTier = data[2]
            cursor.close()
            response = jsonify({"inserted" : 1, "insComp" : insComp, "insID" : insID, "insTier" : insTier})
            response.status_code = 200
            response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response
        else:
            cursor.close()
            response = jsonify({"inserted" : 0})
            response.status_code = 200
            response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response
    except Exception as err:
        return {"error":  f"{err}"}

@settingsPageData.route('/settingsUpdPrivacy', methods=['POST'])
def settingsUpdPrivacyFunc():
    """
    Update Privacy Settings
    ---
    tags:
      - Settings
    parameters:
      - name: userId
        in: body
        type: integer
        required: true
        description: Patient ID
      - name: patientPrivacy
        in: body
        type: boolean
        required: true
        description: New Privacy Setting
    responses:
      200:
        description: Privacy settings updated successfully.
        schema:
          type: object
          properties:
            inserted:
              type: boolean
      500:
        description: Internal server error.
    """
    try:
        userId = request.json.get('userId')
        newPrivacy = request.json.get('patientPrivacy')

        cursor = mysql.connection.cursor()
        
        cursor.execute(f'UPDATE patients SET allRecordsViewable = {newPrivacy} WHERE patientID = {userId};')
        mysql.connection.commit()
        if(cursor.rowcount > 0): # We ensure the table was modified
            cursor.close()
            response = jsonify({"inserted" : 1})
            response.status_code = 200
            response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response
        else:
            cursor.close()
            response = jsonify({"inserted" : 0})
            response.status_code = 200
            response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response
    except Exception as err:
        return {"error":  f"{err}"}

@settingsPageData.route('/settingsRemoveAccount', methods=['POST'])
def settingsRemAccFunc():
    """
    Remove User Account
    ---
    tags:
      - Settings
    parameters:
      - name: userId
        in: body
        type: integer
        required: true
        description: User ID
      - name: userType
        in: body
        type: string
        required: true
        description: User Type (Patient or Therapist)
    responses:
      200:
        description: Account removal success message.
        schema:
          type: object
          properties:
            deletion:
              type: string
              description: Deletion status.
      500:
        description: Error while removing account.
    """
    try:
        userId = request.json.get('userId')
        userType = request.json.get('userType')

        cursor = mysql.connection.cursor()

        if (userType == "Patient"):
            cursor.execute(f'SELECT invoiceID FROM invoices WHERE invoices.patientID = {userId}')
            if(cursor.rowcount > 0):
                cursor.close()
                response = jsonify({"deletion" : "Unpaid invoices"})
                response.status_code = 500
                response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
                response.headers['Access-Control-Allow-Credentials'] = 'true'
                response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
                response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
                return response

            cursor.execute(f'''
                SELECT users.userID, users.userName, patients.mainTherapistID
                FROM users, patients
                WHERE patients.patientID = users.userID AND patients.patientID = {userId}''')
            deletedUserInfo = cursor.fetchall() 
            realUserId = deletedUserInfo[0][0]
            patientName = deletedUserInfo[0][1]
            mainTherapistID = deletedUserInfo[0][2]

            # chats: deps on patients
            # completedDailySurveys: deps on patients
            # completedSurveys: deps on patients
            # details: deps on patients
            # feedback: deps on patients
            # journals: deps on patients
            # payments: deps on patients
            # reviews: deps on patients
            # surveys: deps on patients
            # therapistPatientsList: deps on patients
            cursor.execute(f'''
                DELETE FROM chats WHERE patientID = {userId}''')
            cursor.execute(f'''
                DELETE FROM completedDailySurveys WHERE patientID = {userId}''')
            cursor.execute(f'''
                DELETE FROM completedSurveys WHERE patientID = {userId}''')
            cursor.execute(f'''
                DELETE FROM details WHERE patientID = {userId}''')
            cursor.execute(f'''
                DELETE FROM feedback WHERE patientID = {userId}''')
            cursor.execute(f'''
                DELETE FROM journals WHERE patientID = {userId}''')
            cursor.execute(f'''
                DELETE FROM payments WHERE patientID = {userId}''')
            cursor.execute(f'''
                DELETE FROM reviews WHERE patientID = {userId}''')
            cursor.execute(f'''
                DELETE FROM surveys WHERE patientID = {userId}''')
            cursor.execute(f'''
                DELETE FROM therapistPatientsList WHERE patientID = {userId}''')
            # testimonials: deps on users
            # notifications: deps on users
            # patients: deps on users
            # users: no deps
            cursor.execute(f'''
                DELETE FROM testimonials WHERE userID = {realUserId}''')
            cursor.execute(f'''
                DELETE FROM notifications WHERE userID = {realUserId}''')
            cursor.execute(f'''
                DELETE FROM patients WHERE patientID = {userId}''')
            cursor.execute(f'''
                DELETE FROM users WHERE userID = {realUserId}''')

            if(mainTherapistID):
                cursor.execute(f"SELECT userID FROM therapists WHERE therapists.therapistID = {mainTherapistID}")
                theraUserID = cursor.fetchone()[0]
                cursor.execute(f'''
                    INSERT INTO notifications(userID, message)
                    VALUES ({theraUserID}, "Patient {patientName} has left Mentcare.")''')
                if str(theraUserID) in app.socketsNavbar:
                    app.socketio.emit("update-navbar", room=app.socketsNavbar[str(theraUserID)])
            
            mysql.connection.commit()
            response = jsonify({"deletion" : "successful"})
            response.status_code = 200
            response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response
        elif (userType == "Therapist"):
            #   Set therapist as Active or Inactive
            cursor.execute(f'''
                UPDATE therapists 
                SET isActive = CASE 
                    WHEN isActive = TRUE THEN FALSE 
                    ELSE TRUE 
                END
                WHERE therapistID = {userId}
                            ''')
            mysql.connection.commit()
            cursor.execute(f'SELECT isActive FROM therapists WHERE therapistID = {userId}')
            isActive = cursor.fetchone()[0]

            #   Set therapist relations with patients to Active ONLY IF the patients have this therapist as their mainTherapist
            #     cursor.execute(f'''
            #         UPDATE therapistPatientsList tpl
            #         INNER JOIN patients ON tpl.patientID = patients.patientID
            #         SET tpl.status = 'Active'
            #         WHERE tpl.therapistID = {userId} AND patients.mainTherapistID = {userId};
            #                     ''')
                # mysql.connection.commit()
            
            #   Set all therapist relations with patients to Inactive
            if isActive == False:
                cursor.execute(f'''
                    UPDATE therapistPatientsList
                    SET status = 'Inactive'
                    WHERE therapistID = {userId}
                                ''')
                cursor.execute(f"SELECT userID FROM patients WHERE mainTherapistID = {userId}")
                idsToNotify = cursor.fetchall()
                cursor.execute(f'''
                    UPDATE patients
                    SET mainTherapistID = NULL
                    WHERE mainTherapistID = {userId}
                                ''')
                for patientUserID in idsToNotify:
                    cursor.execute(f'''
                        INSERT INTO notifications(userID, message, redirectLocation)
                        VALUES ({patientUserID[0]}, "Your therapist has deactivated their account.", "/therapistlist")''')
                    mysql.connection.commit()
                    if str(patientUserID[0]) in app.socketsNavbar:
                        app.socketio.emit("update-navbar", room=app.socketsNavbar[str(patientUserID[0])])

            response = jsonify({"isActive" : isActive})
            response.status_code = 200
            response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response
        else:
            cursor.close()
            response = jsonify({"deletion" : "failed"})
            response.status_code = 500
            response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response
        
        # mysql.connection.commit()
        
        # if(cursor.rowcount > 0): # We ensure the table was modified
        #     cursor.close()
        #     return jsonify({"deleted" : 1}), 200
        # else:
        #     cursor.close()
        #     return jsonify({"deleted" : 0}), 200
    except Exception as err:
        return {"error":  f"{err}"}
