#Stephon Kumar

from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'

DATABASE = 'hw13.db'

def get_db():
    """Connect to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Render the login page and authenticate users."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """Display the dashboard with students and quizzes."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    conn = get_db()
    students = conn.execute('SELECT * FROM students').fetchall()
    quizzes = conn.execute('SELECT * FROM quizzes').fetchall()
    conn.close()
    return render_template('dashboard.html', students=students, quizzes=quizzes)

@app.route('/student/add', methods=['GET', 'POST'])
def add_student():
    """Add a new student to the database."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        conn = get_db()
        conn.execute('INSERT INTO students (first_name, last_name) VALUES (?, ?)', (first_name, last_name))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    return render_template('add_student.html')

@app.route('/quiz/add', methods=['GET', 'POST'])
def add_quiz():
    """Add a new quiz to the database."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        subject = request.form.get('subject')
        num_questions = request.form.get('num_questions')
        quiz_date = request.form.get('quiz_date')
        conn = get_db()
        conn.execute('INSERT INTO quizzes (subject, num_questions, quiz_date) VALUES (?, ?, ?)',
                     (subject, num_questions, quiz_date))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    return render_template('add_quiz.html')

@app.route('/student/<int:id>')
def student_results(id):
    """Display quiz results for a specific student."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    conn = get_db()
    results = conn.execute("""
        SELECT quizzes.id as quiz_id, quizzes.subject, quizzes.quiz_date, results.score
        FROM results
        JOIN quizzes ON results.quiz_id = quizzes.id
        WHERE results.student_id = ?
    """, (id,)).fetchall()
    conn.close()
    return render_template('student_results.html', results=results)

@app.route('/results/add', methods=['GET', 'POST'])
def add_result():
    """Add a new quiz result for a student."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    conn = get_db()
    students = conn.execute('SELECT * FROM students').fetchall()
    quizzes = conn.execute('SELECT * FROM quizzes').fetchall()
    conn.close()

    if request.method == 'POST':
        student_id = request.form.get('student_id')
        quiz_id = request.form.get('quiz_id')
        score = request.form.get('score')
        conn = get_db()
        conn.execute('INSERT INTO results (student_id, quiz_id, score) VALUES (?, ?, ?)',
                     (student_id, quiz_id, score))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    return render_template('add_result.html', students=students, quizzes=quizzes)

@app.route('/logout')
def logout():
    """Log the user out and redirect to login."""
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
