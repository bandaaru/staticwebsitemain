import os
import datetime
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from flask_mail import Mail, Message
import uuid
from werkzeug.utils import secure_filename
# ================= CONFIGURATION =================
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "agrifabrix"
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}
MAX_FILE_SIZE_MB = 5

MY_EMAIL = "nagasaiyaswanthbandaru@gmail.com"
MY_APP_PASSWORD = "eton jytr umcm ahbd" # 16-character Google App Password
RECIPIENT_EMAIL = "nagasaiyaswanthbandaru@gmail.com"
LOGO_URL = "https://agrifabrix.in/l.png" 
# =================================================
app = Flask(__name__)
CORS(app)

# Email Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = MY_EMAIL
app.config['MAIL_PASSWORD'] = MY_APP_PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = MY_EMAIL

mail = Mail(app)

# MongoDB Connection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Collections
contact_collection = db["contact_details"]
newsletter_collection = db["news_letter_subscribers"]
onboarding_collection = db["onboarding_contacts"]
franchise_collection = db["franchise_applications"]
career_collection = db["career_applications"]
otp_collection = db["career_otp_verifications"]

# OTP Generation and Verification for Career Applications
import random

# Helper function to save uploaded files
def save_file(file, folder):
    """Saves an uploaded file to a specific folder and returns the relative path."""
    if not file:
        return None

    # Create absolute path for saving
    target_dir = os.path.join(os.path.dirname(__file__), UPLOAD_FOLDER, folder)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # Generate a unique filename to avoid collisions
    original_filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4().hex}_{original_filename}"
    file_path = os.path.join(target_dir, unique_filename)

    file.save(file_path)
    
    # Return path relative to backend root
    return os.path.join(UPLOAD_FOLDER, folder, unique_filename)

