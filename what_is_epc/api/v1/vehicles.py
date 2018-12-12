import os

from flask import Blueprint, request
from flask_restful import Api, Resource
from ...commons import exceptions
from . import OpSuccess, OpException
from ...extensions import db
from ...models import Vehicles, VehicleAssemblyGroups, AssemblyGroups
import csv
import tempfile

bp = Blueprint('vehicles', __name__)
api = Api(bp)

VehicleMenu = ['manufacturer', 'brand', 'model', 'displacement', 'years', 'mode']
AssemblyGMenu = ['outer_teething_wheel', 'inner_teething_wheel', 'length',
                 'abs', 'material_number']
VAGMenu = ['assembly_group_id', 'side', 'oe_numbers', 'other_numbers']


def csv_read(csv_file):
    with open(csv_file) as f:
        reader = csv.reader(f, delimiter=",")
        l = ['manufacturer', 'brand', 'model', 'displacement', 'years', 'mode',
             'side', 'oe_numbers', 'other_numbers',
             'assembly_group_id', 'outer_teething_wheel', 'inner_teething_wheel', 'length',
             'abs', 'material_number']
        n = []
        for line in reader:
            d = dict(zip(l, line))
            n.append(d)
            # print(line)
    return n


@api.resource('/csv')
class VehiclesApi(Resource):
    def get(self):
        pass

    def post(self):
        try:
            file = request.files['file']
            # make temp file
            tmp = tempfile.mktemp()
            file.save(tmp)
            data_list = csv_read(tmp)
            os.unlink(tmp)
            # step 1 insert vehicles info
            db.session.execute(
                Vehicles.__table__.insert().prefix_with("IGNORE"),
                [dict([(key, data[key]) for key in VehicleMenu]) for data in data_list]
            )

            # step 2 insert assembly groups info
            db.session.execute(
                AssemblyGroups.__table__.insert().prefix_with("IGNORE"),
                [dict(dict([(key, data[key]) for key in AssemblyGMenu]),
                      **{'id': data['assembly_group_id']}) for data in data_list]
            )

            # step 3 insert relationships info
            db.session.execute(
                VehicleAssemblyGroups.__table__.insert().prefix_with("IGNORE"),
                [dict(dict([(key, data[key]) for key in VAGMenu]),
                      **{
                          'vehicle_id': db.session.query(Vehicles).filter(
                              Vehicles.brand == data['brand'],
                              Vehicles.manufacturer == data['manufacturer'],
                              Vehicles.model == data['model'],
                              Vehicles.displacement == data['displacement'],
                              Vehicles.years == data['years'],
                              Vehicles.mode == data['mode']).first().id
                      }) for data in data_list]
            )
            db.session.commit()

            return OpSuccess()

        except Exception as e:
            # print(str(e))
            db.session.rollback()
            return OpException(exceptions.DataValidateError())
        finally:
            if 'db' in locals():
                db.session.close()


@api.resource('/_search')
class SearchApi(Resource):
    def get(self):
        try:
            arg = request.args['q']
            rule = db.or_(Vehicles.manufacturer.like('%%%s%%' % arg),
                          Vehicles.model.like('%%%s%%' % arg)
                          )
            v_list = Vehicles.query.filter(rule).with_entities(Vehicles.manufacturer,
                                                               Vehicles.model).distinct().all()
            return OpSuccess(
                [{'manufacturer': _.manufacturer,
                  'model': _.model} for _ in v_list])
        except Exception as e:
            print(str(e))
            return OpException(exceptions.DataValidateError())
        finally:
            if 'db' in locals():
                db.session.close()
