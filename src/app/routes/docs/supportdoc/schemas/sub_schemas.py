from flask_restx import Namespace, fields


api = Namespace("Documentos Soporte", description="Operaciones relacionadas con Documentos Soporte")


BillingPeriodDS = api.model("BillingPeriodDS", {
    'From': fields.String(required=True, description="Numero inicial autorizado"),
    'To': fields.String(required=True, description="Numero final autorizado"),
    'InvoiceAuthorization': fields.String(required=True, description="Resolucion DIAN factura"),
    'StartDate': fields.String(required=True, description="Fecha inicio yyyy-mm-dd"),
    'EndDate': fields.String(required=True, description="Fecha fin yyyy-mm-dd")
})


AdditionalDS = api.model("AdditionalDS", {
      'CUDS': fields.String(required=True, description="CUDS"),
      'SendEmail': fields.Boolean(required=True, description="Bandera que indica si se envia el documento al email"),
      'DianSoftwareId': fields.String(required=True, description="Se obtiene de la plataforma de la DIAN"),
      'DianPin': fields.String(required=True, description="Se obtiene de la plataforma de la DIAN"),
      'DianTechnicalKey': fields.String(required=True, description="Se obtiene del endpoint Numbering"),
      'DianTestSetId': fields.String(required=True, description="Se obtiene de la plataforma de la DIAN"),
      'CustomizationID': fields.String(required=True, description="Procedencia del vendedor. Colocar 10 = Residentes 11 = No residentes"),
      'ProfileExecutionId': fields.String(required=True, description="1= Produccion 2= Habilitacion")
})


PaymentMeansDS = api.model("PaymentMeansDS", {
    'Code': fields.String(required=False, description="1 Contado 2 Credito"),
    'Mean': fields.String(required=False, description="10 Efectivo tabla 13.3.4.2 anexo 1.8"),
    'DueDate': fields.String(required=False, description="Fecha de vencimiento de la factura")
})

PaymentExchangeRate = api.model("PaymentExchangeRate", {
    'SourceCurrencyCode': fields.String(required=False, description="Codigo de la moneda para intercambiar USD, EUR, anexo 1.8, tabla 13.3.3"),
    'CalculationRate': fields.String(required=False, description="Tasa de cambio en pesos COP"),
    'Date': fields.String(required=False, description="Fecha del intercambio"),
})


IdentificationIssuerDS = api.model("IdentificationIssuerDS", {
    'DocumentNumber': fields.String(required=True, description="Numero documento emisor"),
    'DocumentType': fields.String(required=True, description="13=CED 31=NIT tabla 13.2.1 Anexo 1.8"),
    'CountryCode': fields.String(required=True, description="CO para Colombia"),
    'CheckDigit': fields.String(required=False, description="Digito verificacion solo si es NIT"),
})
AddressIssuerDS = api.model("AddressIssuerDS", {
    'DepartmentCode': fields.String(required=True, description="Codigo departamento DANE"),
    'DepartmentName': fields.String(required=False, description="Nombre departamento"),
    'CityCode': fields.String(required=True, description="Codigo ciudad DANE"),
    'CityName': fields.String(required=False, description="Nombre ciudad"),
    'AddressLine': fields.String(required=False, description="Direccion del emisor"),
    'PostalCode': fields.String(required=False, description="Codigo postal emisor"),
    'Country': fields.String(required=True, description="CO para Colombia")
})
AccountingCustomerParty = api.model("AccountingCustomerParty", {
    'LegalType': fields.String(required=True, description="1 Jurídica 2 Natural"),
    'Identification': fields.Nested(IdentificationIssuerDS),
    'Name': fields.String(required=True, description="Nombre emisor"),
    'Email': fields.String(required=False, description="Email emisor que tenga registrado en la DIAN"),
    'IndustryClasificationCode': fields.String(required=False, description="codigo actividad economica (CIU), si son varios van separados con ;"),
    'Address': fields.Nested(AddressIssuerDS),
    'TaxScheme': fields.String(required=True, description="IVA,INC,IVA e INC,No aplica"),
    'ResponsabilityTypes': fields.String(required=True, description="O-13 Gran contrib,O-15 autorrete,O-23 agente ret iva,O-47 regimen simple,R-99-PN no aplica tabla 13.2.6.1")
})


