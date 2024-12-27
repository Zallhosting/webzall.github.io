from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# Routes
@app.route('/')
def home():
    return '''
    <html>
        <head>
            <title>Phone Tracking</title>
            <style>
                body {
                    background-color: black;
                    color: red;
                    font-family: Arial, sans-serif;
                }
                .content {
                    text-align: center;
                    margin-top: 100px;
                }
                .content h1 {
                    font-size: 50px;
                }
                .content p {
                    font-size: 20px;
                }
            </style>
        </head>
        <body>
            <div class="content">
                <h1>Phone Tracking App</h1>
                <p>By ZallKaltim</p>
            </div>
        </body>
    </html>
    '''

@app.route('/track-location', methods=['POST'])
def track_location():
    data = request.get_json()
    location = {
        'latitude': data.get('latitude'),
        'longitude': data.get('longitude')
    }
    # Log action
    user_id = data.get('user_id')
    if user_id:
        log_action(user_id, 'track-location')
    return jsonify({'message': 'Location tracked successfully!', 'location': location})

@app.route('/send-alert', methods=['POST'])
def send_alert():
    data = request.get_json()
    user_id = data.get('user_id')
    if user_id:
        log_action(user_id, 'send-alert')
    return jsonify({'message': 'Security alert sent!'})

@app.route('/lock-device', methods=['POST'])
def lock_device():
    data = request.get_json()
    user_id = data.get('user_id')
    if user_id:
        log_action(user_id, 'lock-device')
    return jsonify({'message': 'Device locked remotely!'})

@app.route('/wipe-data', methods=['POST'])
def wipe_data():
    data = request.get_json()
    user_id = data.get('user_id')
    if user_id:
        log_action(user_id, 'wipe-data')
    return jsonify({'message': 'Device data wiped remotely!'})

@app.route('/link-phone', methods=['POST'])
def link_phone():
    data = request.get_json()
    phone_number = data.get('phone_number')
    if phone_number:
        user = User(phone_number=phone_number)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'Phone number linked successfully!', 'user_id': user.id})
    return jsonify({'message': 'Invalid phone number!'}), 400

@app.route('/get-logs', methods=['GET'])
def get_logs():
    user_id = request.args.get('user_id')
    if user_id:
        logs = Log.query.filter_by(user_id=user_id).all()
        return jsonify({'logs': [{'action': log.action, 'timestamp': log.timestamp} for log in logs]})
    return jsonify({'message': 'User ID required!'}), 400

# Utility Function
def log_action(user_id, action):
    log = Log(user_id=user_id, action=action)
    db.session.add(log)
    db.session.commit()

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
