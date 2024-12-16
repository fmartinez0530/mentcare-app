from flask import request, jsonify, json, Blueprint
from app import mysql
import app
from datetime import datetime
#app = Flask(__name__)
# If you need socketio stuff maybe uncomment the below line.
# from flask_socketio import SocketIO, join_room, leave_room, send, emit


chatPageData = Blueprint('chatPageData', __name__)

@chatPageData.route("/getCharging", methods=['POST'])
def get_charging():
    """
    Get Therapist Charging Price
    ---
    tags:
      - Chat
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              therapistId:
                type: integer
                example: 1
    responses:
      200:
        description: Charging price fetched successfully
        content:
          application/json:
            schema:
              type: array
              items:
                type: number
      500:
        description: Internal server error
    """
    try:
        therapist_id = request.json.get('therapistId')
        cursor = mysql.connection.cursor()

        cursor.execute('''SELECT chargingPrice FROM therapists where therapistID = %s''', (therapist_id, ))
        charging = cursor.fetchall()

        mysql.connection.commit()
        cursor.close()
        # print(charging)

        response = jsonify(charging)
        response.status_code = 200
        response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    
    except Exception as err:
        return jsonify({"error": str(err)}), 500


@chatPageData.route("/updateStatus", methods=['POST'])
def set_chat_status():
    """
    Update Chat or Request Status
    ---
    tags:
      - Chat
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
              therapistId:
                type: integer
                example: 2
              status:
                type: string
                example: "Active"
              type:
                type: string
                example: "chat"
    responses:
      200:
        description: Status updated successfully
      500:
        description: Internal server error
    """
    try:
        patient_id = request.json.get('patientId')
        therapist_id = request.json.get('therapistId')
        status = request.json.get('status')
        type = request.json.get('type')

        cursor = mysql.connection.cursor()
        if (type == 'chat' and status == 'Active'):
            cursor.execute('UPDATE therapistPatientsList SET chatStatus = %s, requestStatus = \'Inactive\' where therapistID = %s and patientID = %s;', (status, therapist_id, patient_id))
        if (type == 'chat' and status == 'Inactive'):
            cursor.execute('UPDATE therapistPatientsList SET chatStatus = %s where therapistID = %s and patientID = %s;', (status, therapist_id, patient_id))
        elif (type == 'request'):
            cursor.execute('UPDATE therapistPatientsList SET requestStatus = %s where therapistID = %s and patientID = %s;', (status, therapist_id, patient_id))

        mysql.connection.commit()
        cursor.close()
        response = jsonify({"message": "Success"})
        response.status_code = 200
        response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    
    except Exception as err:
        return jsonify({"error": str(err)}), 500

