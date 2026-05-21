-- =========================================
-- STUDENT TABLE
-- =========================================

CREATE TABLE IF NOT EXISTS Student (

    StudentID TEXT PRIMARY KEY,

    Name TEXT NOT NULL,

    Course TEXT NOT NULL,

    Semester TEXT NOT NULL,

    Password TEXT NOT NULL

);


-- =========================================
-- ADMIN TABLE
-- =========================================

CREATE TABLE IF NOT EXISTS Admin (

    Username TEXT PRIMARY KEY,

    Password TEXT NOT NULL

);


-- =========================================
-- MARKS TABLE
-- =========================================

CREATE TABLE IF NOT EXISTS Marks (

    StudentID TEXT PRIMARY KEY,

    Maths INTEGER,
    DBMS INTEGER,
    Python INTEGER,
    OS INTEGER,
    Java INTEGER,

    FOREIGN KEY(StudentID)
    REFERENCES Student(StudentID)

);


-- =========================================
-- RESULT TABLE
-- =========================================

CREATE TABLE IF NOT EXISTS Result (

    StudentID TEXT PRIMARY KEY,

    Total INTEGER,

    Percentage REAL,

    Grade TEXT,

    Status TEXT,

    FOREIGN KEY(StudentID)
    REFERENCES Student(StudentID)

);


-- =========================================
-- DEFAULT ADMIN
-- =========================================

INSERT OR IGNORE INTO Admin
VALUES ('admin', 'admin123');