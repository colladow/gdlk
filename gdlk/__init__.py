import json
import os

from flask import Flask, render_template, url_for

def load_config(root_path):
    env = 'dev'

    if os.environ.has_key('GDLK_ENV'):
        env = os.environ['GDLK_ENV']

    cfg_file = open(os.path.join(root_path, 'config', 'gdlk.' + env + '.json'))

    return json.loads(cfg_file.read())

app = Flask(__name__)

config = load_config(app.root_path)

if config:
    app.config.update(config)

def register_api(view, endpoint, url, pk='id', pk_type='int'):
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, defaults={pk: None},
                     view_func=view_func, methods=['GET',])
    app.add_url_rule(url, view_func=view_func, methods=['POST',])
    app.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func,
                     methods=['GET', 'PUT', 'DELETE'])

import gdlk.pages
import gdlk.combos
import gdlk.users
