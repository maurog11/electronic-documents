# -*- coding: utf-8 -*-
#########################################################

from app.models import BaseModel
from app import db
from app.exception import InternalServerError, NotFound
from sqlalchemy.orm import validates
from app.utils import FieldValidations, ResponseData


class CertsModel(BaseModel):
    __tablename__ = 'certs'

    IssuerNit = db.Column(db.String(20), nullable=False, unique=True, comment='Nit de la empresa o emisor ')
    Format = db.Column(db.Text, nullable=True, comment='pdf del documento en bytes')
    Key = db.Column(db.String(20), nullable=False, comment='Nit de la empresa o emisor ')
    Description = db.Column(db.String(100), nullable=True, comment='descripcion del documento')
    DueDate = db.Column(db.String(20), nullable=True, comment='descripcion del documento')

    def export_data(self):
        return {
            'Id': self.Id,
            'CreateDate': self.CreateDate,
            'UpdateDate': self.UpdateDate,
            'IssuerNit': self.IssuerNit,
            'Key': self.Key,
            'Format': self.Format,
            'Description': self.Description,
            'DueDate': self.DueDate
        }

    def import_data(self, data):
        if 'CreateDate' in data:
            self.CreateDate = data['CreateDate']
        if 'UpdateDate' in data:
            self.UpdateDate = data['UpdateDate']
        if 'IssuerNit' in data:
            self.IssuerNit = data['IssuerNit']
        if 'Key' in data:
            self.Key = data['Key']
        if 'Format' in data:
            self.Format = data['Format']
        if 'Description' in data:
            self.Description = data['Description']
        if 'DueDate' in data:
            self.DueDate = data['DueDate']
        return self

    @staticmethod
    def get_data(export: bool = False):
        try:
            response = db.session.query(CertsModel) \
                .all()
            if export:
                response = [CertsModel.export_data(x) for x in response]
            return response
        except Exception as e:
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def get_by_id(id: int, export: bool = False):
        try:
            response = db.session.query(CertsModel) \
                .filter(CertsModel.Id == id) \
                .first()
            if export and response:
                response = CertsModel.export_data(response)
            return response
        except Exception as e:
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def get_by_nit(id: str, export: bool = False):
        try:
            response = db.session.query(CertsModel) \
                .filter(CertsModel.IssuerNit == id) \
                .first()
            if export and response:
                response = CertsModel.export_data(response)
            return response
        except Exception as e:
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def update_data(data: dict):
        try:
            update_data = CertsModel.get_by_id(id=data['Id'], export=False)
            if not update_data:
                return NotFound('Los datos ingresados no pertenecen o no son validos para el registro consultado')

            update_data = CertsModel.import_data(update_data, data=data)
            CertsModel.save(update_data, create=True, commit=True)
            response = {
                'data': CertsModel.export_data(update_data),
                'statusCode': 200,
                'message': 'Registro modificado correctamente'
            }
            return response
        except Exception as e:
            print('Error: {er}'.format(er=e))
            response = ResponseData.internal_server_error(str(e))
            return response

    @validates(('name', 'email', 'status'))
    def validate_name_permit(self, key, name):
        try:
            FieldValidations.is_none(key, name)
            FieldValidations.is_empty(key, name)
            return name
        except Exception as e:
            print(e)
            raise InternalServerError(e)
