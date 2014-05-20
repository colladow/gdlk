import json

from flask import make_response, request, abort
from flask.views import MethodView

from gdlk import app, register_api
from gdlk.db import get_db, normalize_rows

class ComboAPI(MethodView):

    select_fields = [
        'id', 'title', 'game_id', 'author',
        'character', 'commands','is_public',
        'video_url', 'created', 'updated'
    ]

    update_fields = [
        'title', 'game_id', 'author',
        'character', 'commands', 'is_public',
        'video_url', 'updated'
    ]

    def _clean_form(self, form):
        keys = []
        values = []

        for k in ComboAPI.update_fields:
            if form.has_key(k):
                keys.append(k)
                values.append(form[k])

        return keys, values

    def get(self, combo_id):
        db = get_db()

        select = ', '.join(ComboAPI.select_fields)

        if combo_id is not None:
            cur = db.execute('''
                select %s
                from combos
                where id = ?
            ''' % select, [combo_id])

            combos = cur.fetchall()

            if len(combos) == 0:
                abort(404)
            else:
                combos = normalize_rows(combos)[0]
        else:
            cur = db.execute('''
                select %s
                from combos
            ''' % select, [])

            combos = normalize_rows(cur.fetchall())

        return json.dumps(combos)

    def post(self):
        db = get_db()
        fields, combo = self._clean_form(request.form)

        insert = ', '.join(fields)
        qs = ', '.join(['?' for i in range(len(fields))])

        db.execute('''
            insert into combos (%s) values (%s)
        ''' % (insert, qs), combo)

        db.commit()

        return make_response(json.dumps({ 'success': 'ok' }), 201, {})

    def put(self, combo_id):
        db = get_db()
        fields, combo = self._clean_form(request.form)
        combo.append(combo_id)

        update = []

        for f in fields:
            if f == 'updated':
                update.append('updated = current_timestamp')
                continue

            update.append('%s = ?' % f)

        update = ', '.join(update)

        db.execute('''
            update combos
            set %s
            where id = ?
        ''' % update, combo)

        db.commit()

        return make_response(json.dumps({ 'success': 'ok' }), 200, {})

    def delete(self, combo_id):
        db = get_db()

        db.execute('''
            delete from combos
            where id = ?
        ''', [combo_id])

        db.commit()

        return make_response(json.dumps({ 'success': 'ok' }), 200, {})

register_api(ComboAPI, 'combo_api', '/combos/', pk='combo_id')
