# controllers/auth_controller.py
import sqlite3
from models.student import get_db_connection

class AuthController:
    @staticmethod
    def login(username, password, role):
        conn = get_db_connection()
        if role == 'admin':
            user = conn.execute("SELECT * FROM Admin WHERE Username = ? AND Password = ?", (username, password)).fetchone()
        else:
            user = conn.execute("SELECT * FROM Student WHERE StudentID = ? AND Password = ?", (username, password)).fetchone()
        conn.close()
        return user