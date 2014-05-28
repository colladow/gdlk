from datetime import datetime

from bson import json_util
from bson.objectid import ObjectId
from flask import make_response, request, abort
from flask.views import MethodView

from gdlk import app, register_api
from gdlk.db import get_db

class ComboAPI(MethodView):

    def get(self, combo_id):
        db = get_db('combos')

        if combo_id is not None:
            combos = db.find_one({ '_id': ObjectId(combo_id) })

            if combos is None: abort(404)
        else:
            combos = db.find({})

        return json_util.dumps(combos)

    def post(self):
        db = get_db('combos')

        try:
            combo = {
                'title': request.form['title'],
                'game': request.form['game'],
                'author': request.form['author'],
                'character': request.form['character'],
                'commands': request.form['commands'],
                'public': request.form.get('public', default=False),
                'videoUrl': request.form.get('videoUrl'),
                'created': datetime.now(),
                'updated': datetime.now()
            }
        except KeyError:
            return make_response(json_util.dumps({ 'error': 'bodied' }), 500, {})

        db.insert(combo)

        if combo['_id'] is None:
            return make_response(json_util.dumps({ 'error': 'bodied' }), 500, {})
        else:
            return make_response(json_util.dumps(combo), 201, {})

    def put(self, combo_id):
        db = get_db('combos')

        valid_fields = [
            'title', 'game', 'author', 'character',
            'commands', 'public', 'videoUrl',
        ]
        changes = {}

        for k, v in request.form.iteritems():
            if k in valid_fields:
                changes[k] = v

        if len(changes) == 0:
            return make_response(json_util.dumps({ 'error': 'bodied' }), 500, {})

        changes['updated'] = datetime.now()

        result = db.update({ '_id': ObjectId(combo_id) }, changes)

        if result is None:
            return make_response(json_util.dumps({ 'error': 'bodied' }), 500, {})
        else:
            changes['_id'] = combo_id
            return make_response(json_util.dumps(changes), 200, {})

    def delete(self, combo_id):
        get_db('combos').remove({ '_id': ObjectId(combo_id) })

        return make_response(json_util.dumps({ 'success': 'ok' }), 200, {})

@app.route('/combos/commands', methods=['GET'])
def list_commands():
    commands = list(get_db('commands').find({}))

    return json_util.dumps(commands)

register_api(ComboAPI, 'combo_api', '/combos/', pk='combo_id')
