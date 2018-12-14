import os

from flask import Blueprint, request, jsonify, current_app
from flask_restful import Api, Resource
from ...commons import exceptions
from . import OpSuccess, OpException
from ...models import Vehicles
from ...extensions import db

bp = Blueprint('brands', __name__)
api = Api(bp)


@api.resource('/test')
class TestApi(Resource):
    def get(self):
        pass


@api.resource('/')
class BrandApi(Resource):
    def get(self):
        try:
            brands = db.session.query(db.distinct(Vehicles.brand)).all()
            return OpSuccess([_[0] for _ in brands])
        except Exception as e:
            return OpException(exceptions.DataValidateError())
        finally:
            if 'db' in locals():
                db.session.close()