import sqlite3
import pathlib

def dict_factory(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

def db():
    db_path = str(pathlib.Path(__file__).parent.parent.resolve()) + "/company.db"
    conn = sqlite3.connect(db_path)
    conn.row_factory = dict_factory
    return conn
