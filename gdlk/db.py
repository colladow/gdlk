from datetime import datetime

from bson import json_util
from flask import g
import pymongo

from gdlk import app

DB_CONFIG = app.config['DATABASE']

def connect_db():
    return pymongo.MongoClient(DB_CONFIG['HOST'], DB_CONFIG['PORT'])

def get_conn():
    if not hasattr(g, 'mongo_conn'):
        g.mongo_conn = connect_db()

    return g.mongo_conn

def get_db(collection):
    return get_conn()[DB_CONFIG['NAME']][collection]

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'mongo_conn'):
        g.mongo_conn.close()

def init_db(fname='config/seed.json'):
    with app.app_context():
        with app.open_resource(fname, mode='r') as f:
            data = json_util.loads(f.read())

            for key, collection in data.iteritems():
                get_db(key).drop()
                db = get_db(key)

                db.insert(collection)
