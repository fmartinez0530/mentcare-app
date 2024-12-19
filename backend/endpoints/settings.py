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
                response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
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
            cursor.execute('SET FOREIGN_KEY_CHECKS = 0')
            mysql.connection.commit()
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
            
            cursor.execute('SET FOREIGN_KEY_CHECKS = 1')
            mysql.connection.commit()
            
            response = jsonify({"deletion" : "successful"})
            response.status_code = 200
            response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
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
            response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response
        else:
            cursor.close()
            response = jsonify({"deletion" : "failed"})
            response.status_code = 500
            response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
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