AddressCustomerDS = api.model("AddressCustomerDS", {
    'DepartmentCode': fields.String(required=True, description="Codigo departamento DANE"),
    'DepartmentName': fields.String(required=False, description="Nombre departamento"),
    'CityCode': fields.String(required=True, description="Codigo ciudad DANE"),
    'CityName': fields.String(required=False, description="Nombre ciudad"),
    'AddressLine': fields.String(required=False, description="Direccion del adquiriente"),
    'PostalCode': fields.String(required=False, description="Codigo postal"),
    'Country': fields.String(required=True, description="CO para Colombia")
})
IdentificationCustomerDS = api.model("IdentificationCustomerDS", {
    'DocumentNumber': fields.String(required=True, description="Numero documento adquiriente"),
    'DocumentType': fields.String(required=True, description="13 CED 31 NIT tabla 13.2.1 Anexo 1.8 resolucion 67-2021"),
    'CountryCode': fields.String(required=True, description="Codigo pais CO para Colombia"),
    'CheckDigit': fields.String(required=False, description="Digito verificacion solo si es NIT")
})
CustommerDocumentContacts = api.model("DocumentContacts", {
    'Name': fields.String(required=True, description="Nombre contacto"),
    'Type': fields.String(required=True, description="1 Jurídica 2 Natural"),
    'Telephone': fields.String(required=False, description="Telefono contacto")
})
AccountingSupplierParty = api.model("AccountingSupplierParty", {
    'TeleFax': fields.String(required=True, description="Telefax adquiriente"),
    'DocumentContacts': fields.List(fields.Nested(CustommerDocumentContacts)),
    'LegalType': fields.String(required=True, description="1 Jurídica 2 Natural"),
    'Identification': fields.Nested(IdentificationCustomerDS),
    'Name': fields.String(required=True, description="Nombre adquiriente"),
    'Email': fields.String(required=False, description="Email adquiriente"),
    'Address': fields.Nested(AddressCustomerDS),
    'TaxScheme': fields.String(required=True, description="IVA,INC,IVA e INC,No aplica"),
    'ResponsabilityTypes': fields.List(fields.String(required=True, description="O-13 Gran contribuyente,O-15 autorretenedor,O-23 agente retenedor iva,O-47 regimen simple,R-99-PN no aplica, de la tabla 13.2.6.1 resolucion 67-2021")),
})


