import os
import unittest
import tempfile
import json

import gdlk

class GdlkTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, gdlk.app.config['DATABASE'] = tempfile.mkstemp()

        gdlk.app.config['TESTING'] = True

        self.app = gdlk.app.test_client()

        gdlk.db.init_db()

        self.create_user('dictator@shadoloo.org', 'Dictator', 'yesyes')

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(gdlk.app.config['DATABASE'])

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
        assert rv['success'] == 'ok'

    def test_get_user(self):
        rv = self._load_response(self.app.get('/users/1'))
        assert rv['handle'] == 'Dictator'

    def test_edit_user(self):
        user = self._load_response(self.app.get('/users/1'))
        changed = user.copy()
        new_handle = 'M. Bison'
        changed['handle'] = new_handle

        rv = self._load_response(self.app.put('/users/1', data=changed))
        assert rv['success'] == 'ok'

        new_user = self._load_response(self.app.get('/users/1'))
        assert new_user['email'] == user['email']
        assert new_user['handle'] == new_handle

        self.app.put('/users/1/', data=user)

    def test_delete_user(self):
       self.create_user('boxer@shadoloo.org', 'Boxer', 'myfightmoney')

       user = self._load_response(self.app.get('/users/2'))
       assert user['handle'] == 'Boxer'

       rv = self._load_response(self.app.delete('/users/2'))
       assert rv['success'] == 'ok'

       rv = self.app.get('/users/2')
       assert rv.status_code == 404

if __name__ == '__main__':
    unittest.main()
