# -*- coding: utf-8 -*-

from flask import Blueprint, request, current_app
from flask_restful import Api, Resource
from ...commons import exceptions
from . import OpSuccess, OpException
import os
from ..vin_code import predict
import base64
import json

bp = Blueprint('vincode', __name__)
api = Api(bp)


@api.resource('/ocr')
class VinOCRApi(Resource):
    def post(self):
        try:
            pic_file = request.files['picfile']
            img_base64data = base64.b64encode(pic_file.read())
            appcode = current_app.config['IMG_2_VIN_APP_CODE']
            url = current_app.config['IMG_2_VIN_APP_URL']
            config = None
            stat, header, content = predict(url, appcode, img_base64data, config)
            if stat != 200:
                return OpException(exceptions.QueryFail('未能正确识别，请重新上传'))
            return OpSuccess(json.loads(content)["vin"])
        except:
            return OpException(exceptions.QueryFail('未能正确识别，请重新上传'))
