from flask import request, jsonify, json, Blueprint #,render_template, request
from app import mysql # , socketio, sockets
import os
from werkzeug.utils import secure_filename
# If you need socketio stuff maybe uncomment the below line. 100% uncomment the stuff directly above
# from flask_socketio import SocketIO, join_room, leave_room, send, emit

# Feel free to add more imports


registrationPageData = Blueprint('registrationPageData', __name__)

@registrationPageData.route("/validateUserEmail", methods=['POST'])
def validateEmailFunc():
    """
    Validate User Email
    ---
    tags:
      - Registration
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              email:
                type: string
                example: "test@example.com"
            required:
              - email
    responses:
      200:
        description: Email is valid for registration
      409:
        description: Email is already registered
      500:
        description: Internal server error
    """

    email = request.json.get('email')
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT email FROM users WHERE email LIKE %s", (email, ))
    if(cursor.rowcount > 0):
        response = jsonify({"message" : "Email/User already exists"})
        response.status_code = 409
        response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    else:
        response = jsonify({"message" : "Email is good for use"})
        response.status_code = 200
        response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    
@registrationPageData.route("/registerPatient", methods=['POST'])
def registerPatientFunc():
    """
    Register Patient
    ---
    tags:
      - Registration
    requestBody:
      required: true
      content:
        multipart/form-data:
          schema:
            type: object
            properties:
              fname:
                type: string
                example: "John"
              lname:
                type: string
                example: "Doe"
              email:
                type: string
                example: "john.doe@example.com"
              password:
                type: string
                example: "password123"
              gender:
                type: string
                example: "Male"
              profileImg:
                type: string
                format: binary
              company:
                type: string
                example: "InsuranceCo"
              insuranceId:
                type: string
                example: "INS123456"
              tier:
                type: string
                example: "Gold"
            required:
              - fname
              - lname
              - email
              - password
    responses:
      200:
        description: Patient successfully registered
      400:
        description: Invalid data or missing fields
      500:
        description: Internal server error
    """
    try:
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        fullname = fname + ' ' + lname
        email = request.form.get('email')
        password = request.form.get('password')
        gender = request.form.get('gender')

        # profileImgBinary = None
        # if 'profileImg' in request.files:
        #     profileImg = request.files['profileImg']
        #     if profileImg:
        #         profileImgBinary = profileImg.read()  # Read the binary data of the image
        #     else:
        #         return jsonify({"error": "Invalid file type. Only image files are allowed."}), 400

        insuranceCompany = request.form.get('company')
        insuranceID = request.form.get('insuranceId')
        insuranceTier = request.form.get('tier')

        weight = request.form.get('weight')
        height = request.form.get('height')
        calories = request.form.get('calories')
        water = request.form.get('water')
        exercise = request.form.get('exercise')
        sleep = request.form.get('sleep')
        energy = request.form.get('energy')
        stress = request.form.get('stress')

        cursor = mysql.connection.cursor()
        # if profileImgBinary == None:
        #     cursor.execute('''
        #             INSERT INTO users (userName, email, pass, userType)
        #             VALUES (%s, %s, %s, 'Patient')
        #             ''', (fullname, email, password))
        # else:
        #     cursor.execute('''
        #             INSERT INTO users (userName, email, pass, userType, profileImg)
        #             VALUES (%s, %s, %s, 'Patient', %s)
        #             ''', (fullname, email, password, profileImgBinary))
        if gender == 'null':
            cursor.execute('''
                INSERT INTO users (userName, email, pass, userType)
                VALUES (%s, %s, %s, 'Patient')
            ''', (fullname, email, password))
            mysql.connection.commit()
        else:
            cursor.execute('''
                INSERT INTO users (userName, email, pass, gender, userType)
                VALUES (%s, %s, %s, %s, 'Patient')
            ''', (fullname, email, password, gender))
            mysql.connection.commit()
        print("\nSUCCESSFULLY ADDED USER!\n")

        #   Retrive userID of newly created user
        cursor.execute("SELECT userID FROM users WHERE email LIKE %s AND pass LIKE %s", (email, password))
        data = cursor.fetchone()
        userID = data[0]

        #   Insert profile picture (if it exists)
        if 'profileImg' in request.files:
            profileImg = request.files['profileImg']
            extension = profileImg.filename.rsplit('.', 1)[1].lower()
            UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'frontend', 'public', 'assets', 'profile-pics')
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            filename = f'user-{userID}.{extension}'
            filename = secure_filename(filename)
            print(filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            profileImg.save(file_path)
            cursor.execute('''
                UPDATE users
                SET profileImg = %s
                WHERE email LIKE %s AND pass LIKE %s
            ''', (filename, email, password))
            mysql.connection.commit()

        #   Insert insurance information (if it exists)
        if insuranceCompany and insuranceID and insuranceTier:
            cursor.execute('''
                    INSERT INTO patients (userID, insuranceCompany, insuranceID, insuranceTier)
                    VALUES (%s, %s, %s, %s)
                    ''', (userID, insuranceCompany, insuranceID, insuranceTier))
        else:
            cursor.execute('INSERT INTO patients (userID) VALUES (%s)', (userID, ))
        mysql.connection.commit()

        #   Retrive patientID of newly created user
        cursor.execute("SELECT patientID FROM patients WHERE userID = %s", (userID,))
        data = cursor.fetchone()
        patientID = data[0]

        cursor.close()
        response = jsonify({"message" : "User successfully registered", "patientID" : patientID, "userID" : userID})
        response.status_code = 200
        response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    except Exception as err:
        return jsonify({"error":  f"{err}"}), 400
    
@registrationPageData.route("/registerTherapist", methods=['POST'])
def registerTherapistFunc():
    """
    Register Therapist
    ---
    tags:
      - Registration
    requestBody:
      required: true
      content:
        multipart/form-data:
          schema:
            type: object
            properties:
              fname:
                type: string
                example: "Alice"
              lname:
                type: string
                example: "Smith"
              email:
                type: string
                example: "alice.smith@example.com"
              password:
                type: string
                example: "securepassword"
              gender:
                type: string
                example: "Female"
              license:
                type: string
                example: "LIC-123456"
              specializations:
                type: string
                example: "Anxiety, Depression"
              profileImg:
                type: string
                format: binary
            required:
              - fname
              - lname
              - email
              - password
              - license
              - specializations
    responses:
      200:
        description: Therapist successfully registered
      400:
        description: Invalid data or missing fields
      500:
        description: Internal server error
    """
    try:
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        fullname = fname + ' ' + lname
        email = request.form.get('email')
        password = request.form.get('password')
        gender = request.form.get('gender')
        license = request.form.get('license')
        specsArray = request.form.get('specializations')

        cursor = mysql.connection.cursor()

        if gender == 'null':
            cursor.execute('''
                INSERT INTO users (userName, email, pass, userType)
                VALUES (%s, %s, %s, 'Therapist')
            ''', (fullname, email, password))
            mysql.connection.commit()
        else:
            cursor.execute('''
                INSERT INTO users (userName, email, pass, gender, userType)
                VALUES (%s, %s, %s, %s, 'Therapist')
            ''', (fullname, email, password, gender))
            mysql.connection.commit()

        #   Retrive userID of newly created user
        cursor.execute("SELECT userID FROM users WHERE email LIKE %s AND pass LIKE %s", (email, password))
        data = cursor.fetchone()
        userID = data[0]

        #   Insert profile picture (if it exists)
        if 'profileImg' in request.files:
            profileImg = request.files['profileImg']
            extension = profileImg.filename.rsplit('.', 1)[1].lower()
            UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'frontend', 'public', 'assets', 'profile-pics')
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            filename = f'user-{userID}.{extension}'
            filename = secure_filename(filename)
            print(filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            profileImg.save(file_path)
            cursor.execute('''
                UPDATE users
                SET profileImg = %s
                WHERE email LIKE %s AND pass LIKE %s
            ''', (filename, email, password))
            mysql.connection.commit()

        #   Insert new therapists information in therapists table
        content = '{"survey" : [{"question": "How was your day?", "questionType": "string"}, {"question": "How much do you weigh in pounds?", "questionType": "number"}, {"question": "Did you eat today", "questionType": "boolean"}, {"question": "How much do you look forward to tomorrow?", "questionType": "range10"}]}'
        defaultText = "Hi, I'm new to MentCare! I'll be updating my information soon!"

        cursor.execute('''
                INSERT INTO therapists (userID, licenseNumber, specializations, acceptingPatients, content, DaysHours, Price, Intro, Education, chargingPrice, isActive)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 20, 1)
                ''', (userID, license, specsArray, 1, content, defaultText, defaultText, defaultText, defaultText))
        mysql.connection.commit()

        #   Retrive therapistID of newly created user
        cursor.execute("SELECT therapistID FROM therapists WHERE userID = %s", (userID,))
        data = cursor.fetchone()
        therapistID = data[0]

        cursor.close()

        response = jsonify({"message" : "User successfully registered", "therapistID" : therapistID, "userID" : userID})
        response.status_code = 200
        response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    except Exception as err:
        return jsonify({"error":  f"{err}"}), 400