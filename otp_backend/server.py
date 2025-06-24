from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# Configure your email here
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'catmeowwalhalla@gmail.com'
app.config['MAIL_PASSWORD'] = 'vkba vfgd feod outw'  # Use App Password if 2FA is enabled

mail = Mail(app)
otp_store = {}

def generate_otp():
    return str(random.randint(100000, 999999))

@app.route('/send-otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({'message': 'Email required'}), 400

    otp = generate_otp()
    otp_store[email] = otp

    try:
        msg = Message('Your Herbal-i OTP Code',
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[email])
        msg.body = f'Your OTP is: {otp}'
        mail.send(msg)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'message': 'Failed to send email', 'error': str(e)}), 500

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    email = data.get('email')
    otp = data.get('otp')
    if otp_store.get(email) == otp:
        otp_store.pop(email, None)
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Invalid OTP'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000) 