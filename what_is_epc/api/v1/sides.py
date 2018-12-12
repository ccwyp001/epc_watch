import os

from flask import Blueprint, request, jsonify, current_app
from flask_restful import Api, Resource
from ...commons import exceptions
from ...extensions import db
from ...models import VehicleAssemblyGroups
from . import OpSuccess, OpException

bp = Blueprint('sides', __name__)
api = Api(bp)


@api.resource('/test')
class TestApi(Resource):
    def get(self):
        pass


@api.resource('/')
class SidesApi(Resource):
    def get(self):
        try:
            arg = request.args['vehicle_id']
            v_list = VehicleAssemblyGroups.query.filter(
                VehicleAssemblyGroups.vehicle_id == arg
            ).all()
            return OpSuccess([_.display() for _ in v_list])
        except Exception as e:
            return OpException(exceptions.DataValidateError())
        finally:
            if 'db' in locals():
                db.session.close()
