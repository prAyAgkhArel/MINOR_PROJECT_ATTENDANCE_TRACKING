from flask import Flask, render_template, request, url_for, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from sqlalchemy.exc import IntegrityError
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
    first_name: Mapped[str] = mapped_column(String(1000), nullable=False)
    last_name: Mapped[str] = mapped_column(String(1000), nullable=False)
    roll_no: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    faculty: Mapped[str] = mapped_column(String(100), nullable=False)
    sem: Mapped[int] = mapped_column(Integer, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)


#create table admin
class Admin(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(1000), nullable=False)

class Ad_student(db.Model):
    uid: Mapped[str] = mapped_column(String(100), primary_key=True)
    campus_rollno:Mapped[str] = mapped_column(String(100), unique=True, nullable = False)
    first_name: Mapped[str] = mapped_column(String(1000), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable = False)
    # face data column

#create table for teacher
class Ad_teacher(db.Model):
    uid: Mapped[str] = mapped_column(String(100), primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    first_name: Mapped[str] = mapped_column(String(1000), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    #face_data column


with app.app_context():
    db.create_all()

    #ADD ADMIN
    if not Admin.query.filter_by(email='hiteshlabh307@gmail.com').first():
        hashed_password = generate_password_hash('@admin123123', method='pbkdf2:sha256', salt_length=8)
        new_admin = Admin(email='hiteshlabh307@gmail.com', password=hashed_password, name='Hitesh')
        db.session.add(new_admin)
        db.session.commit()





@app.route('/')
def home():
    if session.get('logged_in'):
        role = session.get('user_role')
        if role == 'admin':
            return redirect(url_for('admin', name=session.get('user_name')))
        elif role == 'student':
            return redirect(url_for('student', name=session.get('user_name')))
    return render_template("index.html", logged_in=session.get('logged_in', False))

# from your_app import db
# from your_app.models import Student  # Import the Student model




@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        roll_no = request.form.get('rollno')
        sem = request.form.get('sem')
        faculty = request.form.get('faculty')


        # Check if the student already exists by roll number in the Student table
        existing_student = db.session.execute(db.select(Student).where(Student.roll_no == roll_no)).first()
        if existing_student:
            flash("This roll number is already registered. Please log in.", "warning")
            return redirect(url_for('login'))  # Redirect to login page or stay on register page


        # Hash the password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        # Save new student to the database
        with app.app_context():
            new_student = Student(email=email, password=hashed_password, first_name=first_name, last_name=last_name, roll_no=roll_no, sem=sem, faculty=faculty)
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
                session['logged_in'] = True
                session['user_role'] = 'student'
                session['user_name'] = student.first_name
                return redirect(url_for('student', name=student.first_name))
            else:
                flash("Incorrect password.", "danger")
                return redirect(url_for('login'))

        # Check if the admin exists
        admin = db.session.execute(db.select(Admin).where(Admin.email == email)).scalars().first()

        if admin:
            # Verify the password for admin
            if check_password_hash(admin.password, password):
                flash("Admin login successful!", "success")
                session['logged_in'] = True
                session['user_role'] = 'admin'
                session['user_name'] = admin.name
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
    if session.get('user_role') != 'admin':
        flash("You are not authorized to access this page.", "danger")
        return redirect(url_for('home'))
    return render_template('admin_dashboard.html', name=name, logged_in=session.get('logged_in', False))

@app.route('/student/<name>')
def student(name):
    if session.get('user_role') != 'student':
        flash('Your are not authorized to access this page.', category='danger')
        return redirect(url_for('home'))
    return render_template('student_dashboard.html', name=name, logged_in=session.get('logged_in', False))

@app.route('/teacher/<name>')
def teacher(name):
    return render_template('techer_dashboard.html', name=name, logged_in=session.get('logged_in', False))




#ADD Student
@app.route('/admin/<name>/add_student', methods=['GET', 'POST'])
def add_student(name):
    if session.get('user_role', '') != 'admin':
        flash("Unauthorized access!", "danger")
        return redirect(url_for('home'))

    if request.method == 'POST':
        try:
            with app.app_context():
                campus_rollno = request.form.get('campus_rollno')
                nuid = request.form.get('nuid')
                first_name = request.form.get('first_name')
                last_name = request.form.get('last_name')


                existing_student = db.session.execute(db.select(Ad_student).where(Ad_student.campus_rollno==campus_rollno)).scalars().first()

                if existing_student:
                    flash(' This RFID or Roll Number already exists!', "danger")
                    return redirect(url_for('admin', name=session['user_name']))

                new_student = Ad_student(
                    campus_rollno=campus_rollno,
                    uid=str(nuid),
                    first_name = first_name,
                    last_name = last_name
                )

                db.session.add(new_student)
                db.session.commit()
                flash("Student RFID mapping added successfully!", "success")

        except Exception as e:
            db.session.rollback()
            flash(f"Error: {str(e)}", "danger")

        return redirect(url_for('admin', name=session['user_name']))

    return render_template("add_student.html", admin_name=session['user_name'], logged_in=session.get('logged_in', False))



#ADD teacher
@app.route('/admin/<name>/add_teacher', methods=['POST', 'GET'])
def add_teacher(name):
    if session.get('user_role', '') != 'admin':
        flash("Unauthorized access!", "danger")
        return redirect(url_for('home'))

    if request.method == 'POST':
        try:
            with app.app_context():
                nuid = request.form.get('nuid')
                first_name = request.form.get('first_name')
                last_name = request.form.get('last_name')
                email = request.form.get('email')
                password = request.form.get('password')
                #face

                existing_teacher = db.session.execute(db.select(Ad_teacher).where(Ad_teacher.uid == nuid)).scalars().first()
                if existing_teacher:
                    flash(' This RFID already exists!', "danger")
                    return redirect(url_for('admin', name=session['user_name']))

                hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
                new_teacher = Ad_teacher(uid=nuid, first_name=first_name, last_name=last_name, email=email, password=hashed_password)

                db.session.add(new_teacher)
                db.session.commit()
                flash("Teacher RFID  added successfully!", "success")


            return redirect(url_for('admin', name=session['user_name']))

        except Exception as e:
            db.session.rollback()
            flash(f"Error: {str(e)}", "danger")

    return render_template('add_teacher.html', admin_name = session['user_name'], logged_in=session.get('logged_in', False))

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for('home'))




if __name__ == "__main__":
    app.run(debug=True)
