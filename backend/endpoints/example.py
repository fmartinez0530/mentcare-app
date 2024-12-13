from flask import request, jsonify, json, Blueprint #,render_template, request
from app import mysql # , socketio, sockets
# If you need socketio stuff maybe uncomment the below line. 100% uncomment the stuff directly above
# from flask_socketio import SocketIO, join_room, leave_room, send, emit

# Feel free to add more imports

examplePageStuff = Blueprint('examplePageStuff', __name__)

# these endpoints heed to have unique names across the entire app (i.e there can only be one "/endpointOne" anywhere)
@examplePageStuff.route('/endpointOne', methods=['POST'])
def endpointNumberOneFunc():
    try:
        something = request.json.get('userInformation')

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users LIMIT 1')
        data = cursor.fetchall()
        cursor.close()

        return jsonify({"someSQLdata" : data}), 200
    except Exception as err:
        return {"error":  f"{err}"}
    
@examplePageStuff.route('/endpointTwo', methods=['GET'])
def second_Endpoint_Function():
    return jsonify({"data" : "foobar"}), 200