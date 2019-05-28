# coding:utf-8
import json
from functools import wraps
from flask import Blueprint, request, jsonify, current_app
from flask_restful import Api, Resource
from ...commons import exceptions
from . import OpSuccess, OpException, USER_ROLE
from ...models import Users
from ...extensions import db
from flask_jwt_extended import (
    jwt_required, create_access_token, jwt_refresh_token_required,
    create_refresh_token, get_jwt_identity)
from flask_bcrypt import check_password_hash, generate_password_hash
from datetime import datetime

bp = Blueprint('users', __name__)
api = Api(bp)


def double_wrap(f):
    @wraps(f)
    def new_dec(*args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            # actual decorated function
            return f(args[0])
        else:
            # decorator arguments
            return lambda real_f: f(real_f, *args, **kwargs)

    return new_dec


@double_wrap
def check_identity(fn, roles=0):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        _ = json.loads(current_user)
        if _.get('roles', 0) & roles:
            return fn(*args, **kwargs)
        return OpException(exceptions.InsufficientPrivilege())

    return wrapper


@api.resource('/test')
class TestApi(Resource):
    @jwt_required
    @check_identity(roles=USER_ROLE['PERM'])
    def get(self):
        pass


@api.resource('/login')
class Login(Resource):
    def post(self):
        try:
            data = request.json
            username = data['username']
            user = Users.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, data['password']):
                if user.roles < USER_ROLE['PERM']:
                    return OpException(exceptions.InsufficientPrivilege())
                identity = json.dumps({'id': user.id, 'roles': user.roles})
                access_token = create_access_token(identity=identity)
                refresh_token = create_refresh_token(identity=identity)
                return OpSuccess({"access_token": access_token,
                                  "refresh_token": refresh_token})
            return OpException(exceptions.AccountLoginFailed())
        except:
            return OpException(exceptions.AccountLoginFailed())


@api.resource('/token')
class Refresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        print(current_user)
        ret = {
            'access_token': create_access_token(identity=current_user)
        }
        return OpSuccess(ret)


@api.resource('/', '/<int:id>')
class UserApi(Resource):
    @jwt_required
    @check_identity(roles=USER_ROLE['PERM'])
    def get(self, id):
        try:
            user = Users.query.get(id)
            return OpSuccess(user.display())
        except:
            return OpException(exceptions.DataValidateError())

    def post(self):
        try:
            data = request.json
            username = data['username']
            user = Users.query.filter_by(username=username).first()
            if user:
                if user.roles:
                    return OpException(exceptions.UserAlreadyExist())
                else:
                    db.session.delete(user)
                    db.session.flush()
            user = Users.from_json(data)
            db.session.add(user)
            db.session.commit()
            return OpSuccess(message='申请已提交', result_code=202)
        except:
            db.session.rollback()
            return OpException(exceptions.DataValidateError())
        finally:
            if 'db' in locals():
                db.session.close()

    @jwt_required
    @check_identity(roles=USER_ROLE['ADM'])
    def put(self):
        try:
            data = request.json
            username = data['username']
            user = Users.query.filter_by(username=username).first()
            if user:
                if user.roles:
                    return OpException(exceptions.UserAlreadyExist())
                else:
                    db.session.delete(user)
                    db.session.flush()
            user = Users.from_json(data)
            user.roles = USER_ROLE['PERM']
            db.session.add(user)
            db.session.commit()
            return OpSuccess(message='用户已创建', result_code=201)
        except:
            db.session.rollback()
            return OpException(exceptions.DataValidateError())
        finally:
            if 'db' in locals():
                db.session.close()

    @jwt_required
    @check_identity(roles=USER_ROLE['ADM'])
    def delete(self, id):
        try:
            user = Users.query.get(id)
            jwt_info = json.loads(get_jwt_identity())
            if id == jwt_info.get('id', 0):
                return OpException(exceptions.DataValidateError())
            db.session.delete(user)
            db.session.commit()
            return OpSuccess(message='用户已删除', result_code=200)
        except Exception as e:
            # print(str(e))
            return OpException(exceptions.DataValidateError())

    @jwt_required
    @check_identity(roles=USER_ROLE['PERM'])
    def patch(self, id):
        try:
            data = request.json
            user = Users.query.get(id)
            jwt_info = json.loads(get_jwt_identity())
            old_password = data['old_pwd']
            new_password = data['new_pwd']
            if id != jwt_info.get('id', 0):
                return OpException(exceptions.InsufficientPrivilege())
            if user and check_password_hash(user.password, old_password) and new_password:
                user.password = generate_password_hash(new_password)
                user.update_at = datetime.utcnow()
                db.session.add(user)
                db.session.commit()
                return OpSuccess(message='密码已更新', result_code=200)
            return OpException(exceptions.DataValidateError())
        except:
            return OpException(exceptions.DataValidateError())


@api.resource('/temp', '/temp/<int:id>')
class TempUserApi(Resource):
    @jwt_required
    @check_identity(roles=USER_ROLE['ADM'])
    def get(self):
        try:
            user = Users.query.filter(Users.roles == USER_ROLE['TEMP']).all()
            return OpSuccess([_.display() for _ in user])
        except:
            return OpException(exceptions.DataValidateError())

    @jwt_required
    @check_identity(roles=USER_ROLE['ADM'])
    def put(self, id):
        try:
            user = Users.query.get(id)
            if user.roles == USER_ROLE['TEMP']:
                user.roles = USER_ROLE['PERM']
                user.update_at = datetime.utcnow()
                db.session.add(user)
                db.session.commit()
                return OpSuccess(message='权限已更新', result_code=200)
            return OpException(exceptions.DataValidateError())
        except Exception as e:
            # print(str(e))
            db.session.rollback()
            return OpException(exceptions.DataValidateError())
        finally:
            if 'db' in locals():
                db.session.close()


@api.resource('/perm', '/perm/<int:id>')
class PermUserApi(Resource):
    @jwt_required
    @check_identity(roles=USER_ROLE['ADM'])
    def get(self):
        try:
            user = Users.query.filter(Users.roles == USER_ROLE['PERM']).all()
            return OpSuccess([_.display() for _ in user])
        except:
            return OpException(exceptions.DataValidateError())
