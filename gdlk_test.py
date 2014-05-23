import os
import unittest
import tempfile
import json

import gdlk

class GdlkTestCase(unittest.TestCase):

    def setUp(self):
        gdlk.app.config['TESTING'] = True

        self.app = gdlk.app.test_client()

        gdlk.db.init_db()

        self.user = self._load_response(self.create_user('dictator@shadoloo.org', 'Dictator', 'yesyes'))
        self.user['_id'] = self.user['_id']['$oid']

        data = {
            'title': 'Wombo',
            'game': 'Ultra Street Fighter IV',
            'author': 'dictator@shadoloo.org',
            'character': 'Dictator',
            'commands': 'short short short short LK.scissor kick'
        }
        self.combo = self._load_response(self.app.post('/combos/', data=data))
        self.combo['_id'] = self.combo['_id']['$oid']

    def tearDown(self):
        with gdlk.app.app_context():
            db = gdlk.db.get_conn()
            db.drop_database(gdlk.app.config['DATABASE']['NAME'])

    def _load_response(self, resp):
        return json.loads(resp.get_data())

    def create_user(self, email, handle, password):
        return self.app.post('/users/', data=dict(
            email=email,
            handle=handle,
            password=password
        ))

    def login(self, email, password):
        return self.app.post('/login', data=dict(
            email=email,
            password=password
        ))

    def test_login(self):
        rv = self._load_response(self.login('dictator@shadoloo.org', 'yesyes'))
        assert rv['success'] == 'ok'

        rv = self._load_response(self.login('dictator@shadoloo.org', 'divekick'))
        assert rv['error'] == 'bodied'

    def test_logout(self):
        rv = self._load_response(self.app.get('/logout'))
        assert rv['success'] == 'ok'

    def test_add_user(self):
        rv = self._load_response(self.create_user('claw@shadoloo.org', 'Claw', 'heyaaw'))
        assert rv['handle'] == 'Claw'

    def test_get_user(self):
        rv = self._load_response(self.app.get('/users/%s' % self.user['_id']))
        assert rv['handle'] == 'Dictator'

    def test_edit_user(self):
        user = self._load_response(self.app.get('/users/%s' % self.user['_id']))
        changed = {
            'handle': 'M. Bison'
        }

        rv = self._load_response(self.app.put('/users/%s' % self.user['_id'], data=changed))
        assert rv['handle'] == changed['handle']

        new_user = self._load_response(self.app.get('/users/%s' % self.user['_id']))
        assert new_user['handle'] == changed['handle']

    def test_delete_user(self):
       user = self._load_response(self.create_user('boxer@shadoloo.org', 'Boxer', 'myfightmoney'))

       rv = self._load_response(self.app.get('/users/%s' % user['_id']['$oid']))
       assert rv['handle'] == 'Boxer'

       rv = self._load_response(self.app.delete('/users/%s' % user['_id']['$oid']))
       assert rv['success'] == 'ok'

       rv = self.app.get('/users/%s' % user['_id']['$oid'])
       assert rv.status_code == 404

    def test_combo_create(self):
        data = {
            'title': 'Wombo',
            'game': 'Ultra Street Fighter IV',
            'author': 'dictator@shadoloo.org',
            'character': 'Dictator',
            'commands': 'short short short short LK.scissor kick'
        }

        rv = self._load_response(self.app.post('/combos/', data=data))
        assert rv['title'] == 'Wombo'

    def test_combo_get(self):
        rv = self._load_response(self.app.get('/combos/%s' % self.combo['_id']))
        assert rv['title'] == 'Wombo'

    def test_combo_update(self):
        changed = { 'title': 'Combo' }

        rv = self._load_response(self.app.put('/combos/%s' % self.combo['_id'], data=changed))
        assert rv['title'] == changed['title']

        rv = self._load_response(self.app.get('/combos/%s' % self.combo['_id']))
        assert rv['title'] == changed['title']

    def test_combo_delete(self):
        rv = self._load_response(self.app.delete('/combos/%s' % self.combo['_id']))
        assert rv['success'] == 'ok'

        rv = self.app.get('/combos/%s' % self.combo['_id'])
        assert rv.status_code == 404

if __name__ == '__main__':
    unittest.main()
