import os
import sqlite3


DEFAULT_DATABASE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "studysync.db")


def get_database_path(config=None):
    """Return the configured SQLite database path."""
    config = config or {}
    return config.get("DATABASE", DEFAULT_DATABASE)


def init_db(db_path):
    """Create the SQLite tables used by StudySync AI."""
    connection = sqlite3.connect(db_path)
    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS study_plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                topic TEXT NOT NULL,
                UNIQUE(subject, topic)
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS completion_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                topic TEXT NOT NULL,
                completed_at TEXT NOT NULL,
                UNIQUE(subject, topic)
            )
            """
        )
        connection.commit()
    finally:
        connection.close()


def get_connection(db_path):
    """Open a SQLite connection with row factory support."""
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection


def seed_sample_data(db_path):
    """Add a small Demo subject/topic set for local development."""
    connection = get_connection(db_path)
    try:
        connection.executemany(
            "INSERT OR IGNORE INTO study_plans (subject, topic) VALUES (?, ?)",
            [
                ("DBMS", "Topic 1"),
                ("DBMS", "Topic 2"),
                ("Biology", "Cells"),
                ("Biology", "Photosynthesis"),
            ],
        )
        connection.commit()
    finally:
        connection.close()