LinesWithholdingTaxTotalDS = api.model("WithholdingTaxTotalDS", {
    'WithholdingTaxCategory': fields.String(required=False, description="Columna nombre de la tabla 13.2.2 anexo 1.8, resolucion 67-2021"),
    'TaxAmount': fields.String(required=False, description="Tax amount/valor impuesto"),
    'TaxableAmount': fields.String(required=False, description="Taxable amount/base gravable")
})
LinesWithholdingTaxSubTotalDS = api.model("WithholdingTaxSubTotalDS", {
    'WithholdingTaxCategory': fields.String(required=True, description="Columna nombre de la tabla 13.2.2 anexo 1.8, resolucion 67-2021"),
    'TaxPercentage': fields.String(required=True, description="Tax percentage/valor porcentaje"),
    'TaxableAmount': fields.String(required=True, description="Taxable amount/base gravable"),
    'TaxAmount': fields.String(required=True, description="Tax amount/valor impuesto")
})
LinesItemDS = api.model("ItemDS", {
    'SellerItemIdentification': fields.String(required=False, description="Seller item identification/codigo articulo"),
    'Description': fields.String(required=True, description="Descripcion"),
    'IncomePurposeCode': fields.String(required=False, description="Codigo proposito de ingresos"),
    'UnitsPerPackage': fields.String(required=False, description="Unidades por paquete"),
    'BrandName': fields.String(required=False, description="Marca articulo"),
    'ModelName': fields.String(required=False, description="Modelo articulo")
})
LinesAllowanceChargeDS = api.model("AllowanceChargeDS", {
    'ChargeIndicator': fields.String(required=False, description="Indicador de carga True=Debito False=Credito"),
    'BaseAmount': fields.String(required=False, description="Base amount"),
    'ReasonCode': fields.String(required=False, description="Reason code"),
    'Reason': fields.String(required=False, description="Reason"),
    'Amount': fields.String(required=False, description="Amount"),
    'Percentage': fields.String(required=False, description="Percentage"),
    'SequenceIndicator': fields.String(required=False, description="Sequence indicator")
})
LinesTaxTotalDS = api.model("TaxTotalDS", {
    'TaxCategory': fields.String(required=False, description="Columna nombre de la tabla 13.2.2 anexo 1.8, resolucion 67-2021"),
    'TaxAmount': fields.String(required=False, description="Tax amount/valor impuesto"),
    'RoundingAmount': fields.String(required=False, description="Rounding amount/ redondeo"),
})
LinesTaxSubTotalDS = api.model("TaxSubTotalDS", {
    'TaxableAmount': fields.String(required=False, description="Taxable amount/base gravable"),
    'TaxCategory': fields.String(required=False, description="Columna nombre de la tabla 13.2.2 anexo 1.8, resolucion 67-2021"),
    'TaxPercentage': fields.String(required=False, description="Tax percentage"),
    'PerUnitAmount': fields.String(required=False, description="Per unit amount"),
    'TaxAmount': fields.String(required=False, description="Tax amount")
})

LinesInvoicePeriodDS = api.model("InvoicePeriodDS", {
    'StarDate': fields.String(required=False, description="Fecha de compra, si la operacion es semanal maximo 6 dias antes de la fecha de emision del documento"),
    'DescriptionCode': fields.String(required=False, description="Codigo operacion 1= Por operacion 2 = Acumulado semanal")
})
LinesDesDS = api.model("LineDesDS", {
    'Number': fields.String(required=False, description="Numero"),
    'Quantity': fields.String(required=False, description="Cantidad"),
    'QuantityUnitOfMeasure': fields.String(required=False, description="Poner 10 o mirar la tabla 3.3.6 anexo 1.8 resolucion 67-2021"),
    'TaxSubTotals': fields.List(fields.Nested(LinesTaxSubTotalDS)),
    'TaxTotals': fields.List(fields.Nested(LinesTaxTotalDS)),
    'InvoicePeriod': fields.Nested(LinesInvoicePeriodDS),
    'UnitPrice': fields.String(required=False, description="Precio unidad"),
    'GrossAmount': fields.String(required=False, description="Valor bruto"),
    'NetAmount': fields.String(required=False, description="Valor neto"),
    'WithholdingTaxTotals': fields.List(fields.Nested(LinesWithholdingTaxTotalDS))
})


TaxSubTotalsDS = api.model("TaxSubTotalsDS", {
    'TaxCategory': fields.String(required=True, description="Columna nombre de la tabla 13.2.2 anexo 1.8, resolucion 67-2021"),
    'TaxPercentage': fields.String(required=True, description="Valor porcentaje"),
    'TaxableAmount': fields.String(required=True, description="Base gravable"),
    'TaxAmount': fields.String(required=True, description="Valor impuesto")
})


WithholdingTaxSubTotalsDS = api.model("WithholdingTaxSubTotal", {
    'WithholdingTaxCategory': fields.String(required=True, description="Columna nombre de la tabla 13.2.2 anexo 1.8, resolucion 67-2021"),
    'TaxPercentage': fields.String(required=True, description="Valor porcentaje"),
    'TaxableAmount': fields.String(required=True, description="Base gravable"),
    'TaxAmount': fields.String(required=True, description="Valor impuesto")
})


