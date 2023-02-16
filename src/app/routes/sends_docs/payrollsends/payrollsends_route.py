# -*- coding: utf-8 -*-
#########################################################
from flask import request, make_response, jsonify
from app.utils import validate_json, ResponseData
from app.auth import auth_token
from app.controllers import PayRollSendsController as Controller
from flask_restx import Resource
from .schemas import PayRollSendsModel, PayRollSendsFilterModel, PayRollSendsFilterNumberModel, StatusModel,\
    allPayRollModel, api


@api.route('/all', methods=['POST'])
@api.response(200, 'Registros encontrados')
@api.response(404, 'No se encontraron registros')
@api.response(500, 'Se presentó un error en el servidor.')
class All(Resource):
    decorators = [auth_token.login_required]

    @api.doc('get_all_payrolls')
    @api.expect(allPayRollModel)
    def post(self):
        """
        Consulta las nominas almacenadas en la base de datos por numero y tamaño de pagina
        """
        data = request.json
        response = Controller.all(data=data)
        return response


@api.route('/getby', methods=['POST'])
@api.response(201, 'Registro encontrado')
@api.response(404, 'Registro no encontrado.')
@api.response(500, 'Se presentó un error en el servidor.')
class GetBy(Resource):
    decorators = [auth_token.login_required]

    @api.doc('create_new_')
    @api.expect(PayRollSendsFilterModel)
    def post(self):
        """
        Consulta registros almacenados en la base de datos por rango de fecha
        """
        data = request.json
        response = Controller.get_by(data=data)
        return response


@api.route('/data/<int:id>/get', methods=['GET'])
@api.response(401, 'La peticion carece de un id')
@api.response(404, 'Registro no encontrado.')
@api.response(500, 'Se presentó un error en el servidor.')
@api.param('id', 'Identificador de Envio de Nomina')
class GetByid(Resource):
    decorators = [auth_token.login_required]

    @api.doc('get_payrollsend_by_id')
    def get(self, id):
        """
        Obtiene una nomina dado su id
        """
        response = Controller.get_by_id(id)
        return response


@api.route('/pdf-xml', methods=['POST'])
@api.response(201, 'Registro encontrado')
@api.response(400, 'Error al hacer la peticion.')
@api.response(500, 'Se presentó un error en el servidor.')
class Pdf(Resource):
    decorators = [auth_token.login_required]

    @api.doc('pdf')
    @api.expect(PayRollSendsFilterNumberModel)
    def post(self):
        """
        Consulta el pdf y el xml de un documento
        """
        re_json = validate_json(request.json)
        if 'resultCode' in re_json and re_json['resultCode'] == 400:
            response = make_response(jsonify(re_json['resultCode']), 400)
            return response

        response = Controller.pdf(data=re_json)
        return response


@api.route('/xml', methods=['POST'])
@api.response(201, 'Registro encontrado')
@api.response(400, 'Error al hacer la peticion.')
@api.response(500, 'Se presentó un error en el servidor.')
class Xml(Resource):
    decorators = [auth_token.login_required]

    @api.doc('xml')
    @api.expect(PayRollSendsFilterNumberModel)
    def post(self):
        """
        Consulta un xml de un documento
        """
        re_json = request.json
        response = Controller.xml(data=re_json)
        if 'message' in response and 'Error' in response['message']:
            return response
        return make_response(response, 200)


@api.route('/status', methods=['POST'])
@api.response(200, 'Documento se encontro en los registros de la DIAN')
@api.response(404, 'Documento no se encontro en los registros')
class Status(Resource):
    decorators = [auth_token.login_required]

    @api.expect(StatusModel)
    def post(self):
        """
        Obtiene el estado de un documento de la DIAN dado su CUFE
                """
        data = request.json
        response = Controller.status_send(data)
        return response


@api.route('/new', methods=['POST'])
@api.response(201, 'Nota de nomina enviada correctamente')
class NewData(Resource):
    decorators = [auth_token.login_required]

    @api.doc('create_new_payroll_send')
    @api.expect(PayRollSendsModel)
    def post(self):
        """
        Crea una nueva Nomina
        """
        data = validate_json(request.json)
        if 'resultCode' in data and data['resultCode'] == 400:
            response = make_response(jsonify(data), 400)
            return response
        try:
            response = Controller.new_data_send(data)
        except Exception as e:
            response = ResponseData.internal_server_error(str(e))
        return response


@api.route('/update', methods=['PUT'])
@api.response(201, 'Nomina actualizada correctamente')
class UpdateData(Resource):
    decorators = [auth_token.login_required]

    @api.doc('update_payroll')
    @api.marshal_with(PayRollSendsModel)
    def put(self):
        """
        Actualiza una Nomina
        """
        data = request.json
        response = Controller.update_data(data=data)
        return response
