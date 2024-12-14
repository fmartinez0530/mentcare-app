from flask import request, jsonify, Blueprint
from app import mysql

# Define Blueprint
loginPageData = Blueprint('loginPageData', __name__)

@loginPageData.route('/patientOrTherapist', methods=['POST'])
def patientOrTherapistFunc():
    """
    Authenticate user and determine their role (Patient or Therapist)
    ---
    tags:
      - Login
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              description: User's email address.
            password:
              type: string
              description: User's password.
    responses:
      200:
        description: User successfully authenticated.
        schema:
          type: object
          properties:
            userType:
              type: string
              description: Role of the user (Patient or Therapist).
            userID:
              type: integer
              description: Patient ID or Therapist ID.
            realUserID:
              type: integer
              description: User's unique ID in the system.
            isActive:
              type: integer
              description: Active status for therapists (1 for active, 0 for inactive).
      404:
        description: No user found with the provided email and password.
      500:
        description: Server error.
    """
    try:
        email = request.json.get('email')
        password = request.json.get('password')
        cursor = mysql.connection.cursor()
        cursor.execute('''
                SELECT userID, userType FROM users WHERE users.email LIKE %s AND users.pass LIKE %s
                ''', (email, password))
        data = cursor.fetchone()
        if data:
            userID = data[0]
            fakeUserID = 0
            user_type = data[1]  # Access the first (and only) column in the row
            isActive = 0
            if user_type == 'Patient':
                cursor.execute('''
                SELECT patientID FROM patients WHERE userID = %s               
                ''', (userID, ))
                data = cursor.fetchone()
                fakeUserID = data[0]
            elif user_type == 'Therapist':
                cursor.execute('''
                SELECT therapistID, isActive FROM therapists WHERE userID = %s               
                ''', (userID, ))
                data = cursor.fetchone()
                fakeUserID = data[0]
                isActive = data[1]
            
            cursor.close()
            response = jsonify({"userType": user_type, "userID": fakeUserID, "realUserID": userID, "isActive" : isActive})
            response.status_code = 200
            response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response
        else:
            response = jsonify({"error": "No user found with the given email and password"})
            response.status_code = 404
            response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response
    except Exception as err:
        return {"error": f"{err}"}, 500
