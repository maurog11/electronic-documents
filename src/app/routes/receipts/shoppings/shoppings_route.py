# -*- coding: utf-8 -*-
#########################################################
from flask import request, make_response, jsonify
from app.controllers import ShoppingsController as Controller
from app.auth import auth_token
from flask_restx import Resource
from app.utils import validate_json
from .schemas import allShoppingsModel, shoppingsFilterNumberModel, shoppingsModel, api


@api.route('/all', methods=['POST'])
@api.response(200, 'Registros encontrados')
@api.response(404, 'No se encontraron registros')
@api.response(500, 'Se presentó un error en el servidor.')
class All(Resource):
    decorators = [auth_token.login_required]

    @api.doc('get_all_shoppings')
    @api.expect(allShoppingsModel)
    def post(self):
        """

        Consulta registros en la base de datos por numero y tamaño de pagina
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

    @api.doc('get_shopping_by_id')
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
    @api.expect(shoppingsFilterNumberModel)
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
    @api.expect(shoppingsFilterNumberModel)
    def post(self):
        """
        Consulta un xml de un documento
        """
        re_json = request.json
        response = Controller.xml(data=re_json)
        return response


@api.route('/refresh', methods=['POST'])
class RefreshData(Resource):
    # decorators = [auth_token.login_required]

    @api.doc('refresh_shopping')
    @api.expect(shoppingsModel)
    def post(self):
        """
        Refresca un registro
        """
        data = validate_json(request.json)
        if 'resultCode' in data and data['resultCode'] == 400:
            response = make_response(jsonify(data), 400)
            return response
        response = Controller.refresh_data(data=data)
        return response


@api.route('/update', methods=['PUT'])
@api.response(201, 'Envio de factura actualizado correctamente')
class UpdateData(Resource):
    decorators = [auth_token.login_required]

    @api.doc('update_sendinvoice')
    @api.marshal_with(shoppingsModel)
    def put(self):
        """

        Actualiza un registro
        """
        data = request.json
        response = Controller.update_data(data=data)
        return response




