# -*- coding: utf-8 -*-
#########################################################

from app.models import BaseModel
from app import db
from app.exception import InternalServerError
from sqlalchemy.orm import validates
from app.utils import FieldValidations


class DepartmentModel(BaseModel):
    __tablename__ = 'departments'

    code = db.Column(db.String(10), unique=True, nullable=False, comment='Codigo departamento ')
    name = db.Column(db.String(100), nullable=False, comment='Nombre ')

    def export_data(self):
        return {
            'Id': self.Id,
            'CreateDate': self.CreateDate,
            'UpdateDate': self.UpdateDate,
            'code': self.code,
            'name': self.name

        }

    def import_data(self, data):
        if 'CreateDate' in data:
            self.CreateDate = data['CreateDate']
        if 'UpdateDate' in data:
            self.UpdateDate = data['UpdateDate']
        if 'CreateBy' in data:
            self.CreateBy = data['CreateBy']
        if 'UpdateBy' in data:
            self.UpdateBy = data['UpdateBy']
        if 'IsDeleted' in data:
            self.IsDeleted = data['IsDeleted']
        if 'code' in data:
            self.code = data['code']
        if 'name' in data:
            self.name = data['name']

        return self

    @staticmethod
    def get_data(export: bool = False):
        try:
            response = db.session.query(DepartmentModel) \
                .all()
            if export:
                response = [DepartmentModel.export_data(x) for x in response]
            return response
        except Exception as e:
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def get_by_code(id: str, export: bool = False):
        try:
            response = db.session.query(DepartmentModel) \
                .filter(DepartmentModel.code == id) \
                .first()
            if export and response:
                response = DepartmentModel.export_data(response)
            return response
        except Exception as e:
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def get_by_id(id: int, export: bool = False):
        try:
            response = db.session.query(DepartmentModel) \
                .filter(DepartmentModel.id == id) \
                .first()
            if export and response:
                response = DepartmentModel.export_data(response)
            return response
        except Exception as e:
            print(e)
            raise InternalServerError(e)

    @validates(('name', 'email', 'status'))
    def validate_name_permit(self, key, name):
        try:
            FieldValidations.is_none(key, name)
            FieldValidations.is_empty(key, name)
            return name
        except Exception as e:
            print(e)
            raise InternalServerError(e)
