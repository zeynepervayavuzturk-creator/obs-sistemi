from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False) # 'admin', 'academician', 'student'
    name_surname = db.Column(db.String(100), nullable=False)
    student_number = db.Column(db.String(20), nullable=True) # Sadece öğrenciler için

    # İlişkiler
    courses_taught = db.relationship('Course', backref='academician', lazy=True)
    enrollments = db.relationship('Enrollment', backref='student', lazy=True)

class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    academician_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    # İlişkiler
    enrollments = db.relationship('Enrollment', backref='course', lazy=True)

class Enrollment(db.Model):
    __tablename__ = 'enrollment'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    
    vize = db.Column(db.Float, default=0.0)
    final = db.Column(db.Float, default=0.0)
    proje = db.Column(db.Float, default=0.0)
    sunum = db.Column(db.Float, default=0.0)
    devamsizlik = db.Column(db.Integer, default=0)
    
    # Bir öğrenci bir derse yalnızca bir kez kayıt olabilir
    __table_args__ = (db.UniqueConstraint('student_id', 'course_id', name='_student_course_uc'),)
