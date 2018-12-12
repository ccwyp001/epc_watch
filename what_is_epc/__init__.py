from flask import Flask
from werkzeug.utils import find_modules, import_string

from config import config
from .extensions import db
from . import models  # use for migrate


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])
    app.config.from_pyfile('config.py', silent=True)

    db.init_app(app)
    app.url_map.strict_slashes = False

    register_blueprints(app, 'v1', 'what_is_epc.api.v1')
    return app


def register_blueprints(app, v, package):
    for module_name in find_modules(package):
        module = import_string(module_name)
        if hasattr(module, 'bp'):
            bp = module.bp
            app.register_blueprint(bp, url_prefix='/api/{0}/{1}'.format(v, bp.name))