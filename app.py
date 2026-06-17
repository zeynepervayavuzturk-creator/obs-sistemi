from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Course, Enrollment

app = Flask(__name__)
app.config['SECRET_KEY'] = 'obs-secret-key-1234'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///obs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_initial_data():
    hashed_password = generate_password_hash('123456', method='pbkdf2:sha256')
    
    # Admin
    if not User.query.filter_by(username='admin').first():
        db.session.add(User(username='admin', password=hashed_password, role='admin', name_surname='Sistem Yöneticisi'))
        
    # Akademisyenler
    if not User.query.filter_by(username='hoca1').first():
        db.session.add(User(username='hoca1', password=hashed_password, role='academician', name_surname='Prof. Dr. Ahmet Yılmaz'))
    if not User.query.filter_by(username='hoca2').first():
        db.session.add(User(username='hoca2', password=hashed_password, role='academician', name_surname='Doç. Dr. Ayşe Demir'))

    # Öğrenciler
    if not User.query.filter_by(username='ogrenci1').first():
        db.session.add(User(username='ogrenci1', password=hashed_password, role='student', name_surname='Ali Kaya', student_number='2023001'))
    if not User.query.filter_by(username='ogrenci2').first():
        db.session.add(User(username='ogrenci2', password=hashed_password, role='student', name_surname='Zeynep Çelik', student_number='2023002'))
        
    db.session.commit()
    
    # Dersler
    hoca1 = User.query.filter_by(username='hoca1').first()
    hoca2 = User.query.filter_by(username='hoca2').first()
    
    if not Course.query.filter_by(name='Matematik 101').first():
        db.session.add(Course(name='Matematik 101', academician_id=hoca1.id if hoca1 else None))
    if not Course.query.filter_by(name='Fizik 101').first():
        db.session.add(Course(name='Fizik 101', academician_id=hoca2.id if hoca2 else None))
        
    db.session.commit()
    
    # Kayıtlar
    ogr1 = User.query.filter_by(username='ogrenci1').first()
    ogr2 = User.query.filter_by(username='ogrenci2').first()
    mat101 = Course.query.filter_by(name='Matematik 101').first()
    fiz101 = Course.query.filter_by(name='Fizik 101').first()
    
    if ogr1 and mat101 and not Enrollment.query.filter_by(student_id=ogr1.id, course_id=mat101.id).first():
        db.session.add(Enrollment(student_id=ogr1.id, course_id=mat101.id, vize=85, final=90))
    if ogr1 and fiz101 and not Enrollment.query.filter_by(student_id=ogr1.id, course_id=fiz101.id).first():
        db.session.add(Enrollment(student_id=ogr1.id, course_id=fiz101.id, vize=70, final=65, devamsizlik=2))
    if ogr2 and mat101 and not Enrollment.query.filter_by(student_id=ogr2.id, course_id=mat101.id).first():
        db.session.add(Enrollment(student_id=ogr2.id, course_id=mat101.id, vize=55, proje=80))

    db.session.commit()

