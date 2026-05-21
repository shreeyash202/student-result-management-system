# models/result.py

import sqlite3
from models.student import get_db_connection


class ResultModel:

    @staticmethod
    def save_result(student_id, total, percentage, grade, status):

        conn = get_db_connection()

        # Replace old result
        conn.execute(
            "DELETE FROM Result WHERE StudentID = ?",
            (student_id,)
        )

        conn.execute(
            """
            INSERT INTO Result
            (StudentID, Total, Percentage, Grade, Status)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                student_id,
                total,
                percentage,
                grade,
                status
            )
        )

        conn.commit()

        conn.close()

    @staticmethod
    def get_result(student_id):

        conn = get_db_connection()

        result = conn.execute(
            """
            SELECT

                r.*,

                s.Name,
                s.Course,
                s.Semester,

                m.Maths,
                m.DBMS,
                m.Python,
                m.OS,
                m.Java

            FROM Result r

            JOIN Student s
            ON r.StudentID = s.StudentID

            JOIN Marks m
            ON r.StudentID = m.StudentID

            WHERE r.StudentID = ?
            """,
            (student_id,)
        ).fetchone()

        conn.close()

        return result