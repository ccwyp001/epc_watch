# -*- coding: utf-8 -*-


import json
import requests
import base64


def get_img_base64(img_file):
    with open(img_file, 'rb') as infile:
        s = infile.read()
        return base64.b64encode(s)


def predict(url, appcode, img_base64, kv_config):
    param = {}
    param['image'] = str(img_base64, encoding='utf-8')
    if kv_config is not None:
        param['configure'] = json.dumps(kv_config)
    body = json.dumps(param)

    headers = {'Authorization': 'APPCODE %s' % appcode}
    try:
        response = requests.post(url=url, headers=headers, data=body, timeout=10)
        return response.status_code, response.headers, response.text
    except requests.HTTPError as e:
        return e.status_code, e.headers, e.text


def vin_show(url, appcode, vin_code):
    import urllib3
    urllib3.disable_warnings()
    querys = 'vin=%s' % vin_code
    url = url + '?' + querys
    headers = {'Authorization': 'APPCODE %s' % appcode}
    try:
        response = requests.get(url=url, headers=headers, verify=False, timeout=10)
        return response.status_code, response.headers, response.text
    except requests.HTTPError as e:
        return e.status_code, e.headers, e.text
