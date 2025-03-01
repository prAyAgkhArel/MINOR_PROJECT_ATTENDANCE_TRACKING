from flask import Flask, render_template, request, url_for, redirect, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, event
import os
from collections import defaultdict
from datetime import datetime, timedelta
from timestamps import timestamps, period_mapping

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'

# CREATE DATABASE
class Base(DeclarativeBase):
    pass

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, 'users.db')
db = SQLAlchemy(model_class=Base)
db.init_app(app)

#CREATE TABLE student
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


class Routine(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rid: Mapped[str] = mapped_column(String(100), nullable=False)
    day: Mapped[str] = mapped_column(String(100), nullable=False)
    p1: Mapped[str] = mapped_column(String(10), nullable=True)
    p2: Mapped[str] = mapped_column(String(10), nullable=True)
    p3: Mapped[str] = mapped_column(String(10), nullable=True)
    p4: Mapped[str] = mapped_column(String(10), nullable=True)
    p5: Mapped[str] = mapped_column(String(10), nullable=True)
    p6: Mapped[str] = mapped_column(String(10), nullable=True)
    p7: Mapped[str] = mapped_column(String(10), nullable=True)
    p8: Mapped[str] = mapped_column(String(10), nullable=True)

class Course_details(db.Model):
    course: Mapped[str] = mapped_column(String(100), nullable=False)
    courseid: Mapped[str] = mapped_column(String(100), primary_key=True)
    teacherid: Mapped[str] = mapped_column(String(100), nullable=False)
    classid: Mapped[str] = mapped_column(String(100), nullable = False)

class StudentAttendance(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    roll_no: Mapped[str] = mapped_column(String(100), nullable=False)
    courseid_taken: Mapped[str] = mapped_column(String(100), nullable=False)
    total_attendance: Mapped[int] = mapped_column(Integer, nullable=True)

class TeacherAttendance(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    teacher_uid: Mapped[str] = mapped_column(String(100), nullable=False)
    course_id: Mapped[str] = mapped_column(String(100), nullable=False)
    total_attendance: Mapped[int] = mapped_column(Integer, nullable=True)


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
            print("Session name:", session.get('user_name'))
            print("Session roll_no:", session.get('roll_no'))
            return redirect(url_for('student', name=session.get('user_name')))
        elif role == 'teacher':
            return redirect(url_for('teacher', name=session.get('user_name')))


    return render_template("index.html", logged_in=session.get('logged_in', False))




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
                session['roll_no'] = student.roll_no
                print(f"This is fetched from table: {student.roll_no}")
                print(f"session['roll_no']{session['roll_no']}")
                return redirect(url_for('student', name=student.first_name))
            else:
                flash("Incorrect password.", "danger")
                return redirect(url_for('login'))

        teacher = db.session.execute(db.select(Ad_teacher).where(Ad_teacher.email == email)).scalars().first()
        if teacher:
            # Verify the password for student
            if check_password_hash(teacher.password, password):
                flash("Login successful!", "success")
                session['logged_in'] = True
                session['user_role'] = 'teacher'
                session['user_name'] = teacher.first_name
                return redirect(url_for('teacher', name=teacher.first_name))
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
    # Fetch the student based on the first name
    student = db.session.execute(db.select(Student).where(Student.first_name == name)).scalars().first()

    if student is None:
        flash('Student not found.', category='danger')
        return redirect(url_for('home'))

    print("This is student: ", student.first_name)

    # Check if the user role is 'student'
    if session.get('user_role') != 'student':
        flash('You are not authorized to access this page.', category='danger')
        return redirect(url_for('home'))

    # Create the composite key (faculty + semester)
    composite_key = student.faculty + str(
        student.sem)

    # Fetch routine based on the composite key using a LIKE query
    routines = db.session.execute(db.select(Routine).where(Routine.rid.like(f'{composite_key}%'))).scalars().all()
    print("here is routine", routines)

    if routines is None:
        flash('Routine not found.', category='danger')
        return redirect(url_for('home'))

    attendance_details = StudentAttendance.query.filter_by(roll_no= student.roll_no).all()
    #is a attendance_details for the student logged in

    return render_template('student_dashboard.html',
                           attendance_details = attendance_details,
                           # name=name,
                           # roll_no=student.roll_no,
                           # course=routines[0].p1,
                           # routines=routines,
                           # routine=routine,  # Pass the routine data to the template
                           logged_in=session.get('logged_in', False))


@app.route('/teacher/<name>')
def teacher(name):
    if session.get('user_role') != 'teacher':
        flash('Your are not authorized to access this page.', category='danger')
        return redirect(url_for('home'))

    teacher = Ad_teacher.query.filter_by(first_name = name).first()
    uid = teacher.uid

    attendance_details = TeacherAttendance.query.filter_by(teacher_uid = uid).all()
    return render_template('teacher_dashboard.html', name=name, attendance_details=attendance_details, logged_in=session.get('logged_in', False))

#ADD teacher



# -------------------------------ROUTINE Management Section START---------------------------------------


@app.route('/admin/<name>/manage_routine')
def manage_routine(name):
    return render_template('update_or_preview.html', logged_in=session.get('logged_in', False))


# def time_to_24hr_format(time_str):
#     return datetime.strptime(time_str, '%I:%M %p').strftime('%H:%M')


# def time_to_minutes(time_str):
#     try:
#         dt = datetime.strptime(time_str, '%I:%M %p')
#         return dt.hour * 60 + dt.minute
#     except:
#         return None


@app.route('/admin/<name>/update_or_preview', methods=['POST', 'GET'])
def update_or_preview(name):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        faculty = request.form.get('faculty')
        sem = request.form.get('sem')
        action = request.form.get('action')

        if not faculty or not sem:
            flash('Please select both Faculty and Semester', 'error')
            return redirect(url_for('update_or_preview', name=name))

        if action == 'update':
            session['current_faculty'] = faculty
            session['current_sem'] = sem
            flash(f'Update mode activated for {faculty} semester {sem}', 'info')
            return redirect(url_for('update', name=name, faculty=faculty, sem=sem))

    return render_template('update_or_preview.html',
                           logged_in=session.get('logged_in', False))


@app.route('/admin/<name>/update_routine/<faculty>/<sem>', methods=['POST', 'GET'])
def update(name, faculty, sem):
    from_timestamps = ['01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00']
    to_timestamps = ['02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00']

    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        days = request.form.getlist('day[]')
        from_times = request.form.getlist('from_time[]')
        to_times = request.form.getlist('to_time[]')
        courses = request.form.getlist('course[]')
        teachers = request.form.getlist('teacher[]')

        # Existing time validation logic
        day_intervals = defaultdict(list)
        conflicts = []

        def parse_time(time_str):
            return datetime.strptime(time_str, '%H:%M')


        for i, (day, f_time, t_time) in enumerate(zip(days, from_times, to_times)):
            if not all([day, f_time, t_time]):
                continue

            try:
                start = parse_time(f_time)
                end = parse_time(t_time)
                if start >= end:
                    conflicts.append(i + 1)
                    continue
            except:
                conflicts.append(i + 1)
                continue

            for (existing_start, existing_end) in day_intervals[day]:
                if not (end <= existing_start or start >= existing_end):
                    conflicts.append(i + 1)
                    break

            day_intervals[day].append((start, end))

        if conflicts:
            flash(f'Time slot conflict in rows: {", ".join(map(str, set(conflicts)))}', 'error')
            return redirect(url_for('update', name=name, faculty=faculty, sem=sem))

        # New logic for consolidated entries
        entries_by_rid = {}
        try:
            for n in range(len(days)):
                day = days[n]
                from_time = from_times[n]
                course = courses[n]
                teacher = teachers[n]

                rid = f"{faculty}{sem}{day}"


                period = period_mapping.get(from_time)
                if not period:
                    flash(f'Invalid time slot in row {n + 1}', 'error')
                    continue

                # Get or create routine entry
                routine_entry = entries_by_rid.get(rid)
                if not routine_entry:
                    routine_entry = Routine.query.filter_by(rid=rid).first()
                    if not routine_entry:
                        routine_entry = Routine(rid=rid, day=day)
                    entries_by_rid[rid] = routine_entry

                # Update the period
                setattr(routine_entry, period, f"{course} ({teacher})" if teacher else course)

            # Save all changes
            for entry in entries_by_rid.values():
                db.session.merge(entry)
            db.session.commit()
            flash('Routine updated successfully!', 'success')

        except Exception as e:
            db.session.rollback()
            flash(f'Error updating routine: {str(e)}', 'error')

        return redirect(url_for('update', name=name, faculty=faculty, sem=sem))

    # GET request handling
    classid = faculty + sem
    courses = Course_details.query.filter_by(classid=classid).all()
    teachers = []
    for course in courses:
        teacher = Ad_teacher.query.filter_by(uid=course.teacherid).first()
        teachers.append(teacher)

    return render_template('update_routine.html',
                           name=name,
                           faculty=faculty,
                           sem=sem,
                           from_times=from_timestamps,
                           to_times=to_timestamps,
                           courses=courses,
                           teachers=teachers)


#_________________________________Routine Management SEction END_____________________________________




#---------------------------Course Management Section START------------------------------------------

@app.route('/admin/<name>/add_course', methods=['POST', 'GET'])
def add_course(name):
    if request.method == 'POST':
        course_name = request.form.get('course_name')
        first_name = request.form.get('teacher_firstname')
        last_name = request.form.get('teacher_lastname')
        class_id = request.form.get('class_id')

        # Check if teacher exists in Teacher table
        teacher = Ad_teacher.query.filter_by(first_name=first_name, last_name=last_name).first()

        if not teacher:
            flash("Teacher not found. Please register the teacher first.", 'danger')
            return redirect(url_for('add_course', name=name))

        # Generate Course ID automatically
        last_course = Course_details.query.order_by(Course_details.courseid.desc()).first()
        if last_course:
            last_number = int(last_course.courseid[1:])
            course_id = f"C{last_number + 1}"
        else:
            course_id = "C1"


        course= Course_details.query.filter_by(course = course_name, teacherid=teacher.uid, classid=class_id).first()
        print(course)
        #print(f"this is from course_details table matching from the form:{ course.teacherid, course.classid}")
        if course:
            flash('Course for the teacher and faculty already exists.', 'warning')
            return redirect(url_for('add_course', name=name))
        # Save to Database
        new_course = Course_details(
            course=course_name,
            courseid=course_id,
            teacherid=teacher.uid,
            classid=class_id
        )

        db.session.add(new_course)
        db.session.commit()
        flash("Course added successfully!", 'success')

        # setting up teacher attendance table

        # Fetch all courses assigned to this teacher from Course_details
        courses = db.session.execute(
            db.select(Course_details.course).where(Course_details.teacherid == teacher.uid)).scalars().all()

        # Update teacher_attendance table for each course
        if courses:
            for course_id in courses:
                new_attendance_entry = TeacherAttendance(teacher_uid=teacher.uid, course_id=course_name, total_attendance=0)
                db.session.add(new_attendance_entry)

            db.session.commit()
            flash("Teacher added and attendance table updated successfully!", "success")

        return redirect(url_for('admin', name=name))

    return render_template('add_course.html', admin_name=name)

@app.route('/admin/courses/<classid>/<course_name>', methods=['POST', 'GET'])
def course_details(classid, course_name):

    if session.get('user_role', '') != 'admin':
        flash("Unauthorized access!", "danger")
        return redirect(url_for('home'))

    course = Course_details.query.filter_by(  # Fixed
        course=course_name,
        classid=classid
    ).first()

    if request.method == "POST":
        first_name = request.form.get('teacher_firstname')
        last_name = request.form.get('teacher_lastname')
        teacher = Ad_teacher.query.filter_by(first_name=first_name, last_name=last_name).first()

        if teacher:
            course.teacherid = teacher.uid
            db.session.commit()
            flash("Teacher assigned successfully!", "success")

        else:
            flash('Teacher not found', "danger")

    teacher = Ad_teacher.query.filter_by(  # Fixed
        uid=course.teacherid
    ).first()

    if not teacher:
        flash("Teacher not found! Add teacher fo", "warning")
        return redirect(url_for('home'))

    print("course", course)
    return render_template('update_course.html',
                           admin_name="name1",
                           # courses= courses,
                           classid=classid,
                           course_name = course_name,
                           first_name = teacher.first_name,
                           last_name = teacher.last_name

                           )

@app.route('/admin/courses', methods=['GET'])
def get_courses():

    # if 'user_name' not in session or session['user_name'] != name:
    #     flash("Unauthorized Access", "danger")
    #     return redirect(url_for('login'))
    if session.get('user_role', '') != 'admin':
        flash("Unauthorized access!", "danger")
        return redirect(url_for('home'))

    courses = Course_details.query.all()  # This fetches all the rows
    course_list = []  # Empty list to store dictionaries

    # Loop through each course and append dictionary
    for course in courses:
        course_list.append({
            'course': course.course,
            'classid': course.classid,
            'teacherid': course.teacherid
        })

    # course_id = [course[0] for course in Course_details.query.with_entities(Course_details.courseid).distinct().all()]
    print("courses: ",course_list)

    return render_template('course_list.html', course_list=course_list)

#-----------------------Course Management Section END-------------------------------------------------


# @app.route('/get_class_ids', methods=['GET'])
# def get_class_ids():
#     course_name = request.args.get('course_name')
#     class_ids = [
#         c.classid for c in Course_details.query.filter_by(course=course_name).all()  # Fixed
#     ] if course_name else []
#     return jsonify({"class_ids": class_ids})


# @app.route('/get_teacher', methods=['POST'])
# def get_teacher():
#     data = request.get_json()
#     course = Course_details.query.filter_by(  # Fixed
#         course=data.get('course_name'),
#         classid=data.get('class_id')
#     ).first()
#
#     if not course:
#         return jsonify({"firstname": "", "lastname": ""})
#
#     teacher = Ad_teacher.query.get(course.teacherid)
#     return jsonify({
#         "firstname": teacher.first_name if teacher else "",
#         "lastname": teacher.last_name if teacher else ""
#     })


#---------------------TEACHER MANAGEMENT SECTION START---------------------------------------------
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

                # Check if RFID already exists
                existing_teacher = db.session.execute(db.select(Ad_teacher).where(Ad_teacher.uid == nuid)).scalars().first()
                if existing_teacher:
                    flash('This RFID already exists!', "danger")
                    return redirect(url_for('admin', name=session['user_name']))

                # Hash password
                hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

                # Add teacher to Ad_teacher table
                new_teacher = Ad_teacher(uid=nuid, first_name=first_name, last_name=last_name, email=email, password=hashed_password)
                db.session.add(new_teacher)
                db.session.commit()
                flash('Teacher Added Successfully', 'success')



            return redirect(url_for('admin', name=session['user_name']))

        except Exception as e:
            db.session.rollback()
            flash(f"Error: {str(e)}", "danger")

    return render_template('add_teacher.html', admin_name=session['user_name'], logged_in=session.get('logged_in', False))



@app.route('/admin/teachers')
def get_teachers():

    if session.get('user_role', '') != 'admin':
        flash("Unauthorized access!", "danger")
        return redirect(url_for('home'))

    teachers = Ad_teacher.query.all()  # This fetches all the rows
    teacher_list = []  # Empty list to store dictionaries

    # Loop through each course and append dictionary
    for teacher in teachers:
        teacher_list.append({
            'first_name': teacher.first_name,
            'last_name': teacher.last_name,
            'email': teacher.email,
            'uid': teacher.uid
        })

    # course_id = [course[0] for course in Course_details.query.with_entities(Course_details.courseid).distinct().all()]
    print("courses: ", teacher_list)

    return render_template('all_teachers.html',
                           teacher_list=teacher_list
                           )


#--------------------------------TEACHER MANAGEMENT SECTION END-------------------------------




#----------------------STUDENT MANAGEMENT SECTION START-------------------------------------------

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

               #------------------- # updating in student attendance table------------------------------

                # Fetch the last added student from Ad_student table
                student = Ad_student.query.filter_by(campus_rollno=campus_rollno).first()
                if student:
                    campus_rollno = student.campus_rollno
                    print(
                        f"Processing student: {student.first_name} {student.last_name}, Campus Roll No: {campus_rollno}")

                    # Fetch faculty and sem from Student table
                    stu = Student.query.filter_by(roll_no=campus_rollno).first()
                    if stu:
                        faculty = stu.faculty
                        sem = stu.sem

                        if faculty is not None and sem is not None:
                            routine_id = str(faculty) + str(sem)
                            print(f"Routine ID: {routine_id}")
                        else:
                            print("Faculty or Semester is missing")
                            return redirect(url_for('admin', name=session['user_name']))
                        print(type(faculty))
                        print(type(sem))


                        # Fetch routine rows that match the routine_id prefix
                        routines = db.session.execute(
                            db.select(Routine).where(Routine.rid.like(f'{routine_id}%'))).scalars().all()
                        unique_courses = set()

                        # Loop through all the routine rows and collect unique course values
                        if routines:
                            for routine in routines:
                                for column in Routine.__table__.columns:
                                    if column.name.startswith("p"):
                                        course = getattr(routine, column.name)
                                        if course and '(' in course:
                                            course = course.split('(')[0]  # Extract course name before bracket
                                            unique_courses.add(course)

                            # Insert all unique courses into StudentAttendance table with total attendance initialized to 0
                            for course in unique_courses:
                                new_attendance = StudentAttendance(roll_no=campus_rollno, courseid_taken=course,
                                                                   total_attendance=0)
                                db.session.add(new_attendance)
                            db.session.commit()
                            print(f"Attendance records added for {student.first_name} {student.last_name}")
                        else:
                            print("No routine found for this student")
                    else:
                        print("Student details not found in Student table")
                else:
                    print("No student found in Ad_student table")


        except Exception as e:
            db.session.rollback()
            flash(f"Error: {str(e)}", "danger")

        return redirect(url_for('admin', name=session['user_name']))

    return render_template("add_student.html", admin_name=session['user_name'], logged_in=session.get('logged_in', False))
@app.route('/admin/students')
def get_students():

    if session.get('user_role', '') != 'admin':
        flash("Unauthorized access!", "danger")
        return redirect(url_for('home'))

    students = Ad_student.query.all()  # This fetches all the rows
    student_list = []  # Empty list to store dictionaries

    # Loop through each course and append dictionary
    for student in students:
        student_list.append({
            'first_name': student.first_name,
            'last_name': student.last_name,
            'campus_rollno': student.campus_rollno,
            'uid': student.uid
        })

    # course_id = [course[0] for course in Course_details.query.with_entities(Course_details.courseid).distinct().all()]
    print("courses: ", student_list)

    return render_template('all_students.html',
                           student_list=student_list
                           )
#---------------------------STUDENT MANAGEMENT SECTION END---------------------------------



# @app.route('/admin/<name>/update_course', methods=['POST', 'GET'])
# def update_course(name):
#     if 'user_name' not in session or session['user_name'] != name:
#         flash("Unauthorized Access", "danger")
#         return redirect(url_for('login'))
#
#     courses = courses = [course[0] for course in Course_details.query.with_entities(Course_details.course).distinct().all()]
#     classid = [classid[0] for classid in
#                          Course_details.query.with_entities(Course_details.classid).distinct().all()]
#
#     if request.method == 'POST':
#         course_name = request.form.get('course_name')
#         class_id = request.form.get('class_id')
#         teacher_firstname = request.form.get('teacher_firstname').strip()
#         teacher_lastname = request.form.get('teacher_lastname').strip()
#
#         # Find existing course-class pair
#         course = Course_details.query.filter_by(
#             course=course_name,
#             classid=class_id
#         ).first()
#
#         if not course:
#             flash("Course-class combination not found!", "warning")
#             return redirect(url_for('update_course', name=name))
#
#         # Find teacher
#         teacher = Ad_teacher.query.filter_by(
#             first_name=teacher_firstname,
#             last_name=teacher_lastname
#         ).first()
#
#         if not teacher:
#             flash("Teacher not found in system!", "danger")
#             return redirect(url_for('update_course', name=name))
#
#         # Update course
#         course.teacherid = teacher.uid
#         db.session.commit()
#         flash("Course teacher updated successfully!", "success")
#         return redirect(url_for('admin', name=name))
#
#     return render_template('update_course.html',
#                            admin_name=name,
#                            courses= courses,
#                            classid=classid
#                            )


@app.route('/admin/<name>/update_holiday', methods=['POST', 'GET'])
def update_holiday(name):
    return render_template('update_holiday.html', logged_in=session.get('logged_in', False))


@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for('home'))
# -----------------------------RFID INTEGRATION------------------------


# def is_time_in_range(start, end):
#     # Convert 12-hour time strings to datetime objects
#     start = datetime.strptime(start, "%I:%M %p")
#     end = datetime.strptime(end, "%I:%M %p")
#     now = datetime.now().strftime("%I:%M %p")

def is_time_in_range(start, end):
    now = datetime.now().time()  # Keep 'now' as time only
    start = datetime.strptime(start, "%H:%M").time()  # Convert start to time
    end = datetime.strptime(end, "%H:%M").time()  # Convert end to time

    return start <= now <= end



@app.route('/api/rfid', methods=['POST'])
def receive_rfid():
    data = request.json
    uid = data.get("uid")  # Extract the 'uid' field from the JSON data

    if uid:
        print(f"Received UID: {uid}")

        # Fetch UID from Database
        student = Ad_student.query.filter_by(uid=uid).first()
        teacher = Ad_teacher.query.filter_by(uid=uid).first()

        if student:
            print(f'Update attendance of {student.first_name}')
            campus_rollno = student.campus_rollno

            # Query Student table
            stu = Student.query.filter_by(roll_no=campus_rollno).first()
            if not stu:
                return jsonify({"message": "Student Not Found in Student Table", "status": "failed"})

            faculty = stu.faculty
            sem = stu.sem
            routine_id = str(faculty) + str(sem)

            # Fetch Routine
            routines = Routine.query.filter(Routine.rid.like(f'{routine_id}%')).all()

            today = datetime.now().strftime('%A')
            todays_routine = Routine.query.filter(Routine.rid.like(f'{routine_id}%'), Routine.day == today).first()
            print("Today's Routine p1:", todays_routine.p1)
            print("Today's Routine p2:", todays_routine.p2)

            if todays_routine:
                for index in range(len(timestamps) - 1):
                    if is_time_in_range(timestamps[index], timestamps[index + 1]):
                        ongoing_period = [period for start, period in period_mapping.items() if start == timestamps[index]][0]
                        ongoing_course = getattr(todays_routine, ongoing_period)

                        if ongoing_course:
                            ongoing_course_cleaned = ongoing_course.split('(')[0] if '(' in ongoing_course else ongoing_course
                            print(f"ongoing course for student: {ongoing_course_cleaned}")

                            # Attendance Update
                            attendance_row = StudentAttendance.query.filter_by(roll_no=campus_rollno, courseid_taken=ongoing_course_cleaned).first()
                            if attendance_row:
                                attendance_row.total_attendance += 1
                                db.session.commit()
                                print(f"Attendance Updated for {student.first_name} in {ongoing_course_cleaned} :{attendance_row.total_attendance}")
                            else:
                                print("Attendance Row Not Found")
                        else:
                            print("No Course Found for Ongoing Period")
                        break
                else:
                    print("No Period Now!")
            else:
                print("Routine Not Found")

            return jsonify({"message": "UID Matched", "status": "success"})

        elif teacher:
            print(teacher.first_name)
            # update teacher attendance
            # query routine table for day = today and time= time.now() and get all the courses going on
            # query Course_details with all the coursenames that are fetched
            # and among them select the row that has (teacherid = uid)
            # from that row get the value of attribute 'classid'
            # classid = something + a number something= faculty and number = sem
            #  so get course , classid and teacherid
            # update the total_attendance in TeacherAttendance for that (teacher_uid = uid, course_id = course)
            print(f"Teacher detected: {teacher.first_name}")

            # Get today's day
            today = datetime.now().strftime('%A')
            print("Today is:", today)

            # Get ongoing periods
            for index in range(len(timestamps) - 1):
                if is_time_in_range(timestamps[index], timestamps[index + 1]):
                    ongoing_period = [period for start, period in period_mapping.items() if start == timestamps[index]][
                        0]
                    print("Ongoing Period:", ongoing_period)

                    # Fetch All Routines where Teacher is Assigned
                    ongoing_routines = Routine.query.filter_by(day=today).all()

                    # Check which routine matches the teacher's course
                    for routine in ongoing_routines:
                        course_name = getattr(routine, ongoing_period)
                        if course_name:
                            course_cleaned = course_name.split('(')[0][:-1] if '(' in course_name else course_name

                            # Match Teacher's Course from Course_details
                            teacher_course = Course_details.query.filter_by(course=course_cleaned,
                                                                            teacherid=teacher.uid).first()


                            if teacher_course:
                                print(f"Teacher {teacher.first_name} is taking {course_cleaned}")

                                # Update TeacherAttendance
                                attendance_row = TeacherAttendance.query.filter_by(teacher_uid=teacher.uid,
                                                                                   course_id=course_cleaned).first()
                                if attendance_row:
                                    attendance_row.total_attendance += 1
                                    db.session.commit()
                                    print(f"Attendance Updated for {teacher.first_name} in {course_cleaned}")
                                else:
                                    print("No Attendance Row Found, Creating New Row")
                                    new_attendance = TeacherAttendance(teacher_uid=teacher.uid,
                                                                       course_id=course_cleaned, total_attendance=1)
                                    db.session.add(new_attendance)
                                    db.session.commit()
                                return jsonify({"message": "Teacher Attendance Updated", "status": "success"})
                            else:
                                print(f"No Course Found for {teacher.first_name} in {course_cleaned}")



                    break
            else:
                print("No Period Now for Teacher")

            return jsonify({"message": "UID Matched", "status": "success"})
        else:
            return jsonify({"message": "UID Not Found", "status": "failed"})

    return jsonify({"message": "Invalid Request", "status": "error"})




if __name__ == "__main__":
    app.run(debug=True,
            host='192.168.1.78',
            port=5000)

