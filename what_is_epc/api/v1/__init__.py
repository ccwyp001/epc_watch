from flask import jsonify


def OpSuccess(result=None):
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