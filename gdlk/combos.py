import json

from flask import make_response, request

from gdlk import app
from gdlk.db import get_db, normalize_rows, build_insert

def clean_combo(form):
    return [
        form['title'],
        form['game'],
        form['character'],
        form['commands']
    ]

@app.route('/combos')
def combos_index():
    db = get_db()
    cur = db.execute('select id, title, game, character, commands from combos')

    combos = cur.fetchall()

    return json.dumps(normalize_rows(combos))

@app.route('/combos', methods=['POST'])
def combos_post():
    db = get_db()
    combo = clean_combo(request.form)

    db.execute('''
        insert into combos (title, game, character, commands) values (?, ?, ?, ?)
    ''', combo)

    db.commit()

    return make_response(json.dumps({ 'success': 'ok' }), 201, {})

@app.route('/combos/<int:cid>', methods=['PUT'])
def combos_put(cid):
    db = get_db()
    combo = clean_combo(request.form)
    combo.append(cid)

    db.execute('''
        update combos
        set title = ?,
            game = ?,
            character = ?,
            commands = ?,
            updated = current_timestamp
        where id = ?
    ''', combo)

    db.commit()

    return make_response(json.dumps({ 'success': 'ok' }), 200, {})

@app.route('/combos/<int:cid>', methods=['DELETE'])
def combos_delete(cid):
    db = get_db()

    db.execute('''
        delete from combos
        where id = ?
    ''', [cid])

    db.commit()

    return make_response(json.dumps({ 'success': 'ok' }), 200, {})
