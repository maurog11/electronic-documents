# -*- coding: utf-8 -*-
#########################################################

from app.exception import InternalServerError, NotFound
from app.models import ConsecutivePayRollModel
from app import db


class ConsecutivePayRollController:

    @staticmethod
    def get_all():
        try:
            response = ConsecutivePayRollModel.get_data(export=True)
            return response
        except Exception as e:
            print('Error: {er}'.format(er=e))
            raise InternalServerError(e)

    @staticmethod
    def get_by_id(id: int):
        try:
            response = ConsecutivePayRollModel.get_by_id(id=id, export=True)
            if not response:
                raise NotFound('No se encontraron datos para la consulta.+')
            return response
        except Exception as e:
            print('Error: {er}'.format(er=e))
            raise

    @staticmethod
    def new_data(data: dict):
        try:
            new_data = ConsecutivePayRollModel()
            new_data = ConsecutivePayRollModel.import_data(new_data, data=data)
            ConsecutivePayRollModel.save(new_data, create=True, commit=True)
            '''
            data1 = request.get_json()
            film_dict = schema.ExampleSchema.load(data1)
            film = ExampleModel(name=film_dict['name'],
                                email=film_dict['email'],
                                status=film_dict['status'],
                                CreateDate=film_dict['CreateDate'],
                                UpdateDate=film_dict['UpdateDate'],
                                CreateBy=film_dict['CreateBy'],
                                UpdateBy=film_dict['UpdateBy'],
                                IsDeleted=film_dict['IsDeleted']
                                )
            for actor in film_dict['actors']:
                film.actors.append(ExampleDetailsModel(actor['name']))
            film.save()
            '''

            for actor in data["actors"]:
                ConsecutivePayRollModel.actors.append(ConsecutivePayRollModel(actor['name']))

            db.session.add(ConsecutivePayRollModel.actors)
            db.session.commit()

            response = {
                'data': ConsecutivePayRollModel.export_data(new_data),
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
            update_data = ConsecutivePayRollModel.get_by_id(id=data['id'], export=False)
            if not update_data:
                return NotFound('Los datos ingresados no pertenecen o no son validos para el registro consultado')
            update_data = ConsecutivePayRollModel.import_data(update_data, data=data)
            ConsecutivePayRollModel.save(update_data, create=True, commit=True)
            response = {
                'data': ConsecutivePayRollModel.export_data(update_data),
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
            delete_data = ConsecutivePayRollModel.get_by_id(id=id, export=False)
            if not delete_data:
                return NotFound('Los datos ingresados no pertenecen o no son validos para el registro consultado')
            ConsecutivePayRollModel.delete(delete_data, commit=True)
            response = {
                'statusCode': 200,
                'message': 'Registro eliminado correctamente'
            }
            return response
        except Exception as e:
            print('Error: {er}'.format(er=e))
            raise
