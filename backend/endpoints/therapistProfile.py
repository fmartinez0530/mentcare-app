from flask import request, jsonify, json, Blueprint
from app import mysql
from datetime import datetime

# Define the Blueprint
therapist_routes = Blueprint('therapist_routes', __name__)

# Fetch a specific therapist by UserID
@therapist_routes.route('/therapistProfileInfo', methods=['POST'])
def thersProfInfoFunc():
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
            return jsonify({"error": "Therapist not found"}), 404

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

    return jsonify({"Therapist": therapistInfo, "fives": counts[5], "fours": counts[4], "threes": counts[3], "twos": counts[2], "ones": counts[1]})

@therapist_routes.route('/therapistReviewInfo', methods=['POST'])
def theraReviewFunc():
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

    return jsonify({"reviews": reviews})

@therapist_routes.route('/therapistUpdateInfo', methods=['POST'])
def theraUpdInfoFunc():
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
        return jsonify({"specializations": therapistInfo[0], "education": therapistInfo[1], "aboutMe": therapistInfo[2], "availability": therapistInfo[3], "pricing": therapistInfo[4], "pricingNum": therapistInfo[5] }), 200
    except Exception as err:
        return {"error":  f"{err}"}
    
@therapist_routes.route('/isCurrentTherapist', methods=['POST'])
def isCurrentTheraFunc():
    try:
        urlUserID = int(request.json.get('urlUserId'))
        userID = int(request.json.get("userId"))
        userType = request.json.get("userType")

        if(userType != "Patient"):
            return jsonify({"isCurrentTherapist": 0, "swapable": 0 }), 200
        
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

        return jsonify({"isCurrentTherapist": (therapistID == mainTherapistID), "swapable": (mainTherapistID == None or mainTherapistID == therapistID)  }), 200
    except Exception as err:
        return {"error":  f"{err}"}
    
@therapist_routes.route('/addRemTherapist', methods=['POST'])
def addRemTheraFunc():
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
        
        mysql.connection.commit()
        cursor.execute(f"""
            SELECT mainTherapistID
            FROM patients
            WHERE patients.patientID = {userID}
        """)
        hasThera = cursor.fetchone()[0]
        cursor.close()

        return jsonify({"nowHasTherapist": hasThera }), 200
    except Exception as err:
        return {"error":  f"{err}"}
    
@therapist_routes.route('/leaveReview', methods=['POST'])
def leaveReviewFunc():
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

        return jsonify({"reviewSent": 1 }), 200
    except Exception as err:
        return {"error":  f"{err}", "reviewSent": 0 }