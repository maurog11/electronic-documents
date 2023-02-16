# -*- coding: utf-8 -*-
#########################################################

from app.exception import InternalServerError, NotFound
from app.models import ConsecutiveNotesModel
from app import db


class ConsecutiveNotesController:

    @staticmethod
    def get_all():
        try:
            response = ConsecutiveNotesModel.get_data(export=True)
            return response
        except Exception as e:
            print('Error: {er}'.format(er=e))
            raise InternalServerError(e)

    @staticmethod
    def get_by_id(id: int):
        try:
            response = ConsecutiveNotesModel.get_by_id(id=id, export=True)
            if not response:
                raise NotFound('No se encontraron datos para la consulta.+')
            return response
        except Exception as e:
            print('Error: {er}'.format(er=e))
            raise

    @staticmethod
    def new_data(data: dict):
        try:
            new_data = ConsecutiveNotesModel()
            new_data = ConsecutiveNotesModel.import_data(new_data, data=data)
            ConsecutiveNotesModel.save(new_data, create=True, commit=True)
            response = {
                'data': ConsecutiveNotesModel.export_data(new_data),
                'statusCode': 201,
                'message': 'Registro almacenado correctamente'
            }
            return response
        except Exception as e:
            print('Error: {er}'.format(er=e))
            raise InternalServerError(e)

    @staticmethod
    def update_data(data: dict):
        try:
            update_data = ConsecutiveNotesModel.get_by_id(id=data['id'], export=False)
            if not update_data:
                return NotFound('Los datos ingresados no pertenecen o no son validos para el registro consultado')
            update_data = ConsecutiveNotesModel.import_data(update_data, data=data)
            ConsecutiveNotesModel.save(update_data, create=True, commit=True)
            response = {
                'data': ConsecutiveNotesModel.export_data(update_data),
                'statusCode': 200,
                'message': 'Registro modificado correctamente'
            }
            return response
        except Exception as e:
            print('Error: {er}'.format(er=e))
            raise

    @staticmethod
    def delete_data(id: int):
        try:
            delete_data = ConsecutiveNotesModel.get_by_id(id=id, export=False)
            if not delete_data:
                return NotFound('Los datos ingresados no pertenecen o no son validos para el registro consultado')
            ConsecutiveNotesModel.delete(delete_data, commit=True)
            response = {
                'statusCode': 200,
                'message': 'Registro eliminado correctamente'
            }
            return response
        except Exception as e:
            print('Error: {er}'.format(er=e))
            raise
