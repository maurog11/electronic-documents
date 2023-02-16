from flask_restx import fields
from .sub_schemas import api
from .sub_schemas import (
   BillingPeriodDS,
   AdditionalNDS,
   PaymentMeansDS,
   PaymentExchangeRate,
   AccountingCustomerParty,
   AccountingSupplierParty,
   LinesDesDS,
   TaxSubTotalsDS,
   WithholdingTaxSubTotalsDS,
   AllowanceChargesDS,
   TaxTotalsDS,
   WithholdingTaxTotalsDS,
   TotalDS,
   DocumentReferencesDS,
   AdditionalCustomerDS,
   PdfDataDS,
)


DsNotesSendsModel = api.model(
    "DsNotesSends", {
         'BillingPeriod': fields.Nested(BillingPeriodDS),
         'AdditionalNDS': fields.Nested(AdditionalNDS),
         'SeriePrefix': fields.String(required=True, description="Serie prefix"),
         'SerieNumber': fields.String(required=True, description="Serie number"),
         'IssueDate': fields.String(required=True, description="Issue date"),
         'DueDate': fields.String(required=True, description="Due date"),
         'IssueTime': fields.String(required=True, description="Issue time"),
         'CorrelationDocumentId': fields.String(required=True, description="Correlation document id"),
         'SerieExternalKey': fields.String(required=True, description="Serie external key"),
         'DeliveryDate': fields.String(required=True, description="DeliveryDate"),
         'DeliveryTime': fields.String(required=True, description="Delivery time"),
         'PaymentMeans': fields.List(fields.Nested(PaymentMeansDS)),
         'PaymentExchangeRate': fields.List(fields.Nested(PaymentExchangeRate)),
         'AccountingCustomerParty': fields.Nested(AccountingCustomerParty),
         'AccountingSupplierParty': fields.Nested(AccountingSupplierParty),
         'Currency': fields.String(required=True, description="Currency"),
         'OperationType': fields.String(required=True, description="Operation type"),
         'Lines': fields.List(fields.Nested(LinesDesDS)),
         'TaxSubTotals': fields.List(fields.Nested(TaxSubTotalsDS)),
         'WithholdingTaxSubTotals': fields.List(fields.Nested(WithholdingTaxSubTotalsDS)),
         'AllowanceCharges': fields.List(fields.Nested(AllowanceChargesDS)),
         'TaxTotals': fields.List(fields.Nested(TaxTotalsDS)),
         'WithholdingTaxTotals': fields.List(fields.Nested(WithholdingTaxTotalsDS)),
         'Total': fields.Nested(TotalDS),
         'DocumentReferences': fields.List(fields.Nested(DocumentReferencesDS)),
         'AdditionalCustomers': fields.List(fields.Nested(AdditionalCustomerDS)),
         'PdfData': fields.Nested(PdfDataDS),
      })

DsNotesSendsFilterModel = api.model(
    "DsNotesSendsFilterModel", {
        "IssuerNit": fields.String(required=True, description="Nit de emisor"),
        "StartClientNit": fields.String(required=False, description="Rango inicial del nit del cliente"),
        "EndClientNit": fields.String(required=False, description="Rango final del nit del cliente"),
        "StartDate": fields.String(required=False, description="Fecha inicial a consultar aaaa-mm-dd"),
        "EndDate": fields.String(required=False, description="Fecha final a consultar aaaa-mm-dd"),
        "StartNumber": fields.String(required=False, description="Rango inicial del documento incluido el prefijo"),
        "EndNumber": fields.String(required=False, description="Rango final del documento incluido el prefijo"),
        "Status": fields.String(required=True, description="Estado del documento 1= enviado a la DIAN, 0= rechazado por la DIAN")
    }
)

DsNotesSendsFilterNumberModel = api.model(
    "DsNotesSendsFilterNumberModel", {
        "Nit": fields.String(required=True, description="Nit de emisor"),
        "DocType": fields.String(required=False, description="NC= Nota Credito, ND= Nota Debito"),
        "SeriePrefix": fields.String(required=False, description="prefijo del documento"),
        "SerieNumber": fields.String(required=False, description="numero del documento")

    }
)

allNotesSdModel = api.model(
    "allNotesSd", {
        "pageSize": fields.Integer(required=True, description="Tamaño de la pagina"),
        "pageNumber": fields.Integer(required=True, description="Numero de la pagina")
    }
)