# Helper function to generate HTML email templates
def get_html_template(title, content, cta_text=None, cta_link=None):
    # Brand Color: #0a6b34 (AgriFabriX Green)
    return f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0;">
        <div style="max-width: 600px; margin: 0 auto; border: 1px solid #eee; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
            <div style="background-color: #ffffff; padding: 25px; text-align: center; border-bottom: 2px solid #0a6b34;">
                <img src="{LOGO_URL}" alt="AgriFabriX" style="max-height: 80px; width: auto;">
            </div>
            <div style="padding: 30px; background-color: #ffffff;">
                <h2 style="color: #0a6b34; margin-top: 0; font-size: 20px; border-bottom: 1px solid #f0f0f0; padding-bottom: 10px;">{title}</h2>
                <div style="font-size: 16px;">
                    {content}
                </div>
                {f'<div style="text-align: center; margin-top: 30px;"><a href="{cta_link}" style="background-color: #0a6b34; color: #ffffff; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-weight: bold;">{cta_text}</a></div>' if cta_text and cta_link else ""}
            </div>
            <div style="background-color: #f9f9f9; padding: 15px; text-align: center; font-size: 12px; color: #777;">
                <p style="margin: 5px 0;">&copy; 2026 AgriFabriX. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """

# Async email helper
def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            print(f"Background email failed: {e}")

# Main email function (now returns instantly)
def send_email(subject, recipient, body, is_html=True):
    msg = Message(subject, recipients=[recipient])
    if is_html:
        msg.html = body
    else:
        msg.body = body
    
    # Start sending in the background
    threading.Thread(target=send_async_email, args=(app, msg)).start()
    return True

# Contact Form Route
@app.route("/api/static/Contact", methods=["POST"])
def contact():
    data = request.get_json()
    print(f"DEBUG: Data received: {data}")
    required_fields = ["name", "email", "phone", "message"]

    if not all(field in data and data[field] for field in required_fields):
        return jsonify({"error": "All fields are required."}), 400

    contact_doc = {
        "name": data["name"],
        "email": data["email"],
        "phone": data["phone"],
        "message": data["message"],
        "submitted_at": datetime.datetime.utcnow()
    }

    try:
        contact_collection.insert_one(contact_doc)
        
        # Send mail to admin
        admin_content = f"""
        <p>You have a new contact form submission:</p>
        <table style="width: 100%; border-collapse: collapse;">
            <tr><td style="padding: 8px; border-bottom: 1px solid #eee;"><strong>Name:</strong></td><td style="padding: 8px; border-bottom: 1px solid #eee;">{data['name']}</td></tr>
            <tr><td style="padding: 8px; border-bottom: 1px solid #eee;"><strong>Email:</strong></td><td style="padding: 8px; border-bottom: 1px solid #eee;">{data['email']}</td></tr>
            <tr><td style="padding: 8px; border-bottom: 1px solid #eee;"><strong>Phone:</strong></td><td style="padding: 8px; border-bottom: 1px solid #eee;">{data['phone']}</td></tr>
            <tr><td style="padding: 8px; border-bottom: 1px solid #eee;"><strong>Message:</strong></td><td style="padding: 8px; border-bottom: 1px solid #eee;">{data['message']}</td></tr>
        </table>
        """
        send_email("New Contact Form Submission", RECIPIENT_EMAIL, get_html_template("Contact Inquiry Received", admin_content))

        # Send welcome mail to user
        user_content = f"<p>Hello <strong>{data['name']}</strong>,</p><p>Thank you for reaching out to AgriFabriX. We have received your message and our team will get back to you within 24 hours.</p><p>In the meantime, feel free to explore our digital marketplace for the latest agri-solutions.</p>"
        send_email("Welcome to AgriFabriX", data['email'], get_html_template("Thank You for Contacting Us", user_content, "Explore Marketplace", "https://store.agrifabrix.in/"))

        return jsonify({"message": "Contact form submitted successfully!"}), 201
    except Exception as e:
        return jsonify({"error": f"Failed to submit contact form: {str(e)}"}), 500

# Newsletter Subscription Route
@app.route("/api/static/Subscribe", methods=["POST"])
def subscribe():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email is required."}), 400

    try:
        if newsletter_collection.find_one({"email": email}):
            return jsonify({"message": "You're already subscribed!"}), 200

        newsletter_collection.insert_one({
            "email": email,
            "subscribed_at": datetime.datetime.utcnow()
        })

        # Send mail to admin
        send_email("New Newsletter Subscription", RECIPIENT_EMAIL, get_html_template("New Subscriber Alert", f"<p>New person subscribed to the newsletter: <strong>{email}</strong></p>"))

        # Send welcome mail to user
        sub_content = "<p>Thank you for joining the AgriFabriX community! You're now subscribed to receive our latest updates, insights, and exclusive marketplace offers.</p>"
        send_email("Welcome to the AgriFabriX Newsletter", email, get_html_template("Welcome to the Family!", sub_content, "Explore Marketplace", "https://store.agrifabrix.in/"))

        return jsonify({"message": "Thanks for subscribing!"}), 201
    except Exception as e:
        return jsonify({"error": f"Subscription failed: {str(e)}"}), 500

# Onboarding Form Route
@app.route("/api/static/Onboarding", methods=["POST"])
def onboarding():
    data = request.get_json()
    required_fields = ["contactName", "email", "phone", "orgType", "partnershipReason"]

    if not all(field in data and data[field] for field in required_fields):
        return jsonify({"error": "All fields are required."}), 400

    onboarding_doc = {
        "contact_name": data["contactName"],
        "email": data["email"],
        "phone": data["phone"],
        "organization_type": data["orgType"],
        "partnership_reason": data["partnershipReason"],
        "submitted_at": datetime.datetime.utcnow()
    }

    try:
        onboarding_collection.insert_one(onboarding_doc)

        # Send mail to admin
        admin_content = f"""
        <p>A new partnership request has been submitted:</p>
        <ul>
            <li><strong>Contact Name:</strong> {data['contactName']}</li>
            <li><strong>Email:</strong> {data['email']}</li>
            <li><strong>Phone:</strong> {data['phone']}</li>
            <li><strong>Organization Type:</strong> {data['orgType']}</li>
            <li><strong>Reason:</strong> {data['partnershipReason']}</li>
        </ul>
        """
        send_email("New Onboarding Inquiry", RECIPIENT_EMAIL, get_html_template("New Partnership Request", admin_content))

        # Send welcome mail to user
        onboarding_content = f"<p>Hello <strong>{data['contactName']}</strong>,</p><p>We are excited to receive your partnership request. Our team is currently reviewing your application and will contact you shortly to discuss how we can grow together.</p>"
        send_email("AgriFabriX Partnership Interest", data['email'], get_html_template("Onboarding Request Received", onboarding_content, "Explore Marketplace", "https://store.agrifabrix.in/"))

        return jsonify({"message": "Thank you for your interest! We'll get in touch shortly."}), 201
    except Exception as e:
        return jsonify({"error": f"Submission failed: {str(e)}"}), 500

# Franchise Application Route
@app.route("/api/static/Franchise", methods=["POST"])
def franchise():
    data = request.get_json()
    required_fields = ["name", "email", "phone", "city", "investment"]

    if not all(field in data and data[field] for field in required_fields):
        return jsonify({"error": "Important fields (Name, Email, Phone, City, Investment) are required."}), 400

    franchise_doc = {
        "name": data["name"],
        "email": data["email"],
        "phone": data["phone"],
        "city": data["city"],
        "investment": data["investment"],
        "message": data.get("message", ""),
        "submitted_at": datetime.datetime.utcnow()
    }

    try:
        franchise_collection.insert_one(franchise_doc)
        
        # Send mail to admin
        admin_content = f"""
        <p>A new <strong>Franchise Application</strong> has been received with the following details:</p>
        <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
            <tr><td style="padding: 10px; border: 1px solid #eee; background-color: #f9f9f9; width: 40%;"><strong>Applicant Name</strong></td><td style="padding: 10px; border: 1px solid #eee;">{data['name']}</td></tr>
            <tr><td style="padding: 10px; border: 1px solid #eee; background-color: #f9f9f9;"><strong>Email Address</strong></td><td style="padding: 10px; border: 1px solid #eee;">{data['email']}</td></tr>
            <tr><td style="padding: 10px; border: 1px solid #eee; background-color: #f9f9f9;"><strong>Phone Number</strong></td><td style="padding: 10px; border: 1px solid #eee;">{data['phone']}</td></tr>
            <tr><td style="padding: 10px; border: 1px solid #eee; background-color: #f9f9f9;"><strong>Target City/Location</strong></td><td style="padding: 10px; border: 1px solid #eee;">{data['city']}</td></tr>
            <tr><td style="padding: 10px; border: 1px solid #eee; background-color: #f9f9f9;"><strong>Investment Range</strong></td><td style="padding: 10px; border: 1px solid #eee;">{data['investment']}</td></tr>
            <tr><td style="padding: 10px; border: 1px solid #eee; background-color: #f9f9f9;"><strong>Additional Message</strong></td><td style="padding: 10px; border: 1px solid #eee;">{data.get('message', 'N/A')}</td></tr>
            <tr><td style="padding: 10px; border: 1px solid #eee; background-color: #f9f9f9;"><strong>Submission Time</strong></td><td style="padding: 10px; border: 1px solid #eee;">{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</td></tr>
        </table>
        """
        send_email("New Franchise Application: " + data['name'], RECIPIENT_EMAIL, get_html_template("Franchise Inquiry Alert", admin_content))
 
        # Send welcome/acknowledgment mail to user
        user_content = f"""
        <p>Hello <strong>{data['name']}</strong>,</p>
        <p>Thank you for your interest in partnering with AgriFabriX! We have successfully received your franchise application for the <strong>{data['city']}</strong> location.</p>
        <p>Our franchise development team is currently reviewing your profile and will get in touch with you shortly to discuss the next steps in our selection process.</p>
        <p><strong>Meanwhile, explore our Marketplace</strong> to see the range of innovative solutions we bring to the agricultural sector.</p>
        <p>We are excited about the possibility of growing together!</p>
        """
        send_email("Your AgriFabriX Franchise Application", data['email'], get_html_template("Application Successfully Received", user_content, "Explore Marketplace", "https://store.agrifabrix.in/"))
 
        return jsonify({"message": "Franchise application submitted successfully!"}), 201
    except Exception as e:
        return jsonify({"error": f"Failed to submit franchise application: {str(e)}"}), 500


@app.route("/api/static/Career/SendOTP", methods=["POST"])
def send_career_otp():
    data = request.get_json()
    email = data.get("email")
    
    if not email:
        return jsonify({"error": "Email is required."}), 400
        
    otp = str(random.randint(100000, 999999))
    
    try:
        # Store OTP in DB (upsert for specific email)
        otp_collection.update_one(
            {"email": email},
            {"$set": {
                "otp": otp,
                "created_at": datetime.datetime.utcnow(),
                "verified": False
            }},
            upsert=True
        )
        
        # Send OTP email
        otp_content = f"""
        <p>Your verification code for AgriFabriX Career Application is:</p>
        <div style="text-align: center; margin: 20px 0;">
            <span style="font-size: 32px; font-weight: bold; letter-spacing: 5px; color: #0a6b34; background: #f0fdf4; padding: 10px 20px; border-radius: 5px; border: 1px dashed #0a6b34;">
                {otp}
            </span>
        </div>
        <p>This code will expire in 10 minutes.</p>
        <p>If you didn't request this, please ignore this email.</p>
        """
        send_email("AgriFabriX Verification Code", email, get_html_template("Verify Your Email", otp_content))
        
        return jsonify({"message": "OTP sent successfully!"}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to send OTP: {str(e)}"}), 500

@app.route("/api/static/Career/VerifyOTP", methods=["POST"])
def verify_career_otp():
    data = request.get_json()
    email = data.get("email")
    otp = data.get("otp")
    
    if not email or not otp:
        return jsonify({"error": "Email and OTP are required."}), 400
        
    try:
        otp_data = otp_collection.find_one({"email": email})
        
        if not otp_data:
            return jsonify({"error": "No OTP found for this email."}), 404
            
        # Check expiry (10 minutes)
        if (datetime.datetime.utcnow() - otp_data["created_at"]).total_seconds() > 600:
            return jsonify({"error": "OTP has expired. Please request a new one."}), 400
            
        if otp_data["otp"] == otp:
            otp_collection.update_one({"email": email}, {"$set": {"verified": True}})
            return jsonify({"message": "Email verified successfully!"}), 200
        else:
            return jsonify({"error": "Invalid OTP. Please try again."}), 400
            
    except Exception as e:
        return jsonify({"error": f"Verification failed: {str(e)}"}), 500

# Career Application Route
@app.route("/api/static/Career/Apply", methods=["POST"])
def career_apply():
    print("DEBUG: Career Application received")
    # Since we are receiving files, we use request.form instead of request.get_json()
    data = request.form
    app_type = data.get("application_type") # job / fellowship / internship

    if not app_type:
        return jsonify({"error": "application_type is required"}), 400

    required_fields = ["full_name", "email", "phone"]
    if not all(data.get(field) for field in required_fields):
        return jsonify({"error": "Full Name, Email, and Phone are required."}), 400

    try:
        # ---- Upload Files ----
        print("DEBUG: Processing file uploads...")
        resume_path = save_file(request.files.get("resume"), "resumes")
        id_proof_path = save_file(request.files.get("id_proof"), "id_proofs")
        certificates_path = save_file(request.files.get("certificates"), "certificates")
        print(f"DEBUG: Files saved. Resume: {resume_path}")

        career_doc = {
            "application_type": app_type,
            "full_name": data.get("full_name"),
            "email": data.get("email"),
            "phone": data.get("phone"),
            "city": data.get("city"),
            "state": data.get("state"),
            "country": data.get("country", "India"),
            "education": data.get("education"),
            "experience": data.get("experience"),
            "internship_type": data.get("internship_type"),
            "fellowship_program": data.get("fellowship_program"),
            "linkedin": data.get("linkedin"),
            "portfolio": data.get("portfolio"),
            "reason": data.get("reason"),
            "skills": data.get("skills"),
            "resume": resume_path,
            "id_proof": id_proof_path,
            "certificates": certificates_path,
            "submitted_at": datetime.datetime.utcnow(),
            "status": "pending"
        }

        print("DEBUG: Inserting into MongoDB...")
        career_collection.insert_one(career_doc)
        print("DEBUG: MongoDB insertion successful")

        # ---- Send Email Notification to Admin ----
        admin_content = f"""
        <p>A new <strong>Career Application ({app_type.capitalize()})</strong> has been received:</p>
        <table style="width: 100%; border-collapse: collapse;">
            <tr><td style="padding: 8px; border-bottom: 1px solid #eee;"><strong>Full Name:</strong></td><td style="padding: 8px; border-bottom: 1px solid #eee;">{data.get('full_name')}</td></tr>
            <tr><td style="padding: 8px; border-bottom: 1px solid #eee;"><strong>Email:</strong></td><td style="padding: 8px; border-bottom: 1px solid #eee;">{data.get('email')}</td></tr>
            <tr><td style="padding: 8px; border-bottom: 1px solid #eee;"><strong>Phone:</strong></td><td style="padding: 8px; border-bottom: 1px solid #eee;">{data.get('phone')}</td></tr>
            <tr><td style="padding: 8px; border-bottom: 1px solid #eee;"><strong>Location:</strong></td><td style="padding: 8px; border-bottom: 1px solid #eee;">{data.get('city')}, {data.get('state')}, {data.get('country')}</td></tr>
            <tr><td style="padding: 8px; border-bottom: 1px solid #eee;"><strong>Education:</strong></td><td style="padding: 8px; border-bottom: 1px solid #eee;">{data.get('education')}</td></tr>
            <tr><td style="padding: 8px; border-bottom: 1px solid #eee;"><strong>Experience:</strong></td><td style="padding: 8px; border-bottom: 1px solid #eee;">{data.get('experience')}</td></tr>
        </table>
        <p><strong>Reason for applying:</strong><br>{data.get('reason')}</p>
        """
        
        # We manually use Message to attach files
        msg = Message(f"New Application: {data.get('full_name')} ({app_type.capitalize()})", recipients=[RECIPIENT_EMAIL])
        msg.html = get_html_template(f"New {app_type.capitalize()} Application", admin_content)
        
        # Attach files if they exist
        for path in [resume_path, id_proof_path, certificates_path]:
            if path:
                # Use standard open() for reliability with absolute/dynamic paths
                abs_path = os.path.join(os.path.dirname(__file__), path)
                print(f"DEBUG: Attaching file: {abs_path}")
                if os.path.exists(abs_path):
                    try:
                        with open(abs_path, 'rb') as fp:
                            msg.attach(os.path.basename(path), "application/octet-stream", fp.read())
                    except Exception as fe:
                        print(f"DEBUG: Failed to attach file {path}: {str(fe)}")

        print("DEBUG: Sending emails in background...")
        threading.Thread(target=send_async_email, args=(app, msg)).start()

        # ---- Send Acknowledgment to User ----
        user_content = f"""
        <p>Hello <strong>{data.get('full_name')}</strong>,</p>
        <p>Thank you for applying for a {app_type} position at AgriFabriX! We have received your application and documents.</p>
        <p>Our talent acquisition team will review your profile and get back to you within 3-5 business days if your skills align with our current needs.</p>
        <p>Best regards,<br>AgriFabriX Team</p>
        """
        send_email("Application Received - AgriFabriX", data.get('email'), get_html_template("We Received Your Application", user_content))

        return jsonify({"message": "Application submitted successfully!"}), 201

    except Exception as e:
        print(f"ERROR: {str(e)}")
        return jsonify({"error": f"Failed to submit application: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
