from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
import os

app = Flask(__name__)
app.secret_key = 'some_secret_key'


# Create  Database
class Base(DeclarativeBase):
    pass


# Replace username, password, localhost, and dbname with your actual MySQL credentials and database name.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'mysql://username:password@localhost/database_name')


# Create the extension
db = SQLAlchemy(model_class=Base)
# Initialise the app with the extension
db.init_app(app)


###########
# # Create the database
# mysql -u username -p -e "CREATE DATABASE dbname;"
#
# # Run the Flask application to create the tables
# python main.py
###########


# user model for database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    profession = db.Column(db.String(100), nullable=False)
    photo = db.Column(db.String(100))
    description = db.Column(db.Text)


with app.app_context():
    db.create_all()


def allowed_file(filename):
    ALLOWED_EXTENSION = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        profession = request.form['profession']
        photo = request.files['photo']
        description = request.form['description']

        # Validate the file type and size
        if photo and allowed_file(photo.filename):
            # Save the photo to the uploads folder
            photo.save('uploads/' + photo.filename)

            # Create a new user instance
            new_user = User(name=name, email=email, phone=phone, profession=profession, photo=photo.filename,
                            description=description)

            # Add the user to the database
            db.session.add(new_user)
            db.session.commit()

            return 'Form submitted successfully!'
        else:
            flash('Invalid file type or size. Please upload a JPEG or PNG image.')
            return render_template('index.html')
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
