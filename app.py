from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import flash
from flask import session

from controllers.auth_controller import AuthController
from controllers.student_controller import StudentController
from controllers.marks_controller import MarksController

from models.student import get_db_connection
from models.result import ResultModel

import sqlite3

app = Flask(__name__)
def initialize_database():

    conn = sqlite3.connect('student_result.db')

    cursor = conn.cursor()

    with open('database/schema.sql', 'r') as f:
        cursor.executescript(f.read())

    conn.commit()
    conn.close()

initialize_database()

app.secret_key = "srms_secret_key"


# =========================================
# LOGIN PAGE
# =========================================

@app.route('/')
def home():

    return render_template('login.html')


# =========================================
# LOGIN
# =========================================

@app.route('/login', methods=['POST'])
def login():

    username = request.form['username']

    password = request.form['password']

    role = request.form['role']

    user = AuthController.login(
        username,
        password,
        role
    )

    if user:

        session['user'] = username

        session['role'] = role

        # ADMIN LOGIN
        if role == 'admin':

            return redirect('/dashboard')

        # STUDENT LOGIN
        else:

            return redirect(
                f'/student_result/{username}'
            )

    flash("Invalid username or password.")

    return redirect('/')


# =========================================
# LOGOUT
# =========================================

@app.route('/logout')
def logout():

    session.clear()

    return redirect('/')


# =========================================
# ADMIN DASHBOARD
# =========================================

@app.route('/dashboard')
def dashboard():

    # Admin protection
    if 'role' not in session:

        return redirect('/')

    if session['role'] != 'admin':

        return redirect('/')

    conn = get_db_connection()

    students = conn.execute(
        "SELECT * FROM Student"
    ).fetchall()

    conn.close()

    return render_template(
        'dashboard.html',
        students=students
    )


# =========================================
# ADD STUDENT
# =========================================

@app.route('/admin/add_student', methods=['POST'])
def add_student():

    student_id = request.form['student_id']

    name = request.form['name']

    course = request.form['course']

    semester = request.form['semester']

    password = request.form['password']

    success, message = StudentController.register(
        student_id,
        name,
        course,
        semester,
        password
    )

    flash(message)

    return redirect('/dashboard')


# =========================================
# DELETE STUDENT
# =========================================

@app.route('/admin/delete_student/<student_id>')
def delete_student(student_id):

    success, message = StudentController.remove(
        student_id
    )

    flash(message)

    return redirect('/dashboard')


# =========================================
# BULK STUDENT UPLOAD
# =========================================

@app.route('/admin/bulk_upload', methods=['POST'])
def bulk_upload():

    file = request.files['csv_file']

    success, message = StudentController.bulk_upload(
        file
    )

    flash(message)

    return redirect('/dashboard')


# =========================================
# MANUAL MARKS ENTRY
# =========================================

@app.route(
    '/admin/enter_marks/<student_id>',
    methods=['GET', 'POST']
)
def enter_marks(student_id):

    if request.method == 'POST':

        maths = request.form['maths']

        dbms = request.form['dbms']

        python_marks = request.form['python']

        os_marks = request.form['os']

        java = request.form['java']

        success, message = MarksController.submit_marks(
            student_id,
            maths,
            dbms,
            python_marks,
            os_marks,
            java
        )

        flash(message)

        return redirect('/dashboard')

    return render_template(
        'marks_entry.html',
        student_id=student_id
    )


# =========================================
# BULK MARKS UPLOAD
# =========================================

@app.route(
    '/admin/bulk_upload_marks',
    methods=['POST']
)
def bulk_upload_marks():

    file = request.files['csv_file']

    success, message = MarksController.bulk_upload(
        file
    )

    flash(message)

    return redirect('/dashboard')


# =========================================
# STUDENT RESULT VIEW
# =========================================

@app.route('/student_result/<student_id>')
def student_result(student_id):

    result = ResultModel.get_result(student_id)

    if not result:

        flash("Result not available.")

        return redirect('/')

    return render_template(
        'performance_report.html',
        res=result
    )


# =========================================
# MAIN
# =========================================

if __name__ == '__main__':

    app.run(debug=True)