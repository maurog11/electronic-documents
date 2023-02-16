# -*- coding: utf-8 -*-
#########################################################
from typing import Dict, Any
from flask import make_response, jsonify
from app.exception import InternalServerError, NotFound
from app.models import NotesSendsModel
from app.utils import ResponseData


class NotesSendsController:

    @staticmethod
    def all(data: Dict[str, int]):
        try:
            pageNumber, pageSize = (data["pageNumber"], data["pageSize"])
            db_data = NotesSendsModel.get_data(export=True, pageNumber=pageNumber, pageSize=pageSize)
            if not db_data:
                response = ResponseData.not_found()
                return response
            response = make_response(jsonify(db_data), 200)
            return response
        except KeyError as e:
            print('Error: {er}'.format(er=e))
            response = ResponseData.bad_request(error=str(e))
            return response

    @staticmethod
    def pdf(data: Dict[str, str]):
        try:
            Nit = data['Nit']
            SeriePrefix = data['SeriePrefix']
            SerieNumber = data['SerieNumber']
            DocType = data['DocType']
            db_data = NotesSendsModel.get_by_number(Nit=Nit, SeriePrefix=SeriePrefix, SerieNumber=SerieNumber,
                                               DocType=DocType, export=True)
            xml: str = ''
            pdf: str = ''
            if not db_data:
                response = ResponseData.not_found()
                return response

            pdf = NotesSendsModel.export_pdf(db_data)
            xml = NotesSendsController.xml(data=data)

            response = {
                'pdf': pdf,
                'xml': xml
            }
            return make_response(response, 200)
        except KeyError as e:
            print('Error: {er}'.format(er=e))
            response = ResponseData.bad_request(error=str(e))
            return response

    @staticmethod
    def xml(data: Dict[str, str]):
        try:
            Nit = data['Nit']
            SeriePrefix = data['SeriePrefix']
            SerieNumber = data['SerieNumber']
            DocType = data['DocType']
            db_data = NotesSendsModel.get_by_number(Nit=Nit, SeriePrefix=SeriePrefix, SerieNumber=SerieNumber,
                                               DocType=DocType, export=True)
            if not db_data:
                response = ResponseData.not_found()
                return response
            else:
                xml = NotesSendsModel.export_xml(db_data)
                return xml
        except KeyError as e:
            print('Error: {er}'.format(er=e))
            response = ResponseData.bad_request(error=str(e))
            return response

    @staticmethod
    def get_by_id(id: int):
        try:
            if not id and not isinstance(id, int):
                raise ValueError('El id debe ser un entero, y diferente de null')

            response = NotesSendsModel.get_by_id(id=id, export=True)
            if not response:
                response = ResponseData.not_found_by_id(ide=id)
            else:
                response = ResponseData.response_get(data=response)
            return response
        except Exception as e:
            print('Error: {er}'.format(er=e))
            response = ResponseData.bad_request(str(e))
            return response

    @staticmethod
    def get_by_nds(data: dict, pageNumber=0, pageSize=None):
        try:
            response = NotesSendsModel.get_by(data=data, export=True, pageNumber=pageNumber, pageSize=pageSize)
            if not response:
                response = ResponseData.not_found()
            return response
        except Exception as e:
            print('Error: {er}'.format(er=e))
            raise InternalServerError(e)

    @staticmethod
    def get_by(data: Dict[str, Any]):
        try:
            pageNumber, pageSize = (data["pageNumber"], data["pageSize"])
            db_data = NotesSendsModel.get_by(data=data, export=True, pageNumber=pageNumber, pageSize=pageSize)
            if not db_data:
                response = ResponseData.not_found()
                return response
            response = make_response(jsonify(db_data), 200)
            return response
        except KeyError as e:
            print('Error: {er}'.format(er=e))
            response = ResponseData.bad_request(error=str(e))
            return response

    @staticmethod
    def get_by_number(Nit: str, SeriePrefix: str, SerieNumber: str, DocType: str):
        try:
            response = NotesSendsModel.get_by_number(Nit=Nit, SeriePrefix=SeriePrefix, SerieNumber=SerieNumber, DocType=DocType, export=True)
            if not response:
                raise NotFound('No se encontraron datos para la consulta.+')
            return response
        except Exception as e:
            print('Error: {er}'.format(er=e))
            raise

    @staticmethod
    def new_data(data: dict):
        try:
            new_data = NotesSendsModel()
            new_data = NotesSendsModel.import_data(new_data, data=data)
            NotesSendsModel.save(new_data, create=True, commit=True)
            response = {
                'data': NotesSendsModel.export_data(new_data),
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
            update_data = NotesSendsModel.get_by_id(id=data['Id'], export=False)
            if not update_data:
                return NotFound('Los datos ingresados no pertenecen o no son validos para el registro consultado')
            update_data = NotesSendsModel.import_data(update_data, data=data)
            NotesSendsModel.save(update_data, create=True, commit=True)
            response = {
                'data': NotesSendsModel.export_data(update_data),
                'statusCode': 200,
                'message': 'Registro modificado correctamente'
            }
            return response
        except Exception as e:
            print('Error: {er}'.format(er=e))
            raise

