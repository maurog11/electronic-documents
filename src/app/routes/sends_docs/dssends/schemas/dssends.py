from flask_restx import fields
from .sub_schemas import api
from .sub_schemas import (
   BillingPeriod,
   Additional,
   PaymentMeans,
   PaymentExchangeRate,
   AccountingCustomerParty,
   AccountingSupplierParty,
   LinesDes,
   TaxSubTotals,
   WithholdingTaxSubTotals,
   AllowanceCharges,
   TaxTotals,
   WithholdingTaxTotals,
   Total,
   DocumentReferences,
   AdditionalCustomer,
   PdfData,
)


DsSendsModel = api.model(
    "DsSends", {
         'BillingPeriod': fields.Nested(BillingPeriod),
         'AdditionalDS': fields.Nested(Additional),
         'SeriePrefix': fields.String(required=True, description="Prefijo de la factura"),
         'SerieNumber': fields.String(required=True, description="Numero de serie de la factura"),
         'IssueDate': fields.String(required=True, description="Fecha creacion factura aaaa-mm-dd"),
         'DueDate': fields.String(required=True, description="Fecha vencimiento factura aaaa-mm-dd"),
         'IssueTime': fields.String(required=True, description="Hora creacion factura hh:mm:ss GMT"),
         'CorrelationDocumentId': fields.String(required=True, description="Id documento correlacion"),
         'SerieExternalKey': fields.String(required=True, description="Llave externa"),
         'DeliveryDate': fields.String(required=True, description="Fecha entrega"),
         'DeliveryTime': fields.String(required=True, description="Hora entrega"),
         'PaymentMeans': fields.List(fields.Nested(PaymentMeans)),
         'PaymentExchangeRate': fields.List(fields.Nested(PaymentExchangeRate)),
         'AccountingCustomerParty': fields.Nested(AccountingCustomerParty),
         'AccountingSupplierParty': fields.Nested(AccountingSupplierParty),
         'Currency': fields.String(required=True, description="Divisa para colombia COP"),
         'OperationType': fields.String(required=True, description="Tipo de operacion 01"),
         'Lines': fields.List(fields.Nested(LinesDes)),
         'TaxSubTotals': fields.List(fields.Nested(TaxSubTotals)),
         'WithholdingTaxSubTotals': fields.List(fields.Nested(WithholdingTaxSubTotals)),
         'AllowanceCharges': fields.List(fields.Nested(AllowanceCharges)),
         'TaxTotals': fields.List(fields.Nested(TaxTotals)),
         'WithholdingTaxTotals': fields.List(fields.Nested(WithholdingTaxTotals)),
         'Total': fields.Nested(Total),
         'DocumentReferences': fields.List(fields.Nested(DocumentReferences)),
         'AdditionalCustomers': fields.List(fields.Nested(AdditionalCustomer)),
         'PdfData': fields.Nested(PdfData),
      })

DsSendsFilterModel = api.model(
    "DsSendsFilterModel", {
        "issuerNit": fields.String(required=True, description="Nit de emisor"),
        "startClientNit": fields.String(required=False, description="Rango inicial del nit del cliente"),
        "endClientNit": fields.String(required=False, description="Rango final del nit del cliente"),
        "startDate": fields.String(required=False, description="Fecha inicial a consultar aaaa-mm-dd"),
        "endDate": fields.String(required=False, description="Fecha final a consultar aaaa-mm-dd"),
        "startNumber": fields.String(required=False, description="Rango inicial del documento incluido el prefijo"),
        "endNumber": fields.String(required=False, description="Rango final del documento incluido el prefijo"),
        "status": fields.String(required=True, description="Estado del documento 1= enviado a la DIAN, 0= rechazado por la DIAN"),
        "pageSize": fields.Integer(required=True, description="Tamaño de la pagina"),
        "pageNumber": fields.Integer(required=True, description="Numero de la pagina")
    }
)

DsSendsFilterNumberModel = api.model(
    "DsSendsFilterNumberModel", {
        "Nit": fields.String(required=True, description="Nit de emisor"),
        "DocType": fields.String(required=False, description="NC= Nota Credito, ND= Nota Debito"),
        "SeriePrefix": fields.String(required=False, description="prefijo del documento"),
        "SerieNumber": fields.String(required=False, description="numero del documento")

    }
)

allSupportDocsModel = api.model(
    "allSupportDocsModel", {
        "pageSize": fields.Integer(required=True, description="Tamaño de la pagina"),
        "pageNumber": fields.Integer(required=True, description="Numero de la pagina")
    }
)
