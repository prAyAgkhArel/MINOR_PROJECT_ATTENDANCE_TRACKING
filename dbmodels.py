# from main import db
#
# class Student(db.Model):
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     first_name: Mapped[str] = mapped_column(String(1000), nullable=False)
#     last_name: Mapped[str] = mapped_column(String(1000), nullable=False)
#     roll_no: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
#     faculty: Mapped[str] = mapped_column(String(100), nullable=False)
#     sem: Mapped[int] = mapped_column(Integer, nullable=False)
#     email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
#     password: Mapped[str] = mapped_column(String(100), nullable=False)
#
#
# #create table admin
# class Admin(db.Model):
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
#     password: Mapped[str] = mapped_column(String(100), nullable=False)
#     name: Mapped[str] = mapped_column(String(1000), nullable=False)
#
# class Ad_student(db.Model):
#     uid: Mapped[str] = mapped_column(String(100), primary_key=True)
#     campus_rollno:Mapped[str] = mapped_column(String(100), unique=True, nullable = False)
#     first_name: Mapped[str] = mapped_column(String(1000), nullable=False)
#     last_name: Mapped[str] = mapped_column(String(100), nullable = False)
#     # face data column
#
# #create table for teacher
# class Ad_teacher(db.Model):
#     uid: Mapped[str] = mapped_column(String(100), primary_key=True)
#     email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
#     password: Mapped[str] = mapped_column(String(100), nullable=False)
#     first_name: Mapped[str] = mapped_column(String(1000), nullable=False)
#     last_name: Mapped[str] = mapped_column(String(100), nullable=False)
#     #face_data column
#
#
# class Routine(db.Model):
#     rid: Mapped[str] = mapped_column(String(100), primary_key=True)
#     day: Mapped[str] = mapped_column(String(100), nullable=False)
#     p1: Mapped[str] = mapped_column(String(10), nullable=True)
#     p2: Mapped[str] = mapped_column(String(10), nullable=True)
#     p3: Mapped[str] = mapped_column(String(10), nullable=True)
#     p4: Mapped[str] = mapped_column(String(10), nullable=True)
#     p5: Mapped[str] = mapped_column(String(10), nullable=True)
#     p6: Mapped[str] = mapped_column(String(10), nullable=True)
#     p7: Mapped[str] = mapped_column(String(10), nullable=True)
#     p8: Mapped[str] = mapped_column(String(10), nullable=True)
#
# class Course_details(db.Model):
#     course: Mapped[str] = mapped_column(String(100), nullable=False)
#     courseid: Mapped[str] = mapped_column(String(100), primary_key=True)
#     teacherid: Mapped[str] = mapped_column(String(100), nullable=False)
#     classid: Mapped[str] = mapped_column(String(100), nullable = False)
#
# class StudentAttendance(db.Model):
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     roll_no: Mapped[str] = mapped_column(String(100), nullable=False)
#     courseid_taken: Mapped[str] = mapped_column(String(100), nullable=False)
#     total_attendance: Mapped[int] = mapped_column(Integer, nullable=True)
#
# class TeacherAttendance(db.Model):
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     teacher_uid: Mapped[str] = mapped_column(String(100), nullable=False)
#     course_id: Mapped[str] = mapped_column(String(100), nullable=False)
#     total_attendance: Mapped[int] = mapped_column(Integer, nullable=True)