@chatPageData.route('/sendInvoice', methods=['POST'])
def send_invoice():
    """
    Send Invoice
    ---
    tags:
      - Chat
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
              therapistId:
                type: integer
                example: 2
              amountDue:
                type: number
                example: 150.00
    responses:
      200:
        description: Invoice sent successfully
      500:
        description: Internal server error
    """
    try: 
        patient_id = request.json.get('patientId')
        therapist_id = request.json.get('therapistId')
        amount = str(round(float(request.json.get('amountDue')), 2))

        print("GOT HERE GOT HERE GOT HERE")

        print(patient_id)
        print(therapist_id)
        print(amount)

        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO invoices (patientID, therapistID, amountDue, dateCreated) VALUES
                        (%s, %s, %s, %s);''', (patient_id, therapist_id, amount, datetime.now()))
        
        mysql.connection.commit()
        cursor.close()
        response = jsonify({"message": "Success"})
        response.status_code = 200
        response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

    except Exception as err:
        return jsonify({"error": str(err)}), 500

@chatPageData.route("/userChats", methods=['POST'])
def get_user_chats():
    """
    Get User Chats
    ---
    tags:
      - Chat
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              chooseId:
                type: integer
                example: 1
              userType:
                type: string
                example: "Therapist"
    responses:
      200:
        description: Chats fetched successfully
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  userID:
                    type: integer
                  userName:
                    type: string
                  content:
                    type: string
                  chatStatus:
                    type: string
                  requestStatus:
                    type: string
      500:
        description: Internal server error
    """
    try:
        choose_id = request.json.get('chooseId')
        user_type = request.json.get('userType')

        cursor = mysql.connection.cursor()

        if user_type == "Therapist":
            cursor.execute('''
                SELECT p.patientID, u.userName AS patientName, c.content, chatStatus, requestStatus
                FROM patients p
                INNER JOIN therapistPatientsList tpl ON p.patientID = tpl.patientID
                INNER JOIN users u ON p.userID = u.userID
                INNER JOIN chats c ON tpl.patientID = c.patientID AND tpl.therapistID = c.therapistID
                WHERE tpl.therapistID = %s
            ''', (choose_id,))
        elif user_type == "Patient":
            cursor.execute('''
                SELECT t.therapistID, u.userName AS therapistName, c.content, status, chatStatus, requestStatus
                FROM therapists t
                INNER JOIN therapistPatientsList tpl ON t.therapistID = tpl.therapistID
                INNER JOIN users u ON t.userID = u.userID
                INNER JOIN chats c ON tpl.patientID = c.patientID AND tpl.therapistID = c.therapistID
                WHERE tpl.patientID = %s
            ''', (choose_id,))
        else:
            response = jsonify({"error": "Invalid user type"})
            response.status_code = 500
            response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response

        data = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in data]
        cursor.close()

        response = jsonify(results)
        response.status_code = 200
        response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    
@chatPageData.route('/startChat', methods=['POST'])
def startChatFunc():
    """
    Start Chat for a Patient
    ---
    tags:
      - Chat
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
              therapistId:
                type: integer
                example: 2
    responses:
      200:
        description: Chat started successfully
      500:
        description: Internal server error
    """
    try:
        patientID = request.json.get('patientId')
        therapistID = request.json.get('therapistId')

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT userID FROM patients WHERE patientID = %s', (patientID, ))
        data = cursor.fetchone()
        userID = data[0]
        # Emit the event to the connected socket clients
        if str(userID) in app.sockets:
            app.socketio.emit('start-chat-for-patient', {
                'therapistID': therapistID
            }, room=app.sockets[str(userID)])

        response = jsonify({"message": "Chat started successfully!"})
        response.status_code = 200
        response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    except Exception as err:
        return jsonify({"error": str(err)}), 500

@chatPageData.route('/endChat', methods=['POST'])
def endChatFunc():
    """
    End Chat for a Patient
    ---
    tags:
      - Chat
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
        description: Chat ended successfully
      500:
        description: Internal server error
    """
    try:
        patientID = request.json.get('patientId')

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT userID FROM patients WHERE patientID = %s', (patientID, ))
        data = cursor.fetchone()
        userID = data[0]

        # Emit the event to the connected socket clients
        if str(userID) in app.sockets:
            app.socketio.emit('end-chat-for-patient', {
                'message':'inactive'
            }, room=app.sockets[str(userID)])

        response = jsonify({"message": "Chat ended successfully!"})
        response.status_code = 200
        response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    
@chatPageData.route('/requestChat', methods=['POST'])
def requestChatFunc():
    """
    Request Chat from a Therapist
    ---
    tags:
      - Chat
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              therapistId:
                type: integer
                example: 2
              patientId:
                type: integer
                example: 1
    responses:
      200:
        description: Chat requested successfully
      500:
        description: Internal server error
    """
    try:
        therapistID = request.json.get('therapistId')
        patientID = request.json.get('patientId')

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT userID FROM therapists WHERE therapistID = %s', (therapistID, ))
        data = cursor.fetchone()
        userID = data[0]

        # Emit the event to the connected socket clients
        if str(userID) in app.sockets:
            app.socketio.emit('request-chat', {
                'patientID':patientID
            }, room=app.sockets[str(userID)])

        response = jsonify({"message": "Requested"})
        response.status_code = 200
        response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    
@chatPageData.route("/sendMessage", methods=['POST'])
def send_message():
    """
    Send a Chat Message
    ---
    tags:
      - Chat
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
              therapistId:
                type: integer
                example: 2
              message:
                type: string
                example: "Hello, how are you?"
              sender:
                type: string
                example: "P"
    responses:
      200:
        description: Message sent successfully
      500:
        description: Internal server error
    """
    try:

        patient_id = request.json.get('patientId')
        therapist_id = request.json.get('therapistId')
        message = request.json.get('message')
        sender = request.json.get('sender')

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT content FROM chats WHERE patientID = %s AND therapistID = %s', (patient_id, therapist_id))
        chat_data = cursor.fetchone()

        if chat_data:
            try:
                content = json.loads(chat_data[0])
                if "chats" not in content:
                    raise ValueError("Err Json")
            except Exception as e:
                response = jsonify({"error": f"Err: {str(e)}"})
                response.status_code = 500
                response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
                response.headers['Access-Control-Allow-Credentials'] = 'true'
                response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
                response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
                return response

            content['chats'].append({"msg": message, "sender": sender})

            cursor.execute(
                'UPDATE chats SET content = %s WHERE patientID = %s AND therapistID = %s',
                (json.dumps(content), patient_id, therapist_id)
            )
        else:
            new_content = {"chats": [{"msg": message, "sender": sender}]}
            cursor.execute(
                'INSERT INTO chats (patientID, therapistID, content, startTime) VALUES (%s, %s, %s, %s)',
                (patient_id, therapist_id, json.dumps(new_content), datetime.now())
            )

        mysql.connection.commit()
        cursor.close()

        if sender == 'P':
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT userID FROM therapists WHERE therapistID = %s', (therapist_id, ))
            data = cursor.fetchone()
            userID = data[0]
        elif sender == 'T':
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT userID FROM patients WHERE patientID = %s', (patient_id, ))
            data = cursor.fetchone()
            userID = data[0]
        print(userID)
        print(therapist_id)
        print(sender)
        print(message)
        print(patient_id)
        print(f"Current app.sockets before emit: {app.sockets}")
        print(f"Looking for userID: {userID}")

        if str(userID) in app.sockets:
            room = app.sockets[str(userID)]
            print(room)
            app.socketio.emit('new-message', { 'patientId': patient_id, 'therapistId': therapist_id, 'message': message, 'sender': sender }, room=room)
            print("New message sent to room " + room + " - " + message)

        response = jsonify({"message": "Success"})
        response.status_code = 200
        response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    except Exception as err:
        return jsonify({"error": str(err)}), 500
