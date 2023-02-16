from flask_restx import Namespace, fields


api = Namespace("Envios facturas", description="Operaciones relacionadas con envios de facturas")


BillingPeriod = api.model("BillingPeriod", {
    'From': fields.String(required=True, description="Debe ir el numero inicial autorizado"),
    'To': fields.String(required=True, description="Debe ir el numero final autorizado"),
    'InvoiceAuthorization': fields.String(required=True, description="Debe corresponder a un número de autorización de este contribuyente emisor"),
    'StartDate': fields.Date(required=True, description="Debe ir la fecha de inicio del documento en formato AAAA-MM-DD"),
    'EndDate': fields.Date(required=True, description="Debe ir la fecha final del documento en formato AAAA-MM-DD")
})


Additional = api.model("Additional", {
      'CUFE': fields.String(required=True, description="Codigo unico de f.e"),
      'Contingency': fields.String(required=True, description="N= No contingencia S= Si contingencia"),
      'SendEmail': fields.Boolean(required=True, description="Debe colocar True o False"),
      'DianSoftwareId': fields.String(required=True, description="Este valor se obtiene de la plataforma de la DIAN"),
      'DianPin': fields.String(required=True, description="Este valor se obtiene de la plataforma de la DIAN"),
      'DianTechnicalKey': fields.String(required=True, description="Este valor se obtiene del endpoint Numbering con el nit y el diansoftwareid"),
      'DianTestSetId': fields.String(required=True, description="Este valor se obtiene de la plataforma de la DIAN"),
      'ProfileExecutionId': fields.String(required=True, description="1= Produccion 2= Habilitacion"),
})


PaymentMeans = api.model("PaymentMean", {
    'Code': fields.String(required=False, description="1= Contado 2=Credito"),
    'Mean': fields.String(required=False, description="10= Efectivo, 42= Consignacion Bancaria, 47= Transferencia Debito Bancaria, 48= Tarjeta Credito, 49= Tarjeta Debito, tabla 13.3.4.2 anexo 1.8, resolucion 12-2021"),
    'DueDate': fields.Date(required=False, description="Fecha de vencimiento de la factura"),
})

PaymentExchangeRate = api.model("PaymentExchangeRate", {
    'SourceCurrencyCode': fields.String(required=False, description="Codigo de la moneda para intercambiar= USD ó EUR, anexo 1.8, tabla 13.3.3 resolucion 12"),
    'CalculationRate': fields.String(required=False, description="Tasa de cambio en pesos colombianos= COP"),
    'Date': fields.Date(required=False, description="Fecha del intercambio"),
})

IdentificationIssuer = api.model("Identification", {
    'DocumentNumber': fields.String(required=True, description="Numero documento emisor"),
    'DocumentType': fields.String(required=True, description="11= Registro civil, 12= Tarjeta de identidad, 13= Cedula ciudadania, 21= Tarjeta extranjeria, 22= Cédula de extranjería 31=NIT, 41= Pasaporte, 42= Documento de identificación extranjero, tabla 13.2.1 Anexo 1.8, resolucion 12-2021"),
    'CountryCode': fields.String(required=True, description="CO= Colombia, para los demas codigos en la tabla 13.4.1 resolucion 12"),
    'CheckDigit': fields.String(required=False, description="Digito verificacion solo si es NIT"),
})
AddressIssuer = api.model("Address", {
    'DepartmentCode': fields.String(required=True, description="Codigo departamento DANE, mirar en la tabla 13.4.2 Departamentos resolucion 12"),
    'DepartmentName': fields.String(required=False, description="Nombre departamento"),
    'CityCode': fields.String(required=True, description="Codigo ciudad DANE, mirar en la tabla 13.4.3 Municipios resolucion 12"),
    'CityName': fields.String(required=False, description="Nombre ciudad"),
    'AddressLine': fields.String(required=False, description="Direccion del emisor"),
    'PostalCode': fields.String(required=False, description="Codigo postal emisor"),
    'Country': fields.String(required=True, description="CO= Colombia, para los demas codigos en la tabla 13.4.1 resolucion 12")
})
IssuerParty = api.model("IssuerParty", {
    'LegalType': fields.String(required=True, description="1= Persona jurídica 2= Persona natural"),
    'Identification': fields.Nested(IdentificationIssuer),
    'Name': fields.String(required=True, description="Nombre del emisor"),
    'Email': fields.String(required=False, description="Email emisor que tenga registrado en la DIAN"),
    'IndustryClasificationCode': fields.String(required=False, description="codigo actividad economica (CIIU), si son varios van separados con ;"),
    'Address': fields.Nested(AddressIssuer),
    'TaxScheme': fields.String(required=True, description="IVA,INC,IVA e INC ó No aplica"),
    'ResponsabilityTypes': fields.String(required=True, description="O-13 Gran contribuyente,O-15 autorretenedor,O-23 agente retenedor iva,O-47 regimen simple,R-99-PN no aplica, de la tabla 13.2.6.1 resolucion 12-2021")
})


