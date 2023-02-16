from flask_restx import fields
from .sub_schemas import api
from .sub_schemas import (
   BillingPeriodDS,
   AdditionalDS,
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
   PdfDataDS
)

GetNumberingModel = api.model(
    'GetNumbering', {
        'Nit': fields.String(required=True, description="Nit del emisor")
    }
)

GetStatusModel = api.model(
    'GetStatus', {
        'Nit': fields.String(required=True, description="Nit del emisor"),
        'CUFE': fields.String(required=True, description="CUFE, CUNE, CUDE a consultar")
    }
)

SupportDocModel = api.model(
    "SupportDoc", {
         'BillingPeriod': fields.Nested(BillingPeriodDS),
         'Additional': fields.Nested(AdditionalDS),
         'SeriePrefix': fields.String(required=True, description="Prefijo de serie de la factura"),
         'SerieNumber': fields.String(required=True, description="Numero de serie de la factura"),
         'IssueDate': fields.String(required=True, description="Fecha creacion de la factura"),
         'DueDate': fields.String(required=True, description="Fecha vencimiento de la factura"),
         'IssueTime': fields.String(required=True, description="Hora de creacion de la factura"),
         'NoteDocument': fields.String(required=False, description="Comentarios del documento"),
         'CorrelationDocumentId': fields.String(required=True, description="Id documento correlacion"),
         'SerieExternalKey': fields.String(required=True, description="Serie llave externa"),
         'DeliveryDate': fields.String(required=True, description="Fecha envio factura f"),
         'DeliveryTime': fields.String(required=True, description="Hora envio factura"),
         'PaymentMeans': fields.List(fields.Nested(PaymentMeansDS)),
         'PaymentExchangeRate': fields.List(fields.Nested(PaymentExchangeRate)),
         'AccountingCustomerParty': fields.Nested(AccountingCustomerParty),
         'AccountingSupplierParty': fields.Nested(AccountingSupplierParty),
         'Currency': fields.String(required=True, description="Divisa"),
         'OperationType': fields.String(required=True, description="Tipo de operacion"),
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

SupportDocNoteModel = api.model(
    "SupportDocNote", {
         'BillingPeriod': fields.Nested(BillingPeriodDS),
         'Additional': fields.Nested(AdditionalDS),
         'SeriePrefix': fields.String(required=True, description="Prefijo de la nota"),
         'SerieNumber': fields.String(required=True, description="Numero de nota"),
         'IssueDate': fields.String(required=True, description="Fecha de emision nota"),
         'DueDate': fields.String(required=True, description="Fecha de vencimiento nota"),
         'IssueTime': fields.String(required=True, description="Hora de emision"),
         'CorrelationDocumentId': fields.String(required=True, description="Texto libre"),
         'SerieExternalKey': fields.String(required=False, description="Llave externa"),
         'DeliveryDate': fields.String(required=False, description="Fecha de entrega"),
         'DeliveryTime': fields.String(required=False, description="Tiempo de entrega"),
         'PaymentMeans': fields.List(fields.Nested(PaymentMeansDS)),
         'AccountingCustomerParty': fields.Nested(AccountingCustomerParty),
         'AccountingSupplierParty': fields.Nested(AccountingSupplierParty),
         'Currency': fields.String(required=True, description="Divisa"),
         'OperationType': fields.String(required=True, description="Tipo de operacion"),
         'ReasonCredit': fields.String(required=True, description="Codigo de la nota credito"),
         'NoteDocument': fields.String(required=True, description="Texto adicional"),
         'Lines': fields.List(fields.Nested(LinesDesDS)),
         'TaxSubTotals': fields.List(fields.Nested(TaxSubTotalsDS)),
         'WithholdingTaxSubTotals': fields.List(fields.Nested(WithholdingTaxSubTotalsDS)),
         'AllowanceCharges': fields.List(fields.Nested(AllowanceChargesDS)),
         'TaxTotals': fields.List(fields.Nested(TaxTotalsDS)),
         'WithholdingTaxTotals': fields.List(fields.Nested(WithholdingTaxTotalsDS)),
         'Total': fields.Nested(TotalDS),
         'DocumentReferences': fields.List(fields.Nested(DocumentReferencesDS)),
         'AdditionalCustomers': fields.List(fields.Nested(AdditionalCustomerDS)),
         'PdfData': fields.Nested(PdfDataDS)
      })

SupportDocNumberModel = api.model(
    "SupportDocNumberModel", {
        "Nit": fields.String(required=True, description="Nit de emisor"),
        "DocType": fields.String(required=False, description="Tipo de documento DS=documento soporte"),
        "SeriePrefix": fields.String(required=False, description="prefijo del documento"),
        "SerieNumber": fields.String(required=False, description="numero del documento")

    }
)

supportDocFilterCufeModel = api.model(
    "SendsFilterModel", {
        "Nit": fields.String(required=True, description="Nit de emisor"),
        "Id": fields.Integer(required=True, description="Id del documento"),
        "Cufe": fields.String(required=True, description="nuevo CUDS")
    }
)
