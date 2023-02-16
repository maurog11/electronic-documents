# -*- coding: utf-8 -*-
#########################################################

from flask import request, jsonify
from flask_restx import Resource
from .schemas import CertsModel, ByidModel, api, AddCerts
from app.controllers import CertsController as Controller
from app.auth import auth_token


@api.route('/get', methods=['GET'])
class GetAll(Resource):
    decorators = [auth_token.login_required]

    @api.doc('get_all_certificates')
    def get(self):
        """
        Obtiene todos los Certificados almacenados en la base de datos
        """
        response = Controller.get_all()
        return jsonify(data=response)


@api.route('/data/<int:id>/get', methods=['GET'])
@api.response(401, 'La peticion carece de un id')
@api.response(404, 'Certificado no encontrada.')
@api.response(500, 'Se presentó un error en el servidor.')
@api.param('id', 'El identificador del certificado')
class GetByid(Resource):
    decorators = [auth_token.login_required]

    @api.doc('get_certificate_by_id')
    def get(self, id):
        """
        Obtiene un Certificado dado su id
        """
        response = Controller.get_by_id(id)
        return response


@api.route('/add', methods=['POST'])
@api.response(201, 'Certificado almacenado correctamente')
@api.param('data', 'La información necesaria para almacenar el certificado')
class AddCertificate(Resource):
    decorators = [auth_token.login_required]

    @api.doc('create_certificate')
    @api.expect(AddCerts)
    def post(self):
        """
        Crea un certificado o actualiza los datos el certificado existente
        """
        data = request.json
        result = Controller.add_new_certificate(data=data)
        status = 200
        if 'statusCode' in result:
            status = result['statusCode']
        response = jsonify(result)
        response.status_code = status
        return response


@api.route('/update', methods=['PUT'])
@api.response(201, 'Certificado actualizado correctamente')
class UpdateData(Resource):
    decorators = [auth_token.login_required]

    @api.doc('update_certificate')
    @api.marshal_with(CertsModel)
    def put(self):
        """
        Actualiza un Certificado
        """
        data = request.json
        response = Controller.update_data(data=data)
        return jsonify(data=response)