with app.app_context():
    db.drop_all() # Schema degistigi icin tablolari sifirliyoruz
    db.create_all()
    create_initial_data()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif current_user.role == 'academician':
            return redirect(url_for('academician_dashboard'))
        else:
            return redirect(url_for('student_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user.role == 'academician':
                return redirect(url_for('academician_dashboard'))
            else:
                return redirect(url_for('student_dashboard'))
        else:
            flash('Kullanıcı adı veya şifre hatalı.', 'danger')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# --- ADMIN ROUTES ---
@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return "Yetkisiz Erişim", 403
    users = User.query.all()
    courses = Course.query.all()
    academicians = User.query.filter_by(role='academician').all()
    students = User.query.filter_by(role='student').all()
    return render_template('admin_dashboard.html', users=users, courses=courses, academicians=academicians, students=students)

@app.route('/admin/user/add', methods=['POST'])
@login_required
def add_user():
    if current_user.role != 'admin':
        return "Yetkisiz Erişim", 403
    username = request.form.get('username')
    name_surname = request.form.get('name_surname')
    role = request.form.get('role')
    student_number = request.form.get('student_number')
    
    if User.query.filter_by(username=username).first():
        flash('Bu kullanıcı adı zaten mevcut.', 'danger')
        return redirect(url_for('admin_dashboard'))
        
    hashed_password = generate_password_hash('123456', method='pbkdf2:sha256')
    new_user = User(
        username=username, 
        name_surname=name_surname, 
        role=role, 
        password=hashed_password,
        student_number=student_number if role == 'student' else None
    )
    db.session.add(new_user)
    db.session.commit()
    flash(f'{role.capitalize()} {name_surname} başarıyla eklendi. Varsayılan Şifre: 123456', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/user/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        return "Yetkisiz Erişim", 403
    
    user_to_delete = User.query.get_or_404(user_id)
    
    if user_to_delete.id == current_user.id:
        flash('Kendi hesabınızı silemezsiniz.', 'danger')
        return redirect(url_for('admin_dashboard'))
        
    # İlişkili kayıtları temizle
    if user_to_delete.role == 'student':
        Enrollment.query.filter_by(student_id=user_to_delete.id).delete()
    elif user_to_delete.role == 'academician':
        courses = Course.query.filter_by(academician_id=user_to_delete.id).all()
        for c in courses:
            c.academician_id = None
            
    db.session.delete(user_to_delete)
    db.session.commit()
    flash(f'Kullanıcı ({user_to_delete.username}) başarıyla silindi.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/course/add', methods=['POST'])
@login_required
def add_course():
    if current_user.role != 'admin':
        return "Yetkisiz Erişim", 403
    name = request.form.get('name')
    academician_id = request.form.get('academician_id')
    
    try:
        academician_id = int(academician_id) if academician_id else None
        new_course = Course(name=name, academician_id=academician_id)
        db.session.add(new_course)
        db.session.commit()
        flash('Ders başarıyla eklendi.', 'success')
    except Exception as e:
        flash('Hata oluştu.', 'danger')
        
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/enroll', methods=['POST'])
@login_required
def enroll_student():
    if current_user.role != 'admin':
        return "Yetkisiz Erişim", 403
    student_id = int(request.form.get('student_id'))
    course_id = int(request.form.get('course_id'))
    
    existing = Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first()
    if existing:
        flash('Öğrenci zaten bu derse kayıtlı.', 'danger')
    else:
        enrollment = Enrollment(student_id=student_id, course_id=course_id)
        db.session.add(enrollment)
        db.session.commit()
        flash('Öğrenci derse kaydedildi.', 'success')
    return redirect(url_for('admin_dashboard'))

# --- ACADEMICIAN ROUTES ---
@app.route('/academician_dashboard')
@login_required
def academician_dashboard():
    if current_user.role != 'academician':
        return "Yetkisiz Erişim", 403
    # Sorumlu olduğu dersleri çek
    courses = Course.query.filter_by(academician_id=current_user.id).all()
    return render_template('academician_dashboard.html', courses=courses)

@app.route('/update_grade/<int:enrollment_id>', methods=['POST'])
@login_required
def update_grade(enrollment_id):
    if current_user.role != 'academician':
        return "Yetkisiz Erişim", 403
    enrollment = Enrollment.query.get_or_404(enrollment_id)
    if enrollment.course.academician_id != current_user.id:
        return "Yetkisiz Erişim", 403
        
    vize = request.form.get('vize')
    final = request.form.get('final')
    proje = request.form.get('proje')
    sunum = request.form.get('sunum')
    devamsizlik = request.form.get('devamsizlik')
    
    enrollment.vize = float(vize) if vize else 0.0
    enrollment.final = float(final) if final else 0.0
    enrollment.proje = float(proje) if proje else 0.0
    enrollment.sunum = float(sunum) if sunum else 0.0
    enrollment.devamsizlik = int(devamsizlik) if devamsizlik else 0
    
    db.session.commit()
    flash('Notlar ve devamsızlık güncellendi.', 'success')
    return redirect(url_for('academician_dashboard'))

@app.route('/take_attendance/<int:course_id>', methods=['POST'])
@login_required
def take_attendance(course_id):
    if current_user.role != 'academician':
        return "Yetkisiz Erişim", 403
    course = Course.query.get_or_404(course_id)
    if course.academician_id != current_user.id:
        return "Yetkisiz Erişim", 403
        
    # Get all enrollments for this course
    enrollments = Enrollment.query.filter_by(course_id=course.id).all()
    
    # Check which students were marked absent
    for en in enrollments:
        status = request.form.get(f'attendance_{en.student_id}')
        if status == 'absent':
            en.devamsizlik += 1
            
    db.session.commit()
    flash('Yoklama başarıyla alındı. Gelmeyen öğrencilerin devamsızlığı 1 artırıldı.', 'success')
    return redirect(url_for('academician_dashboard'))

@app.route('/student_detail/<int:student_id>')
@login_required
def student_detail(student_id):
    if current_user.role != 'academician':
        return "Yetkisiz Erişim", 403
    student = User.query.get_or_404(student_id)
    if student.role != 'student':
        return "Bu kullanıcı bir öğrenci değil.", 400
    # Öğrencinin aldığı tüm ders kayıtları
    enrollments = Enrollment.query.filter_by(student_id=student.id).all()
    return render_template('student_detail.html', student=student, enrollments=enrollments)

# --- STUDENT ROUTES ---
@app.route('/student_dashboard')
@login_required
def student_dashboard():
    if current_user.role != 'student':
        return "Yetkisiz Erişim", 403
    # Öğrencinin tüm kayıtları
    enrollments = Enrollment.query.filter_by(student_id=current_user.id).all()
    return render_template('student_dashboard.html', enrollments=enrollments)

if __name__ == '__main__':
    app.run(debug=True)
