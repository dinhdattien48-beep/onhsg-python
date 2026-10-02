"""
database.py - Module quản lý cơ sở dữ liệu SQLite cho tiến độ học sinh.
Lưu trữ: kết quả chấm bài, trạng thái hoàn thành, cài đặt API.
"""

import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "hsg_python.db")


def get_connection():
    """Tạo kết nối đến SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    """Khởi tạo các bảng trong database."""
    conn = get_connection()
    cursor = conn.cursor()

    # Bảng lưu tiến độ từng bài tập
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            problem_id TEXT NOT NULL,
            stage_id INTEGER NOT NULL,
            code TEXT NOT NULL,
            score INTEGER DEFAULT 0,
            total_tests INTEGER DEFAULT 10,
            status TEXT DEFAULT 'pending',
            results_json TEXT,
            ai_feedback TEXT,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Bảng lưu trạng thái hoàn thành bài tập (AC 10/10)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            problem_id TEXT PRIMARY KEY,
            stage_id INTEGER NOT NULL,
            completed INTEGER DEFAULT 0,
            best_score INTEGER DEFAULT 0,
            attempts INTEGER DEFAULT 0,
            last_code TEXT,
            completed_at TIMESTAMP
        )
    """)

    # Bảng lưu cài đặt (API key, model name)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def save_submission(problem_id: str, stage_id: int, code: str, score: int,
                    total_tests: int, status: str, results: list, ai_feedback: str = ""):
    """Lưu kết quả nộp bài."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO submissions (problem_id, stage_id, code, score, total_tests, status, results_json, ai_feedback)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (problem_id, stage_id, code, score, total_tests, status,
          json.dumps(results, ensure_ascii=False), ai_feedback))

    # Cập nhật progress
    cursor.execute("""
        INSERT INTO progress (problem_id, stage_id, completed, best_score, attempts, last_code, completed_at)
        VALUES (?, ?, ?, ?, 1, ?, ?)
        ON CONFLICT(problem_id) DO UPDATE SET
            best_score = MAX(best_score, ?),
            attempts = attempts + 1,
            last_code = ?,
            completed = CASE WHEN ? >= ? THEN 1 ELSE completed END,
            completed_at = CASE WHEN ? >= ? AND completed = 0 THEN ? ELSE completed_at END
    """, (problem_id, stage_id, 1 if score >= total_tests else 0, score, code,
          datetime.now().isoformat() if score >= total_tests else None,
          score, code,
          score, total_tests,
          score, total_tests, datetime.now().isoformat()))

    conn.commit()
    conn.close()


def get_progress():
    """Lấy toàn bộ tiến độ học tập."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM progress")
    rows = cursor.fetchall()
    conn.close()
    return {row["problem_id"]: dict(row) for row in rows}


def get_submissions(problem_id: str, limit: int = 5):
    """Lấy lịch sử nộp bài của một bài tập."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM submissions
        WHERE problem_id = ?
        ORDER BY submitted_at DESC
        LIMIT ?
    """, (problem_id, limit))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def save_setting(key: str, value: str):
    """Lưu cài đặt."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO settings (key, value) VALUES (?, ?)
        ON CONFLICT(key) DO UPDATE SET value = ?
    """, (key, value, value))
    conn.commit()
    conn.close()


def get_setting(key: str, default: str = "") -> str:
    """Lấy cài đặt."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
    row = cursor.fetchone()
    conn.close()
    return row["value"] if row else default


# Khởi tạo database khi import module
init_db()
