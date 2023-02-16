# -*- coding: utf-8 -*-
#########################################################
from app.exception import InternalServerError, NotFound
from app.models import ApplicationModel as Model
from app.utils import ResponseData


class ApplicationController:

    @staticmethod
    def get_all():
        try:
            response = Model.get_data(export=True)
            return response
        except Exception as e:
            print('Error: {er}'.format(er=e))
            raise InternalServerError(e)

    @staticmethod
    def get_by_id(ide: int):
        try:
            response = Model.get_by_id(id=ide, export=True)
            if not response:
                response = ResponseData.not_found_by_id(ide=ide)
            else:
                response = ResponseData.response_get(data=response)
            return response
        except Exception as e:
            print('Error: {er}'.format(er=e))
            raise InternalServerError(e)

    @staticmethod
    def new_data(data: dict):
        try:
            if_exist = Model.get_by_api_key(api_key=data['apiKey'], one=True)
            if if_exist:
                response = ResponseData.response_unique(field='ApiKey', value=data['apiKey'], action='new')
                return response

            new_data = Model()
            new_data = new_data.import_data(data=data)
            Model.save_data(new_data, create=True, commit=True)
            response = ResponseData.response_save(data=Model.export_data(new_data))
            return response
        except Exception as e:
            print('Error: {er}'.format(er=e))
            raise InternalServerError(e)

    @staticmethod
    def update_data(data: dict):
        try:
            if_exist = Model.get_by_api_key(api_key=data['apiKey'], one=False)
            if len(if_exist) > 0:
                others = 0
                for detail in if_exist:
                    if detail.Id != data['id']:
                        others += 1
                if others > 0:
                    response = ResponseData.response_unique(field='ApiKey', value=data['apiKey'], action='update')
                    return response

            result = Model.get_by_id(id=data['id'], export=False)
            if not result:
                return ResponseData.not_found_by_id(ide=data['id'])
            result = Model.import_data(result, data=data)
            Model.save_data(result, create=False, commit=True)
            response = ResponseData.response_update(data={})
            return response
        except Exception as e:
            print('Error: {er}'.format(er=e))
            raise InternalServerError(e)

