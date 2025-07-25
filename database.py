from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

# Flask app and DB initialization
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///arogyabodhini.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Symptom model
class Symptom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    medicine = db.Column(db.Text, nullable=False)
    remedy = db.Column(db.Text, nullable=False)
    diet = db.Column(db.Text, nullable=False)
    wellness_tip = db.Column(db.Text, nullable=False)

# Initialize and populate the DB
def init_db():
    with app.app_context():
        db.create_all()

        # Add a sample user if none exist
        if not User.query.first():
            test_user = User(
                username="testuser",
                email="test@example.com",
                password=generate_password_hash("testpassword")
            )
            db.session.add(test_user)

        # Add sample symptoms if none exist
        if not Symptom.query.first():
            symptoms_data = [
                {
                    "name": "Fever",
                    "medicine": "Paracetamol, Ibuprofen",
                    "remedy": "Drink lukewarm water, take rest",
                    "diet": "Light food, fruits, drink water",
                    "wellness_tip": "Monitor temperature regularly"
                },
                {
                    "name": "Cold",
                    "medicine": "Cetirizine, Steam inhalation",
                    "remedy": "Steam 2-3 times a day",
                    "diet": "Hot soups, turmeric milk",
                    "wellness_tip": "Avoid cold drinks and rest"
                },
                {
                    "name": "Cough",
                    "medicine": "Cough syrup, Warm honey",
                    "remedy": "Honey + ginger mixture",
                    "diet": "Warm fluids, avoid fried food",
                    "wellness_tip": "Gargle with salt water"
                },
                {
                    "name": "Headache",
                    "medicine": "Aspirin, Rest and hydration",
                    "remedy": "Cold compress, sleep",
                    "diet": "Avoid caffeine, stay hydrated",
                    "wellness_tip": "Limit screen time"
                },
                {
                    "name": "Stomach Pain",
                    "medicine": "Antacid, ORS solution",
                    "remedy": "Use heating pad, avoid spicy food",
                    "diet": "Bananas, rice, applesauce, toast (BRAT diet)",
                    "wellness_tip": "Eat in small portions"
                },
                {
                    "name": "Vomiting",
                    "medicine": "Ondansetron, Hydration therapy",
                    "remedy": "Ginger tea, lemon water",
                    "diet": "ORS, clear liquids, dry crackers",
                    "wellness_tip": "Rest and hydrate well"
                },
                {
                    "name": "Motions",
                    "medicine": "ORS, Probiotics",
                    "remedy": "Curd with rice, avoid dairy",
                    "diet": "Plain rice, bananas, curd",
                    "wellness_tip": "Drink safe water, stay hygienic"
                }
            ]

            for data in symptoms_data:
                symptom = Symptom(
                    name=data["name"],
                    medicine=data["medicine"],
                    remedy=data["remedy"],
                    diet=data["diet"],
                    wellness_tip=data["wellness_tip"]
                )
                db.session.add(symptom)

        db.session.commit()
        print("✅ Database initialized successfully!")

if __name__ == "__main__":
    init_db()
