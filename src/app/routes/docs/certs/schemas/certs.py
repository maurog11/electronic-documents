from flask_restx import Namespace, fields


api = Namespace('Certificados', description='Operaciones relacionadas con Certificados')


ByidModel = api.model('GetByid', {
    'id': fields.Integer(required=True, description='Identificador unico de un certificado')
}, mask={'id'})

CertsModel = api.model('Cert', {
    'CreateDate': fields.DateTime(description='Fecha en la que se creo el certificado'),
    'UpdateDate': fields.DateTime(description='Fecha en la que se actualizo el certificado'),
    'CreateBy': fields.String(description='Usuario que creo el certificado'),
    'UpdateBy': fields.String(description='Usuario que actualizo el certificado'),
    'IsDeleted': fields.Boolean(description='Se ha eliminado el certificado?'),
    'IssuerNit': fields.String(required=True, description='Nit del emisor del certificado'),
    'Key': fields.String(required=True, description='Llave del certificado'),
    'Format': fields.String(required=True, description='Formato del certificado'),
    'Description': fields.String(description='Descripcion del certificado'),
    'DueDate': fields.DateTime(required=True, description='Fecha de vencimiento del certificado'),
})

AddCerts = api.model('Cert', {
    'IssuerNit': fields.String(required=True, description='Nit del emisor del certificado'),
    'Key': fields.String(required=True, description='Llave del certificado'),
    'Format': fields.String(required=True, description='Formato del certificado en Base64'),
    'Description': fields.String(required=True, description='Descripción del certificado'),
    'DueDate': fields.Date(required=True, description='Fecha de vencimiento del certificado Formato: YYYY-MM-DD')
})
