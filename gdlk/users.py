import json
import bcrypt

from flask import make_response, request, abort, session
from flask.views import MethodView

from gdlk import app, register_api
from gdlk.db import get_db, normalize_rows

class User:
    @classmethod
    def get(cls, user_id):
        db = get_db()

        cur = db.execute('''
            select id, email, handle
            from users
            where id = ?
        ''', [user_id])

        rows = normalize_rows(cur.fetchall())

        if len(rows) == 0:
            return None
        else:
            return rows[0]

    @classmethod
    def hash_password(cls, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(10))

    @classmethod
    def set_password(cls, user_id, pw):
        db = get_db()

        password = cls.hash_password(pw)

        cur = db.execute('''
            update users
            set password = ?
            where id = ?
        ''', [password, user_id])

        db.commit()

    @classmethod
    def check_password(cls, email, password):
        db = get_db()

        cur = db.execute('''
            select password
            from users
            where email = ?
        ''', [email])

        hashed = cur.fetchall()[0]['password'].encode('utf-8')

        return bcrypt.hashpw(password.encode('utf-8'), hashed) == hashed

class UserAPI(MethodView):
    def get(self, user_id):
        if user_id is not None:
            users = User.get(user_id)

            if users is None:
                abort(404)
        else:
            cur = db.execute('''
                select email, handle
                from users
            ''' % select, [])

            users = normalize_rows(cur.fetchall())

        return json.dumps(users)

    def post(self):
        db = get_db()

        values = [
            request.form['email'],
            request.form['handle'],
            User.hash_password(request.form['password'])
        ]

        db.execute('''
            insert into users (email, handle, password) values (?, ?, ?)
        ''', values)

        db.commit()

        return make_response(json.dumps({ 'success': 'ok' }), 201, {})

    def put(self, user_id):
        db = get_db()

        user = [
            request.form['email'],
            request.form['handle']
        ]

        db.execute('''
            update users
            set email = ?,
                handle = ?
        ''', user)

        db.commit()

        return make_response(json.dumps({ 'success': 'ok' }), 200, {})

    def delete(self, user_id):
        db = get_db()

        db.execute('''
            delete from users
            where id = ?
        ''', [user_id])

        db.commit()

        return make_response(json.dumps({ 'success': 'ok' }), 200, {})

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    if not User.check_password(email, password):
        return make_response(json.dumps({ 'error': 'bodied' }), 403, {})

    session['email'] = email
    return make_response(json.dumps({ 'success': 'ok' }), 200, {})

@app.route('/logout')
def logout():
    session.pop('email', None)
    return make_response(json.dumps({ 'success': 'ok' }), 200, {})

register_api(UserAPI, 'user_api', '/users/', pk='user_id')
