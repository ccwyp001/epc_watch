import os

from flask import Blueprint, request, jsonify, current_app
from flask_restful import Api, Resource
from ...commons import exceptions
from ...extensions import db
from ...models import Vehicles
from . import OpException, OpSuccess

bp = Blueprint('displacements', __name__)
api = Api(bp)


@api.resource('/test')
class TestApi(Resource):
    def get(self):
        pass


@api.resource('/')
class DisplacementsApi(Resource):
    def get(self):
        try:
            arg1 = request.args['manufacturer']
            arg2 = request.args['models']
            v_list = Vehicles.query.filter(
                Vehicles.manufacturer == arg1,
                Vehicles.model == arg2
            ).all()
            return OpSuccess([_.display() for _ in v_list])
        except Exception as e:
            return OpException(exceptions.DataValidateError())
        finally:
            if 'db' in locals():
                db.session.close()
