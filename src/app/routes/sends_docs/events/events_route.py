# -*- coding: utf-8 -*-
#########################################################
from flask import request, make_response, jsonify
from app.controllers import EventsController as Controller
from app.auth import auth_token
from flask_restx import Resource
from app.utils import validate_json
from .schemas import EventsModelAcuse, EventsModelReceipt, EventsModelAccept, EventsModelClaim, EventsModelTacitAccept,\
    EventsFilterNumberModel, EventsFilterModel, allEventsModel, statusEventModel, api


@api.route('/all', methods=['POST'])
@api.response(200, 'Registros encontrados')
@api.response(404, 'No se encontraron registros')
@api.response(500, 'Se presentó un error en el servidor.')
class All(Resource):
    decorators = [auth_token.login_required]

    @api.doc('get_all_events')
    @api.expect(allEventsModel)
    def post(self):
        """

        Consulta registros almacenados en la base de datos por numero y tamaño de pagina
        """
        data = request.json
        response = Controller.all(data=data)
        return response


@api.route('/data/<int:id>/get', methods=['GET'])
@api.response(401, 'La peticion carece de un id')
@api.response(404, 'Registro no encontrado.')
@api.response(500, 'Se presentó un error en el servidor.')
@api.param('id', 'Identificador de envio')
class GetByid(Resource):
    decorators = [auth_token.login_required]

    @api.doc('get_invoice_by_id')
    def get(self, id):
        """

        Obtiene un registro dado su id
        """
        response = Controller.get_by_id(id)
        return response


@api.route('/getby', methods=['POST'])
@api.response(201, 'Registro encontrado')
@api.response(404, 'Registro no encontrado.')
@api.response(500, 'Se presentó un error en el servidor.')
class GetBy(Resource):
    decorators = [auth_token.login_required]

    @api.doc('get_docs')
    @api.expect(EventsFilterModel)
    def post(self):
        """
        Consulta registros almacenados en la base de datos
        """
        data = request.json
        response = Controller.get_by(data=data)
        return response


@api.route('/xml', methods=['POST'])
@api.response(201, 'Registro encontrado')
@api.response(400, 'Error al hacer la peticion.')
@api.response(500, 'Se presentó un error en el servidor.')
class Xml(Resource):
    decorators = [auth_token.login_required]

    @api.doc('xml')
    @api.expect(EventsFilterNumberModel)
    def post(self):
        """
        Consulta un xml de un documento
        """
        re_json = request.json
        response = Controller.xml(data=re_json)
        return response


@api.route('/status', methods=['POST'])
@api.response(404, 'Registro no encontrado')
@api.response(500, 'Se presentó un error en el servidor.')
class Status(Resource):
    decorators = [auth_token.login_required]

    @api.expect(statusEventModel)
    def post(self):
        """
        Obtiene el estado del evento
        """
        data = request.json
        response = Controller.status(data)
        return response


@api.route('/new-tacitaccept', methods=['POST'])
@api.response(404, 'Registro no encontrado.')
@api.response(500, 'Se presentó un error en el servidor.')
class NewDataTacitAccept(Resource):
    decorators = [auth_token.login_required]

    @api.doc('create_new_event')
    @api.expect(EventsModelTacitAccept)
    def post(self):
        """
        Agrega un nuevo registro
        """
        data0 = validate_json(request.json)
        if 'resultCode' in data0 and data0['resultCode'] == 400:
            response = make_response(jsonify(data0), 400)
            return response
        data = {
            'issueDate': data0['issueDate'],
            'issueTime': data0['issueTime'],
            'registrationNameSenderParty': data0['registrationNameSenderParty'],
            'checkDigitSenderParty': data0['checkDigitSenderParty'],
            'docTypeSenderParty': data0['docTypeSenderParty'],
            'nitSenderParty': data0['nitSenderParty'],
            'legalTypeSenderParty': data0['legalTypeSenderParty'],
            'taxSchemeNameSenderParty': data0['taxSchemeNameSenderParty'],
            'taxSchemeCodeSenderParty': data0['taxSchemeCodeSenderParty'],
            'registrationNameReceiverParty': data0['registrationNameReceiverParty'],
            'taxSchemeNameReceiverParty': data0['taxSchemeNameReceiverParty'],
            'taxSchemeCodeReceiverParty': data0['taxSchemeCodeReceiverParty'],
            'checkDigitReceiverParty': data0['checkDigitReceiverParty'],
            'docTypeReceiverParty': data0['docTypeReceiverParty'],
            'nitReceiverParty': data0['nitReceiverParty'],
            'legalTypeReceiverParty': data0['legalTypeReceiverParty'],
            'electronicMailReceiverParty': data0['electronicMailReceiverParty'],
            'responseCode': '034',
            'description': 'Aceptación Tácita',
            'documentReference': data0['documentReference'],
            'dianPin': data0['dianPin'],
            'dianSoftwareID': data0['dianSoftwareID'],
            'CUFE': data0['CUFE'],
            'documentTypeCode': data0['documentTypeCode'],
            'CUDE': '',
            'note': data0['note']
        }
        response = Controller.new_data(data=data)
        return response


