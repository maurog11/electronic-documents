# -*- coding: utf-8 -*-
#########################################################
from flask_restx import Resource
from flask import request
from app.controllers import ApplicationController as Controller
from .schemas.application_schema import api, ApplicationModel
from app.auth import auth_token


@api.route('/get_all', methods=['GET'])
@api.header(name='Authorization', description='Bearer Token')
class GetAll(Resource):
    decorators = [auth_token.login_required]

    @api.doc('get_all_applications')
    def get(self):
        """
        Consulta todos los registros de la tabla
        """
        response = Controller.get_all()
        return response


@api.response(401, 'La petición carece de credenciales.')
@api.response(404, 'Credencial no encontrada.')
@api.response(500, 'Se presentó un error en el servidor.')
@api.param('id', 'El identificador de la credencial')
@api.header(name='Authorization', description='Bearer Token')
@api.route('/get_by_id/<int:id>', methods=['GET'])
class GetByid(Resource):
    decorators = [auth_token.login_required]

    @api.doc('get_application_by_id')
    def get(self, id):
        """
        Obtiene un registro por su id
        """
        response = Controller.get_by_id(id)
        return response


@api.route('/new_keys/', methods=['POST'])
@api.response(201, 'Registro creado correctamente')
@api.header(name='Authorization', description='Bearer Token')
@api.param('data', 'Los datos de la credencial')
class NewData(Resource):
    decorators = [auth_token.login_required]

    @api.doc('create_new_application')
    @api.expect(ApplicationModel)
    def post(self):
        """
        Crea un nuevo Registro
        """
        data = request.json
        response = Controller.new_data(data=data)
        return response


@api.route('/update_keys/', methods=['PUT'])
@api.response(200, 'Registro actualizado correctamente')
@api.header(name='Authorization', description='Bearer Token')
@api.param('data', 'Los datos de la credencial')
class UpdateData(Resource):
    decorators = [auth_token.login_required]

    @api.doc('update_application')
    @api.expect(ApplicationModel)
    def put(self):
        """
        Actualiza un Registro
        """
        data = request.json
        response = Controller.update_data(data=data)
        return response
