from flask import request, jsonify, json, Blueprint
from app import mysql
import time

landingPageData = Blueprint('landingPageData', __name__)

@landingPageData.route('/sendTestimonial', methods=['POST'])
def send_testimonials():
    try:
        user_id = request.json.get('userId')
        content = request.json.get('content')

        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO testimonials(userID, content, datePosted) VALUES (%s, %s, %s)''', (user_id, content, time.strftime('%Y-%m-%d %H:%M:%S')))

        mysql.connection.commit()
        cursor.close()

        return jsonify({"message": "Success"}), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500

# Fetch testimonials
@landingPageData.route('/getTestimonials', methods=['GET'])
def get_testimonials():
    try:
        print("haha")
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT testimonials.testimonialID, testimonials.content, users.profileImg, users.userName
            FROM testimonials INNER JOIN users ON users.userID = testimonials.userID
            ORDER BY RAND() LIMIT 5; """)
        testimonials = cursor.fetchall()
        cursor.close()

        formatted_testimonials = [
            {
                "id": row[0],
                "content": row[1],
                "img": row[2],
                "username": row[3]
            } for row in testimonials
        ]

        return jsonify(formatted_testimonials)
    except Exception as err:
        return jsonify({"error": str(err)}), 500


# Fetch mission statement, FAQs, and Contact Us data
@landingPageData.route('/companydata', methods=['GET'])
def get_data():
    try:
        cursor = mysql.connection.cursor()
        
        # Fetch mission statement
        cursor.execute("SELECT statement, phone, email FROM mission LIMIT 1")
        mission_data = cursor.fetchone()

        # Fetch FAQs
        cursor.execute("SELECT question, answer FROM company")
        faqs = cursor.fetchall()
        
        cursor.close()

        # Format data
        response = {
            "Mission": mission_data[0] if mission_data else "No mission statement available.",
            "Contact": {
                "Phone": mission_data[1] if mission_data else "No phone available.",
                "Email": mission_data[2] if mission_data else "No email available."
            },
            "FAQs": [{"Question": row[0], "Answer": row[1]} for row in faqs]
        }
        return jsonify(response)
    except Exception as err:
        return {"error": f"{err}"}