@api.route('/new-accept', methods=['POST'])
@api.response(404, 'Registro no encontrado.')
@api.response(500, 'Se presentó un error en el servidor.')
class NewDataAccept(Resource):
    decorators = [auth_token.login_required]

    @api.doc('create_new_event')
    @api.expect(EventsModelAccept)
    def post(self):
        """
        Agrega un nuevo registro
        """
        data0 = validate_json(request.json)
        if 'resultCode' in data0 and data0['resultCode'] == 400:
            response = make_response(jsonify(data0), 400)
            return response

        data = {
            'issueDate': data0['issueDate'],
            'issueTime': data0['issueTime'],
            'registrationNameSenderParty': data0['registrationNameSenderParty'],
            'checkDigitSenderParty': data0['checkDigitSenderParty'],
            'docTypeSenderParty': data0['docTypeSenderParty'],
            'nitSenderParty': data0['nitSenderParty'],
            'legalTypeSenderParty': data0['legalTypeSenderParty'],
            'taxSchemeNameSenderParty': data0['taxSchemeNameSenderParty'],
            'taxSchemeCodeSenderParty': data0['taxSchemeCodeSenderParty'],
            'registrationNameReceiverParty': data0['registrationNameReceiverParty'],
            'taxSchemeNameReceiverParty': data0['taxSchemeNameReceiverParty'],
            'taxSchemeCodeReceiverParty': data0['taxSchemeCodeReceiverParty'],
            'checkDigitReceiverParty': data0['checkDigitReceiverParty'],
            'docTypeReceiverParty': data0['docTypeReceiverParty'],
            'nitReceiverParty': data0['nitReceiverParty'],
            'legalTypeReceiverParty': data0['legalTypeReceiverParty'],
            'electronicMailReceiverParty': data0['electronicMailReceiverParty'],
            'responseCode': '033',
            'description': 'Aceptación expresa',
            'documentReference': data0['documentReference'],
            'CUFE': data0['CUFE'],
            'dianPin': data0['dianPin'],
            'dianSoftwareID': data0['dianSoftwareID'],
            'documentTypeCode': data0['documentTypeCode'],
            'CUDE': '',
            'note': data0['note']
        }
        response = Controller.new_data(data=data)
        return response


@api.route('/new-receipt', methods=['POST'])
@api.response(404, 'Registro no encontrado.')
@api.response(500, 'Se presentó un error en el servidor.')
class NewDataReceipt(Resource):
    decorators = [auth_token.login_required]

    @api.doc('create_new_event')
    @api.expect(EventsModelReceipt)
    def post(self):
        """
        Agrega un nuevo registro
        """
        data0 = validate_json(request.json)
        if 'resultCode' in data0 and data0['resultCode'] == 400:
            response = make_response(jsonify(data0), 400)
            return response
        data = {
             'issueDate': data0['issueDate'],
            'issueTime': data0['issueTime'],
            'registrationNameSenderParty': data0['registrationNameSenderParty'],
            'checkDigitSenderParty': data0['checkDigitSenderParty'],
            'docTypeSenderParty': data0['docTypeSenderParty'],
            'nitSenderParty': data0['nitSenderParty'],
            'legalTypeSenderParty': data0['legalTypeSenderParty'],
            'taxSchemeNameSenderParty': data0['taxSchemeNameSenderParty'],
            'taxSchemeCodeSenderParty': data0['taxSchemeCodeSenderParty'],
            'registrationNameReceiverParty': data0['registrationNameReceiverParty'],
            'taxSchemeNameReceiverParty': data0['taxSchemeNameReceiverParty'],
            'taxSchemeCodeReceiverParty': data0['taxSchemeCodeReceiverParty'],
            'checkDigitReceiverParty': data0['checkDigitReceiverParty'],
            'docTypeReceiverParty': data0['docTypeReceiverParty'],
            'nitReceiverParty': data0['nitReceiverParty'],
            'legalTypeReceiverParty': data0['legalTypeReceiverParty'],
            'electronicMailReceiverParty': data0['electronicMailReceiverParty'],
            'responseCode': '032',
            'description': 'Recibo del bien y/o prestación del servicio',
            'documentReference': data0['documentReference'],
            'dianPin': data0['dianPin'],
            'dianSoftwareID': data0['dianSoftwareID'],
            'CUFE': data0['CUFE'],
            'documentTypeCode': data0['documentTypeCode'],
            'CUDE': '',
            'note': data0['note'],
            'person': data0['person'],
            'number': 0
        }

        response = Controller.new_data(data=data)
        return response


