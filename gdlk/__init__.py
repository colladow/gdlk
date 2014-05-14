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

import gdlk.pages
import gdlk.combos
