# -*- coding: utf-8 -*-
#########################################################

from flask_restx import Namespace, fields

api = Namespace('Aplicaciones', description='Modelo relacionado con la seguridad del API Rest')


ByidModel = api.model('GetByid', {
    'id': fields.Integer(required=True, description='Identificador unico de una credencial')
}, mask={'id'})

ApplicationModel = api.model('applications', {
    'id': fields.Integer(required=True, description='Identificador unico de una credencial'),
    'ApiKey': fields.String(required=True, description='Llave de acceso'),
    'ApiSecret': fields.String(required=True, description='Clave de acceso'),
    'CreateBy': fields.String(description='Usuario que creó el registro'),
    'UpdateBy': fields.String(description='Usuario que actualizó el registro')
})
