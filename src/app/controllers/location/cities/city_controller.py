# -*- coding: utf-8 -*-
#########################################################

from app.exception import InternalServerError, NotFound
from app.models import CityModel
from app.utils import ResponseData


class CityController:

    @staticmethod
    def get_all():
        try:
            response = CityModel.get_data(export=True)
            return response
        except Exception as e:
            print('Error: {er}'.format(er=e))
            raise InternalServerError(e)

    @staticmethod
    def get_by_code(id: str):
        try:
            response = CityModel.get_by_code(id=id, export=True)
            if not response:
                raise NotFound('No se encontraron registros')
            return response
        except Exception as e:
            print('Error: {er}'.format(er=e))
            raise

    @staticmethod
    def get_by_id(id: int):
        try:
            response = CityModel.get_by_id(id=id, export=True)
            if not response:
                response = ResponseData.not_found_by_id(ide=id)
            else:
                response = ResponseData.response_get(data=response)
            return response
        except Exception as e:
            print('Error: {er}'.format(er=e))
            raise InternalServerError(e)



