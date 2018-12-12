import os

from flask import Blueprint, request, jsonify, current_app
from flask_restful import Api, Resource
from ...commons import exceptions
from ...extensions import db
from ...models import AssemblyGroups, VehicleAssemblyGroups, Vehicles
from . import OpException, OpSuccess

bp = Blueprint('assemblies', __name__)
api = Api(bp)


@api.resource('/test')
class TestApi(Resource):
    def get(self):
        pass


@api.resource('/')
class AssemblyGroupsApi(Resource):
    def get(self):
        try:
            arg = request.args['assembly_id']
            v_list = AssemblyGroups.query.filter(
                AssemblyGroups.id == arg
            ).all()
            return OpSuccess([_.display() for _ in v_list])
        except Exception as e:
            return OpException(exceptions.DataValidateError())
        finally:
            if 'db' in locals():
                db.session.close()


@api.resource('/oe_numbers')
class OemApi(Resource):
    def get(self):
        try:
            arg = request.args['assembly_id']
            v_list = VehicleAssemblyGroups.query.filter(
                VehicleAssemblyGroups.assembly_group_id == arg).with_entities(
                VehicleAssemblyGroups.oe_numbers).distinct().all()
            return OpSuccess([_.oe_numbers for _ in v_list])
        except Exception as e:
            print(str(e))
            return OpException(exceptions.DataValidateError())
        finally:
            if 'db' in locals():
                db.session.close()


@api.resource('/vehicles')
class matchVehiclesApi(Resource):
    def get(self):
        try:
            arg = request.args['assembly_id']
            v_list = db.session.query(Vehicles).join(
                VehicleAssemblyGroups, db.and_(
                    Vehicles.id == VehicleAssemblyGroups.vehicle_id,
                    VehicleAssemblyGroups.assembly_group_id == arg)).distinct().all()
            return OpSuccess([{'brand': _.brand,
                               'model': _.model,
                               'years': _.years,
                               'displacement': _.displacement}
                              for _ in v_list])
        except Exception as e:
            print(str(e))
            return OpException(exceptions.DataValidateError())
        finally:
            if 'db' in locals():
                db.session.close()


@api.resource('/oem/_search')
class AssemblyByOemApi(Resource):
    def get(self):
        try:
            arg = request.args['q']
            rule = VehicleAssemblyGroups.oe_numbers.like('%%%s%%' % arg)

            v_list = VehicleAssemblyGroups.query.filter(rule).with_entities(
                VehicleAssemblyGroups.oe_numbers,
                VehicleAssemblyGroups.assembly_group_id).distinct().all()
            return OpSuccess(
                [{'oe_number': _.oe_numbers,
                  'assembly_id': _.assembly_group_id} for _ in v_list])
        except Exception as e:
            print(str(e))
            return OpException(exceptions.DataValidateError())
        finally:
            if 'db' in locals():
                db.session.close()


@api.resource('/_search')
class SearchApi(Resource):
    def get(self):
        try:
            arg = request.args['q']
            rule = AssemblyGroups.id.like('%%%s%%' % arg)
            v_list = AssemblyGroups.query.filter(rule).all()
            return OpSuccess(
                [_.id for _ in v_list])
        except Exception as e:
            print(str(e))
            return OpException(exceptions.DataValidateError())
        finally:
            if 'db' in locals():
                db.session.close()
