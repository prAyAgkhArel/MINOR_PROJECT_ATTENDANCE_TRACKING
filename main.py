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

# CREATE TABLE student
class Student(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(1000), nullable=False)
    roll_no: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

#create table teacher
class Teacher(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(1000), nullable=False)

#create table admin
class Admin(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(1000), nullable=False)





with app.app_context():
    db.create_all()

    # ADD ADMIN
    # hashed_password = generate_password_hash('@admin123123', method='pbkdf2:sha256', salt_length=8)
    # new_admin = Admin(email='hiteshlabh307@gmail.com', password=hashed_password, name='Hitesh')
    # db.session.add(new_admin)
    # db.session.commit()


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
        existing_student = db.session.execute(db.select(Student).where(Student.roll_no == roll_no)).first()
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


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if the student exists
        student = db.session.execute(db.select(Student).where(Student.email == email)).scalars().first()

        if student:
            # Verify the password for student
            if check_password_hash(student.password, password):
                flash("Login successful!", "success")
                return redirect(url_for('student', name=student.name))
            else:
                flash("Incorrect password.", "danger")
                return redirect(url_for('login'))

        # Check if the admin exists
        admin = db.session.execute(db.select(Admin).where(Admin.email == email)).scalars().first()

        if admin:
            # Verify the password for admin
            if check_password_hash(admin.password, password):
                flash("Admin login successful!", "success")
                return redirect(url_for('admin', name=admin.name))
            else:
                flash("Incorrect password.", "danger")
                return redirect(url_for('login'))

        # If no user found with the given email
        flash("No user found with this email address.", "danger")
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/admin/<name>')
def admin(name):
    return render_template('admin_dashboard.html', name=name)

@app.route('/student/<name>')
def student(name):
    return render_template('user_dashboard.html', name=name)

@app.route('/teacher/<name>')
def teacher(name):
    return render_template('techer_dashboard.html', name=name)

@app.route('/logout')
def logout():
    pass


@app.route('/download')
def download():
    pass


if __name__ == "__main__":
    app.run(debug=True)
