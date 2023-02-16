# -*- coding: utf-8 -*-
#########################################################
from typing import Dict

from app.exception import InternalServerError, NotFound, BadRequest
from app.models import CertsModel
from app.utils import ResponseData


class CertsController:

    @staticmethod
    def get_all():
        try:
            response = CertsModel.get_data(export=True)
            return response
        except Exception as e:
            print('Error: {er}'.format(er=e))
            raise InternalServerError(e)

    @staticmethod
    def get_by_id(id: int):
        try:
            response = CertsModel.get_by_id(id=id, export=True)
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
            response = CertsModel.get_by_nit(id=id, export=True)
            return response
        except Exception as e:
            print('Error: {er}'.format(er=e))
            response = ResponseData.internal_server_error(str(e))
            return response

    @staticmethod
    def add_new_certificate(data: dict) -> dict:
        try:
            # consultamos si existe un certificado por el nit del emisor
            certificate: CertsModel = CertsModel.get_by_nit(id=data["IssuerNit"], export=False)
            # en caso de no existir se crea un nuevo registro con los datos enviados
            if not certificate:
                new_certificate = CertsModel()
                new_certificate = CertsModel.import_data(self=new_certificate, data=data)
                CertsModel.save(self=new_certificate, create=True, commit=True)
                response = {
                    'operation': 'Save',
                    'statusCode': 201,
                    'message': 'Certificado agregado correctamente.'
                }
            else:
                # en caso de que exista un registro, actualizamos los valores
                certificate.Format = data["Format"]
                certificate.Key = data["Key"]
                certificate.Description = data["Description"]
                certificate.DueDate = data["DueDate"]
                CertsModel.save(self=certificate, commit=True, create=False)
                response = {
                    'operation': 'Update',
                    'statusCode': 200,
                    'message': 'Certificado modificado correctamente'
                }
            return response
        except Exception as e:
            print(e)
            raise BadRequest('Error: {er}'.format(er=e))

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