AddressCustomer = api.model("AddressCustomer", {
    'DepartmentCode': fields.String(required=True, description="Codigo departamento DANE, mirar en la tabla 13.4.2 Departamentos resolucion 12"),
    'DepartmentName': fields.String(required=False, description="Nombre departamento"),
    'CityCode': fields.String(required=True, description="Codigo ciudad DANE, mirar en la tabla 13.4.3 Municipios resolucion 12"),
    'CityName': fields.String(required=False, description="Nombre ciudad"),
    'AddressLine': fields.String(required=False, description="Direccion del emisor"),
    'PostalCode': fields.String(required=False, description="Codigo postal emisor"),
    'Country': fields.String(required=True, description="CO= Colombia, para los demas codigos en la tabla 13.4.1 resolucion 12")
})
IdentificationCustomer = api.model("IdentificationCustomer", {
    'DocumentNumber': fields.String(required=True, description="Numero documento emisor"),
    'DocumentType': fields.String(required=True, description="11= Registro civil, 12= Tarjeta de identidad, 13= Cedula ciudadania, 21= Tarjeta extranjeria, 22= Cédula de extranjería 31=NIT, 41= Pasaporte, 42= Documento de identificación extranjero, tabla 13.2.1 Anexo 1.8, resolucion 12-2021"),
    'CountryCode': fields.String(required=True, description="CO= Colombia, para los demas codigos en la tabla 13.4.1 resolucion 12"),
    'CheckDigit': fields.String(required=False, description="Digito verificacion solo si es NIT")
})
CustommerDocumentContacts = api.model("DocumentContacts", {
    'Name': fields.String(required=False, description="Nombre de contacto"),
    'Type': fields.String(required=False, description="1= Persona jurídica 2= Persona natural"),
    'Telephone': fields.String(required=False, description="Telefono de contacto")
})
CustomerParty = api.model("CustomerParty", {
    'TeleFax': fields.String(required=False, description="Telefax de adquiriente"),
    'DocumentContacts': fields.List(fields.Nested(CustommerDocumentContacts)),
    'LegalType': fields.String(required=True, description="1= Persona jurídica 2= Persona natural"),
    'Identification': fields.Nested(IdentificationCustomer),
    'Name': fields.String(required=True, description="Nombre de adquiriente"),
    'Email': fields.String(required=False, description="Email de adquiriente"),
    'Address': fields.Nested(AddressCustomer),
    'TaxScheme': fields.String(required=True, description="IVA,INC,IVA e INC ó No aplica"),
    'ResponsabilityTypes': fields.List(fields.String(required=True, description="O-13 Gran contrib,O-15 autorrete,O-23 agente ret iva,O-47 regimen simple,R-99-PN no aplica tabla 13.2.6.1")),
})


