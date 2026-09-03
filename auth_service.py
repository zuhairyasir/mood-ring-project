import sqlite3
import bcrypt
import secrets
from datetime import datetime

DB_PATH = "mood_ring.db"

class AuthService:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self._create_tables()

    def _create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                token TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        self.conn.commit()

    def signup(self, username, email, password):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            return None, "An account with that email already exists"

        password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        cursor.execute(
            "INSERT INTO users (username, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
            (username, email, password_hash.decode("utf-8"), datetime.utcnow().isoformat())
        )
        self.conn.commit()
        token = self._create_session(cursor.lastrowid)
        return token, None

    def login(self, email, password):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, password_hash FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        if not row:
            return None, "Invalid email or password"

        user_id, password_hash = row
        if not bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8")):
            return None, "Invalid email or password"

        token = self._create_session(user_id)
        return token, None

    def get_username_by_email(self, email):
        cursor = self.conn.cursor()
        cursor.execute("SELECT username FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        return row[0] if row else None

    def _create_session(self, user_id):
        token = secrets.token_hex(32)
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO sessions (token, user_id, created_at) VALUES (?, ?, ?)",
            (token, user_id, datetime.utcnow().isoformat())
        )
        self.conn.commit()
        return token

    def get_user_from_token(self, token):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT users.id, users.username FROM sessions
            JOIN users ON sessions.user_id = users.id
            WHERE sessions.token = ?
        ''', (token,))
        row = cursor.fetchone()
        if not row:
            return None
        return {"id": row[0], "username": row[1]}