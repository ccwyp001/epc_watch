import os

from flask import Blueprint, request, jsonify, current_app
from flask_restful import Api, Resource
from ...commons import exceptions
bp = Blueprint('epc', __name__)
api = Api(bp)


def OpSuccess(result):
    business_code = '100000'
    message = '成功'
    data = {}
    data['code'] = business_code
    data['message'] = message
    if result is not None:
        data['result'] = result
    return jsonify(data)


def OpException(exception):
    return exception.to_dict(), exception.http_code


@api.resource('/test')
class TestApi(Resource):
    def get(self):
        pass


