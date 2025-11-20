from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import os
from werkzeug.utils import secure_filename
from functools import wraps

# --- Configuration ---

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)

app.secret_key = 'your_secret_key_here'

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


# --- Utility function ---
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# --- 🌐 Language Support ---
@app.context_processor
def inject_language():
    return {'lang': session.get('lang', 'en')}


@app.route('/set_language/<lang>')
def set_language(lang):
    session['lang'] = lang
    return redirect(request.referrer or url_for('intro'))


# --- Authentication Helper ---
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


# --- ROUTES ---

# 🌱 Intro Page
@app.route('/')
def intro():
    return render_template('intro.html')


# 🏠 Home Page
@app.route('/home')
def home():
    return render_template('index.html')


# 🔐 Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if email and password:
            session['user'] = email
            return redirect(url_for('detection'))

        return render_template('login.html', error='Invalid credentials.')
    
    return render_template('login.html')


# ✍️ Signup Route
@app.route('/signup', methods=['POST'])
def signup():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return render_template('login.html', error='Please provide valid details.')

    session['user'] = email
    return redirect(url_for('detection'))


# 🚪 Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('intro'))


# 🌾 Crop Detection Page
@app.route('/detection', methods=['GET', 'POST'])
@app.route('/detection_page', methods=['GET', 'POST'])
def detection():
    if request.method == 'POST':
        file = request.files.get('file')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            result = {
                "disease": "Leaf Blight",
                "causes": "Fungal infection due to excessive humidity.",
                "prevention": "Use resistant varieties and ensure good air circulation.",
                "treatment": "Apply Mancozeb fungicide and remove infected leaves.",
                "soil": "Loamy soil with good drainage.",
                "water": "Moderate irrigation; avoid waterlogging.",
                "temperature": "25–30°C ideal for healthy growth.",
                "soil_score": 80,
                "water_score": 65,
                "temp_score": 90
            }

            return jsonify(result)
        else:
            return jsonify({'error': 'Invalid file format!'})

    return render_template('detection.html')


# 📍 Map Page
@app.route('/map')
def map_page():
    return render_template('map.html')


# 🧠 Diseases Page (FIXED: correct endpoint)
@app.route('/diseases')
def diseases_info():
    return render_template('diseases.html')


# 👩‍💻 Admin Page
@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')


# 🌍 SDG Page
@app.route('/sdg')
def sdg():
    return render_template('sdg.html')


# --- MAIN ---
if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    app.run(debug=True)
