from flask import Flask, jsonify
from werkzeug.utils import find_modules, import_string
from config import config
from .extensions import db, jwt
from flask_jwt_extended import exceptions
from jwt import ExpiredSignatureError, InvalidTokenError
from . import models  # use for migrate


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])
    app.config.from_pyfile('config.py', silent=True)

    db.init_app(app)
    jwt.init_app(app)
    app.url_map.strict_slashes = False

    # @app.after_request
    # def handle_jwt_error(environ):
    #     print(environ.__dict__)
    #     rs = json.loads(environ.response)
    #
    #     return environ
    @app.errorhandler(ExpiredSignatureError)
    def handle_jwt_error(e):
        business_code = '100400'
        data = {}
        data['code'] = business_code
        data['message'] = str(e)
        return jsonify(data), 401

    register_blueprints(app, 'v1', 'what_is_epc.api.v1')
    return app


def register_blueprints(app, v, package):
    for module_name in find_modules(package):
        module = import_string(module_name)
        if hasattr(module, 'bp'):
            bp = module.bp
            api = module.api
            api.errors.update(api_errors())
            app.register_blueprint(bp, url_prefix='/api/{0}/{1}'.format(v, bp.name))


def api_errors():
    errors = {
        'NoAuthorizationError': {
            'status': 403, 'message': 'Missing Authorization Header'},
        'ExpiredSignatureError': {
            'status': 401, 'message': 'Signature has expired'},
    }
    from .commons.exceptions import BaseException
    errors.update(
        {cls.__name__: cls.__dict__ for cls in BaseException.__subclasses__()}
    )

    return errors