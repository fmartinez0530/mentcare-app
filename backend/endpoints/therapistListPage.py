# endpoints/therapistListPage.py

from flask import request, jsonify, Blueprint, current_app
from flask import send_file
from io import BytesIO
import base64


therapistListData = Blueprint('therapistListData', __name__)

@therapistListData.route('/getTherapists', methods=['GET'])
def get_therapists():
    """
    Fetch All Therapists
    ---
    tags:
      - Therapists
    responses:
      200:
        description: List of therapists retrieved successfully
        schema:
          type: array
          items:
            type: object
            properties:
              userID:
                type: integer
                description: Therapist's user ID
              name:
                type: string
                description: Therapist's name
              gender:
                type: string
                description: Therapist's gender
              profileImg:
                type: string
                description: URL of the therapist's profile image
              specializations:
                type: array
                items:
                  type: string
                description: List of specializations
              intro:
                type: string
                description: Therapist's introduction
              education:
                type: string
                description: Therapist's education details
              availability:
                type: string
                description: Therapist's availability
              price:
                type: string
                description: Charging price of the therapist
              isActive:
                type: boolean
                description: Whether the therapist is currently active
      500:
        description: Internal server error
    """
    try:
        from app import mysql
        cursor = mysql.connection.cursor()

        cursor.execute('''
            SELECT 
                u.userID, 
                u.userName,
                u.gender,
                u.profileImg, 
                t.specializations, 
                t.Intro,
                t.Education,
                t.DaysHours,
                t.chargingPrice,
                t.isActive
            FROM 
                therapists t
            JOIN 
                users u ON t.userID = u.userID
            WHERE 
                u.userType = 'Therapist' AND t.acceptingPatients = 1 AND t.isActive = 1
        ''')
        data = cursor.fetchall()
        cursor.close()

        therapists = []
        for row in data:
            userID, userName, gender, profileImg, specializations, Intro, Education, DaysHours, chargingPrice, isActive = row

            
            if profileImg:
                # profileImg_base64 = base64.b64encode(profileImg).decode('utf-8')
                # profileImg_url = f"data:image/jpeg;base64,{profileImg_base64}"
                profileImg_url = profileImg
            else:
                profileImg_url = None  

            
            if specializations:
                specializations_list = specializations.split(',')
            else:
                specializations_list = []

            therapist = {
                'userID': userID,
                'name': userName,
                'gender' : gender,
                'profileImg': profileImg_url,
                'specializations': specializations_list,
                'intro': Intro,
                'education': Education,
                'availability': DaysHours,
                'price': chargingPrice,
                'isActive': bool(isActive)
            }
            therapists.append(therapist)

        response = jsonify(therapists)
        response.status_code = 200
        response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    except Exception as err:
        return jsonify({"error": str(err)}), 500

@therapistListData.route('/getProfileImage/<int:therapist_id>', methods=['GET'])
def get_profile_image(therapist_id):
    """
    Fetch Therapist Profile Image
    ---
    tags:
      - Therapists
    parameters:
      - name: therapist_id
        in: path
        type: integer
        required: true
        description: ID of the therapist
    responses:
      200:
        description: Profile image retrieved successfully
        content:
          image/jpeg:
            schema:
              type: string
              format: binary
      404:
        description: Profile image not found
      500:
        description: Internal server error
    """
    try:
        from app import mysql
        cursor = mysql.connection.cursor()
        cursor.execute('''
            SELECT u.profileImg
            FROM users u
            JOIN therapists t ON u.userID = t.userID
            WHERE t.therapistID = %s
        ''', (therapist_id,))
        data = cursor.fetchone()
        cursor.close()

        if data and data[0]:
            img_stream = BytesIO(data[0])
            return send_file(img_stream, mimetype='image/jpeg')
        else:
            response = jsonify({"error": "Profile image not found"})
            response.status_code = 404
            response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response
    except Exception as err:
        return jsonify({"error": str(err)}), 500


