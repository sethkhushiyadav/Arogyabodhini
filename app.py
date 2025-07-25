from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///arogyabodhini.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ---------------------------- Models ---------------------------- #

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.String(10))
    comments = db.Column(db.Text)

# ---------------------------- Routes ---------------------------- #

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['username']  # matches your form input name
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return render_template('register.html')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered. Please login.", "warning")
            return redirect(url_for('login'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful. Please login.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_name'] = user.username
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password.", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Please login first.", "warning")
        return redirect(url_for('login'))
    return render_template('dashboard.html', name=session.get('user_name'))

@app.route('/symptoms', methods=['GET', 'POST'])
def symptoms():
    symptoms = [
        {'name': 'Fever', 'medicine': 'Paracetamol, Crocin', 'remedy': 'Rest and drink lukewarm water', 'diet': 'Stay hydrated with fluids', 'wellness_tip': 'Keep your body temperature monitored'},
        {'name': 'Cold', 'medicine': 'Cetirizine, Levocet', 'remedy': 'Steam inhalation, warm water gargling', 'diet': 'Warm soups and fluids', 'wellness_tip': 'Avoid cold drinks'},
        {'name': 'Cough', 'medicine': 'Benadryl, Ascoril', 'remedy': 'Honey and ginger tea', 'diet': 'Light meals, avoid irritants', 'wellness_tip': 'Avoid smoking and dust'},
        # Add more if you want
    ]

    selected_symptom = None
    if request.method == 'POST':
        selected_name = request.form.get('symptom')
        for symptom in symptoms:
            if symptom['name'] == selected_name:
                selected_symptom = symptom
                break

    return render_template('symptoms.html', symptoms=symptoms, selected_symptom=selected_symptom)

@app.route('/results')
def results():
    symptom = request.args.get('symptom', '').lower()

    medicine_data = {
        'fever': ['Paracetamol', 'Crocin'],
        'cold': ['Cetirizine', 'Levocet'],
        'cough': ['Benadryl', 'Ascoril'],
        'headache': ['Saridon', 'Disprin'],
        'stomach pain': ['Cyclopam', 'Meftal-Spas'],
        'vomiting': ['Domstal', 'Emeset'],
        'motions': ['Eldoper', 'Racecadotril']
    }

    remedies_data = {
        'fever': ['Rest', 'Drink lukewarm water', 'Wet cloth on forehead'],
        'cold': ['Steam inhalation', 'Warm water gargling'],
        'cough': ['Honey + Ginger', 'Tulsi kadha'],
        'headache': ['Massage forehead', 'Sleep in quiet room'],
        'stomach pain': ['Ajwain water', 'Fennel seeds'],
        'vomiting': ['Ginger water', 'Ice chips'],
        'motions': ['ORS', 'Banana + Curd']
    }

    diet_tips = [
        "Stay hydrated with warm water.",
        "Eat light and easily digestible food.",
        "Avoid oily and spicy items.",
        "Include fruits and soups in diet."
    ]

    medicines = medicine_data.get(symptom, ['Please consult a doctor.'])
    remedies = remedies_data.get(symptom, ['No home remedy found.'])

    return render_template('results.html', symptom=symptom.title(), medicines=medicines, remedies=remedies, diet_tips=diet_tips)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        rating = request.form['rating']
        comments = request.form['comments']
        fb = Feedback(rating=rating, comments=comments)
        db.session.add(fb)
        db.session.commit()
        flash("Thank you for your feedback!", "success")
        return redirect(url_for('dashboard'))
    return render_template('feedback.html')

# ---------------------------- Main ---------------------------- #

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # creates tables if not exist
    app.run(debug=True)
