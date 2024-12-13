from flask import request, jsonify, json, Blueprint, send_file #,render_template, request
from app import mysql
import app
from io import BytesIO
import os
from werkzeug.utils import secure_filename

settingsPageData = Blueprint('settingsPageData', __name__)

@settingsPageData.route('/settingsAccountData', methods=['POST'])
def settingsPageDataFunc():
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
        
        return jsonify({"userName" : data1[0][0], "email" : data1[0][1],
                        "patientPrivacy" : data2[0][0], "insComp" : data2[0][1], "insID" : data2[0][2], "insTier" : data2[0][3], "isActive" : isActive }), 200
    
    except Exception as err:
        return {"error":  f"{err}"}

@settingsPageData.route('/settingsUpdAccDetails', methods=['POST'])
def settingsUpdAccDetailsFunc():
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
            app.socketio.emit('update-navbar', room=app.socketsNavbar[realUserId])
            print("SUCCESSFULLY UPDATED ACCOUNT DETAILS")
            return jsonify({"inserted" : 1, "userName" : userName, "email" : email, "profileImg" : profileImg}), 200
        else:
            cursor.close()
            return jsonify({"inserted" : 0}), 404
    except Exception as err:
        return {"error":  f"{err}"}
    
@settingsPageData.route('/settingsUpdInsDetails', methods=['POST'])
def settingsUpdInsDetailsFunc():
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
            return jsonify({"inserted" : 1, "insComp" : insComp, "insID" : insID, "insTier" : insTier}), 200
        else:
            cursor.close()
            return jsonify({"inserted" : 0}), 200
    except Exception as err:
        return {"error":  f"{err}"}

@settingsPageData.route('/settingsUpdPrivacy', methods=['POST'])
def settingsUpdPrivacyFunc():
    try:
        userId = request.json.get('userId')
        newPrivacy = request.json.get('patientPrivacy')

        cursor = mysql.connection.cursor()
        
        cursor.execute(f'UPDATE patients SET allRecordsViewable = {newPrivacy} WHERE patientID = {userId};')
        mysql.connection.commit()
        if(cursor.rowcount > 0): # We ensure the table was modified
            cursor.close()
            return jsonify({"inserted" : 1}), 200
        else:
            cursor.close()
            return jsonify({"inserted" : 0}), 200
    except Exception as err:
        return {"error":  f"{err}"}

@settingsPageData.route('/settingsRemoveAccount', methods=['POST'])
def settingsRemAccFunc():
    try:
        userId = request.json.get('userId')
        userType = request.json.get('userType')

        cursor = mysql.connection.cursor()

        if (userType == "Patient"):
            cursor.execute(f'SELECT invoiceID FROM invoices WHERE invoices.patientID = {userId}')
            if(cursor.rowcount > 0):
                cursor.close()
                return jsonify({"deletion" : "Unpaid invoices"}), 500

            cursor.execute(f'SELECT userID FROM patients WHERE patients.patientID = {userId}')
            realUserId = cursor.fetchone()[0]

            # chats: deps on patients
            # completedDailySurveys: deps on patients
            # completedSurveys: deps on patients
            # feedback: deps on patients
            # journals: deps on patients
            # surveys: deps on patients
            # therapistPatientsList: deps on patients
            cursor.execute(f'''
                DELETE FROM payments WHERE patientID = {userId}''')
            cursor.execute(f'''
                DELETE FROM details WHERE patientID = {userId}''')
            cursor.execute(f'''
                DELETE FROM chats WHERE patientID = {userId}''')
            cursor.execute(f'''
                DELETE FROM completedDailySurveys WHERE patientID = {userId}''')
            cursor.execute(f'''
                DELETE FROM completedSurveys WHERE patientID = {userId}''')
            cursor.execute(f'''
                DELETE FROM feedback WHERE patientID = {userId}''')
            cursor.execute(f'''
                DELETE FROM journals WHERE patientID = {userId}''')
            cursor.execute(f'''
                DELETE FROM surveys WHERE patientID = {userId}''')
            cursor.execute(f'''
                DELETE FROM reviews WHERE patientID = {userId}''')
            cursor.execute(f'''
                DELETE FROM testimonials WHERE userID = {realUserId}''')
            cursor.execute(f'''
                DELETE FROM therapistPatientsList WHERE patientID = {userId}''')
            # notifications: deps on users
            # patients: deps on users
            # users: no deps
            cursor.execute(f'''
                DELETE FROM notifications WHERE userID = {realUserId}''')
            cursor.execute(f'''
                DELETE FROM patients WHERE userID = {realUserId}''')
            cursor.execute(f'''
                DELETE FROM users WHERE userID = {realUserId}''')
            mysql.connection.commit()
            return jsonify({"deletion" : "successful"}), 200
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
            if isActive == True:
                cursor.execute(f'''
                    UPDATE therapistPatientsList tpl
                    INNER JOIN patients ON tpl.patientID = patients.patientID
                    SET tpl.status = 'Active'
                    WHERE tpl.therapistID = {userId} AND patients.mainTherapistID = {userId};
                                ''')
                mysql.connection.commit()
            
            #   Set all therapist relations with patients to Inactive
            else:
                cursor.execute(f'''
                    UPDATE therapistPatientsList
                    SET status = 'Inactive'
                    WHERE therapistID = {userId}
                                ''')
                mysql.connection.commit()

            return jsonify({"isActive" : isActive}), 200
        else:
            cursor.close()
            return jsonify({"deletion" : "failed"}), 500
        
        # mysql.connection.commit()
        
        # if(cursor.rowcount > 0): # We ensure the table was modified
        #     cursor.close()
        #     return jsonify({"deleted" : 1}), 200
        # else:
        #     cursor.close()
        #     return jsonify({"deleted" : 0}), 200
    except Exception as err:
        return {"error":  f"{err}"}