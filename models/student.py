# models/student.py
import sqlite3

def get_db_connection():
    # Connects to the local SQLite database file instance
    conn = sqlite3.connect('student_result.db')
    conn.row_factory = sqlite3.Row
    return conn


class StudentModel:

    @staticmethod
    def create_student(student_id, name, course, semester, password):
        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO Student (StudentID, Name, Course, Semester, Password) VALUES (?, ?, ?, ?, ?)",
                (student_id, name, course, semester, password)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    @staticmethod
    def get_student(student_id):
        conn = get_db_connection()
        student = conn.execute(
            "SELECT * FROM Student WHERE StudentID = ?",
            (student_id,)
        ).fetchone()
        conn.close()
        return student

    @staticmethod
    def delete_student(student_id):
        conn = get_db_connection()
        conn.execute(
            "DELETE FROM Student WHERE StudentID = ?",
            (student_id,)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def bulk_insert_students(student_list):
        """
        Takes a list of tuples:
        [(student_id, name, course, semester, password), ...]
        and inserts them in a single fast database transaction.
        """
        conn = get_db_connection()
        try:
            conn.executemany(
                """
                INSERT INTO Student
                (StudentID, Name, Course, Semester, Password)
                VALUES (?, ?, ?, ?, ?)
                """,
                student_list
            )

            conn.commit()
            return True, f"Successfully imported {len(student_list)} students."

        except sqlite3.IntegrityError:
            return False, "Database Error: One or more Student IDs already exist (duplicates)."

        finally:
            conn.close()