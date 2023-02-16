from flask_restx import Namespace, fields


api = Namespace("Emails", description="Operaciones relacionadas con emails")

EmailsModel = api.model(
    "Emails", {
            "issuerNit": fields.String(required=True, description="Nit del emisor"),
            "imap": fields.String(required=True, description="Host de la cuenta de correo"),
            "key": fields.String(required=True, description="Llave de encriptacion"),
            "email": fields.String(required=True, description="Correo electronico"),
            "port": fields.String(required=True, description="Puerto de la cuenta de correo")
      }
)

EmailsFilterModel = api.model(
    "EmailsFilterModel", {
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

allEmailsModel = api.model(
    "allEmailsModel", {
        "pageSize": fields.Integer(required=True, description="Tamaño de la pagina"),
        "pageNumber": fields.Integer(required=True, description="Numero de la pagina")
    }
)
