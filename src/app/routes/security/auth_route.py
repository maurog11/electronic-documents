# -*- coding: utf-8 -*-
#########################################################
from flask_restx import Resource
from flask import request
from .schemas.auth_schema import api, AuthModel
from app.controllers import AuthController


@api.route('/generate_token/', methods=['POST'])
@api.response(201, 'Token generado')
@api.param('data', 'Los datos de la credencial')
class NewData(Resource):
    @api.doc('generate_token')
    @api.expect(AuthModel)
    def post(self):
        """
        Generar el token de acceso
        """
        data = request.json
        response = AuthController.post_data_login(data)
        return response
