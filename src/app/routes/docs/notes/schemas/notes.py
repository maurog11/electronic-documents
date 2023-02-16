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

StatusModel = api.model(
    'Status', {
        'Nit': fields.String(required=True, description="Nit del emisor"),
        'CUFE': fields.String(required=True, description="CUFE, CUNE, CUDE a consultar")
    }
)

NotesModel = api.model(
    "Notes", {
         'BillingPeriod': fields.Nested(BillingPeriod),
         'AdditionalN': fields.Nested(Additional),
         'SeriePrefix': fields.String(required=True, description="Prefijo de la nota"),
         'SerieNumber': fields.String(required=True, description="Numero de nota"),
         'IssueDate': fields.String(required=True, description="Fecha de emision nota"),
         'DueDate': fields.String(required=True, description="Fecha de vencimiento nota"),
         'IssueTime': fields.String(required=True, description="Hora de emision"),
         'CorrelationDocumentId': fields.String(required=True, description="Texto libre"),
         'SerieExternalKey': fields.String(required=False, description="Llave externa"),
         'DeliveryDate': fields.String(required=False, description="Fecha de entrega"),
         'DeliveryTime': fields.String(required=False, description="Tiempo de entrega"),
         'PaymentMeans': fields.List(fields.Nested(PaymentMeans)),
         'PaymentExchangeRate': fields.List(fields.Nested(PaymentExchangeRate)),
         'IssuerParty': fields.Nested(IssuerParty),
         'CustomerParty': fields.Nested(CustomerParty),
         'Currency': fields.String(required=True, description="Divisa"),
         'OperationType': fields.String(required=True, description="Tipo de operacion"),
         'ReasonCredit': fields.String(required=True, description="Codigo de la nota credito"),
         'NoteDocument': fields.String(required=True, description="Texto adicional"),
         'Lines': fields.List(fields.Nested(LinesDes)),
         'TaxSubTotals': fields.List(fields.Nested(TaxSubTotals)),
         'WithholdingTaxSubTotals': fields.List(fields.Nested(WithholdingTaxSubTotals)),
         'AllowanceCharges': fields.List(fields.Nested(AllowanceCharges)),
         'TaxTotals': fields.List(fields.Nested(TaxTotals)),
         'WithholdingTaxTotals': fields.List(fields.Nested(WithholdingTaxTotals)),
         'Total': fields.Nested(Total),
         'DocumentReferences': fields.List(fields.Nested(DocumentReferences)),
         'AdditionalCustomers': fields.List(fields.Nested(AdditionalCustomer)),
         'Pdf': fields.Nested(Pdf),
      })

NotesFilterModel = api.model(
    "NotesFilterModel", {
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

NotesFilterNumberModel = api.model(
    "NotesFilterNumberModel", {
        "Nit": fields.String(required=True, description="Nit de emisor"),
        "DocType": fields.String(required=False, description="Tipo de documento FV=factura DS=documento soporte"),
        "SeriePrefix": fields.String(required=False, description="prefijo del documento"),
        "SerieNumber": fields.String(required=False, description="numero del documento")

    }
)

allNotesModel = api.model(
    "allNotesModel", {
        "pageSize": fields.Integer(required=True, description="Tamaño de la pagina"),
        "pageNumber": fields.Integer(required=True, description="Numero de la pagina")
    }
)

notesFilterCufeModel = api.model(
    "SendsFilterModel", {
        "Nit": fields.String(required=True, description="Nit de emisor"),
        "Id": fields.Integer(required=True, description="Id del documento"),
        "Cufe": fields.String(required=True, description="nuevo CUDE")
    }
)
