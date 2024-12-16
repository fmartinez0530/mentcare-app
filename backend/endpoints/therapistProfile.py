from flask import request, jsonify, json, Blueprint
from app import mysql
import app
from datetime import datetime

# Define the Blueprint
therapist_routes = Blueprint('therapist_routes', __name__)

# Fetch a specific therapist by UserID
@therapist_routes.route('/therapistProfileInfo', methods=['POST'])
def thersProfInfoFunc():
    """
    Fetch Therapist Profile Information
    ---
    tags:
      - Therapist
    parameters:
      - name: urlUserId
        in: body
        type: integer
        required: true
        description: The User ID of the therapist
    responses:
      200:
        description: Therapist profile information retrieved successfully
        schema:
          type: object
          properties:
            Therapist:
              type: object
              description: Therapist details
            fives:
              type: integer
              description: Number of 5-star reviews
            fours:
              type: integer
              description: Number of 4-star reviews
            threes:
              type: integer
              description: Number of 3-star reviews
            twos:
              type: integer
              description: Number of 2-star reviews
            ones:
              type: integer
              description: Number of 1-star reviews
      404:
        description: Therapist not found
      500:
        description: Internal server error
    """
    try:
        urlUserID = request.json.get('urlUserId')

        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT users.userName, therapists.Intro, therapists.Education, 
                   therapists.DaysHours, therapists.Price, 
                   therapists.specializations, users.profileImg, therapists.acceptingPatients, therapists.chargingPrice
            FROM users
            JOIN therapists ON users.userID = therapists.userID
            WHERE users.userID = %s AND users.userType = 'Therapist'
        """, (urlUserID,))
        therapistInfo = cursor.fetchone()

        if not therapistInfo:
            response = jsonify({"error": "Therapist not found"})
            response.status_code = 404
            response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response

        cursor.execute(f"""
            SELECT therapistID
            FROM therapists
            WHERE userID = {urlUserID}
        """)
        therapistID = cursor.fetchone()[0]

        cursor.execute(f"""
            SELECT reviews.stars
            FROM reviews
            WHERE reviews.therapistID = {therapistID}
        """)
        reviews = cursor.fetchall()

        counts = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
        for review in reviews:
            counts[review[0]] = counts[review[0]] + 1

    except Exception as err:
        print(f"Error: {err}")
        return jsonify({"error": err}), 500
    finally:
        cursor.close()

    response = jsonify({"Therapist": therapistInfo, "fives": counts[5], "fours": counts[4], "threes": counts[3], "twos": counts[2], "ones": counts[1]})
    response.status_code = 200
    response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@therapist_routes.route('/therapistReviewInfo', methods=['POST'])
def theraReviewFunc():
    """
    Fetch Therapist Reviews
    ---
    tags:
      - Therapist
    parameters:
      - name: urlUserId
        in: body
        type: integer
        required: true
        description: The User ID of the therapist
      - name: page
        in: body
        type: integer
        required: true
        description: Page number for pagination
    responses:
      200:
        description: Reviews retrieved successfully
        schema:
          type: object
          properties:
            reviews:
              type: array
              items:
                type: object
                properties:
                  content:
                    type: string
                    description: Review content
                  stars:
                    type: integer
                    description: Star rating
                  dateDone:
                    type: string
                    description: Date of the review
                  userName:
                    type: string
                    description: Patient's username
                  profileImg:
                    type: string
                    description: Patient's profile image URL
      500:
        description: Internal server error
    """
    try:
        urlUserID = request.json.get('urlUserId')
        page = request.json.get('page')

        cursor = mysql.connection.cursor()

        cursor.execute(f"""
            SELECT therapistID
            FROM therapists
            WHERE userID = {urlUserID}
        """)
        therapistID = cursor.fetchone()[0]

        cursor.execute(f"""
            SELECT reviews.content, reviews.stars, reviews.dateDone, users.userName, users.profileImg
            FROM reviews, patients, users
            WHERE reviews.therapistID = {therapistID}
            AND reviews.patientID = patients.patientID
            AND patients.userID = users.userID
            LIMIT 4
            OFFSET {4*(int(page) - 1)}
        """)
        reviews = cursor.fetchall()


    except Exception as err:
        return jsonify({"error": err}), 500
    finally:
        cursor.close()

    response = jsonify({"reviews": reviews})
    response.status_code = 200
    response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@therapist_routes.route('/therapistUpdateInfo', methods=['POST'])
def theraUpdInfoFunc():
    """
    Update Therapist Information
    ---
    tags:
      - Therapist
    parameters:
      - name: urlUserId
        in: body
        type: integer
        required: true
        description: The User ID of the therapist
      - name: specializationsArr
        in: body
        type: array
        items:
          type: string
        required: false
        description: Array of specializations
      - name: educationUpd
        in: body
        type: string
        required: false
        description: Updated education details
      - name: aboutMeUpd
        in: body
        type: string
        required: false
        description: Updated about me section
      - name: availabilityUpd
        in: body
        type: string
        required: false
        description: Updated availability
      - name: pricingUpd
        in: body
        type: string
        required: false
        description: Updated pricing details
      - name: pricingUpdNum
        in: body
        type: number
        required: false
        description: Updated pricing amount
    responses:
      200:
        description: Therapist information updated successfully
      500:
        description: Internal server error
    """
    try:
        urlUserID = int(request.json.get('urlUserId'))
        newSpecializations = request.json.get('specializationsArr')
        newEducation = request.json.get('educationUpd')
        newAboutMe = request.json.get('aboutMeUpd')
        newAvailability = request.json.get('availabilityUpd')
        newPricing = request.json.get('pricingUpd')
        newPricingNum = request.json.get('pricingUpdNum')

        print(0)
        cursor = mysql.connection.cursor()

        if(len(newSpecializations) <= 1):
            print(1.1)
            newSpecializations = ''
            cursor.execute("""
                UPDATE therapists
                SET specializations = '', Education = %s, Intro = %s, DaysHours = %s, Price = %s, chargingPrice = %s
                WHERE userID = %s
            """, (newEducation, newAboutMe, newAvailability, newPricing, newPricingNum, urlUserID, ))
            print(1.2)
        else:
            print(2.1)
            if(newSpecializations[0] == ','):
                newSpecializations = newSpecializations[1:]
            cursor.execute("""
                UPDATE therapists
                SET specializations = %s, Education = %s, Intro = %s, DaysHours = %s, Price = %s, chargingPrice = %s
                WHERE userID = %s
            """, (newSpecializations, newEducation, newAboutMe, newAvailability, newPricing, newPricingNum, urlUserID, ))
            print(2.2)

        print(3)
        mysql.connection.commit()
        print(4)

        cursor.execute("""
            SELECT specializations, Education, Intro, DaysHours, Price, chargingPrice
            FROM therapists
            WHERE userID = %s
        """, (urlUserID, ))
        therapistInfo = cursor.fetchone()
        cursor.close()
        print(5)

        print(therapistInfo)
        response = jsonify({"specializations": therapistInfo[0], "education": therapistInfo[1], "aboutMe": therapistInfo[2], "availability": therapistInfo[3], "pricing": therapistInfo[4], "pricingNum": therapistInfo[5] })
        response.status_code = 200
        response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    except Exception as err:
        return {"error":  f"{err}"}
    
@therapist_routes.route('/isCurrentTherapist', methods=['POST'])
def isCurrentTheraFunc():
    """
    Check if Patient's Current Therapist
    ---
    tags:
      - Therapist
    parameters:
      - name: urlUserId
        in: body
        type: integer
        required: true
        description: Therapist's User ID
      - name: userId
        in: body
        type: integer
        required: true
        description: Patient's User ID
      - name: userType
        in: body
        type: string
        required: true
        description: User type (Patient)
    responses:
      200:
        description: Successfully checked current therapist status
        schema:
          type: object
          properties:
            isCurrentTherapist:
              type: boolean
              description: Whether the therapist is the patient's current therapist
            swapable:
              type: boolean
              description: Whether the therapist is swappable
      500:
        description: Internal server error
    """
    try:
        urlUserID = int(request.json.get('urlUserId'))
        userID = int(request.json.get("userId"))
        userType = request.json.get("userType")

        if(userType != "Patient"):
            response = jsonify({"isCurrentTherapist": 0, "swapable": 0 })
            response.status_code = 200
            response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response
        
        cursor = mysql.connection.cursor()

        print("urlUserId:", urlUserID)
        print("userID:", userID)
        print("userType:", userType)
        cursor.execute(f"""
            SELECT mainTherapistID
            FROM patients
            WHERE patientID = {userID}
        """)
        mainTherapistID = cursor.fetchone()[0]
        cursor.execute(f"""
            SELECT therapistID
            FROM therapists
            WHERE userID = {urlUserID}
        """)
        therapistID = cursor.fetchone()[0]
        cursor.close()

        response = jsonify({"isCurrentTherapist": (therapistID == mainTherapistID), "swapable": (mainTherapistID == None or mainTherapistID == therapistID)  })
        response.status_code = 200
        response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    except Exception as err:
        return {"error":  f"{err}"}
    
@therapist_routes.route('/addRemTherapist', methods=['POST'])
def addRemTheraFunc():
    """
    Add or Remove a Therapist
    ---
    tags:
      - Therapist
    parameters:
      - name: urlUserId
        in: body
        type: integer
        required: true
        description: Therapist's User ID
      - name: userId
        in: body
        type: integer
        required: true
        description: Patient's User ID
      - name: currentlyTherapist
        in: body
        type: boolean
        required: true
        description: Whether the therapist is currently assigned to the patient
    responses:
      200:
        description: Successfully added or removed the therapist
        schema:
          type: object
          properties:
            nowHasTherapist:
              type: boolean
              description: Whether the patient now has a therapist
      500:
        description: Internal server error
    """
    try:
        urlUserID = int(request.json.get('urlUserId'))
        userID = int(request.json.get("userId"))
        currentlyTherapist = request.json.get("currentlyTherapist")

        cursor = mysql.connection.cursor()
        cursor.execute(f"""
            SELECT therapistID
            FROM therapists
            WHERE userID = {urlUserID}
        """)
        therapistID = cursor.fetchone()[0]

        cursor.execute(f"""
            SELECT userName
            FROM users, patients
            WHERE users.userID = patients.userID AND patients.patientID = {userID}
        """)
        patientName = cursor.fetchone()[0]

        if(currentlyTherapist):
            cursor.execute(f"""
                UPDATE patients
                SET mainTherapistID = NULL
                WHERE patientID = {userID}
            """)
            cursor.execute(f"""
                UPDATE therapistPatientsList
                SET status = 'Inactive'
                WHERE patientID = {userID} AND therapistID = {therapistID}
            """)

            cursor.execute(f'''
                INSERT INTO notifications(userID, message, redirectLocation)
                VALUES ({urlUserID}, "Patient {patientName} has removed themself from your service.", "/dashboard")''')
            if str(urlUserID) in app.socketsNavbar:
                app.socketio.emit("update-navbar", room=app.socketsNavbar[str(urlUserID)])

        else:
            cursor.execute(f"""
                UPDATE patients
                SET mainTherapistID = {therapistID}
                WHERE patientID = {userID}
            """)

            cursor.execute(f"""
                SELECT pairingID
                FROM therapistPatientsList
                WHERE therapistID = {therapistID} AND patientID = {userID}
            """)
            chatsExist = cursor.fetchone()

            if(chatsExist == None):
                chatsJson = '{"chats": []}' 
                cursor.execute(f"""
                    INSERT INTO chats (patientID, therapistID, content)
                    VALUES ({userID}, {therapistID}, '{chatsJson}')
                """)

                cursor.execute(f"""
                    INSERT INTO therapistPatientsList (therapistID, patientID, status, chatStatus, requestStatus)
                    VALUES ({therapistID}, {userID}, 'Active', 'Inactive', 'Inactive')
                """)
            else:
                # TODO: update so if you re-add an old therapist, status becomes active
                cursor.execute(f"""
                    UPDATE therapistPatientsList
                    SET status = 'Active'
                    WHERE patientID = {userID} AND therapistID = {therapistID}
                """)


            cursor.execute(f'''
                INSERT INTO notifications(userID, message, redirectLocation)
                VALUES ({urlUserID}, "Patient {patientName} has added themself from your service.", "/dashboard")''')
            if str(urlUserID) in app.socketsNavbar:
                app.socketio.emit("update-navbar", room=app.socketsNavbar[str(urlUserID)])

        mysql.connection.commit()
        cursor.execute(f"""
            SELECT mainTherapistID
            FROM patients
            WHERE patients.patientID = {userID}
        """)
        hasThera = cursor.fetchone()[0]
        cursor.close()

        response = jsonify({"nowHasTherapist": hasThera })
        response.status_code = 200
        response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    except Exception as err:
        return {"error":  f"{err}"}
    
@therapist_routes.route('/leaveReview', methods=['POST'])
def leaveReviewFunc():
    """
    Leave a Review for Therapist
    ---
    tags:
      - Therapist
    parameters:
      - name: urlUserId
        in: body
        type: integer
        required: true
        description: Therapist's User ID
      - name: userId
        in: body
        type: integer
        required: true
        description: Patient's User ID
      - name: review
        in: body
        type: string
        required: true
        description: Review content
      - name: stars
        in: body
        type: integer
        required: true
        description: Star rating
    responses:
      200:
        description: Review successfully submitted
        schema:
          type: object
          properties:
            reviewSent:
              type: boolean
              description: Whether the review was successfully sent
      500:
        description: Internal server error
    """
    try:
        urlUserID = int(request.json.get('urlUserId'))
        userID = int(request.json.get("userId"))
        review = request.json.get("review")
        stars = int(request.json.get("stars"))

        cursor = mysql.connection.cursor()

        cursor.execute(f"""
            SELECT therapistID
            FROM therapists
            WHERE userID = {urlUserID}
        """)
        therapistID = cursor.fetchone()[0]

        cursor.execute(f"""
            INSERT INTO reviews (therapistID, patientID, content, stars, dateDone)
            VALUES ({therapistID}, {userID}, '{review}', {stars}, '{datetime.today().date()}')
        """)
        
        mysql.connection.commit()
        cursor.close()

        response = jsonify({"reviewSent": 1 })
        response.status_code = 200
        response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    except Exception as err:
        return {"error":  f"{err}", "reviewSent": 0 }