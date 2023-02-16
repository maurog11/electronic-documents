# -*- coding: utf-8 -*-
#########################################################
from flask import request, jsonify, make_response
from app.controllers import EmailsController as Controller
from app.auth import auth_token
from flask_restx import Resource
from app.utils import validate_json
from .schemas import EmailsModel, EmailsFilterModel, allEmailsModel, api


@api.route('/all', methods=['POST'])
@api.response(200, 'Registros encontrados')
@api.response(404, 'No se encontraron registros')
@api.response(500, 'Se presentó un error en el servidor.')
class All(Resource):
    decorators = [auth_token.login_required]

    @api.doc('get_all_emails')
    @api.expect(allEmailsModel)
    def post(self):
        """

        Consulta registros almacenadas en la base de datos por numero y tamaño de pagina
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

    @api.doc('get_email_by_id')
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
    @api.expect(EmailsFilterModel)
    def post(self):
        """
        Consulta registros almacenados en la base de datos
        """
        data = request.json
        response = Controller.get_by(data=data)
        return response


@api.route('/new', methods=['POST'])
@api.response(201, 'Nota enviada correctamente')
class NewData(Resource):
    decorators = [auth_token.login_required]

    @api.doc('create_new_email')
    @api.expect(EmailsModel)
    def post(self):
        """
        Crea un nuevo registro
        """
        not_validate = [
            'Port'
        ]
        data = validate_json(request.json, to_not_validate=not_validate)
        if 'resultCode' in data and data['resultCode'] == 400:
            response = make_response(jsonify(data), 400)
            return response
        response = Controller.new_data(data=data)
        return response


@api.route('/update', methods=['PUT'])
@api.response(201, 'Nota actualizada correctamente')
class UpdateData(Resource):
    decorators = [auth_token.login_required]

    @api.doc('update_note')
    @api.marshal_with(EmailsModel)
    def put(self):
        """

        Actualiza un registro
        """
        data = request.json
        response = Controller.update_data(data=data)
        return jsonify(data=response)
