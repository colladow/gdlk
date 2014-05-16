from flask import g
import sqlite3

from gdlk import app

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv 

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()

    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('config/schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def normalize_rows(rows):
    if len(rows) == 0:
        return []

    keys = rows[0].keys()
    l = []

    for r in rows:
        d = {}

        for k in keys:
            d[k] = r[k]

        l.append(d)

    return l
