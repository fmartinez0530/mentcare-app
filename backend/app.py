from flask import Flask, request, jsonify, json, send_file #,render_template, request
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from datetime import datetime
from io import BytesIO
from flasgger import Swagger
import os
app = Flask(__name__)
frontend_url = os.getenv('FRONTEND_URL', 'https://mentcare-frontend.onrender.com')
CORS(app, origins='*', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'], allow_headers=['Content-Type', 'Authorization'], supports_credentials=True)
socketio = SocketIO(app, cors_allowed_origins='*', methods=['GET', 'POST', 'OPTIONS'])
sockets = {}
socketsNavbar = {}
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')  # Default to localhost if not set
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_ROOT_PASSWORD', '')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DATABASE', 'mentcare')


mysql = MySQL(app)

# Initialize Swagger
swagger = Swagger(app)

from endpoints.example import examplePageStuff
app.register_blueprint(examplePageStuff)

# adrian

from endpoints.chatPage import chatPageData
app.register_blueprint(chatPageData)

from endpoints.paymentPage import paymentPageData
app.register_blueprint(paymentPageData)

# akul

from endpoints.landingPage import landingPageData
app.register_blueprint(landingPageData)

from endpoints.therapistProfile import therapist_routes
app.register_blueprint(therapist_routes)

# anish

from endpoints.therapistListPage import therapistListData
app.register_blueprint(therapistListData)

from endpoints.patientProfile import PatientProfileData
app.register_blueprint(PatientProfileData)

# fausto

from endpoints.loginPage import loginPageData
app.register_blueprint(loginPageData)

from endpoints.registrationPage import registrationPageData
app.register_blueprint(registrationPageData)

from endpoints.patientDashboard import PatientDashboardData
app.register_blueprint(PatientDashboardData)

# joel

from endpoints.therapistDashboard import TherapistDashboardData
app.register_blueprint(TherapistDashboardData)

from endpoints.settings import settingsPageData
app.register_blueprint(settingsPageData)

@app.before_request
def handle_options():
    if request.method == "OPTIONS":
        response = app.make_response("")
        response.headers["Access-Control-Allow-Origin"] = "https://mentcare-frontend.onrender.com"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        return response, 200

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@app.route("/")
def defaultFunc():
    """
    Check Backend Status
    ---
    tags:
      - General
    responses:
      200:
        description: Backend status
        schema:
          type: object
          properties:
            status:
              type: string
              example: "Backend is alive"
    """
    # return {"status": "Backend is alive"}
    response = jsonify({'status': 'Backend is alive'})
    response.status_code = 200
    response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@app.route("/navbarData", methods=['POST'])
def navbarDataFunc():
    """
    Fetch Navbar Data
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            fakeUserID:
              type: integer
              description: Fake user ID
            userType:
              type: string
              description: User type (e.g., Patient or Therapist)
    responses:
      200:
        description: Navbar data fetched successfully
        schema:
          type: array
          items:
            type: object
            properties:
              userID:
                type: integer
              userName:
                type: string
              userType:
                type: string
      404:
        description: User not found
    """
    try:
        fakeUserId = request.json.get('fakeUserID')
        userType = request.json.get('userType')
        totalResults = []

        cursor = mysql.connection.cursor()

        if userType == 'Patient':
            cursor.execute('''
                    SELECT users.userID, userName, userType FROM users
                    INNER JOIN patients ON users.userID = patients.userID
                    WHERE patients.patientID = %s
                    ''', (fakeUserId, ))
        elif userType == 'Therapist':
            cursor.execute('''
                    SELECT users.userID, userName, userType, therapists.isActive FROM users
                    INNER JOIN therapists ON users.userID = therapists.userID
                    WHERE therapists.therapistID = %s
                    ''', (fakeUserId, ))
        data = cursor.fetchall()
        if data:
            columns = [column[0] for column in cursor.description]
            results = [dict(zip(columns, row)) for row in data]                
            totalResults.append(results)

            userId = results[0]['userID']

            cursor.execute('''
                    SELECT notificationID, message, redirectLocation FROM notifications WHERE userID = %s
                    ''', (userId, ))
            notifs_data = cursor.fetchall()
            if notifs_data:
                notifs_columns = [column[0] for column in cursor.description]
                notifs_results = [dict(zip(notifs_columns, row)) for row in notifs_data]
                totalResults.append(notifs_results)
            else:
                totalResults.append(None)
            
            # return jsonify(totalResults)
            response = jsonify(totalResults)
            response.status_code = 200
            response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response
        else:
            response = jsonify({"message" : "User not found"})
            response.status_code = 404
            response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response

    except Exception as err:
        return {"error":  f"{err}"}
    
