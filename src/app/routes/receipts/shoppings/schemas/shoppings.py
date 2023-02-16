from flask_restx import fields, Namespace

api = Namespace("Compras", description="Operaciones relacionadas con compras")

shoppingsModel = api.model(
    "shoppingsModel", {
        "nit": fields.String(required=True, description="Nit de emisor"),
        "docType": fields.String(required=True, description="Tipo de documento FV=factura DS=documento soporte"),
        "startDate": fields.String(required=True, description="Fecha de inicio"),
        "endDate": fields.String(required=True, description="Fecha de fin")
    }
)

allShoppingsModel = api.model(
    "allShoppings", {
        "pageSize": fields.Integer(required=True, description="Tamaño de la pagina"),
        "pageNumber": fields.Integer(required=True, description="Numero de la pagina")
    }
)

shoppingsFilterNumberModel = api.model(
    "shoppingsFilterNumber", {
        "Nit": fields.String(required=True, description="Nit de emisor"),
        "DocType": fields.String(required=False, description="Tipo de documento FV=factura DS=documento soporte"),
        "SeriePrefix": fields.String(required=False, description="prefijo del documento"),
        "SerieNumber": fields.String(required=False, description="numero del documento")

    }
)
