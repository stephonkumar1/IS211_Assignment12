--Stephon Kumar

-- Create table for students
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL
);

-- Create table for quizzes
CREATE TABLE quizzes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT NOT NULL,
    num_questions INTEGER NOT NULL,
    quiz_date DATE NOT NULL
);

-- Create table for quiz results
CREATE TABLE results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    quiz_id INTEGER NOT NULL,
    score INTEGER NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students (id),
    FOREIGN KEY (quiz_id) REFERENCES quizzes (id)
);
