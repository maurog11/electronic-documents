from flask_restx import fields
from .sub_schemas import api
from .sub_schemas import (
    FechasPagos,
    Periodo,
    NumeroSecuenciaXML,
    GeneracionXML,
    InfoGeneral,
    Notas,
    Empleador,
    Trabajador,
    Pago,
    Devengados,
    Deducciones,
    Pdf
)

StatusModel = api.model(
    'Status', {
        'Nit': fields.String(required=True, description="Nit del emisor"),
        'CUFE': fields.String(required=True, description="CUFE, CUNE, CUDE a consultar")
    }
)


PayRollSendsModel = api.model(
    "PayRollSends", {
        'FechasPagos': fields.Nested(FechasPagos),
        'Periodo': fields.Nested(Periodo),
        'NumeroSecuenciaXML': fields.Nested(NumeroSecuenciaXML),
        'LugarGeneracionXML': fields.Nested(GeneracionXML),
        'InformacionGeneral': fields.Nested(InfoGeneral),
        'Notas': fields.Nested(Notas),
        'Empleador': fields.Nested(Empleador),
        'Trabajador': fields.Nested(Trabajador),
        'Pago': fields.Nested(Pago),
        'Devengados': fields.Nested(Devengados),
        'Deducciones': fields.Nested(Deducciones),
        'DevengadosTotal': fields.String(required=False, description="Debe ir el valor Total de todos los Devengados del Trabajador"),
        'DeduccionesTotal': fields.String(required=False, description="Debe ir el valor Total de todas las Deducciones del Trabajador"),
        'ComprobanteTotal': fields.String(required=False, description="Debe ser la Diferencia entre DevengadosTotal - DeduccionesTotal"),
        'CorrelationDocumentId': fields.String(required=False, description="id documento correlacion saphety"),
        'Pdf': fields.Nested(Pdf)
    })

PayRollSendsFilterModel = api.model(
    "PayRollSendsFilterModel", {
        "issuerNit": fields.String(required=True, description="Nit de emisor"),
        "startClientNit": fields.String(required=False, description="Rango inicial del nit del cliente"),
        "endClientNit": fields.String(required=False, description="Rango final del nit del cliente"),
        "startDate": fields.Date(required=False, description="Fecha inicial a consultar aaaa-mm-dd"),
        "endDate": fields.Date(required=False, description="Fecha final a consultar aaaa-mm-dd"),
        "startNumber": fields.String(required=False, description="Rango inicial del documento incluido el prefijo"),
        "endNumber": fields.String(required=False, description="Rango final del documento incluido el prefijo"),
        "status": fields.String(required=True, description="Estado del documento 1= enviado a la DIAN, 0= rechazado por la DIAN"),
        "pageSize": fields.Integer(required=True, description="Tamaño de la pagina"),
        "pageNumber": fields.Integer(required=True, description="Numero de la pagina")
    }
)

PayRollSendsFilterNumberModel = api.model(
    "PayRollSendsFilterNumberModel", {
        "Nit": fields.String(required=True, description="Nit de emisor"),
        "DocType": fields.String(required=False, description="NO= Nomina"),
        "SeriePrefix": fields.String(required=False, description="prefijo del documento"),
        "SerieNumber": fields.String(required=False, description="numero del documento")

    }
)

allPayRollModel = api.model(
    "allPayRolls", {
        "pageSize": fields.Integer(required=True, description="Tamaño de la pagina"),
        "pageNumber": fields.Integer(required=True, description="Numero de la pagina")
    }
)
