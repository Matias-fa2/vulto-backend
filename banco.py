import sqlite3
import os

# TODO: mudar pra postgres um dia
DB_PATH = os.path.join(os.path.dirname(__file__), "data", "vulto.db")

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
conn.row_factory = sqlite3.Row


def query(sql, params=()):
    cur = conn.cursor()
    cur.execute(sql, params)
    return [dict(r) for r in cur.fetchall()]


def execute(sql, params=()):
    cur = conn.cursor()
    cur.execute(sql, params)
    conn.commit()
    return cur.lastrowid


def get_config(chave, default=None):
    r = query("select valor from config where chave = ?", (chave,))
    if len(r) == 0:
        return default
    return r[0]["valor"]
