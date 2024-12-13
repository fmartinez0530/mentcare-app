from flask import request, jsonify, json, Blueprint #,render_template, request
from app import mysql, socketio, app
from flask import Flask, request, jsonify, json #,render_template, request
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from datetime import datetime
import app
#app = Flask(__name__)
# If you need socketio stuff maybe uncomment the below line.
# from flask_socketio import SocketIO, join_room, leave_room, send, emit


chatPageData = Blueprint('chatPageData', __name__)

@chatPageData.route("/getCharging", methods=['POST'])
def get_charging():
    try:
        therapist_id = request.json.get('therapistId')
        cursor = mysql.connection.cursor()

        cursor.execute('''SELECT chargingPrice FROM therapists where therapistID = %s''', (therapist_id, ))
        charging = cursor.fetchall()

        mysql.connection.commit()
        cursor.close()
        print(charging[0][0])

        return jsonify(charging)
    
    except Exception as err:
        return jsonify({"error": str(err)}), 500


@chatPageData.route("/updateStatus", methods=['POST'])
def set_chat_status():
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
        return jsonify({"message": "Success"}), 200
    
    except Exception as err:
        return jsonify({"error": str(err)}), 500

@chatPageData.route('/sendInvoice', methods=['POST'])
def send_invoice():
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
        return jsonify({"message": "Success"}), 200

    except Exception as err:
        return jsonify({"error": str(err)}), 500

@chatPageData.route("/userChats", methods=['POST'])
def get_user_chats():
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
        else:
            cursor.execute('''
                SELECT t.therapistID, u.userName AS therapistName, c.content, status, chatStatus, requestStatus
                FROM therapists t
                INNER JOIN therapistPatientsList tpl ON t.therapistID = tpl.therapistID
                INNER JOIN users u ON t.userID = u.userID
                INNER JOIN chats c ON tpl.patientID = c.patientID AND tpl.therapistID = c.therapistID
                WHERE tpl.patientID = %s
            ''', (choose_id,))

        data = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in data]
        cursor.close()

        return jsonify(results), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    
@chatPageData.route('/startChat', methods=['POST'])
def startChatFunc():
    try:
        patientID = request.json.get('patientId')
        therapistID = request.json.get('therapistId')

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT userID FROM patients WHERE patientID = %s', (patientID, ))
        data = cursor.fetchone()
        userID = data[0]

        print('got in')
        # Emit the event to the connected socket clients
        app.socketio.emit('start-chat-for-patient', {
            'therapistID': therapistID
        }, room=app.sockets[str(userID)])

        return jsonify({"message": "Chat started successfully!"}), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500

@chatPageData.route('/endChat', methods=['POST'])
def endChatFunc():
    try:
        patientID = request.json.get('patientId')

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT userID FROM patients WHERE patientID = %s', (patientID, ))
        data = cursor.fetchone()
        userID = data[0]

        # Emit the event to the connected socket clients
        app.socketio.emit('end-chat-for-patient', {
            'message':'inactive'
        }, room=app.sockets[str(userID)])

        return jsonify({"message": "Chat ended successfully!"}), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    
@chatPageData.route('/requestChat', methods=['POST'])
def requestChatFunc():
    try:
        therapistID = request.json.get('therapistId')
        patientID = request.json.get('patientId')

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT userID FROM therapists WHERE therapistID = %s', (therapistID, ))
        data = cursor.fetchone()
        userID = data[0]

        # Emit the event to the connected socket clients
        app.socketio.emit('request-chat', {
            'patientID':patientID
        }, room=app.sockets[str(userID)])

        return jsonify({"message": "Requested"}), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    
@chatPageData.route("/sendMessage", methods=['POST'])
def send_message():
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
                return jsonify({"error": f"Err: {str(e)}"}), 500

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
        else:
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT userID FROM patients WHERE patientID = %s', (patient_id, ))
            data = cursor.fetchone()
            userID = data[0]
        print(userID)
        print(therapist_id)
        print(sender)
        print(message)
        print(patient_id)
        room = app.sockets[str(userID)]
        print(room)
        app.socketio.emit('new-message', { 'patientId': patient_id, 'therapistId': therapist_id, 'message': message, 'sender': sender }, room=room)
        print("New message sent to room " + room + " - " + message)

        return jsonify({"message": "Success"}), 200

    except Exception as err:
        return jsonify({"error": str(err)}), 500