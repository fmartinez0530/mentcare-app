from flask import request, jsonify, json, Blueprint #,render_template, request
from app import mysql # , socketio, sockets
from datetime import datetime;
from datetime import date;
# If you need socketio stuff maybe uncomment the below line. 100% uncomment the stuff directly above
# from flask_socketio import SocketIO, join_room, leave_room, send, emit

# Feel free to add more imports


paymentPageData = Blueprint('paymentPageData', __name__)

@paymentPageData.route('/endpointOne', methods=['GET'])
def sample_endpoint_function():
    return jsonify({"data" : "I exist"}), 200

@paymentPageData.route('/getDetails', methods=['POST'])
def get_details():
    try:
        patient_id = request.json.get('patientId')

        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT * from details WHERE patientID = %s''', (patient_id,))
        details = cursor.fetchall()
        print(details)

        mysql.connection.commit()
        cursor.close()

        return jsonify(details)

    except Exception as err:
        return jsonify({"error": str(err)}), 500

@paymentPageData.route('/submitPayment', methods=['POST'])
def submit_payment():
    try: 
        patient_id = request.json.get('patientId')
        invoice_id = request.json.get('invoiceId')
        amount = str(float(request.json.get('amount')))
        date_paid = datetime.now()
        card_num = request.json.get('cardNum')
        cvc = request.json.get('cvc')
        exp_date = request.json.get('expDate')
        first_name = request.json.get('firstName')
        last_name = request.json.get('lastName')
        city = request.json.get('city')
        billing_address = request.json.get('billingAddress')
        state = request.json.get('state')
        country = request.json.get('country')
        zip = request.json.get('zip')
        phone = request.json.get('phone')
        check = request.json.get('check')
        alreadyIn = request.json.get('alreadyIn')

        print(patient_id)
        print(invoice_id)
        print(amount)
        print(date_paid)
        print(card_num)
        print(cvc)
        print(exp_date)
        print(first_name)
        print(last_name)
        print(city)
        print(billing_address)
        print(state)
        print(country)
        print(zip)
        print(phone)
        print(check)
        print(alreadyIn)

        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO payments (patientID, amount, datePaid, cardNum, cvc, expDate, firstName, lastName, city, billingAddress, state, country, zip, phone) VALUES
                        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);''', (patient_id, amount, date_paid, card_num, cvc, exp_date, first_name, last_name, city, billing_address, state, country, zip, phone))

        if (check == True and alreadyIn == False):
            print("Got through")
            cursor.execute('''INSERT INTO details (patientID, cardNum, cvc, expDate, firstName, lastName, city, billingAddress, state, country, zip, phone) VALUES 
                           (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);''', (patient_id, card_num, cvc, exp_date, first_name, last_name, city, billing_address, state, country, zip, phone))
            print("Got through")

        if (check == False and alreadyIn == True):
            print('deleted')
            cursor.execute('''DELETE FROM details WHERE patientID = %s;''', (patient_id,))

        print("got through")
        cursor.execute('''DELETE FROM invoices WHERE invoiceID = %s;''', (invoice_id,))
        print("got through")
        
        mysql.connection.commit()
        cursor.close()
        return jsonify({"message": "Success"}), 200

    except Exception as err:
        return jsonify({"error": str(err)}), 500