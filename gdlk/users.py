from datetime import datetime

import bcrypt
from bson import json_util
from bson.objectid import ObjectId
from flask import make_response, request, abort, session
from flask.views import MethodView

from gdlk import app, register_api
from gdlk.db import get_db

class User:
    @classmethod
    def get(cls, user_id):
        db = get_db('users')

        return db.find_one({ '_id': ObjectId(user_id) })

    @classmethod
    def hash_password(cls, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(10))

    @classmethod
    def set_password(cls, user_id, pw):
        db = get_db('users')

        password = cls.hash_password(pw)

        return db.update({ '_id': ObjectId(user_id) }, { '$set': { 'password': password }})

    @classmethod
    def check_password(cls, email, password):
        db = get_db('users')

        user = db.find_one({ 'email': email })

        if user is None: return False

        hashed = user['password'].encode('utf-8')

        return bcrypt.hashpw(password.encode('utf-8'), hashed) == hashed

class UserAPI(MethodView):
    def get(self, user_id):
        if user_id is not None:
            users = User.get(user_id)

            if users is None: abort(404)
        else:
            users = list(get_db('users').find({}))

        return json_util.dumps(users)

    def post(self):
        db = get_db('users')

        new_user = {
            'email': request.form['email'],
            'handle': request.form['handle'],
            'password': User.hash_password(request.form['password']),
            'created': datetime.now(),
            'updated': datetime.now()
        }

        db.insert(new_user)

        if new_user['_id'] is None:
            return make_response(json_util.dumps({ 'error': 'bodied' }), 400, {})
        else:
            return make_response(json_util.dumps(new_user), 201, {})

    def put(self, user_id):
        db = get_db('users')

        valid_fields = ['email', 'handle']

        changes = {}

        for k, v in request.form.iteritems():
            if k in valid_fields:
                changes[k] = v

        if len(changes) == 0:
            return make_response(json_util.dumps({ 'error': 'bodied' }), 400, {})

        changes['updated'] = datetime.now()

        result = db.update({ '_id': ObjectId(user_id) }, changes)

        if result is None:
            return make_response(json_util.dumps({ 'error': 'bodied' }), 400, {})
        else:
            changes['_id'] = user_id

            return make_response(json_util.dumps(changes), 200, {})

    def delete(self, user_id):
        get_db('users').remove({ '_id': ObjectId(user_id) })

        return make_response(json_util.dumps({ 'success': 'ok' }), 200, {})

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    if not User.check_password(email, password):
        return make_response(json_util.dumps({ 'error': 'bodied' }), 403, {})

    session['email'] = email
    return make_response(json_util.dumps({ 'success': 'ok' }), 200, {})

@app.route('/logout')
def logout():
    session.pop('email', None)
    return make_response(json_util.dumps({ 'success': 'ok' }), 200, {})

register_api(UserAPI, 'user_api', '/users/', pk='user_id')
