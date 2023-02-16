# -*- coding: utf-8 -*-
#########################################################
from app.exception import InternalServerError, NotFound
from app.models import EmailsModel
from app.utils import ResponseData


class EmailsController:

    @staticmethod
    def get_all():
        try:
            response = EmailsModel.get_data(export=True)
            return response
        except Exception as e:
            print('Error: {er}'.format(er=e))
            raise InternalServerError(e)

    @staticmethod
    def get_by_id(id: int):
        try:
            response = EmailsModel.get_by_id(id=id, export=True)
            if not response:
                response = ResponseData.not_found_by_id(ide=id)
            else:
                response = ResponseData.response_get(data=response)
            return response
        except Exception as e:
            print('Error: {er}'.format(er=e))
            raise InternalServerError(e)

    @staticmethod
    def get_by_nit(id: str):
        try:
            # if not id or isinstance(id, str):
            #     return ResponseData.bad_request('El Nit debe ser un string y diferente de null')
            response = EmailsModel.get_by_nit(id=id, export=True)
            return response
        except Exception as e:
            print('Error: {er}'.format(er=e))
            response = ResponseData.internal_server_error(str(e))
            return response

    @staticmethod
    def new_data(data: dict):
        try:
            new_data = EmailsModel()
            new_data = EmailsModel.import_data(new_data, data=data)
            EmailsModel.save(new_data, create=True, commit=True)
            response = {
                'data': EmailsModel.export_data(new_data),
                'statusCode': 201,
                'message': 'Registro almacenado correctamente'
            }
            return response
        except Exception as e:
            print('Error: {er}'.format(er=e))
            response = ResponseData.bad_request(error=str(e))
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
