from flask_restx import fields
from .sub_schemas import api
from .sub_schemas import (
   BillingPeriod,
   Additional,
   PaymentMeans,
   PaymentExchangeRate,
   IssuerParty,
   CustomerParty,
   LinesDes,
   TaxSubTotals,
   WithholdingTaxSubTotals,
   AllowanceCharges,
   TaxTotals,
   WithholdingTaxTotals,
   Total,
   DocumentReferences,
   AdditionalCustomer,
   Pdf
)


SendsModel = api.model(
    "SendsInvoices", {
         'BillingPeriod': fields.Nested(BillingPeriod),
         'Additional': fields.Nested(Additional),
         'SeriePrefix': fields.String(required=True, description="Debe ir el prefijo de autorizacion de numeracion"),
         'SerieNumber': fields.String(required=True, description="Debe ir el numero de serie autorizado"),
         'IssueDate': fields.Date(required=True, description="Debe ir la fecha de emision del documento. Considerando zona horaria de Colombia (-5), en formato AAAA-MM-DD"),
         'DueDate': fields.Date(required=True, description="Debe ir la fecha de vencimiento del documento en formato AAAA-MM-DD"),
         'IssueTime': fields.String(required=True, description="Debe ir la hora de emision del documento. Considerando zona horaria de Colombia (-5), en formato HH:MM:SSdhh:mm"),
         'NoteDocument': fields.String(required=False, description="Deben ir los comentarios del documento, texto libre"),
         'CorrelationDocumentId': fields.String(required=False, description="Debe ir el id documento correlacion saphety"),
         'SerieExternalKey': fields.String(required=False, description="Debe ir la llave externa saphety"),
         'DeliveryDate': fields.Date(required=False, description="Debe ir la fecha de entrega en formato AAAA-MM-DD"),
         'DeliveryTime': fields.String(required=False, description="Debe ir la hora de entrega en formato HH:MM:SS"),
         'PaymentMeans': fields.List(fields.Nested(PaymentMeans)),
         'PaymentExchangeRate': fields.List(fields.Nested(PaymentExchangeRate)),
         'IssuerParty': fields.Nested(IssuerParty),
         'CustomerParty': fields.Nested(CustomerParty),
         'Currency': fields.String(required=True, description="COP= Peso Colombiano, USD= Dolar, mirar las demas en la tabla 13.3.3 anexo 1.8 resolucion 12"),
         'OperationType': fields.String(required=True, description="10= estandar, 09= AIU, 11= Mandatos, mirar las demas en la tabla 13.1.5 anexo 1.8 resolucion 12"),
         'Lines': fields.List(fields.Nested(LinesDes)),
         'TaxSubTotals': fields.List(fields.Nested(TaxSubTotals)),
         'WithholdingTaxSubTotals': fields.List(fields.Nested(WithholdingTaxSubTotals)),
         'AllowanceCharges': fields.List(fields.Nested(AllowanceCharges)),
         'TaxTotals': fields.List(fields.Nested(TaxTotals)),
         'WithholdingTaxTotals': fields.List(fields.Nested(WithholdingTaxTotals)),
         'Total': fields.Nested(Total),
         'DocumentReferences': fields.List(fields.Nested(DocumentReferences)),
         'AdditionalCustomers': fields.List(fields.Nested(AdditionalCustomer)),
         'Pdf': fields.Nested(Pdf)
      })

SendsFilterModel = api.model(
    "SendsFilterModel", {
        "issuerNit": fields.String(required=True, description="Nit de emisor"),
        "startClientNit": fields.String(required=False, description="Rango inicial del nit del cliente"),
        "endClientNit": fields.String(required=False, description="Rango final del nit del cliente"),
        "startDate": fields.Date(required=False, description="Fecha inicial a consultar en formato AAAA-MM-DD"),
        "endDate": fields.Date(required=False, description="Fecha final a consultar en formato AAAA-MM-DD"),
        "startNumber": fields.String(required=False, description="Rango inicial del documento incluido el prefijo"),
        "endNumber": fields.String(required=False, description="Rango final del documento incluido el prefijo"),
        "status": fields.String(required=True, description="Estado del documento 1= enviado a la DIAN, 0= rechazado por la DIAN"),
        "pageSize": fields.Integer(required=True, description="Tama??o de la pagina"),
        "pageNumber": fields.Integer(required=True, description="Numero de la pagina")
    }
)

allInvoicesModel = api.model(
    "allInvoices", {
        "pageSize": fields.Integer(required=True, description="Tama??o de la pagina"),
        "pageNumber": fields.Integer(required=True, description="Numero de la pagina")
    }
)

SendsFilterNumberModel = api.model(
    "SendsFilterModel", {
        "Nit": fields.String(required=True, description="Nit de emisor"),
        "DocType": fields.String(required=False, description="Tipo de documento FV=factura DS=documento soporte"),
        "SeriePrefix": fields.String(required=False, description="prefijo del documento"),
        "SerieNumber": fields.String(required=False, description="numero del documento")

    }
)

SendsFilterCufeModel = api.model(
    "SendsFilterModel", {
        "Nit": fields.String(required=True, description="Nit de emisor"),
        "Id": fields.Integer(required=True, description="Id del documento"),
        "Cufe": fields.String(required=True, description="nuevo CUFE")
    }
)
