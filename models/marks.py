# models/marks.py

import sqlite3
from models.student import get_db_connection


class MarksModel:

    @staticmethod
    def enter_marks(student_id, maths, dbms, python_marks, os_marks, java):

        conn = get_db_connection()

        # Replace old marks
        conn.execute(
            "DELETE FROM Marks WHERE StudentID = ?",
            (student_id,)
        )

        conn.execute(
            """
            INSERT INTO Marks
            (StudentID, Maths, DBMS, Python, OS, Java)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                student_id,
                maths,
                dbms,
                python_marks,
                os_marks,
                java
            )
        )

        conn.commit()
        conn.close()

    @staticmethod
    def get_marks(student_id):

        conn = get_db_connection()

        marks = conn.execute(
            "SELECT * FROM Marks WHERE StudentID = ?",
            (student_id,)
        ).fetchone()

        conn.close()

        return marks

    @staticmethod
    def bulk_insert_marks(mark_list):

        conn = get_db_connection()

        try:

            conn.executemany(
                """
                INSERT OR REPLACE INTO Marks
                (StudentID, Maths, DBMS, Python, OS, Java)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                mark_list
            )

            conn.commit()

            return True, f"{len(mark_list)} marks imported successfully."

        except sqlite3.Error as e:
            return False, str(e)

        finally:
            conn.close()