@app.route('/retriveProfilePic', methods=['POST'])
def retriveProfilePicFunc():
    try:
        realUserID = request.json.get('realUserID')
        cursor = mysql.connection.cursor()
        cursor.execute('''
            SELECT profileImg FROM users
            WHERE userID = %s
        ''', (realUserID,))

        data = cursor.fetchone()
        if data and data[0] is not None:
            # profile_img_data = data[0]
            # if profile_img_data:
            #     img_stream = BytesIO(profile_img_data)
            #     return send_file(img_stream, mimetype='image/jpeg')
            # else:
            response = jsonify({"profileImg": data[0]})
            response.status_code = 200
            response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response
        else:
            response = jsonify({"error": "Profile image is null"})
            response.status_code = 404
            response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response
    except Exception as err:
        return {"error":  f"{err}"}
    
@app.route('/deleteNotification', methods=['POST'])
def delNotifFunc():
    """
    Delete a Notification
    ---
    tags:
      - Notifications
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            notificationID:
              type: integer
              example: 1
    responses:
      200:
        description: Notification deleted successfully
      500:
        description: Internal Server Error
    """
    try:
        notificationID = request.json.get('notificationID')

        cursor = mysql.connection.cursor()
        cursor.execute('''
                    DELETE FROM notifications WHERE notificationID = %s
                    ''', (notificationID, ))
        mysql.connection.commit()
        cursor.close()

        response = jsonify({"message" : "Notification succesfully delete!"})
        response.status_code = 200
        response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    except Exception as err:
        return {"error":  f"{err}"}
    
@app.route('/updateSocketsNavbar', methods=['POST'])
def updateSocketsNavFunc():
    """
    Update Navbar Sockets
    ---
    tags:
      - Sockets
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            realUserID:
              type: integer
              example: 101
    responses:
      200:
        description: Navbar sockets updated successfully
      500:
        description: Internal Server Error
    """
    try:
        print("GOT HERE")
        realUserID = request.json.get('realUserID')
        #socketsNavbar[realUserID] = request.sid
        #print("UPDATE NAVBAR SOCKETS CONNECTIONS")
        print("CURRENT NAVBAR SOCKETS CONNECTIONS: ", socketsNavbar)
        #print(f"Added socketId {request.sid} for userId {realUserID} to socketsNavbar")

        response = jsonify({"message" : "Sockets navbar succesfully updated!"})
        response.status_code = 200
        response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    except Exception as err:
        return {"error":  f"{err}"}

#############   BEGINNING OF SOCKETIO CODE   ############

if __name__ == '__main__':
    socketio.run(app)

#   Initiate socket connection (for whatever page users goes into)
@socketio.on('init-socket-comm')
def initializeSocketCommunication(data):
    #   In this case, userID is the ACTUAL userID
    userId = data.get('userID')
    socketId = request.sid
    sockets[userId] = socketId
    print("CURRENT SOCKETS CONNECTIONS: ", sockets)
    print(f"Added socketId {socketId} for userId {userId}")

#   Removes socket connection (for the page user was just in)
@socketio.on('rem-socket-comm')
def removeSocketCommunication(data):
    #   In this case, userID is the ACTUAL userID
    userId = data.get('userID')
    if userId in sockets:
        socketId = sockets.pop(userId)
        print(f"Removed socketId {socketId} for userId {userId} to sockets")
    else:
        print(f"userId {userId} not found in sockets dictionary")

#   Initiate socket connection for the user's navbar
@socketio.on('init-socket-navbar-comm')
def initializeSocketCommunication(data):
    #   In this case, userID is the ACTUAL userID
    userId = data.get('userID')
    socketId = request.sid
    socketsNavbar[userId] = socketId
    print("CURRENT NAVBAR SOCKETS CONNECTIONS: ", socketsNavbar)
    print(f"Added socketId {socketId} for userId {userId} to socketsNavbar")

#   Removes socket connection for the user's navbar
@socketio.on('rem-socket-navbar-comm')
def removeSocketCommunication(data):
    #   In this case, userID is the ACTUAL userID
    userId = data.get('userID')
    if userId in sockets:
        socketId = sockets.pop(userId)
        print(f"Removed socketId {socketId} for userId {userId} to sockets")
    else:
        print(f"userId {userId} not found in sockets dictionary")

#   (WIP) Sent from Patient Overview Page to a Patient's Dashboard Page
@socketio.on('send-new-feedback')
def sendFeedback(data):
    patientId = data.get('patientID')
    feedback = data.get('feedback')

    if patientId in sockets:
        socketio.emit('new-feedback', {'feedback': feedback}, room=sockets[patientId])
