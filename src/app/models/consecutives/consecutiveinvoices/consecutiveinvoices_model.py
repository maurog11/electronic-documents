# -*- coding: utf-8 -*-
#########################################################

from app.models import BaseModel
from app import db
from app.exception import InternalServerError
from sqlalchemy.orm import validates
from app.utils import FieldValidations


class ConsecutiveInvoicesModel(BaseModel):
    __tablename__ = 'consecutiveinvoices'

    IssuerNit = db.Column(db.String(20), unique=False, nullable=False, comment='Nit ')
    DocType = db.Column(db.String(5), nullable=False, unique=False, comment='FV factura DS Documento soporte ')
    YearSend = db.Column(db.String(4), nullable=False, unique=False,comment='Año de envio, se reinicia cada año')
    Consecutive = db.Column(db.Float, nullable=False, unique=False,comment='Consecutivo actual')

    def export_data(self):
        return {
            'CreateDate': self.CreateDate,
            'UpdateDate': self.UpdateDate,
            'CreateBy': self.CreateBy,
            'UpdateBy': self.UpdateBy,
            'IsDeleted': self.IsDeleted,
            'IssuerNit': self.IssuerNit,
            'DocType': self.DocType,
            'YearSend': self.YearSend,
            'Consecutive': self.Consecutive
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
        if 'IssuerNit' in data:
            self.IssuerNit = data['IssuerNit']
        if 'DocType' in data:
            self.DocType = data['DocType']
        if 'YearSend' in data:
            self.YearSend = data['YearSend']
        if 'Consecutive' in data:
            self.Consecutive = data['Consecutive']

        return self

    @staticmethod
    def get_data(export: bool = False):
        try:
            response = db.session.query(ConsecutiveInvoicesModel) \
                .all()
            if export:
                response = [ConsecutiveInvoicesModel.export_data(x) for x in response]
            return response
        except Exception as e:
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def get_by_id(id: int, export: bool = False):
        try:
            response = db.session.query(ConsecutiveInvoicesModel) \
                .filter(ConsecutiveInvoicesModel.id == id) \
                .first()
            if export and response:
                response = ConsecutiveInvoicesModel.export_data(response)
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