@api.route('/new-claim', methods=['POST'])
@api.response(404, 'Registro no encontrado.')
@api.response(500, 'Se presentó un error en el servidor.')
class NewDataClaim(Resource):
    decorators = [auth_token.login_required]

    @api.doc('create_new_event')
    @api.expect(EventsModelClaim)
    def post(self):
        """
        Agrega un nuevo registro
        """
        data0 = validate_json(request.json)
        if 'resultCode' in data0 and data0['resultCode'] == 400:
            response = make_response(jsonify(data0), 400)
            return response

        data = {
            'issueDate': data0['issueDate'],
            'issueTime': data0['issueTime'],
            'registrationNameSenderParty': data0['registrationNameSenderParty'],
            'checkDigitSenderParty': data0['checkDigitSenderParty'],
            'docTypeSenderParty': data0['docTypeSenderParty'],
            'nitSenderParty': data0['nitSenderParty'],
            'legalTypeSenderParty': data0['legalTypeSenderParty'],
            'taxSchemeNameSenderParty': data0['taxSchemeNameSenderParty'],
            'taxSchemeCodeSenderParty': data0['taxSchemeCodeSenderParty'],
            'registrationNameReceiverParty': data0['registrationNameReceiverParty'],
            'taxSchemeNameReceiverParty': data0['taxSchemeNameReceiverParty'],
            'taxSchemeCodeReceiverParty': data0['taxSchemeCodeReceiverParty'],
            'checkDigitReceiverParty': data0['checkDigitReceiverParty'],
            'docTypeReceiverParty': data0['docTypeReceiverParty'],
            'nitReceiverParty': data0['nitReceiverParty'],
            'legalTypeReceiverParty': data0['legalTypeReceiverParty'],
            'electronicMailReceiverParty': data0['electronicMailReceiverParty'],
            'responseCode': '031',
            'claimCode': data0['claimCode'],
            'dianPin': data0['dianPin'],
            'dianSoftwareID': data0['dianSoftwareID'],
            'description': 'Reclamo de la Factura Electrónica de Venta',
            'documentReference': data0['documentReference'],
            'note': data0['note'],
            'CUFE': data0['CUFE'],
            'documentTypeCode': data0['documentTypeCode'],
            'CUDE': ''
        }
        response = Controller.new_data(data=data)
        return response


@api.route('/new-acuse', methods=['POST'])
@api.response(404, 'Registro no encontrado.')
@api.response(500, 'Se presentó un error en el servidor.')
class NewDataAcuse(Resource):
    decorators = [auth_token.login_required]

    @api.doc('create_new_event')
    @api.expect(EventsModelAcuse)
    def post(self):
        """
        Agrega un nuevo registro
        """
        data0 = validate_json(request.json)
        if 'resultCode' in data0 and data0['resultCode'] == 400:
            response = make_response(jsonify(data0), 400)
            return response
        data = {
            'issueDate': data0['issueDate'],
            'issueTime': data0['issueTime'],
            'registrationNameSenderParty': data0['registrationNameSenderParty'],
            'checkDigitSenderParty': data0['checkDigitSenderParty'],
            'docTypeSenderParty': data0['docTypeSenderParty'],
            'nitSenderParty': data0['nitSenderParty'],
            'legalTypeSenderParty': data0['legalTypeSenderParty'],
            'taxSchemeNameSenderParty': data0['taxSchemeNameSenderParty'],
            'taxSchemeCodeSenderParty': data0['taxSchemeCodeSenderParty'],
            'registrationNameReceiverParty': data0['registrationNameReceiverParty'],
            'taxSchemeNameReceiverParty': data0['taxSchemeNameReceiverParty'],
            'taxSchemeCodeReceiverParty': data0['taxSchemeCodeReceiverParty'],
            'checkDigitReceiverParty': data0['checkDigitReceiverParty'],
            'docTypeReceiverParty': data0['docTypeReceiverParty'],
            'nitReceiverParty': data0['nitReceiverParty'],
            'legalTypeReceiverParty': data0['legalTypeReceiverParty'],
            'electronicMailReceiverParty': data0['electronicMailReceiverParty'],
            'responseCode': '030',
            'dianPin': data0['dianPin'],
            'dianSoftwareID': data0['dianSoftwareID'],
            'description': 'Acuse de recibo de Factura Electrónica de Venta',
            'documentReference': data0['documentReference'],
            'CUFE': data0['CUFE'],
            'documentTypeCode': data0['documentTypeCode'],
            'CUDE': '',
            'note': data0['note'],
            'person': data0['person'],
            'number': 0
        }
        response = Controller.new_data(data=data)
        return response


@api.route('/update', methods=['PUT'])
@api.response(404, 'Registro no encontrado.')
@api.response(500, 'Se presentó un error en el servidor.')
class UpdateData(Resource):
    decorators = [auth_token.login_required]

    @api.doc('update_event')
    @api.marshal_with(EventsModelAcuse)
    def put(self):
        """

        Actualiza un registro
        """
        data = request.json
        response = Controller.update_data(data=data)
        return response




