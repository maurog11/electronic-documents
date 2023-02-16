# -*- coding: utf-8 -*-
#########################################################
from flask_restx import Resource
from flask import request
from .schemas.mail_schema import api, SendModel, ByidModel
from app.auth import auth_token
from app.utils.mail_service import send_mail, get_mail_by_id


@api.response(401, 'La petición carece de credenciales.')
@api.response(404, 'El mensaje no fue encontrado.')
@api.response(500, 'Se presentó un error en el servidor.')
@api.param('id', 'El identificador del mensaje')
@api.header(name='Authorization', description='Bearer Token')
@api.route('/getId', methods=['POST'])
class GetByid(Resource):
    decorators = [auth_token.login_required]

    @api.doc('get_message_by_id')
    @api.expect(ByidModel)
    def post(self, id):
        """
        Consulta el registro de actividad de un mensaje por su id
        """
        response = get_mail_by_id(_id=id)
        return response


@api.route('/send/', methods=['POST'])
@api.response(200, 'El mensaje fue enviado correctamente')
@api.header(name='Authorization', description='Bearer Token')
@api.param('data', 'Los datos utilizados para el envió del email y para rellenar la información de la plantilla.')
class SendData(Resource):
    decorators = [auth_token.login_required]

    @api.doc('send_message')
    @api.expect(SendModel)
    def post(self):
        """
        Enviar un mensaje a un correo, endpoint para testear de manera funcional
        """
        data = request.json
        response = send_mail(data=data)
        return response