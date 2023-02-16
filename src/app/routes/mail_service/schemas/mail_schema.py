# -*- coding: utf-8 -*-
#########################################################

from flask_restx import Namespace, fields

api = Namespace('MailService', description='Servicio de email')

SendModel = api.model('Send', {
    'to': fields.String(required=True, description='Email al que se desea enviar el mensaje.'),
    'subject': fields.String(required=True, description='Asunto del mensaje.'),
    'file': fields.String(required=False, description='BASE64 del archivo que se desea adjuntar'),
    'fileName': fields.String(required=False, description='Nombre del archivo a adjuntar con extensión'),
    'type': fields.String(required=False, description='Tipo de archivo a adjuntar, eje: pdf, zip, rar, png,...etc.'),
    'companyName': fields.String(required=True, description='Nombre de la compañía emisora'),
    'companyNit': fields.String(required=True, description='Nit de la compañía emisora'),
    'documentNumber': fields.String(required=True, description='Número del documento emitido'),
    'documentDate': fields.String(required=True, description='Fecha del documento emitido'),
    'documentType': fields.String(required=True, description='Tipo del documento emitido, eje: Factura electrónica de venta')
})

ByidModel = api.model('GetByid', {
    'id': fields.String(required=True, description='Identificador unico del mensaje.')
}, mask={'id'})