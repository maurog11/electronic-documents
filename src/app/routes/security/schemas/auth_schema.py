# -*- coding: utf-8 -*-
#########################################################

from flask_restx import Namespace, fields

api = Namespace('Auth', description='Autenticación en el API')

AuthModel = api.model('Auth', {
    'apiKey': fields.String(required=True, description='Llave de acceso'),
    'apiSecret': fields.String(required=True, description='Clave de acceso'),
    'username': fields.String(required=True, description='Usuario que realiza la petición - Formato: nit-username')
})
