from flask import request, jsonify, Blueprint
from app import mysql
import time
from flasgger import SwaggerView

landingPageData = Blueprint('landingPageData', __name__)

@landingPageData.route('/sendTestimonial', methods=['POST'])
def send_testimonials():
    """
    Submit a new testimonial
    ---
    tags:
      - Testimonials
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - userId
            - content
          properties:
            userId:
              type: integer
              description: User ID of the person submitting the testimonial.
            content:
              type: string
              description: Content of the testimonial.
    responses:
      200:
        description: Testimonial successfully added.
      500:
        description: Server error.
    """
    try:
        user_id = request.json.get('userId')
        content = request.json.get('content')

        cursor = mysql.connection.cursor()
        cursor.execute('''
            INSERT INTO testimonials(userID, content, datePosted) 
            VALUES (%s, %s, %s)
        ''', (user_id, content, time.strftime('%Y-%m-%d %H:%M:%S')))

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


@landingPageData.route('/getTestimonials', methods=['GET'])
def get_testimonials():
    """
    Fetch testimonials
    ---
    tags:
      - Testimonials
    responses:
      200:
        description: List of testimonials.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: Testimonial ID.
              content:
                type: string
                description: Content of the testimonial.
              img:
                type: string
                description: Profile image of the user.
              username:
                type: string
                description: Username of the user.
      500:
        description: Server error.
    """
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT testimonials.testimonialID, testimonials.content, users.profileImg, users.userName
            FROM testimonials
            INNER JOIN users ON users.userID = testimonials.userID
            ORDER BY testimonialID DESC LIMIT 5;
        """)
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

        response = jsonify(formatted_testimonials)
        response.status_code = 200
        response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    except Exception as err:
        return jsonify({"error": str(err)}), 500


@landingPageData.route('/companydata', methods=['GET'])
def get_data():
    """
    Fetch company data (Mission, FAQs, and Contact Information)
    ---
    tags:
      - Company Data
    responses:
      200:
        description: Company data retrieved successfully.
        schema:
          type: object
          properties:
            Mission:
              type: string
              description: Company mission statement.
            Contact:
              type: object
              properties:
                Phone:
                  type: string
                  description: Contact phone number.
                Email:
                  type: string
                  description: Contact email address.
            FAQs:
              type: array
              items:
                type: object
                properties:
                  Question:
                    type: string
                    description: FAQ question.
                  Answer:
                    type: string
                    description: FAQ answer.
      500:
        description: Server error.
    """
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
        responseData = {
            "Mission": mission_data[0] if mission_data else "No mission statement available.",
            "Contact": {
                "Phone": mission_data[1] if mission_data else "No phone available.",
                "Email": mission_data[2] if mission_data else "No email available."
            },
            "FAQs": [{"Question": row[0], "Answer": row[1]} for row in faqs]
        }

        response = jsonify(responseData)
        response.status_code = 200
        response.headers['Access-Control-Allow-Origin'] = 'https://mentcare-frontend.onrender.com'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    except Exception as err:
        return {"error": f"{err}"}
