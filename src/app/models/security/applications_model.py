# -*- coding: utf-8 -*-
#########################################################

from app.models import BaseModel
from app import db
from app.exception import InternalServerError
from sqlalchemy.orm import validates
from app.utils import FieldValidations
from datetime import datetime
from flask import g


class ApplicationModel(BaseModel):
    __tablename__ = 'applications'

    ApiKey = db.Column(db.String(100), unique=True, nullable=False, comment='Api Key de acceso')
    ApiSecret = db.Column(db.String(100), nullable=False, unique=False, comment='Api Secret de acceso ')

    def export_data(self):
        return {
            'apiKey': self.ApiKey,
            'apiSecret': self.ApiSecret
        }

    def import_data(self, data):
        if 'createDate' in data:
            self.CreateDate = data['createDate']
        if 'updateDate' in data:
            self.UpdateDate = data['updateDate']
        if 'createBy' in data:
            self.CreateBy = data['createBy']
        if 'updateBy' in data:
            self.UpdateBy = data['updateBy']
        if 'isDeleted' in data:
            self.IsDeleted = data['isDeleted']
        if 'apiKey' in data:
            self.ApiKey = data['apiKey']
        if 'apiSecret' in data:
            self.ApiSecret = data['apiSecret']
        return self

    def save_data(self, create: bool = False, commit: bool = False):
        try:
            if create:
                self.CreateDate = datetime.now()
                self.CreateBy = g.user_name
            self.UpdateDate = datetime.now()
            self.UpdateBy = g.user_name
            self.IsDeleted = 0
            db.session.add(self)
            db.session.flush()
            if commit:
                db.session.commit()
            return self
        except Exception as e:
            print(e)
            db.session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def get_data(export: bool = False):
        try:
            response = db.session.query(ApplicationModel) \
                .all()
            if export:
                response = [ApplicationModel.export_data(x) for x in response]
            return response
        except Exception as e:
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def get_by_apikey_and_api_secret(api_key: str, api_secret: str, export: bool = True):
        try:
            response = db.session.query(ApplicationModel) \
                .filter(ApplicationModel.ApiKey == api_key,
                        ApplicationModel.ApiSecret == api_secret) \
                .first()
            if export and response:
                response = ApplicationModel.export_data(response)
            return response
        except Exception as e:
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def get_by_id(id: int, export: bool = False):
        try:
            response = db.session.query(ApplicationModel) \
                .filter(ApplicationModel.Id == id) \
                .first()
            if export and response:
                response = ApplicationModel.export_data(response)
            return response
        except Exception as e:
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def get_by_api_key(api_key: str, export: bool = False, one: bool = False):
        try:
            response = db.session.query(ApplicationModel) \
                .filter(ApplicationModel.ApiKey == api_key)
            if one:
                response = response.first()
            else:
                response = response.all()

            if export and response:
                if one:
                    response = ApplicationModel.export_data(response)
                else:
                    response = [ApplicationModel.export_data(x) for x in response]
            return response
        except Exception as e:
            print(e)
            raise InternalServerError(e)

    @validates(('ApiKey', 'ApiSecret'))
    def validate_name_permit(self, key, name):
        try:
            FieldValidations.is_none(key, name)
            FieldValidations.is_empty(key, name)
            return name
        except Exception as e:
            print(e)
            raise InternalServerError(e)
