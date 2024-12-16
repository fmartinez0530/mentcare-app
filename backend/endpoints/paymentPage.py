from flask import request, jsonify, json, Blueprint #,render_template, request
from app import mysql # , socketio, sockets
from datetime import datetime;
from datetime import date;
# If you need socketio stuff maybe uncomment the below line. 100% uncomment the stuff directly above
# from flask_socketio import SocketIO, join_room, leave_room, send, emit

# Feel free to add more imports


paymentPageData = Blueprint('paymentPageData', __name__)

@paymentPageData.route('/getDetails', methods=['POST'])
def get_details():
    """
    Get Payment Details
    ---
    tags:
      - Payment
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
            required:
              - patientId
    responses:
      200:
        description: Payment details fetched successfully
      500:
        description: Internal server error
    """
    try:
        patient_id = request.json.get('patientId')

        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT * from details WHERE patientID = %s''', (patient_id,))
        details = cursor.fetchall()
        print(details)

        mysql.connection.commit()
        cursor.close()

        response = jsonify(details)
        response.status_code = 200
        response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

    except Exception as err:
        return jsonify({"error": str(err)}), 500

@paymentPageData.route('/submitPayment', methods=['POST'])
def submit_payment():
    """
    Submit Payment
    ---
    tags:
      - Payment
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
              invoiceId:
                type: integer
                example: 101
              amount:
                type: number
                format: float
                example: 150.75
              cardNum:
                type: string
                example: "1234567890123456"
              cvc:
                type: string
                example: "123"
              expDate:
                type: string
                example: "12/25"
              firstName:
                type: string
                example: "John"
              lastName:
                type: string
                example: "Doe"
              city:
                type: string
                example: "New York"
              billingAddress:
                type: string
                example: "123 Main St"
              state:
                type: string
                example: "NY"
              country:
                type: string
                example: "USA"
              zip:
                type: string
                example: "10001"
              phone:
                type: string
                example: "+1234567890"
              check:
                type: boolean
                example: true
              alreadyIn:
                type: boolean
                example: false
            required:
              - patientId
              - invoiceId
              - amount
              - cardNum
              - cvc
              - expDate
              - firstName
              - lastName
              - billingAddress
              - city
              - state
              - zip
              - phone
    responses:
      200:
        description: Payment submitted successfully
      500:
        description: Internal server error
    """
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
        # cursor.execute('''INSERT INTO payments (patientID, amount, datePaid, cardNum, cvc, expDate, firstName, lastName, city, billingAddress, state, country, zip, phone) VALUES
        #                 (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);''', (patient_id, amount, date_paid, card_num, cvc, exp_date, first_name, last_name, city, billing_address, state, country, zip, phone))

        if (check == True and alreadyIn == False):
            print("Got through")
            cursor.execute('''INSERT INTO details (patientID, cardNum, cvc, expDate, firstName, lastName, city, billingAddress, state, country, zip, phone) VALUES 
                           (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);''', (patient_id, card_num, cvc, exp_date, first_name, last_name, city, billing_address, state, country, zip, phone))
            print("Got through")

        elif  (check == False and alreadyIn == True):
            print('deleted')
            cursor.execute('''DELETE FROM details WHERE patientID = %s;''', (patient_id,))

        elif (check == True and alreadyIn == True):
            cursor.execute('''UPDATE details SET 
                cardNum = %s, cvc = %s, expDate = %s, firstName = %s, 
                lastName = %s, city = %s, billingAddress = %s, state = %s, 
                country = %s, zip = %s, phone = %s WHERE patientID = %s''', 
                (card_num, cvc, exp_date, first_name, last_name, city, billing_address, state, country, zip, phone, patient_id,))

        print("got through")
        cursor.execute('''DELETE FROM invoices WHERE invoiceID = %s;''', (invoice_id,))
        print("got through")
        
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