AllowanceChargesDS = api.model("AllowanceCharges", {
    'ChargeIndicator': fields.Boolean(required=True, description="Indicador cargo, True=Debito False=Credito"),
    'BaseAmount': fields.String(required=True, description="Valor base"),
    'ReasonCode': fields.String(required=True, description="Codigo razon tabla 13.3.8 resolucion 67-2021, solo para credito"),
    'Reason': fields.String(required=True, description="Razon texto libre"),
    'Amount': fields.String(required=True, description="Valor"),
    'Percentage': fields.String(required=True, description="Porcentaje"),
    'SequenceIndicator': fields.String(required=True, description="Indicador secuencia"),
})


TaxTotalsDS = api.model("TaxTotals", {
    'TaxCategory': fields.String(required=True, description="Columna nombre de la tabla 13.2.2 anexo 1.8, resolucion 67-2021"),
    'TaxAmount': fields.String(required=True, description="Valor impuesto"),
    'RoundingAmount': fields.String(required=True, description="Valor redondeo"),
})


WithholdingTaxTotalsDS = api.model("WithholdingTaxTotals", {
    'WithholdingTaxCategory': fields.String(required=True, description="Columna nombre de la tabla 13.2.2 anexo 1.8, resolucion 67-2021"),
    'TaxAmount': fields.String(required=True, description="Valor impuesto"),
})


TotalDS = api.model("Total", {
    'GrossAmount': fields.String(required=True, description="Valor bruto"),
    'TotalBillableAmount': fields.String(required=True, description="Importe total facturable"),
    'PayableAmount': fields.String(required=True, description="Cantidad a pagar"),
    'TaxableAmount': fields.String(required=True, description="Base imponible"),
    'AllowancesTotalAmount': fields.String(required=False, description="Importe total descuentos"),
    'ChargesTotalAmount': fields.String(required=False, description="Importe total cargos"),
    'PrePaidTotalAmount': fields.String(required=False, description="Importe total prepago"),
    'TotalIva': fields.String(required=True, description="Total iva"),
    'TotalIca': fields.String(required=True, description="Total ica"),
    'TotalTaxConsume': fields.String(required=True, description="Consumo total de impuestos"),
})


DocumentReferencesDS = api.model("DocumentReferencesDS", {
    'DocumentReferred': fields.String(required=False, description="Documento referido"),
    'IssueDate': fields.String(required=False, description="Fecha creacion"),
    'Type': fields.String(required=False, description="O Orden, D Despacho, R Recibido A Adicional NC Nota Credito NB Nota Debito"),
    'OtherReferenceTypeId': fields.String(required=False, description="Id otra referencia"),
    'OtherReferenceTypeDescription': fields.String(required=False, description="Descripcion otro tipo de referencia"),
    'DocumentReferredCUFE': fields.String(required=False, description="CUFE documento referido")
})

IdentificationAdditionalCustomersDS = api.model("IdentificationAdditionalCustomersDS", {
    'DocumentNumber': fields.String(required=False, description="Numero documento"),
    'DocumentType': fields.String(required=False, description="13 CED 31 NIT tabla 13.2.1 Anexo 1.8"),
    'CountryCode': fields.String(required=False, description="Codigo pais"),
    'CheckDigit': fields.String(required=False, description="Digito verificacion")
})
AdditionalCustomerDS = api.model("AdditionalCustomerDS", {
    'Name': fields.String(required=False, description="Name"),
    'CommercialRegistrationNumber': fields.String(required=False, description="Numero registro comercial"),
    'Identification': fields.Nested(IdentificationAdditionalCustomersDS),
    'ParticipationPercentage': fields.String(required=False, description="Porcentaje participacion")
})


PdfDataDS = api.model("PdfDataDS", {
    'Pdf': fields.String(required=False, description="Pdf string base64"),
})

