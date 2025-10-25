from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from werkzeug.utils import secure_filename

# --- Configuration ---

# Get the base directory (AGROVISION_2)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Create Flask app and specify external template/static paths
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)

# Folder for uploaded images
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file types (you can modify these)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# --- Utility function ---
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# --- ROUTES ---

# 🌱 Intro Page (Root)
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
        # (Later add your login validation logic here)
        return redirect(url_for('intro'))
    return render_template('login.html')


# 🌾 Crop Detection Page
@app.route('/detection', methods=['GET', 'POST'])
def detection():
    if request.method == 'POST':
        file = request.files.get('file')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # --- Replace this with your ML model logic later ---
            # For now, return mock data for frontend display
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
    
    # Render the upload form when page is opened normally
    return render_template('detection.html')



# 📍 Map Page
@app.route('/map')
def map_page():
    return render_template('map.html')


# 🧠 Diseases Info Page
@app.route('/diseases')
def diseases():
    return render_template('diseases.html')


# 👩‍💻 Admin Page
@app.route('/admin')
def admin():
    return render_template('admin.html')


# 🌍 SDG Info Page
@app.route('/sdg')
def sdg():
    return render_template('sdg.html')


# --- Main Entry Point ---
if __name__ == '__main__':
    # Ensure upload folder exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    app.run(debug=True)
