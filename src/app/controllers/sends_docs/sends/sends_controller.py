# -*- coding: utf-8 -*-
#########################################################
from typing import Dict, Any
from flask import make_response, jsonify
from app.exception import InternalServerError
from app.models import SendsModel
from app.utils import ResponseData


class SendsController:

    @staticmethod
    def all(data: Dict[str, int]):
        try:
            pageNumber, pageSize = (data["pageNumber"], data["pageSize"])
            db_data = SendsModel.get_data(export=True, pageNumber=pageNumber, pageSize=pageSize)
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
    def get_by(data: Dict[str, Any]):
        try:
            pageNumber, pageSize = (data["pageNumber"], data["pageSize"])
            db_data = SendsModel.get_by(data=data, export=True, pageNumber=pageNumber, pageSize=pageSize)
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
    def get_by_id(id: int):
        try:
            if not id and not isinstance(id, int):
                raise ValueError('El id debe ser un entero, y diferente de null')

            response = SendsModel.get_by_id(id=id, export=True)
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
    def get_by_number(Nit: str, SeriePrefix: str, SerieNumber: str, DocType: str):
        try:
            response = SendsModel.get_by_number(Nit=Nit, SeriePrefix=SeriePrefix, SerieNumber=SerieNumber, DocType=DocType, export=True)
            if not response:
                response = ResponseData.not_found()
            return response
        except Exception as e:
            print('Error: {er}'.format(er=e))
            raise InternalServerError(e)

    @staticmethod
    def pdf(data: Dict[str, str]):
        try:
            Nit = data['Nit']
            SeriePrefix = data['SeriePrefix']
            SerieNumber = data['SerieNumber']
            DocType = data['DocType']
            db_data = SendsModel.get_by_number(Nit=Nit, SeriePrefix=SeriePrefix, SerieNumber=SerieNumber,
                                                DocType=DocType, export=True)
            xml: str = ''
            pdf: str = ''
            if not db_data:
                response = ResponseData.not_found()
                return response
            pdf = SendsModel.export_pdf(db_data)
            xml = SendsController.xml(data=data)

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
            db_data = SendsModel.get_by_number(Nit=Nit, SeriePrefix=SeriePrefix, SerieNumber=SerieNumber,
                                                      DocType=DocType, export=True)
            if not db_data:
                response = ResponseData.not_found()
                return response
            else:
                xml = SendsModel.export_xml(db_data)
                return xml
        except KeyError as e:
            print('Error: {er}'.format(er=e))
            response = ResponseData.bad_request(error=str(e))
            return response


    @staticmethod
    def new_data(data: dict):
        try:
            new_data = SendsModel()
            new_data = SendsModel.import_data(new_data, data=data)
            new_data = new_data.import_data(data=data)
            SendsModel.save(new_data, create=True, commit=True)
            response = ResponseData.response_save(data=SendsModel.export_data(new_data))
            return response
        except Exception as e:
            print('Error: {er}'.format(er=e))
            response = ResponseData.bad_request(error=str(e))
            return response

    @staticmethod
    def update_data(data: dict):
        try:
            result = SendsModel.get_by_id(id=data['Id'], export=False)
            if not result:
                return ResponseData.not_found()
            result = SendsModel.import_data(result, data=data)
            SendsModel.save_data(result, create=False, commit=True)
            response = ResponseData.response_update(data={})
            return response
        except Exception as e:
            print('Error: {er}'.format(er=e))
            response = ResponseData.bad_request(error=str(e))
            return response


