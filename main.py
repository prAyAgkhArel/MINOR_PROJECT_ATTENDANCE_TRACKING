from flask import Flask, render_template, request, url_for, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'

# CREATE DATABASE
class Base(DeclarativeBase):
    pass

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, 'users.db')
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE TABLE
class Student(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(1000), nullable=False)
    roll_no: Mapped[str] = mapped_column(String(100), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template("index.html")


# from your_app import db
# from your_app.models import Student  # Import the Student model


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        roll_no = request.form.get('rollno')

        # Check if the student already exists by roll number in the Student table
        existing_student = Student.query.filter_by(roll_no=roll_no).first()

        if existing_student:
            flash("This roll number is already registered. Please log in.", "warning")
            return redirect(url_for('login'))  # Redirect to login page or stay on register page

        # Hash the password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        # Save new student to the database
        with app.app_context():
            new_student = Student(email=email, password=hashed_password, name=name, roll_no=roll_no)
            db.session.add(new_student)
            db.session.commit()

        flash("Registration successful!", "success")
        return redirect(url_for('home'))

    return render_template("register.html")


# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     if request.method == 'POST':
#         email_from_form = request.form.get('email')
#         password_from_form = request.form.get('password')
#
#         # Get the user from the database by email
#         with app.app_context():
#             #select ther user such that(User.email == email_from_form), and it is stored by user(User object)
#             user = db.session.execute(db.select(Student).where(Student.email == email_from_form)).scalar_one_or_none()
#
#             #user stores none if no user with the email entered is found
#             if user and check_password_hash(user.password, password_from_form):
#                 return render_template('secrets.html', name=user.name)
#             else:
#                 flash("Invalid email or password!", "danger")
#                 return redirect(url_for('login'))
#
#     return render_template("login.html")

@app.route('/login')
def login():
    pass



@app.route('/admin')
def admin():
    return render_template('admin_dashboard.html')

@app.route('/user')
def user():
    return render_template('user_dashboard.html')


@app.route('/logout')
def logout():
    pass


@app.route('/download')
def download():
    pass


if __name__ == "__main__":
    app.run(debug=True)
