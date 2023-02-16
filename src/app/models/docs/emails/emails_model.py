# -*- coding: utf-8 -*-
#########################################################

from app.models import BaseModel
from app import db
from app.exception import InternalServerError, NotFound
from sqlalchemy.orm import validates
from app.utils import FieldValidations, ResponseData


class EmailsModel(BaseModel):
    __tablename__ = 'emails'

    IssuerNit = db.Column(db.String(20), nullable=False, unique=True, comment='Nit de la empresa o emisor ')
    Imap = db.Column(db.Text, nullable=True, comment='Dirección de correo imap')
    Key = db.Column(db.String(20), nullable=False, comment='Clave de acceso al correo')
    Email = db.Column(db.String(100), nullable=True, comment='Email para recepcion de correos')
    Port = db.Column(db.String(20), nullable=True, comment='Puerto para acceder al imap')

    def export_data(self):
        return {
            'Id': self.Id,
            'CreateDate': self.CreateDate,
            'UpdateDate': self.UpdateDate,
            'IssuerNit': self.IssuerNit,
            'Imap': self.Imap,
            'Key': self.Key,
            'Email': self.Email,
            'Port': self.Port
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
        if 'Imap' in data:
            self.Imap = data['Imap']
        if 'Email' in data:
            self.Email = data['Email']
        if 'Port' in data:
            self.Port = data['Port']
        return self

    @staticmethod
    def get_data(export: bool = False):
        try:
            response = db.session.query(EmailsModel) \
                .all()
            if export:
                response = [EmailsModel.export_data(x) for x in response]
            return response
        except Exception as e:
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def get_by_id(id: int, export: bool = False):
        try:
            response = db.session.query(EmailsModel) \
                .filter(EmailsModel.Id == id) \
                .first()
            if export and response:
                response = EmailsModel.export_data(response)
            return response
        except Exception as e:
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def get_by_nit(id: str, export: bool = False):
        try:
            response = db.session.query(EmailsModel) \
                .filter(EmailsModel.IssuerNit == id) \
                .first()
            if export and response:
                response = EmailsModel.export_data(response)
            return response
        except Exception as e:
            print('Error: {er}'.format(er=e))
            response = ResponseData.internal_server_error(str(e))
            return response

    @staticmethod
    def update_data(data: dict):
        try:
            update_data = EmailsModel.get_by_id(id=data['Id'], export=False)
            if not update_data:
                return NotFound('Los datos ingresados no pertenecen o no son validos para el registro consultado')

            update_data = EmailsModel.import_data(update_data, data=data)
            EmailsModel.save(update_data, create=True, commit=True)
            response = {
                'data': EmailsModel.export_data(update_data),
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