LinesWithholdingTaxTotal = api.model("WithholdingTaxTotal", {
    'WithholdingTaxCategory': fields.String(required=False, description="ReteIVA, ReteICA, ReteRenta, mirar para los demas la tabla 13.2.2 anexo 1.8, resolucion 12-2021"),
    'TaxAmount': fields.String(required=False, description="Valor de impuesto"),
    'TaxableAmount': fields.String(required=False, description="Base gravable"),
})
LinesWithholdingTaxSubTotal = api.model("WithholdingTaxSubTotal", {
    'WithholdingTaxCategory': fields.String(required=False, description="ReteIVA, ReteICA, ReteRenta, mirar para los demas la tabla 13.2.2 anexo 1.8, resolucion 12-2021"),
    'TaxPercentage': fields.String(required=False, description="Valor de porcentaje"),
    'TaxableAmount': fields.String(required=False, description="Base gravable"),
    'TaxAmount': fields.String(required=False, description="Valor de impuesto"),
})
LinesItem = api.model("Item", {
    'SellerItemIdentification': fields.String(required=False, description="Codigo de articulo"),
    'Description': fields.String(required=True, description="Descripcion del articulo, maximo 300 caracteres"),
    'IncomePurposeCode': fields.String(required=False, description="Codigo proposito de ingresos"),
    'UnitsPerPackage': fields.String(required=False, description="Unidades por paquete"),
    'BrandName': fields.String(required=False, description="Marca del articulo"),
    'ModelName': fields.String(required=False, description="Modelo del articulo"),
})
LinesAllowanceCharge = api.model("AllowanceCharge", {
    'ChargeIndicator': fields.String(required=False, description="Indicador de carga, True=Debito False=Credito"),
    'BaseAmount': fields.String(required=False, description="Valor base sobre la que se calcula el descuento"),
    'ReasonCode': fields.String(required=False, description="00= Descuento no condicionado, 01= Descuento condicionado"),
    'Reason': fields.String(required=False, description="Razon (texto libre)"),
    'Amount': fields.String(required=False, description="Valor del descuento"),
    'Percentage': fields.String(required=False, description="Porcentaje del descuento"),
    'SequenceIndicator': fields.String(required=False, description="Indicador de secuencia 1,2.."),
})
LinesTaxTotal = api.model("TaxTotal", {
    'TaxCategory': fields.String(required=False, description="IVA, ICA, IC, mirar para los demas la tabla 13.2.2 anexo 1.8, resolucion 12-2021"),
    'TaxAmount': fields.String(required=False, description="Valor de impuesto"),
    'RoundingAmount': fields.String(required=False, description="Valor de redondeo"),
})
LinesTaxSubTotal = api.model("TaxSubTotal", {
    'TaxableAmount': fields.String(required=False, description="Taxable amount/base gravable"),
    'TaxCategory': fields.String(required=False, description="IVA, ICA, IC, mirar para los demas codigos la tabla 13.2.2 anexo 1.8, resolucion 12-2021"),
    'TaxPercentage': fields.String(required=False, description="Porcentaje impuesto"),
    'PerUnitAmount': fields.String(required=False, description="Valor por unidad"),
    'TaxAmount': fields.String(required=False, description="Valor de impuesto"),
})
LinesDes = api.model("LineDes", {
    'Number': fields.String(required=False, description="Numero de linea"),
    'Quantity': fields.String(required=False, description="Cantidad del articulo"),
    'QuantityUnitOfMeasure': fields.String(required=False, description="10= Grupo, 94= Unidad, NAR= numero de articulos, mirar para los demás codigos la tabla 13.3.6 anexo 1.8, resolucion 12-2021"),
    'TaxSubTotals': fields.List(fields.Nested(LinesTaxSubTotal)),
    'TaxTotals': fields.List(fields.Nested(LinesTaxTotal)),
    'UnitPrice': fields.String(required=False, description="Debe ir el precio unitario"),
    'GrossAmount': fields.String(required=False, description="Debe ir el valor bruto"),
    'NetAmount': fields.String(required=False, description="Debe ir el valor neto"),
    'AllowanceCharges': fields.List(fields.Nested(LinesAllowanceCharge)),
    'Item': fields.Nested(LinesItem),
    'WithholdingTaxSubTotals': fields.List(fields.Nested(LinesWithholdingTaxSubTotal)),
    'WithholdingTaxTotals': fields.List(fields.Nested(LinesWithholdingTaxTotal))
})
TaxSubTotals = api.model("TaxSubTotals", {
    'TaxCategory': fields.String(required=True, description="IVA, ICA, IC, mirar para los demas codigos la tabla 13.2.2 anexo 1.8, resolucion 12-2021"),
    'TaxPercentage': fields.String(required=True, description="Valor porcentaje"),
    'TaxableAmount': fields.String(required=True, description="Base gravable"),
    'TaxAmount': fields.String(required=True, description="Valor impuesto")
})
WithholdingTaxSubTotals = api.model("WithholdingTaxSubTotals", {
    'WithholdingTaxCategory': fields.String(required=True, description="ReteIVA, ReteICA, ReteRenta, mirar para los demas codigos la tabla 13.2.2 anexo 1.8, resolucion 12-2021"),
    'TaxPercentage': fields.String(required=True, description="Valor porcentaje"),
    'TaxableAmount': fields.String(required=True, description="Base gravable"),
    'TaxAmount': fields.String(required=True, description="Valor impuesto")
})
AllowanceCharges = api.model("AllowanceCharges_invoice", {
    'ChargeIndicator': fields.Boolean(required=False, description="Indicador cargo, True=Debito False=Credito"),
    'BaseAmount': fields.String(required=False, description="Valor base"),
    'ReasonCode': fields.String(required=False, description="00= Descuento no condicionado, 01= Descuento condicionado, solo para credito"),
    'Reason': fields.String(required=False, description="Razon (texto libre)"),
    'Amount': fields.String(required=False, description="Valor del descuento"),
    'Percentage': fields.String(required=False, description="Porcentaje de descuento"),
    'SequenceIndicator': fields.String(required=False, description="Indicador de secuencia 1,2.."),
})
TaxTotals = api.model("TaxTotals", {
    'TaxCategory': fields.String(required=True, description="IVA, ICA, IC, mirar para los demas codigos la tabla 13.2.2 anexo 1.8, resolucion 12-2021"),
    'TaxAmount': fields.String(required=True, description="Valor impuesto"),
    'RoundingAmount': fields.String(required=True, description="Valor redondeo"),
})
WithholdingTaxTotals = api.model("WithholdingTaxTotals", {
    'WithholdingTaxCategory': fields.String(required=True, description="ReteIVA, ReteICA, ReteRenta, mirar para los demas codigos la tabla 13.2.2 anexo 1.8, resolucion 12-2021"),
    'TaxAmount': fields.String(required=True, description="Valor de impuesto"),
})
Total = api.model("Total", {
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


DocumentReferences = api.model("DocumentReferences", {
    'DocumentReferred': fields.String(required=False, description="Debe ir el documento referido"),
    'IssueDate': fields.Date(required=False, description="Debe ir la fecha de creacion del documento"),
    'Type': fields.String(required=False, description="O= Orden, D= Despacho, R= Recibido, A= Adicional, NC= Nota Credito=, ND Nota Debito"),
    'OtherReferenceTypeId': fields.String(required=False, description="Id de otra referencia"),
    'OtherReferenceTypeDescription': fields.String(required=False, description="Descripcion otro tipo de referencia"),
    'DocumentReferredCUFE': fields.String(required=False, description="Debe ir el CUFE del documento referido")
})

IdentificationAdditionalCustomers = api.model("IdentificationAdditionalCustomers", {
    'DocumentNumber': fields.String(required=False, description="Numero de documento"),
    'DocumentType': fields.String(required=False, description="11= Registro civil, 12= Tarjeta de identidad, 13= Cedula ciudadania, 21= Tarjeta extranjeria, 22= Cédula de extranjería 31=NIT, 41= Pasaporte, 42= Documento de identificación extranjero, tabla 13.2.1 Anexo 1.8, resolucion 12-2021"),
    'CountryCode': fields.String(required=False, description="CO= Colombia, ES= España, mirar los demas codigos en la tabla 13.4.1 resolucion 12"),
    'CheckDigit': fields.String(required=False, description="Debe ir el digito de verificacion")
})
AdditionalCustomer = api.model("AdditionalCustomers", {
    'Name': fields.String(required=False, description="Debe ir el nombre de adquiriente adicional"),
    'CommercialRegistrationNumber': fields.String(required=False, description="Debe ir el numero registro comercial del adquiriente"),
    'Identification': fields.Nested(IdentificationAdditionalCustomers),
    'ParticipationPercentage': fields.String(required=False, description="Debe ir el porcentaje de participacion")
})


Pdf = api.model("Pdf", {
    'Pdf': fields.String(required=False, description="Pdf string base64")
})
