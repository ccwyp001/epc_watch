import os

from flask import Blueprint, request, jsonify, current_app
from flask_restful import Api, Resource
from ...commons import exceptions
from . import OpException, OpSuccess
from ...extensions import db
from ...models import Vehicles

bp = Blueprint('manufacturers', __name__)
api = Api(bp)


@api.resource('/test')
class TestApi(Resource):
    def get(self):
        pass


@api.resource('/')
class ManufacturersApi(Resource):
    def get(self):
        try:
            arg = request.args['brand']
            _ = db.session.query(
                db.distinct(Vehicles.manufacturer)).filter(Vehicles.brand == arg).all()
            return OpSuccess(_)
        except Exception as e:
            return OpException(exceptions.DataValidateError())
        finally:
            if 'db' in locals():
                db.session.close()
