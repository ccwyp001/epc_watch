from flask import jsonify

USER_ROLE = {
    'REJECT': 0x0,
    'TEMP': 0x1,
    'PERM': 0x2,
    'ADM': 0x4
}


def OpSuccess(result=None, message='成功', result_code=200):
    business_code = '100000'
    data = {}
    data['code'] = business_code
    data['message'] = message
    if result is not None:
        data['result'] = result
    return data, result_code


def OpException(exception):
    return exception.to_dict(), exception.http_code
