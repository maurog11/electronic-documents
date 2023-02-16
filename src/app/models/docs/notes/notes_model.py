# -*- coding: utf-8 -*-
#########################################################
import hashlib
import os
from base64 import b64encode, b64decode
from app.models import BaseModel
from app import db
from app.exception import InternalServerError
from sqlalchemy.orm import validates
from app.utils import FieldValidations, ResponseData


class NotesModel(BaseModel):
    __tablename__ = 'notes'

    IssuerNit = db.Column(db.String(20), nullable=False, comment='Nit de la empresa o emisor ')
    IssuerName = db.Column(db.String(200), nullable=False, comment='Nombre o razon social del emisor ')
    DocType = db.Column(db.String(5), nullable=False, comment='Tipo de Doc AD=Contenedor FV=factura NC=Nota Cr ND=Nota '
                                                              'DB DS=Documento Soporte NOM=Nomina NOMA=Nomina Ajuste ')
    SeriePrefix = db.Column(db.String(4), nullable=False, comment='Prefijo del documento de la empresa ')
    SerieNumber = db.Column(db.String(20), nullable=False, comment='numero del documento de la empresa ')
    InvoiceAuthorization = db.Column(db.String(14), nullable=False, comment='Resoloucion DIAN ')
    Contingency = db.Column(db.String(1), nullable=False, comment='Contigencia S o N')
    StartDate = db.Column(db.String(10), nullable=False, comment='Prefijo del documento de la empresa ')
    EndDate = db.Column(db.String(10), nullable=False, comment='Prefijo del documento de la empresa ')
    FromBillingPeriod = db.Column(db.Integer, nullable=False, comment='Prefijo del documento de la empresa ')
    ToBillingPeriod = db.Column(db.Integer, nullable=False, comment='Prefijo del documento de la empresa ')
    DianSoftwareId = db.Column(db.String(100), nullable=False, comment='id del software de la Dian ')
    DianPin = db.Column(db.String(5), nullable=False, comment='id del software de la Dian ')
    DianTechnicalKey = db.Column(db.String(100), nullable=False, comment='llave tecnica de la Dian ')

    Reason = db.Column(db.String(2), nullable=False, comment='tipo de documento tabla 13.1.3 ')
    ReferenceId = db.Column(db.String(20), nullable=False, comment='factura a la que se aplica la nota ')
    ResponseCode = db.Column(db.String(2), nullable=False, comment='concepto de la nota tabla 13.24.4 o 13.2.5  ')
    NoteDescription = db.Column(db.String(100), nullable=False, comment='comentarios de la nota   ')
    InvoiceDocumentReferenceId = db.Column(db.String(20), nullable=True, comment='factura a aplicar la nota ')
    InvoiceDocumentReferenceIssueDate = db.Column(db.String(10), nullable=True, comment='fecha factura ')
    InvoiceDocumentReferenceCufe = db.Column(db.String(96), nullable=True, comment='cufe factura ')

    OperationType = db.Column(db.String(1), nullable=True, comment='tipo operacion tabla 13.1.5.1 ')
    OrderReferenceId = db.Column(db.String(20), nullable=True, comment='numero de pedido ')
    OrderReferenceIssueDate = db.Column(db.String(20), nullable=True, comment='fecha numero de pedido ')
    DespatchDocumentReferenceId = db.Column(db.String(20), nullable=True, comment='numero de despacho ')
    DespatchDocumentIssueDate = db.Column(db.String(10), nullable=True, comment='fecha despacho')
    ReceiptDocumentReferenceId = db.Column(db.String(20), nullable=True, comment='numero de despacho ')
    ReceiptDocumentIssueDate = db.Column(db.String(10), nullable=True, comment='fecha despacho')
    AdditionalDocumentReferenceId = db.Column(db.String(20), nullable=True, comment='numero de documento contingencia ')
    AdditionalDocumentIssueDate = db.Column(db.String(10), nullable=True, comment='fecha contingencia')
    AdditionalDocumentTypeCode = db.Column(db.String(10), nullable=True, comment='codigo interno')
    ProfileExecutionId = db.Column(db.String(1), nullable=False,
                                   comment='tipo de ambiente 1=Produccion 2=Habilitacion ')
    Uuid = db.Column(db.String(100), nullable=False, comment='cude ')
    IssueDate = db.Column(db.String(10), nullable=False, comment='tipo de ambiente 1=Produccion 2=Habilitacion ')
    IssueTime = db.Column(db.String(14), nullable=False, comment='tipo de ambiente 1=Produccion 2=Habilitacion ')
    DueDate = db.Column(db.String(1), nullable=False, comment='fecha vencimiento ')
    NoteDocument = db.Column(db.String(100), nullable=False, comment='texto libre ')
    Currency = db.Column(db.String(3), nullable=False, comment='divisa ')

    ActualDeliveryDate = db.Column(db.String(10), nullable=False, comment='nit vendedor ')
    ActualDeliveryTime = db.Column(db.String(10), nullable=False, comment='nit vendedor ')

    DeliveryCityCode = db.Column(db.String(5), nullable=True, comment='codigo ciudad vendedor ')
    DeliveryCityName = db.Column(db.String(60), nullable=True, comment='nombre ciudad vendedor ')
    DeliveryPostalZone = db.Column(db.String(10), nullable=True, comment='zona postal vendedor ')
    DeliveryDepartment = db.Column(db.String(60), nullable=True, comment='nombre departamento vendedor ')
    DeliveryDepartmentCode = db.Column(db.String(60), nullable=True, comment='codigo departamento vendedor ')
    DeliveryAddress = db.Column(db.String(5), nullable=True, comment='direccion entrega ')
    DeliveryCountryCode = db.Column(db.String(3), nullable=True, comment='direccion entrega ')
    DeliveryCountryName = db.Column(db.String(3), nullable=True, comment='direccion entrega ')
    DeliveryCountryLanguage = db.Column(db.String(2), nullable=True, comment='direccion entrega ')
    RoundingAmount = db.Column(db.Float, nullable=False, comment='redondeo ')
    LineExtensionAmount = db.Column(db.Float, nullable=False, comment=' Total Valor Bruto antes de tributos:')
    TaxExclusiveAmount = db.Column(db.Float, nullable=False, comment=' Total Valor Base Imponible')
    TaxInclusiveAmount = db.Column(db.Float, nullable=False, comment=' Total de Valor Bruto más tributos')

    TotalIva = db.Column(db.Float, nullable=False, comment=' Total iva')
    TotalTaxConsume = db.Column(db.Float, nullable=False, comment=' Total impuesto al consumo')
    TotalIca = db.Column(db.Float, nullable=False, comment=' Total ica')

    AllowanceTotalAmount = db.Column(db.Float, nullable=False, comment=' Total descuentos')
    ChargeTotalAmount = db.Column(db.Float, nullable=False, comment=' Total cargos')
    PrePaidAmount = db.Column(db.Float, nullable=False, comment=' Total anticipos')
    PayableAmount = db.Column(db.Float, nullable=False, comment=' Total documento')

    def export_data(self):
        return {
            'CreateDate': self.CreateDate,
            'UpdateDate': self.UpdateDate,
            'IssuerNit': self.IssuerNit,
            'IssuerName': self.IssuerName,
            'DocType': self.DocType,
            'SeriePrefix': self.SeriePrefix,
            'SerieNumber': self.SerieNumber,
            'InvoiceAuthorization': self.InvoiceAuthorization,
            'Contingency': self.Contingency,
            'StartDate': self.StartDate,
            'EndDate': self.EndDate,
            'FromBillingPeriod': self.FromBillingPeriod,
            'ToBillingPeriod': self.ToBillingPeriod,
            'DianSoftwareId': self.DianSoftwareId,
            'DianPin': self.DianPin,
            'DianTechnicalKey': self.DianTechnicalKey,
            'Reason': self.Reason,
            'ReferenceId': self.ReferenceId,
            'ResponseCode': self.ResponseCode,
            'NoteDescription': self.NoteDescription,
            'InvoiceDocumentReferenceId': self.InvoiceDocumentReferenceId,
            'InvoiceDocumentReferenceIssueDate': self.InvoiceDocumentReferenceIssueDate,
            'InvoiceDocumentReferenceCufe': self.InvoiceDocumentReferenceCufe,
            'OperationType': self.OperationType,
            'OrderReferenceId': self.OrderReferenceId,
            'OrderReferenceIssueDate': self.OrderReferenceIssueDate,
            'DespatchDocumentReferenceId': self.DespatchDocumentReferenceId,
            'DespatchDocumentIssueDate': self.DespatchDocumentIssueDate,
            'ReceiptDocumentReferenceId': self.ReceiptDocumentReferenceId,
            'ReceiptDocumentIssueDate': self.ReceiptDocumentIssueDate,
            'AdditionalDocumentReferenceId': self.AdditionalDocumentReferenceId,
            'AdditionalDocumentIssueDate': self.AdditionalDocumentIssueDate,
            'AdditionalDocumentTypeCode': self.AdditionalDocumentTypeCode,
            'ProfileExecutionId': self.ProfileExecutionId,
            'Uuid': self.Uuid,
            'IssueDate': self.IssueDate,
            'IssueTime': self.IssueTime,
            'DueDate': self.DueDate,
            'NoteDocument': self.NoteDocument,
            'Currency': self.Currency,
            'ShareHolderParty': self.ShareHolderParty,
            'ActualDeliveryDate': self.ActualDeliveryDate,
            'ActualDeliveryTime': self.ActualDeliveryTime,
            'DeliveryCityCode': self.DeliveryCityCode,
            'DeliveryCityName': self.DeliveryCityName,
            'DeliveryPostalZone': self.DeliveryPostalZone,
            'DeliveryDepartment': self.DeliveryDepartment,
            'DeliveryDepartmentCode': self.DeliveryDepartmentCode,
            'DeliveryAddress': self.DeliveryAddress,
            'DeliveryCountryCode': self.DeliveryCountryCode,
            'DeliveryCountryName': self.DeliveryCountryName,
            'DeliveryCountryLanguage': self.DeliveryCountryLanguage,
            'DeliveryTerms': self.DeliveryTerms,
            'PaymentMeans': self.PaymentMeans,
            'PrepaidPayments': self.PrepaidPayments,
            'AllowanceCharges': self.AllowanceCharges,
            'PaymentExchangeRate': self.PaymentExchangeRate,
            'PaymentAlternativeExchangeRate': self.PaymentAlternativeExchangeRate,
            'RoundingAmount': self.RoundingAmount,
            'LineExtensionAmount': self.LineExtensionAmount,
            'TaxExclusiveAmount': self.TaxExclusiveAmount,
            'TaxInclusiveAmount': self.TaxInclusiveAmount,
            'AllowanceTotalAmount': self.AllowanceTotalAmount,
            'ChargeTotalAmount': self.ChargeTotalAmount,
            'PrePaidAmount': self.PrePaidAmount,
            'PayableAmount': self.PayableAmount,
            'TaxSubTotals': self.TaxSubTotals,
            'WithHoldingTaxTotals': self.WithHoldingTaxTotals,
            'NotesLines': self.NotesLines,
            'Pdf': self.Pdf
        }

    def import_data(self, data):
        if 'CreateDate' in data:
            self.CreateDate = data['CreateDate']
        if 'UpdateDate' in data:
            self.UpdateDate = data['UpdateDate']
        if 'IssuerNit' in data:
            self.IssuerNit = data['IssuerNit']
        if 'IssuerName' in data:
            self.IssuerName = data['IssuerName']
        if 'DocType' in data:
            self.DocType = data['DocType']
        if 'SeriePrefix' in data:
            self.SeriePrefix = data['SeriePrefix']
        if 'SerieNumber' in data:
            self.SerieNumber = data['SerieNumber']
        if 'InvoiceAuthorization' in data:
            self.InvoiceAuthorization = data['InvoiceAuthorization']
        if 'Contingency' in data:
            self.Contingency = data['Contingency']
        if 'StartDate' in data:
            self.StartDate = data['StartDate']
        if 'EndDate' in data:
            self.EndDate = data['EndDate']
        if 'FromBillingPeriod' in data:
            self.FromBillingPeriod = data['FromBillingPeriod']
        if 'ToBillingPeriod' in data:
            self.ToBillingPeriod = data['ToBillingPeriod']
        if 'DianSoftwareId' in data:
            self.DianSoftwareId = data['DianSoftwareId']
        if 'DianPin' in data:
            self.DianPin = data['DianPin']
        if 'DianTechnicalKey' in data:
            self.DianTechnicalKey = data['DianTechnicalKey']
        if 'Reason' in data:
            self.Reason = data['Reason']
        if 'ReferenceId' in data:
            self.ReferenceId = data['ReferenceId']
        if 'ResponseCode' in data:
            self.ResponseCode = data['ResponseCode']
        if 'NoteDescription' in data:
            self.NoteDescription = data['NoteDescription']
        if 'InvoiceDocumentReferenceId' in data:
            self.InvoiceDocumentReferenceId = data['InvoiceDocumentReferenceId']
        if 'InvoiceDocumentReferenceIssueDate' in data:
            self.InvoiceDocumentReferenceIssueDate = data['InvoiceDocumentReferenceIssueDate']
        if 'InvoiceDocumentReferenceCufe' in data:
            self.InvoiceDocumentReferenceCufe = data['InvoiceDocumentReferenceCufe']
        if 'OperationType' in data:
            self.OperationType = data['OperationType']
        if 'OrderReferenceId' in data:
            self.OrderReferenceId = data['OrderReferenceId']
        if 'OrderReferenceIssueDate' in data:
            self.OrderReferenceIssueDate = data['OrderReferenceIssueDate']
        if 'DespatchDocumentReferenceId' in data:
            self.DespatchDocumentReferenceId = data['DespatchDocumentReferenceId']
        if 'DespatchDocumentIssueDate' in data:
            self.DespatchDocumentIssueDate = data['DespatchDocumentIssueDate']
        if 'ReceiptDocumentReferenceId' in data:
            self.ReceiptDocumentReferenceId = data['ReceiptDocumentReferenceId']
        if 'ReceiptDocumentIssueDate' in data:
            self.ReceiptDocumentIssueDate = data['ReceiptDocumentIssueDate']
        if 'AdditionalDocumentReferenceId' in data:
            self.AdditionalDocumentReferenceId = data['AdditionalDocumentReferenceId']
        if 'AdditionalDocumentIssueDate' in data:
            self.AdditionalDocumentIssueDate = data['AdditionalDocumentIssueDate']
        if 'AdditionalDocumentTypeCode' in data:
            self.AdditionalDocumentTypeCode = data['AdditionalDocumentTypeCode']
        if 'ProfileExecutionId' in data:
            self.ProfileExecutionId = data['ProfileExecutionId']
        if 'Uuid' in data:
            self.Uuid = data['Uuid']
        if 'IssueDate' in data:
            self.IssueDate = data['IssueDate']
        if 'IssueTime' in data:
            self.IssueTime = data['IssueTime']
        if 'DueDate' in data:
            self.DueDate = data['DueDate']
        if 'NoteDocument' in data:
            self.NoteDocument = data['NoteDocument']
        if 'Currency' in data:
            self.Currency = data['Currency']
        if 'ActualDeliveryDate' in data:
            self.ActualDeliveryDate = data['ActualDeliveryDate']
        if 'ActualDeliveryTime' in data:
            self.ActualDeliveryTime = data['ActualDeliveryTime']
        if 'DeliveryCityCode' in data:
            self.DeliveryCityCode = data['DeliveryCityCode']
        if 'DeliveryCityName' in data:
            self.DeliveryCityName = data['DeliveryCityName']
        if 'DeliveryPostalZone' in data:
            self.DeliveryPostalZone = data['DeliveryPostalZone']
        if 'DeliveryDepartment' in data:
            self.DeliveryDepartment = data['DeliveryDepartment']
        if 'DeliveryDepartmentCode' in data:
            self.DeliveryDepartmentCode = data['DeliveryDepartmentCode']
        if 'DeliveryAddress' in data:
            self.DeliveryAddress = data['DeliveryAddress']
        if 'DeliveryCountryCode' in data:
            self.DeliveryCountryCode = data['DeliveryCountryCode']
        if 'DeliveryCountryName' in data:
            self.DeliveryCountryName = data['DeliveryCountryName']
        if 'DeliveryCountryLanguage' in data:
            self.DeliveryCountryLanguage = data['DeliveryCountryLanguage']
        if 'RoundingAmount' in data:
            self.RoundingAmount = data['RoundingAmount']
        if 'LineExtensionAmount' in data:
            self.LineExtensionAmount = data['LineExtensionAmount']
        if 'TaxExclusiveAmount' in data:
            self.TaxInclusiveAmount = data['TaxExclusiveAmount']
        if 'TaxInclusiveAmount' in data:
            self.TaxInclusiveAmount = data['TaxInclusiveAmount']
        if 'AllowanceTotalAmount ' in data:
            self.AllowanceTotalAmount = data['AllowanceTotalAmount']
        if 'ChargeTotalAmount' in data:
            self.ChargeTotalAmount = data['ChargeTotalAmount']
        if 'PrePaidAmount' in data:
            self.PrePaidAmount = data['PrePaidAmount']
        if 'PayableAmount' in data:
            self.PayableAmount = data['PayableAmount']
        return self

    @staticmethod
    def get_data(export: bool = False, pageNumber=0, pageSize=None):
        try:
            if pageSize != None:
                response = db.session.query(NotesModel) \
                    .limit(int(pageSize)) \
                    .offset((int(pageNumber) - 1) * int(pageSize)) \
                    .all()
            else:
                response = db.session.query(NotesModel) \
                    .all()
            if export:
                response = [NotesModel.export_data(x) for x in response]
            return response
        except Exception as e:
            print(e)
            response = ResponseData.internal_server_error(str(e))
            return response

    @staticmethod
    def get_by_id(id: int, export: bool = False):
        try:
            response = db.session.query(NotesModel) \
                .filter(NotesModel.Id == id) \
                .first()
            if export and response:
                response = NotesModel.export_data(response)
            return response
        except Exception as e:
            print(e)
            response = ResponseData.internal_server_error(str(e))
            return response

    @staticmethod
    def export_pdf(data: dict):
        try:
            if data["DocType"] == "NC" or data["DocType"] == "ND":
                xissuer = str.zfill(data["IssuerNit"], 10)
                filename = os.getenv("PATH_DOCS") + xissuer + "invoice-note/" + "/" + data["DianXml"]
                filename = filename.replace(".xml", ".pdf")

                with open(filename, "rb") as f:
                    datapdf = f.read()
                datapdf_encode = b64encode(datapdf).decode("utf-8")

                return {
                    'pdf': datapdf_encode
                }

            if data["DocType"] == "NDS":
                xissuer = str.zfill(data["IssuerNit"], 10)
                filename = os.getenv("PATH_DOCS") + xissuer + "supportdoc-note/" + "/" + data["DianXml"]
                filename = filename.replace(".xml", ".pdf")

                with open(filename, "rb") as f:
                    datapdf = f.read()
                datapdf_encode = b64encode(datapdf).decode("utf-8")

                return {
                    'pdf': datapdf_encode
                }

        except Exception as e:
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def export_xml(data: dict):
        try:
            if data["DocType"] == "NC" or data["DocType"] == "ND":
                xissuer = str.zfill(data["IssuerNit"], 10)
                filename = os.getenv("PATH_DOCS") + xissuer + "invoice-note/" + "/" + data["DianXml"]

                with open(filename, "rb") as f:
                    datapdf = f.read()
                datapdf_encode = b64encode(datapdf).decode("utf-8")

                return {
                    'xml': datapdf_encode
                }

            if data["DocType"] == "NDS":
                xissuer = str.zfill(data["IssuerNit"], 10)
                filename = os.getenv("PATH_DOCS") + xissuer + "supportdoc-note/" + "/" + data["DianXml"]

                with open(filename, "rb") as f:
                    datapdf = f.read()
                datapdf_encode = b64encode(datapdf).decode("utf-8")

                return {
                    'xml': datapdf_encode
                }

        except Exception as e:
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def Create_xml_ad(new_data: dict, sends: dict, NumberContainer: int):

        xmlad = ""
        DocType = new_data["DocType"]
        SeriePrefix = new_data["SeriePrefix"]
        SerieNumber = new_data["SerieNumber"]
        ProfileExecutionId = new_data["ProfileExecutionId"]
        IssuerNit = new_data["IssuerNit"]
        IssueDate = new_data["IssueDate"]
        IssueTime = new_data["IssueTime"]
        Issuer = new_data["IssuerParty"]
        IssuerResponsabilityTypes = Issuer["ResponsabilityTypes"]
        IssuerCommercialRegistration = Issuer["CommercialRegistration"]
        IssuerCheckDigit = Issuer["CheckDigit"]
        CUFE = new_data["CUDE"]
        Customer = new_data["CustomerParty"]
        CustomerDocumentType = Customer["DocumentType"]
        CustomerDocumentNumber = Customer["DocumentNumber"]
        CustomerCommercialRegistration = Customer["CommercialRegistration"]
        CustomerResponsabilityTypes = Customer["ResponsabilityTypes"]

        xissuer = str.zfill(IssuerNit, 10)
        path_issuer = os.getenv('PATH_DOCS') + xissuer + "/"
        if DocType == "NC" or "ND":
            path_issuer += "invoice-note/"
        elif DocType == "NDS":
            path_issuer += "supportdoc-note/"
        dian_xml_file = path_issuer + sends["DianXml"]
        with open(dian_xml_file, "rb") as f:
            data_xml = f.read()
        dian_xml = data_xml.decode("utf-8")
        dian_app_response_bytes = b64decode(sends["DianXmlAppResponse"])
        dian_app_response = dian_app_response_bytes.decode("utf-8")

        xmlad = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' \
                '<AttachedDocument\
                xmlns:ext = "urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2"\
                xmlns:cbc = "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"\
                xmlns:cac = "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"\
                xmlns = "urn:oasis:names:specification:ubl:schema:xsd:AttachedDocument-2">' \
                '<cbc:UBLVersionID>UBL 2.1</cbc:UBLVersionID>' \
                '<cbc:CustomizationID>Documentos adjuntos</cbc:CustomizationID>'

        if DocType == "FV":
            xmlad += "<cbc:ProfileID>Factura Electrónica de Venta</cbc:ProfileID>"
        else:
            if DocType == "NC":
                xmlad += '<cbc:ProfileID>Nota Crédito de Factura Electrónica de Venta</cbc:ProfileID>'
            else:
                if DocType == "ND":
                    xmlad += '<cbc:ProfileID>Nota Débito de Factura Electrónica de Venta</cbc:ProfileID>'

        xmlad += '<cbc:ProfileExecutionID>' + ProfileExecutionId + '</cbc:ProfileExecutionID>' \
                 '<cbc:ID>' + str(NumberContainer) + '</cbc:ID>' \
                 '<cbc:IssueDate>' + IssueDate + '</cbc:IssueDate>' \
                 '<cbc:IssueTime>' + IssueTime + '</cbc:IssueTime>' \
                 '<cbc:DocumentType>Contenedor de Factura Electrónica</cbc:DocumentType>' \
                 '<cbc:ParentDocumentID >' + SeriePrefix + SerieNumber + '</cbc:ParentDocumentID>' \
                 '<cac:SenderParty>' \
                 '<cac:PartyTaxScheme>' \
                 '<cbc:RegistrationName>' + IssuerCommercialRegistration + '</cbc:RegistrationName>' \
                 '<cbc:CompanyID schemeAgencyID = "195" schemeID = "' + IssuerNit + '" ' \
                 'schemeName = "' + IssuerCheckDigit + '" ' \
                 'schemeAgencyName = "CO,DIAN(Dirección de Impuestos y Aduanas Nacionales)">' + IssuerNit + \
                 '</cbc:CompanyID>' \
                 '<cbc:TaxLevelCode listName = "48">' + IssuerResponsabilityTypes + '</cbc:TaxLevelCode>' \
                 '<cac:TaxScheme>' \
                 '<cbc:ID>01</cbc:ID>' \
                 '<cbc:Name>IVA</cbc:Name>' \
                 '</cac:TaxScheme>' \
                 '</cac:PartyTaxScheme>' \
                 '</cac:SenderParty>' \
                 '<cac:ReceiverParty>' \
                 '<cac:PartyTaxScheme>' \
                 '<cbc:RegistrationName>' + CustomerCommercialRegistration + '</cbc:RegistrationName>' \
                 '<cbc:CompanyID schemeAgencyID = "195" schemeID = "' + CustomerDocumentNumber + '" ' \
                 'schemeName = "' + CustomerDocumentType + '" ' \
                 'schemeAgencyName = "CO,DIAN(Dirección de Impuestos y Aduanas Nacionales)">' + \
                 CustomerDocumentNumber + '</cbc:CompanyID>' \
                 '<cbc:TaxLevelCode listName = "48">' + CustomerResponsabilityTypes + '</cbc:TaxLevelCode>' \
                 '<cac:TaxScheme>' \
                 '<cbc:ID>01</cbc:ID>' \
                 '<cbc:Name> IVA </cbc:Name>' \
                 '</cac:TaxScheme>' \
                 '</cac:PartyTaxScheme>' \
                 '</cac:ReceiverParty>' \
                 '<cac:Attachment>' \
                 '<cac:ExternalReference>' \
                 '<cbc:MimeCode>txt/xml</cbc:MimeCode>' \
                 '<cbc:EncodingCode>UTF-8</cbc:EncodingCode>' \
                 '<cbc:Description><![CDATA[' + dian_xml + ']]></cbc:Description>' \
                 '</cac:ExternalReference>' \
                 '</cac:Attachment>' \
                 '<cac:ParentDocumentLineReference>' \
                 '<cbc:LineID>1</cbc:LineID>' \
                 '<cac:DocumentReference>' \
                 '<cbc:ID>' + SeriePrefix + SerieNumber + '</cbc:ID>' \
                 '<cbc:UUID schemeName = "CUFE-SHA384">' + str(CUFE) + '</cbc:UUID>' \
                 '<cbc:IssueDate>' + IssueDate + '</cbc:IssueDate>' \
                 '<cbc:DocumentType>ApplicationResponse</cbc:DocumentType>' \
                 '<cac:Attachment>' \
                 '<cac:ExternalReference>' \
                 '<cbc:MimeCode> txt/xml </cbc:MimeCode>' \
                 '<cbc:EncodingCode>UTF-8</cbc:EncodingCode>' \
                 '<cbc:Description><![CDATA[' + dian_app_response + ']]></cbc:Description>' \
                 '</cac:ExternalReference>' \
                 '</cac:Attachment>' \
                 '<cac:ResultOfVerification>' \
                 '<cbc:ValidatorID>Unidad Especial Dirección de Impuestos y Aduanas Nacionales </cbc:ValidatorID>' \
                 '<cbc:ValidationResultCode>002</cbc:ValidationResultCode>' \
                 '<cbc:ValidationDate>"' + IssueDate + '"</cbc:ValidationDate>' \
                 '<cbc:ValidationTime>"' + IssueTime + '"</cbc:ValidationTime>' \
                 '</cac:ResultOfVerification>' \
                 '</cac:DocumentReference>' \
                 '</cac:ParentDocumentLineReference>' \
                 '</AttachedDocument>'
        return xmlad

    @staticmethod
    def Create_xml_notes(new_data: dict):
        def get_tax_scheme(TributeNameU: str):
            TributeName = TributeNameU.upper()
            if TributeName == "IVA":
                return "01"
            if TributeName == "IC":
                return "02"
            if TributeName == "ICA":
                return "03"
            if TributeName == "INC":
                return "04"
            if TributeName == "ReteIVA".upper():
                return "05"
            if TributeName == "ReteRenta".upper():
                return "06"
            if TributeName == "ReteICA".upper():
                return "07"
            if TributeName == "IC Porcentual".upper():
                return "08"
            if TributeName == "FtoHorcicultura".upper():
                return "20"
            if TributeName == "Timbre".upper():
                return "21"
            if TributeName == "INC Bolsas".upper():
                return "22"
            if TributeName == "INCarbono".upper():
                return "23"
            if TributeName == "INCombustibles".upper():
                return "24"
            if TributeName == "Sobretasa Combustibles".upper():
                return "25"
            if TributeName == "Sord Icom".upper():
                return "26"
            if TributeName == "IC Datos".upper():
                return "30"
            if TributeName == "ZZ":
                return "ZZ"
            if TributeName == "IVA e INC".upper():
                return "ZA"
            return ''

        def get_tax_scheme_name(TributeNameU: str):
            TributeName = TributeNameU.upper()
            if TributeName == "IVA":
                return "IVA"
            if TributeName == "IC":
                return "IC"
            if TributeName == "ICA":
                return "ICA"
            if TributeName == "INC":
                return "INC"
            if TributeName == "ReteIVA".upper():
                return "ReteIVA".upper()
            if TributeName == "ReteRenta".upper():
                return "ReteRenta".upper()
            if TributeName == "ReteICA".upper():
                return "ReteICA".upper()
            if TributeName == "IC Porcentual".upper():
                return "IC Porcentual".upper()
            if TributeName == "FtoHorcicultura".upper():
                return "FtoHorcicultura".upper()
            if TributeName == "Timbre".upper():
                return "Timbre".upper()
            if TributeName == "INC Bolsas".upper():
                return "INC Bolsas".upper()
            if TributeName == "INCarbono".upper():
                return "INCarbono".upper()
            if TributeName == "INCombustibles".upper():
                return "INCombustibles".upper()
            if TributeName == "Sobretasa Combustibles".upper():
                return "Sobretasa Combustibles".upper()
            if TributeName == "Sord Icom".upper():
                return "Sord Icom".upper()
            if TributeName == "IC Datos".upper():
                return "IC Datos".upper()
            if TributeName == "ZZ":
                return "No aplica"
            if TributeName == "IVA e INC".upper():
                return "IVA e INC".upper()
            return ''

        # armar xml
        Plane = ""
        SerieNumber = new_data["SerieNumber"]
        FromBillingPeriod = new_data["FromBillingPeriod"]
        ToBillingPeriod = new_data["ToBillingPeriod"]
        SeriePrefix = new_data["SeriePrefix"]
        StartDate = new_data["StartDate"]
        EndDate = new_data["EndDate"]
        IssuerNit = new_data["IssuerNit"]
        ProfileExecutionId = new_data["ProfileExecutionId"]  # 1 produccion 2 habilitacion
        Currency = new_data["Currency"]
        OperationType = new_data["OperationType"]
        SoftwareId = new_data["DianSoftwareId"]
        Pin = new_data["DianPin"]
        TechnicalKey = new_data["DianTechnicalKey"]
        DocType = new_data["DocType"]
        if "Contingency" in new_data:
            Contingency = new_data["Contingency"]
        else:
            Contingency = "N"
        InvoiceAuthorization = new_data["InvoiceAuthorization"]
        Issuer = new_data["IssuerParty"]
        IssuerResponsabilityTypes = Issuer["ResponsabilityTypes"]
        IssuerTaxScheme = Issuer["TaxScheme"]
        if Issuer["DocumentType"] in ('NIT', '31'):
            IssuerDocumentType = "31"
        else:
            IssuerDocumentType = Issuer["DocumentType"]
        IssuerName = Issuer["Name"]
        IssuerCityCode = Issuer["CityCode"]
        IssuerCityName = Issuer["CityName"]
        IssuerDepartmentCode = Issuer["DepartmentCode"]
        IssuerAddressLine = Issuer["AddressLine"]
        IssuerDepartment = Issuer["Department"]
        IssuerCommercialRegistration = Issuer["CommercialRegistration"]
        IssuerContactName = Issuer["ContactName"]
        IssuerContactTelephone = Issuer["ContactTelephone"]
        IssuerContactElectronicMail = Issuer["ContactElectronicMail"]
        NoteDocument = new_data["NoteDocument"]
        IssuerContactNote = Issuer["ContactNote"]
        IssuerLegalType = Issuer["LegalType"]
        IssuerCheckDigit = Issuer["CheckDigit"]

        Customer = new_data["CustomerParty"]
        CustomerLegalType = Customer["LegalType"]
        if Customer["DocumentType"] == "NIT":
            CustomerDocumentType = "31"
        else:
            CustomerDocumentType = "13"

        CustomerName = Customer["Name"]
        CustomerCheckDigit = Customer["CheckDigit"]
        CustomerDocumentNumber = Customer["DocumentNumber"]
        CustomerCommercialRegistration = Customer["CommercialRegistration"]
        CustomerCityCode = Customer["CityCode"]
        CustomerCityName = Customer["CityName"]
        CustomerDepartmentCode = Customer["DepartmentCode"]
        CustomerAddressLine = Customer["AddressLine"]
        CustomerDepartment = Customer["Department"]
        CustomerResponsabilityTypes = Customer["ResponsabilityTypes"]
        CustomerTaxScheme = Customer["TaxScheme"]
        CustomerContactName = Customer["ContactName"]
        CustomerContactTelephone = Customer["ContactTelephone"]
        CustomerContactElectronicMail = Customer["ContactElectronicMail"]
        DeliveryPostalZone = ""
        DeliveryCityName = ""
        DeliveryDepartmentCode = ""
        DeliveryAddress = ""
        DeliveryDepartment = ""
        if "DeliveryPostalZone" in new_data:
            DeliveryPostalZone = new_data["DeliveryPostalZone"]
        if "DeliveryCityName" in new_data:
            DeliveryCityName = new_data["DeliveryCityName"]
        if "DeliveryDepartmentCode" in new_data:
            DeliveryDepartmentCode = new_data["DeliveryDepartmentCode"]
        if "DeliveryAddress" in new_data:
            DeliveryAddress = new_data["DeliveryAddress"]
        if "DeliveryDepartment" in new_data:
            DeliveryDepartment = new_data["DeliveryDepartment"]
        Delivery = None
        DeliveryPartyDocumentNumber = ""
        DeliveryPartyCheckDigit = ""
        DeliveryPartyDocumentType = ""
        DeliveryPartyCommercialRegistration = ""
        DeliveryPartyCityCode = ""
        DeliveryPartyCityName = ""
        DeliveryPartyDepartmentCode = ""
        DeliveryPartyAddressLine = ""
        DeliveryPartyDepartment = ""
        DeliveryPartyResponsabilityTypes = ""
        DeliveryPartyTaxScheme = None
        DeliveryPartyCorporateRegistrationScheme = ""
        DeliveryPartyContactName = ""
        DeliveryPartyContactTelephone = ""
        DeliveryPartyContactTelefax = ""
        DeliveryPartyContactElectronicMail = ""
        DeliveryPartyContactNote = ""

        if "DeliveryParty" in new_data:
            Delivery = new_data["DeliveryParty"]
        if Delivery != None:
            if "DocumentNumber" in Delivery:
                DeliveryPartyDocumentNumber = Delivery["DocumentNumber"]
            if "CheckDigit" in Delivery:
                DeliveryPartyCheckDigit = Delivery["CheckDigit"]
            if "DocumentType" in Delivery:
                DeliveryPartyDocumentType = Delivery["DocumentType"]
            if "CommercialRegistration" in Delivery:
                DeliveryPartyCommercialRegistration = Delivery["CommercialRegistration"]
            if "CityCode" in Delivery:
                DeliveryPartyCityCode = Delivery["CityCode"]
            if "CityName" in Delivery:
                DeliveryPartyCityName = Delivery["CityName"]
            if "DepartmentCode" in Delivery:
                DeliveryPartyDepartmentCode = Delivery["DepartmentCode"]
            if "AddressLine" in Delivery:
                DeliveryPartyAddressLine = Delivery["AddressLine"]
            if "Department" in Delivery:
                DeliveryPartyDepartment = Delivery["Department"]
            if "ResponsabilityTypes" in Delivery:
                DeliveryPartyResponsabilityTypes = Delivery["ResponsabilityTypes"]
            if "TaxScheme" in Delivery:
                DeliveryPartyTaxScheme = Delivery["TaxScheme"]
            if "CorporateRegistrationScheme" in Delivery:
                DeliveryPartyCorporateRegistrationScheme = Delivery["CorporateRegistrationScheme"]
            if "ContactName" in Delivery:
                DeliveryPartyContactName = Delivery["ContactName"]
            if "ContactTelephone" in Delivery:
                DeliveryPartyContactTelephone = Delivery["ContactTelephone"]
            if "ContactTelefax" in Delivery:
                DeliveryPartyContactTelefax = Delivery["ContactTelefax"]
            if "ContactElectronicMail" in Delivery:
                DeliveryPartyContactElectronicMail = Delivery["ContactElectronicMail"]
            if "ContactNote" in Delivery:
                DeliveryPartyContactNote = Delivery["ContactNote"]

        if "DeliveryTerms" in new_data:
            SpecialTerms = new_data["DeliveryTerms"]

        if "ReasonCredit" in new_data:
            ResponseCode = new_data["ReasonCredit"]
        else:
            ResponseCode = new_data["ReasonDebit"]

        TaxTotalsGlobal = None
        TaxSubTotalGlobal = None
        if "TaxSubTotals" in new_data:
            TaxSubTotalGlobal = new_data["TaxSubTotals"]
        if "TaxTotals" in new_data:
            TaxTotalsGlobal = new_data["TaxTotals"]

        PaymentMethod = "2"  # 1 contado  2 crédito
        HalfPayment = "10"  # "41";
        ExpDate = "2022-08-11"  # "2019/09/30";
        PayRef = "1455"  # "1234";
        Lines = ""
        SendDateRef = ""
        ReferenceId = ""
        ReferenceCufe = ""
        NoteDescription = new_data["NoteDocument"]
        DocumentReferences = new_data["DocumentReferences"]
        for DocumentReference in DocumentReferences:
            ReferenceId = DocumentReference["DocumentReferred"]
            SendDateRef = DocumentReference["IssueDate"]
            ReferenceCufe = DocumentReference["DocumentReferredCUFE"]

        IssueDate = new_data["IssueDate"]
        IssueTime = new_data["IssueTime"]  # Hora de la factura incluyendo GMT
        InvoiceVal = new_data["LineExtensionAmount"]
        TaxExclusiveAmount = new_data["TaxExclusiveAmount"]
        TotalInvoiceBeforeDiscount = new_data["TaxInclusiveAmount"]
        GlobalDiscount = "0.0"
        TotalVal = new_data["PayableAmount"]
        TotalIva = new_data["TotalIva"]
        TotalTaxConsume = new_data["TotalTaxConsume"]
        TotalIca = new_data["TotalIca"]
        Nline = 1
        XLabel = ""
        XAmount = ""
        CommercialPrice = 0
        PaymentExchangeRate = {}
        SourceCurrencyCode = ""
        CalculationRate = ""
        DateExchangeRate = ""

        if "PaymentExchangeRate" in new_data:
            PaymentExchangeRate = new_data["PaymentExchangeRate"]
        if "SourceCurrencyCode" in PaymentExchangeRate:
            SourceCurrencyCode = str(PaymentExchangeRate["SourceCurrencyCode"])
        if "CalculationRate" in PaymentExchangeRate:
            CalculationRate = str(PaymentExchangeRate["CalculationRate"])
        if "Date" in PaymentExchangeRate:
            DateExchangeRate = str(PaymentExchangeRate["Date"])

        CUDE = new_data['CUDE']
        if new_data['CUDE'] == '':
            if DocType == "FV" and Contingency == "N":
                CUDE = (SeriePrefix + SerieNumber + IssueDate + IssueTime + str(InvoiceVal) + '01' + str(
                    TotalIva) + '04' + str(TotalTaxConsume) + '03' + str(TotalIca) + str(
                    TotalVal) + IssuerNit + CustomerDocumentNumber + TechnicalKey + ProfileExecutionId)
                h = hashlib.sha384()
                h.update(CUDE.encode('utf-8'))
                CUDE = h.hexdigest()
            else:
                CUDE = (SeriePrefix + SerieNumber + IssueDate + IssueTime + str(InvoiceVal) + '01' + str(
                    TotalIva) + '04' + str(TotalTaxConsume) + '03' + str(TotalIca) + str(
                    TotalVal) + IssuerNit + CustomerDocumentNumber + Pin + ProfileExecutionId)
                h = hashlib.sha384()
                h.update(CUDE.encode('utf-8'))
                CUDE = h.hexdigest()

            new_data["CUDE"] = CUDE

        SoftwareSecurityCode = (SoftwareId + Pin + SeriePrefix + SerieNumber)
        s = hashlib.sha384()
        s.update(SoftwareSecurityCode.encode('utf-8'))
        SoftwareSecurityCode = s.hexdigest()

        if ProfileExecutionId == "1":
            QRCode = "https://catalogo-vpfe.dian.gov.co/document/searchqr?documentkey=" + str(CUDE)
        else:
            QRCode = "https://catalogo-vpfe-hab.dian.gov.co/document/searchqr?documentkey=" + str(CUDE)

        if DocType == "FV" and Contingency == "N":
            QR = ('NumFac=' + SeriePrefix + SerieNumber + ' FecFac=' + IssueDate + ' HorFac=' + IssueTime +
                  ' NitFac=' + IssuerNit + ' DocAdq=' + CustomerDocumentNumber + ' ValFac=' + str(InvoiceVal) +
                  ' ValIva=' + str(TotalIva) + ' ValOtroIm=' + str(TotalTaxConsume) + str(TotalIca) +
                  ' ValTolDocSop=' + str(TotalVal) + ' CUDE=' + str(CUDE) + " QRCode=" + QRCode)
        else:
            QR = ('NumFac=' + SeriePrefix + SerieNumber + ' FecFac=' + IssueDate + ' HorFac=' + IssueTime +
                  ' NitFac=' + IssuerNit + ' DocAdq=' + CustomerDocumentNumber + ' ValFac=' + str(InvoiceVal) +
                  ' ValIva=' + str(TotalIva) + ' ValOtroIm=' + str(TotalTaxConsume) + str(TotalIca) +
                  ' ValTolDocSop=' + str(TotalVal) + ' CUDE=' + str(CUDE) + " QRCode=" + QRCode)

        # Detalle del documento

        details = new_data["Lines"]
        LineCount = str(len(details))
        det = details[0]

        if DocType == "FV":
            XLabel = "InvoiceLine"
        else:
            if DocType == "NC":
                XLabel = "CreditNoteLine"
            else:
                if DocType == "ND":
                    XLabel = "DebitNoteLine"

        if DocType == "FV":
            XAmount = "Invoiced"
        else:
            if DocType == "NC":
                XAmount = "Credited"
            else:
                if DocType == "ND":
                    XAmount = "Debited"

        BaseQuantity = 0.00

        if DocType == "NC" or DocType == "ND":  # nota de credito o debito
            for det in details:
                XDiscRef = det["Description"]
                brand = det["BrandName"]
                model = det["ModelName"]
                packSize = det["PackSizeNumeric"]
                TaxTotalsLines = det["TaxTotals"]
                PriceAmount = det["PriceAmount"]
                if 'CommercialPrice' in det:
                    CommercialPrice = det["CommercialPrice"]
                if 'BaseQuantity' in det:
                    BaseQuantity = det["BaseQuantity"]

                LineExtensionAmount = det["LineExtensionAmount"]

                if DocType != "DV":
                    Lines += '<cac:' + XLabel + '>' \
                             '<cbc:ID>' + str(Nline) + '</cbc:ID>' \
                             '<cbc:' + XAmount + 'Quantity unitCode="' + det["QuantityUnitOfMeasure"] + '">' + \
                             str(det["Quantity"]) + '</cbc:' + XAmount + 'Quantity>' \
                             '<cbc:LineExtensionAmount currencyID="COP">' + str(LineExtensionAmount) + \
                             '</cbc:LineExtensionAmount>'

                else:
                    Lines += '<cac:' + XLabel + '>' \
                             '<cbc:ID>' + str(Nline) + '</cbc:ID>' \
                             '<cbc:' + XAmount + 'Quantity unitCode="' + det["QuantityUnitOfMeasure"] + '">' + \
                             str(det["Quantity"]) + '</cbc:' + XAmount + 'Quantity>' \
                             '<cbc:LineExtensionAmount currencyID="COP">' + str(LineExtensionAmount) + \
                             '</cbc:LineExtensionAmount>'

                AllowanceChargeLines = None
                if "AllowanceChargeLines" in det:
                    AllowanceChargeLines = det["AllowanceChargeLines"]
                if AllowanceChargeLines != None:
                    for charge in AllowanceChargeLines:
                        Lines += '<cac:AllowanceCharge>' \
                                 '<cbc:ID>' + str(charge["Number"]) + '</cbc:ID>' \
                                 '<cbc:ChargeIndicator>' + str(charge["ChargeIndicator"]) + '</cbc:ChargeIndicator>' \
                                 '<cbc:AllowanceChargeReason>' + (charge["AllowanceChargeReason"]) + \
                                 '</cbc:AllowanceChargeReason>' \
                                 '<cbc:MultiplierFactorNumeric>' + str(charge["MultiplierFactorNumeric"]) + \
                                 '</cbc:MultiplierFactorNumeric>' \
                                 '<cbc:Amount currencyID="COP">' + str(charge["Amount"]) + '</cbc:Amount>' \
                                 '<cbc:BaseAmount currencyID="COP">' + str(charge["BaseAmount"]) + '</cbc:BaseAmount>' \
                                 '</cac:AllowanceCharge>'

                if CommercialPrice != 0 and PriceAmount != 0:
                    Lines += '<cac:PricingReference>' \
                             '<cac:AlternativeConditionPrice>' \
                             '<cbc:PriceAmount currencyID="' + Currency + '">' + str(CommercialPrice) + \
                             '</cbc:PriceAmount>' \
                             '<cbc:PriceTypeCode>03</cbc:PriceTypeCode>' \
                             '<cbc:PriceType>Otro valor</cbc:PriceType>' \
                             '</cac:AlternativeConditionPrice>' \
                             '</cac:PricingReference>'

                TaxSubtotalLines = det["TaxSubTotalLines"]
                TaxFilter = []
                for Tax in TaxTotalsLines:
                    TaxFilter = []
                    for xtax in TaxSubtotalLines:
                        if Tax['TaxCategory'] == xtax["TaxCategory"]:
                            TaxFilter.append(xtax)
                    Lines += '<cac:TaxTotal>' \
                             '<cbc:TaxAmount currencyID="' + Currency + '">' + str(Tax["TaxAmount"]) + \
                             '</cbc:TaxAmount>' \
                             '<cbc:RoundingAmount currencyID="' + Currency + '">0.00</cbc:RoundingAmount>'
                    for xtax in TaxFilter:
                        Lines += '<cac:TaxSubtotal>' \
                                 '<cbc:TaxableAmount currencyID="' + Currency + '">' + str(xtax["TaxableAmount"]) + \
                                 '</cbc:TaxableAmount>' \
                                 '<cbc:TaxAmount currencyID="' + Currency + '">' + str(xtax["TaxAmount"]) + \
                                 '</cbc:TaxAmount>' \
                                 '<cac:TaxCategory>' \
                                 '<cbc:Percent>' + str(xtax["TaxPercentage"]) + '</cbc:Percent>' \
                                 '<cac:TaxScheme>' \
                                 '<cbc:ID>' + get_tax_scheme(xtax["TaxCategory"]) + '</cbc:ID>' \
                                 '<cbc:Name>' + get_tax_scheme_name(xtax["TaxCategory"]) + '</cbc:Name>' \
                                 '</cac:TaxScheme>' \
                                 '</cac:TaxCategory>' \
                                 '</cac:TaxSubtotal>'
                    Lines += '</cac:TaxTotal>'
                WithHoldingTaxTotalLines = None
                if "WithHoldingTaxTotalLines" in det:
                    WithHoldingTaxTotalLines = det["WithHoldingTaxTotalLines"]
                WithHoldingTaxSubTotalLines = None
                if "WithHoldingTaxSubTotalLines" in det:
                    WithHoldingTaxSubTotalLines = det["WithHoldingTaxSubTotalLines"]

                if WithHoldingTaxTotalLines != None:
                    for tax in WithHoldingTaxTotalLines:
                        Lines += '<cac:WithholdingTaxTotal>' \
                                 '<cbc:TaxAmount currencyID = "' + Currency + '">' + str(tax["TaxAmount"]) + \
                                 '</cbc:TaxAmount>'
                        for wtax in WithHoldingTaxSubTotalLines:
                            Lines += '<cac:TaxSubtotal>' \
                                     '<cbc:TaxableAmount currencyID = "' + Currency + '">' + \
                                     str(wtax["TaxableAmount"]) + '</cbc:TaxableAmount>' \
                                     '<cbc:TaxAmount currencyID = "' + Currency + '">' + str(wtax["TaxAmount"]) + \
                                     '</cbc:TaxAmount>' \
                                     '<cac:TaxCategory>' \
                                     '<cbc:Percent>' + str(wtax["TaxPercentage"]) + '</cbc:Percent>' \
                                     '<cac:TaxScheme>' \
                                     '<cbc:ID>' + get_tax_scheme(wtax["TaxCategory"]) + '</cbc:ID>' \
                                     '<cbc:Name>' + get_tax_scheme_name(wtax["TaxCategory"]) + '</cbc:Name>' \
                                     '</cac:TaxScheme>' \
                                     '</cac:TaxCategory>' \
                                     '</cac:TaxSubtotal>'
                        Lines += '</cac:WithholdingTaxTotal>'

                StandardItemIdentifications = det["StandardItemIdentifications"]

                Lines += '<cac:Item>' \
                         '<cbc:Description>' + XDiscRef + '</cbc:Description>' \
                         '<cbc:PackSizeNumeric>' + packSize + '</cbc:PackSizeNumeric>' \
                         '<cbc:BrandName>' + brand + '</cbc:BrandName>' \
                         '<cbc:ModelName>' + model + '</cbc:ModelName>'
                for item in StandardItemIdentifications:
                    Lines += '<cac:StandardItemIdentification>' \
                             '<cbc:ID schemeID="999">' + (item["SchemaId"]) + '</cbc:ID>' \
                             '</cac:StandardItemIdentification>'
                Lines += '</cac:Item>'

                Lines += '<cac:Price>' \
                         '<cbc:PriceAmount currencyID="' + Currency + '">' + str(PriceAmount) + '</cbc:PriceAmount>' \
                         '<cbc:BaseQuantity unitCode= "' + (det["QuantityUnitOfMeasure"]) + '">' + str(BaseQuantity) + \
                         '</cbc:BaseQuantity>' \
                         '</cac:Price>' \
                         '</cac:' + XLabel + '>'
                Nline += 1

        if DocType == "NC":
            Plane = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>' \
                    '<CreditNote xmlns="urn:oasis:names:specification:ubl:schema:xsd:CreditNote-2"\
                    xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"\
                    xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" ' \
                    'xmlns:ds="http://www.w3.org/2000/09/xmldsig#"\
                    xmlns:ext="urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2"\
                    xmlns:sts="http://www.dian.gov.co/contratos/facturaelectronica/v1/Structures"\
                    xmlns:xades="http://uri.etsi.org/01903/v1.3.2#" ' \
                    'xmlns:xades141="http://uri.etsi.org/01903/v1.4.1#"\
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\
                    xsi:schemaLocation="urn:oasis:names:specification:ubl:schema:xsd:CreditNote-2 ' \
                    'http://docs.oasis-open.org/ubl/os-UBL-2.1/xsd/maindoc/UBL-CreditNote-2.1.xsd">'

        else:
            if DocType == "ND":
                Plane = '<DebitNote xmlns = "urn:oasis:names:specification:ubl:schema:xsd:DebitNote-2"\
                        xmlns:cac = "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"\
                        xmlns:cbc = "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"\
                        xmlns:ds = "http://www.w3.org/2000/09/xmldsig#"\
                        xmlns:ext = "urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2"\
                        xmlns:sts = "http://www.dian.gov.co/contratos/facturaelectronica/v1/Structures"\
                        xmlns:xades = "http://uri.etsi.org/01903/v1.3.2#"\
                        xmlns:xades141 = "http://uri.etsi.org/01903/v1.4.1#"\
                        xmlns:xsi = "http://www.w3.org/2001/XMLSchema-instance"\
                        xsi:schemaLocation = "urn:oasis:names:specification:ubl:schema:xsd:DebitNote-2 ' \
                        'http://docs.oasis-open.org/ubl/os-UBL-2.1/xsd/maindoc/UBL-DebitNote-2.1.xsd">'

        Plane += '<ext:UBLExtensions>' \
                 '<ext:UBLExtension>' \
                 '<ext:ExtensionContent>'

        if DocType == "DS":
            Plane += '<sts:DianExtensions xmlns:ds = "http://www.w3.org/2000/09/xmldsig#"\
                        xmlns:xades = "http://uri.etsi.org/01903/v1.3.2#"\
                        xmlns:xsi = "http://www.w3.org/2001/XMLSchema-instance"\
                        xmlns:ext = "urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2"\
                        xmlns:xades141 = "http://uri.etsi.org/01903/v1.4.1#"\
                        xmlns:cac = "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"\
                        xmlns:cbc = "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"\
                        xmlns:sts = "dian:gov:co:facturaelectronica:Structures-2-1" >'

        else:
            if DocType == "FV":
                Plane += '<sts:DianExtensions xmlns:ds = "http://www.w3.org/2000/09/xmldsig#"\
                            xmlns:xades = "http://uri.etsi.org/01903/v1.3.2#"\
                            xmlns:xsi = "http://www.w3.org/2001/XMLSchema-instance"\
                            xmlns:ext = "urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2"\
                            xmlns:xades141 = "http://uri.etsi.org/01903/v1.4.1#"\
                            xmlns:cac = "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"\
                            xmlns:cbc = "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"\
                            xmlns:sts = "dian:gov:co:facturaelectronica:Structures-2-1" >'
            else:
                if DocType == "NC":
                    Plane += '<sts:DianExtensions>'
                else:
                    if DocType == "ND":
                        Plane += '<sts:DianExtensions>'

        if DocType == "DS":
            Plane += '<sts:InvoiceControl>' \
                     '<sts:InvoiceAuthorization>' + InvoiceAuthorization + '</sts:InvoiceAuthorization>' \
                     '<sts:AuthorizationPeriod>' \
                     '<cbc:StartDate>' + StartDate + '</cbc:StartDate>' \
                     '<cbc:EndDate>' + EndDate + '</cbc:EndDate>' \
                     '</sts:AuthorizationPeriod>' \
                     '<sts:AuthorizedInvoices>'
            if Contingency == "N":
                Plane += '<sts:Prefix>' + SeriePrefix + '</sts:Prefix>'
                Plane += '<sts:From>' + FromBillingPeriod + '</sts:From>' \
                         '<sts:To>' + ToBillingPeriod + '</sts:To>' \
                         '</sts:AuthorizedInvoices>' \
                         '</sts:InvoiceControl>'

        if DocType == "FV":
            Plane += '<sts:InvoiceControl>' \
                     '<sts:InvoiceAuthorization>' + InvoiceAuthorization + '</sts:InvoiceAuthorization>' \
                     '<sts:AuthorizationPeriod>' \
                     '<cbc:StartDate>' + StartDate + '</cbc:StartDate>' \
                     '<cbc:EndDate>' + EndDate + '</cbc:EndDate>' \
                     '</sts:AuthorizationPeriod>' \
                     '<sts:AuthorizedInvoices>'
            if Contingency == "N":
                Plane += '<sts:Prefix>' + SeriePrefix + '</sts:Prefix>'
                Plane += '<sts:From>' + FromBillingPeriod + '</sts:From>' \
                         '<sts:To>' + ToBillingPeriod + '</sts:To>' \
                         '</sts:AuthorizedInvoices>' \
                         '</sts:InvoiceControl>'

        if DocType == "NC":
            Plane += '<sts:InvoiceSource>' \
                     '<cbc:IdentificationCode listAgencyID = "6" ' \
                     'listAgencyName = "United Nations Economic Commission for Europe" ' \
                     'listSchemeURI = ' \
                     '"urn:oasis:names:specification:ubl:codelist:gc:CountryIdentificationCode-2.1">CO' \
                     '</cbc:IdentificationCode>' \
                     '</sts:InvoiceSource>'
        else:
            if DocType == "ND":
                Plane += '<sts:InvoiceSource>' \
                         '<cbc:IdentificationCode listAgencyID = "6" ' \
                         'listAgencyName = "United Nations Economic Commission for Europe" ' \
                         'listSchemeURI = ' \
                         '"urn:oasis:names:specification:ubl:codelist:gc:CountryIdentificationCode-2.1">CO' \
                         '</cbc:IdentificationCode>' \
                         '</sts:InvoiceSource>'

        Plane += '<sts:SoftwareProvider>' \
                 '<sts:ProviderID schemeAgencyID="195" ' \
                 'schemeAgencyName="CO, DIAN(Dirección de Impuestos y Aduanas Nacionales)" schemeID="' + \
                 IssuerCheckDigit + '" schemeName="31">' + IssuerNit + '</sts:ProviderID>' \
                 '<sts:SoftwareID schemeAgencyID="195" ' \
                 'schemeAgencyName="CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)">' + SoftwareId + \
                 '</sts:SoftwareID>' \
                 '</sts:SoftwareProvider>' \
                 '<sts:SoftwareSecurityCode schemeAgencyID="195" ' \
                 'schemeAgencyName="CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)">' + \
                 str(SoftwareSecurityCode) + '</sts:SoftwareSecurityCode>' \
                 '<sts:AuthorizationProvider>' \
                 '<sts:AuthorizationProviderID schemeAgencyID="195" ' \
                 'schemeAgencyName="CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)" schemeID="4" ' \
                 'schemeName="31">800197268</sts:AuthorizationProviderID>' \
                 '</sts:AuthorizationProvider>' \
                 '<sts:QRCode>' + QR + '</sts:QRCode>' \
                 '</sts:DianExtensions>' \
                 '</ext:ExtensionContent>' \
                 '</ext:UBLExtension>' \
                 '<ext:UBLExtension>' \
                 '<ext:ExtensionContent>' \
                 '</ext:ExtensionContent>' \
                 '</ext:UBLExtension>' \
                 '</ext:UBLExtensions>' \
                 '<cbc:UBLVersionID>UBL 2.1</cbc:UBLVersionID>'

        Plane += '<cbc:CustomizationID>' + OperationType + '</cbc:CustomizationID>'

        if DocType == "NC":
            Plane += '<cbc:ProfileID>DIAN 2.1: Nota Crédito de Factura Electrónica de Venta</cbc:ProfileID>'
            Plane += '<cbc:ProfileExecutionID>' + ProfileExecutionId + '</cbc:ProfileExecutionID>' \
                     '<cbc:ID>' + SeriePrefix + SerieNumber + '</cbc:ID>'
        else:
            if DocType == "ND":
                Plane += '<cbc:ProfileID>DIAN 2.1: Nota Débito de Factura Electrónica de Venta</cbc:ProfileID>'
                Plane += '<cbc:ProfileExecutionID>' + ProfileExecutionId + '</cbc:ProfileExecutionID>' \
                         '<cbc:ID>' + SeriePrefix + SerieNumber + '</cbc:ID>'

        if DocType == "NC":
            Plane += '<cbc:UUID schemeID= "' + ProfileExecutionId + '"  schemeName="CUDE-SHA384">' + str(CUDE) + \
                     '</cbc:UUID>'
        else:
            if DocType == "ND":
                Plane += '<cbc:UUID schemeID= "' + ProfileExecutionId + '" schemeName="CUDE-SHA384">' + str(CUDE) + \
                         '</cbc:UUID>'

        Plane += '<cbc:IssueDate>' + IssueDate + '</cbc:IssueDate>' \
                 '<cbc:IssueTime>' + IssueTime + '</cbc:IssueTime>'

        if DocType == "NC":
            Plane += '<cbc:CreditNoteTypeCode>91</cbc:CreditNoteTypeCode>'
            Plane += '<cbc:Note>' + NoteDocument + '</cbc:Note>' \
                     '<cbc:DocumentCurrencyCode listAgencyID="6" ' \
                     'listAgencyName="United Nations Economic Commission for Europe" listID="ISO 4217 Alpha">' + \
                     Currency + '</cbc:DocumentCurrencyCode>'
        else:
            if DocType == "ND":
                Plane += '<cbc:DebitNoteTypeCode>92</cbc:DebitNoteTypeCode>'
                Plane += '<cbc:Note>' + NoteDocument + '</cbc:Note>' \
                         '<cbc:DocumentCurrencyCode listAgencyID="6" ' \
                         'listAgencyName="United Nations Economic Commission for Europe" listID="ISO 4217 Alpha">' + \
                         Currency + '</cbc:DocumentCurrencyCode>'

        if DocType == "FV" or (DocType == "ND" and ProfileExecutionId == "2"):
            Plane += '<cbc:LineCountNumeric>' + LineCount + '</cbc:LineCountNumeric>'
        else:
            Plane += '<cbc:LineCountNumeric>' + str(Nline - 1) + '</cbc:LineCountNumeric>'
        if DocType == "FV":
            Plane += '<cac:InvoicePeriod>' \
                     '<cbc:StartDate>' + StartDate + '</cbc:StartDate>' \
                                                     '<cbc:EndDate>' + EndDate + '</cbc:EndDate>' \
                                                                                 '</cac:InvoicePeriod>'

        # documentos referencias de nd y nc
        if DocType != "DS":
            Plane += '<cac:DiscrepancyResponse>' \
                     '<cbc:ReferenceID>' + ReferenceId + '</cbc:ReferenceID>' \
                     '<cbc:ResponseCode>' + ResponseCode + '</cbc:ResponseCode>'

            Plane += '<cbc:Description>' + NoteDescription + '</cbc:Description>'
            Plane += '</cac:DiscrepancyResponse>'

            Plane += '<cac:BillingReference>' \
                     '<cac:InvoiceDocumentReference>' \
                     '<cbc:ID>' + ReferenceId + '</cbc:ID>' \
                     '<cbc:UUID schemeName="CUDS-SHA384">' + ReferenceCufe + '</cbc:UUID>' \
                     '<cbc:IssueDate>' + SendDateRef + '</cbc:IssueDate>' \
                     '</cac:InvoiceDocumentReference>' \
                     '</cac:BillingReference>'

        if "CreditNoteId" in new_data:
            if new_data["CreditNoteId"] != "":
                Plane += '<cac:BillingReference>' \
                         '<cac:CreditNoteDocumentReference>' \
                         '<cbc:ID>' + new_data["CreditNoteId"] + '</cbc:ID>' \
                         '<cbc:UUID schemeName="CUFE-SHA384">' + new_data["CreditNoteCude"] + '</cbc:UUID>' \
                         '<cbc:IssueDate>' + new_data["CreditNoteIssueDate"] + '</cbc:IssueDate>' \
                         '</cac:CreditNoteDocumentReference>' \
                         '</cac:BillingReference>'

        if "DebitNoteId" in new_data:
            if new_data["DebitNoteId"] != "":
                Plane += '<cac:BillingReference>' \
                         '<cac:DebitNoteDocumentReference>' \
                         '<cbc:ID>' + new_data["DebitNoteId"] + '</cbc:ID>' \
                         '<cbc:UUID schemeName="CUFE-SHA384">' + new_data["DebitNoteCude"] + '</cbc:UUID>' \
                         '<cbc:IssueDate>' + new_data["DebitNoteIssueDate"] + '</cbc:IssueDate>' \
                         '</cac:DebitNoteDocumentReference>' \
                         '</cac:BillingReference>'

        if "OrderReferenceId" in new_data:
            if new_data["OrderReferenceId"] != "":
                Plane += '<cac:OrderReference>' \
                         '<cbc:ID>' + new_data["OrderReferenceId"] + '</cbc:ID>' \
                         '<cbc:IssueDate>' + new_data["OrderReferenceIssueDate"] + '</cbc:IssueDate>' \
                         '</cac:OrderReference>'

        if "DespatchDocumentReferenceId" in new_data:
            if new_data["DespatchDocumentReferenceId"] != "":
                Plane += '<cac:DespatchDocumentReference>' \
                         '<cbc:ID>' + new_data["DespatchDocumentReferenceId"] + '</cbc:ID>' \
                         '<cbc:IssueDate>' + new_data["DespatchDocumentIssueDate"] + '</cbc:IssueDate>' \
                         '</cac:DespatchDocumentReference>'

        if "ReceiptDocumentReferenceId" in new_data:
            if new_data["ReceiptDocumentReferenceId"] != "":
                Plane += '<cac:ReceiptDocumentReference>' \
                         '<cbc:ID>' + new_data["ReceiptDocumentReferenceId"] + '</cbc:ID>' \
                         '<cbc:IssueDate>' + new_data["ReceiptDocumentIssueDate"] + '</cbc:IssueDate>' \
                         '</cac:ReceiptDocumentReference>'

        if "AdditionalDocumentReferenceId" in new_data:
            if new_data["AdditionalDocumentReferenceId"] != "":
                Plane += '<cac:AdditionalDocumentReference>' \
                         '<cbc:ID>' + new_data["AdditionalDocumentReferenceId"] + '</cbc:ID>' \
                         '<cbc:IssueDate>' + new_data["AdditionalDocumentIssueDate"] + '</cbc:IssueDate>' \
                         '<cbc:DocumentTypeCode>' + new_data["AdditionalDocumentTypeCode"] + \
                         '</cbc:DocumentTypeCode>' \
                         '</cac:AdditionalDocumentReference>'

        Plane += '<cac:AccountingSupplierParty>' \
                 '<cbc:AdditionalAccountID>' + IssuerLegalType + '</cbc:AdditionalAccountID>' \
                 '<cac:Party>' \
                 '<cac:PartyName>' \
                 '<cbc:Name>' + IssuerName + '</cbc:Name>' \
                 '</cac:PartyName>' \
                 '<cac:PhysicalLocation>' \
                 '<cac:Address>' \
                 '<cbc:ID>' + IssuerCityCode + '</cbc:ID>' \
                 '<cbc:CityName>' + IssuerCityName + '</cbc:CityName>' \
                 '<cbc:CountrySubentity>' + IssuerDepartment + '</cbc:CountrySubentity>' \
                 '<cbc:CountrySubentityCode>' + IssuerDepartmentCode + '</cbc:CountrySubentityCode>' \
                 '<cac:AddressLine>' \
                 '<cbc:Line>' + IssuerAddressLine + '</cbc:Line>' \
                 '</cac:AddressLine>' \
                 '<cac:Country>' \
                 '<cbc:IdentificationCode>CO</cbc:IdentificationCode>' \
                 '<cbc:Name languageID="es">Colombia</cbc:Name>' \
                 '</cac:Country>' \
                 '</cac:Address>' \
                 '</cac:PhysicalLocation>' \
                 '<cac:PartyTaxScheme>' \
                 '<cbc:RegistrationName>' + IssuerName + '</cbc:RegistrationName>' \
                 '<cbc:CompanyID schemeAgencyID="195" ' \
                 'schemeAgencyName="CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)" schemeID= "' + \
                 IssuerCheckDigit + '"  schemeName= "' + IssuerDocumentType + '">' + IssuerNit + '</cbc:CompanyID>' \
                 '<cbc:TaxLevelCode listName="05">' + IssuerResponsabilityTypes + '</cbc:TaxLevelCode>' \
                 '<cac:RegistrationAddress>' \
                 '<cbc:ID>' + IssuerCityCode + '</cbc:ID>' \
                 '<cbc:CityName>' + IssuerCityName + '</cbc:CityName>' \
                 '<cbc:CountrySubentity>' + IssuerDepartment + '</cbc:CountrySubentity>' \
                 '<cbc:CountrySubentityCode>' + IssuerDepartmentCode + '</cbc:CountrySubentityCode>' \
                 '<cac:AddressLine>' \
                 '<cbc:Line>' + IssuerAddressLine + '</cbc:Line>' \
                 '</cac:AddressLine>' \
                 '<cac:Country>' \
                 '<cbc:IdentificationCode>CO</cbc:IdentificationCode>' \
                 '<cbc:Name languageID="es">Colombia</cbc:Name>' \
                 '</cac:Country>' \
                 '</cac:RegistrationAddress>' \
                 '<cac:TaxScheme>'

        for Tax in IssuerTaxScheme:
            Plane += '<cbc:ID>' + get_tax_scheme(Tax['TaxCategory']) + '</cbc:ID>' \
                     '<cbc:Name>' + get_tax_scheme_name(Tax["TaxCategory"]) + '</cbc:Name>'
        Plane += '</cac:TaxScheme>' \
                 '</cac:PartyTaxScheme>' \
                 '<cac:PartyLegalEntity>' \
                 '<cbc:RegistrationName>' + IssuerName + '</cbc:RegistrationName>' \
                 '<cbc:CompanyID schemeAgencyID="195" ' \
                 'schemeAgencyName="CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)" ' \
                 'schemeID= "' + IssuerCheckDigit + '" schemeName= "' + IssuerDocumentType + '">' + IssuerNit + \
                 '</cbc:CompanyID>' \
                 '<cac:CorporateRegistrationScheme>' \
                 '<cbc:ID>' + SeriePrefix + '</cbc:ID>'

        if IssuerCommercialRegistration != "":
            Plane += '<cbc:Name>' + IssuerCommercialRegistration + '</cbc:Name>'
        Plane += '</cac:CorporateRegistrationScheme>' \
                 '</cac:PartyLegalEntity>' \
                 '<cac:Contact>' \
                 '<cbc:Name>' + IssuerContactName + '</cbc:Name>' \
                 '<cbc:Telephone>' + IssuerContactTelephone + '</cbc:Telephone>' \
                 '<cbc:ElectronicMail>' + IssuerContactElectronicMail + '</cbc:ElectronicMail>' \
                 '<cbc:Note>' + IssuerContactNote + '</cbc:Note>' \
                 '</cac:Contact>' \
                 '</cac:Party>' \
                 '</cac:AccountingSupplierParty>' \
                 '<cac:AccountingCustomerParty>'
        Plane += '<cbc:AdditionalAccountID>' + CustomerLegalType + '</cbc:AdditionalAccountID>'
        Plane += '<cac:Party>'

        if CustomerLegalType == "2":
            Plane += '<cac:PartyIdentification>' \
                     '<cbc:ID '
            if CustomerDocumentType == "31":
                Plane += 'schemeID="' + CustomerCheckDigit + '" '
            Plane += 'schemeName="' + CustomerDocumentType + '">' + CustomerDocumentNumber + '</cbc:ID>'
            Plane += '</cac:PartyIdentification>'
        Plane += '<cac:PartyName>' \
                 '<cbc:Name>' + CustomerName + '</cbc:Name>' \
                 '</cac:PartyName>' \
                 '<cac:PhysicalLocation>' \
                 '<cac:Address>' \
                 '<cbc:ID>' + CustomerCityCode + '</cbc:ID>' \
                 '<cbc:CityName>' + CustomerCityName + '</cbc:CityName>' \
                 '<cbc:CountrySubentity>' + CustomerDepartment + '</cbc:CountrySubentity>' \
                 '<cbc:CountrySubentityCode>' + CustomerDepartmentCode + '</cbc:CountrySubentityCode>' \
                 '<cac:AddressLine>' \
                 '<cbc:Line>' + CustomerAddressLine + '</cbc:Line>' \
                 '</cac:AddressLine>' \
                 '<cac:Country>' \
                 '<cbc:IdentificationCode>CO</cbc:IdentificationCode>' \
                 '<cbc:Name languageID="es">Colombia</cbc:Name>' \
                 '</cac:Country>' \
                 '</cac:Address>' \
                 '</cac:PhysicalLocation>' \
                 '<cac:PartyTaxScheme>' \
                 '<cbc:RegistrationName>' + CustomerCommercialRegistration + '</cbc:RegistrationName>' \
                 '<cbc:CompanyID schemeAgencyID="195" ' \
                 'schemeAgencyName= "CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)" ' \
                 'schemeID= "' + CustomerCheckDigit + '" schemeName= "' + CustomerDocumentType + '">' + \
                 CustomerDocumentNumber + '</cbc:CompanyID>' \
                 '<cbc:TaxLevelCode listName="04">' + CustomerResponsabilityTypes + '</cbc:TaxLevelCode>' \
                 '<cac:RegistrationAddress>' \
                 '<cbc:ID>' + CustomerCityCode + '</cbc:ID>' \
                 '<cbc:CityName>' + CustomerCityName + '</cbc:CityName>' \
                 '<cbc:CountrySubentity>' + CustomerDepartment + '</cbc:CountrySubentity>' \
                 '<cbc:CountrySubentityCode>' + CustomerDepartmentCode + '</cbc:CountrySubentityCode>' \
                 '<cac:AddressLine>' \
                 '<cbc:Line>' + CustomerAddressLine + '</cbc:Line>' \
                 '</cac:AddressLine>' \
                 '<cac:Country>' \
                 '<cbc:IdentificationCode>CO</cbc:IdentificationCode>' \
                 '<cbc:Name languageID="es">Colombia</cbc:Name>' \
                 '</cac:Country>' \
                 '</cac:RegistrationAddress>' \
                 '<cac:TaxScheme>'

        for Tax in CustomerTaxScheme:
            Plane += '<cbc:ID>' + get_tax_scheme(Tax['TaxCategory']) + '</cbc:ID>' \
                                                                       '<cbc:Name>' + get_tax_scheme_name(
                Tax["TaxCategory"]) + '</cbc:Name>'

        Plane += '</cac:TaxScheme>' \
                 '</cac:PartyTaxScheme>' \
                 '<cac:PartyLegalEntity>' \
                 '<cbc:RegistrationName>' + CustomerCommercialRegistration + '</cbc:RegistrationName>' \
                 '<cbc:CompanyID schemeAgencyID="195" ' \
                 'schemeAgencyName="CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)" schemeID= "' + \
                 CustomerCheckDigit + '" schemeName= "' + CustomerDocumentType + '">' + CustomerDocumentNumber + \
                 '</cbc:CompanyID>'

        if CustomerDocumentType != "":
            Plane += '<cac:CorporateRegistrationScheme><cbc:Name>' + CustomerDocumentType + '</cbc:Name>'
            Plane += '</cac:CorporateRegistrationScheme>'
        Plane += '</cac:PartyLegalEntity>' \
                 '<cac:Contact>' \
                 '<cbc:Name>' + CustomerName + '</cbc:Name>' \
                 '<cbc:Telephone>' + CustomerContactTelephone + '</cbc:Telephone>' \
                 '<cbc:ElectronicMail>' + CustomerContactElectronicMail + '</cbc:ElectronicMail>' \
                 '</cac:Contact>' \
                 '</cac:Party>' \
                 '</cac:AccountingCustomerParty>' \
                 '<cac:TaxRepresentativeParty>' \
                 '<cac:PartyIdentification>' \
                 '<cbc:ID schemeAgencyID="195" ' \
                 'schemeAgencyName="CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)" schemeID="4" ' \
                 'schemeName="31">989123123</cbc:ID>' \
                 '</cac:PartyIdentification>' \
                 '</cac:TaxRepresentativeParty>'

        if DeliveryAddress != "":
            Plane += '<cac:Delivery>' \
                     '<cac:DeliveryAddress>' \
                     '<cbc:ID>' + DeliveryPostalZone + '</cbc:ID>' \
                     '<cbc:CityName>' + DeliveryCityName + '</cbc:CityName>' \
                     '<cbc:CountrySubentity>' + DeliveryDepartment + '</cbc:CountrySubentity>' \
                     '<cbc:CountrySubentityCode>' + DeliveryDepartmentCode + '</cbc:CountrySubentityCode>' \
                     '<cac:AddressLine>' \
                     '<cbc:Line>' + DeliveryDepartmentCode + '</cbc:Line>' \
                     '</cac:AddressLine>' \
                     '<cac:Country>' \
                     '<cbc:IdentificationCode>CO</cbc:IdentificationCode>' \
                     '<cbc:Name languageID="es">Colombia</cbc:Name>' \
                     '</cac:Country>' \
                     '</cac:DeliveryAddress>' \
                     '<cac:DeliveryParty>' \
                     '<cac:PartyName>' \
                     '<cbc:Name>' + DeliveryPartyCommercialRegistration + '</cbc:Name>' \
                     '</cac:PartyName>' \
                     '<cac:PhysicalLocation>' \
                     '<cac:Address>' \
                     '<cbc:ID>' + DeliveryPartyCityCode + '</cbc:ID>' \
                     '<cbc:CityName>' + DeliveryPartyCityName + '</cbc:CityName>' \
                     '<cbc:CountrySubentity>' + DeliveryPartyDepartment + '</cbc:CountrySubentity>' \
                     '<cbc:CountrySubentityCode>' + DeliveryPartyDepartmentCode + '</cbc:CountrySubentityCode>' \
                     '<cac:AddressLine>' \
                     '<cbc:Line>' + DeliveryPartyAddressLine + '</cbc:Line>' \
                     '</cac:AddressLine>' \
                     '<cac:Country>' \
                     '<cbc:IdentificationCode>CO</cbc:IdentificationCode>' \
                     '<cbc:Name languageID="es">Colombia</cbc:Name>' \
                     '</cac:Country>' \
                     '</cac:Address>' \
                     '</cac:PhysicalLocation>' \
                     '<cac:PartyTaxScheme>' \
                     '<cbc:RegistrationName>' + DeliveryPartyCommercialRegistration + '</cbc:RegistrationName>' \
                     '<cbc:CompanyID schemeAgencyID="195" ' \
                     'schemeAgencyName="CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)" schemeID="1" ' \
                     'schemeName="31">981223983</cbc:CompanyID>' \
                     '<cbc:TaxLevelCode listName="04">' + DeliveryPartyResponsabilityTypes + '</cbc:TaxLevelCode>' \
                     '<cac:TaxScheme>'

        if DeliveryPartyTaxScheme != None:
            for Tax in DeliveryPartyTaxScheme:
                Plane += '<cbc:ID>' + get_tax_scheme(Tax['TaxCategory']) + '</cbc:ID>' \
                         '<cbc:Name>' + get_tax_scheme_name(Tax["TaxCategory"]) + '</cbc:Name>' \
                         '</cac:TaxScheme>' \
                         '</cac:PartyTaxScheme>' \
                         '<cac:PartyLegalEntity>' \
                         '<cbc:RegistrationName>' + DeliveryPartyCommercialRegistration + "Transport Company"\
                         '</cbc:RegistrationName>' \
                         '<cbc:CompanyID schemeAgencyID="195" ' \
                         'schemeAgencyName="CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)" ' \
                         'schemeID="1" schemeName="31">981223983</cbc:CompanyID>' \
                         '<cac:CorporateRegistrationScheme>' \
                         '<cbc:Name>' + DeliveryPartyCorporateRegistrationScheme + '</cbc:Name>' \
                         '</cac:CorporateRegistrationScheme>' \
                         '</cac:PartyLegalEntity>' \
                         '<cac:Contact>' \
                         '<cbc:Name>' + DeliveryPartyContactName + '</cbc:Name>' \
                         '<cbc:Telephone>' + DeliveryPartyContactTelephone + '</cbc:Telephone>' \
                         '<cbc:Telefax>' + DeliveryPartyContactTelefax + '</cbc:Telefax>' \
                         '<cbc:ElectronicMail>' + DeliveryPartyContactElectronicMail + '</cbc:ElectronicMail>' \
                         '<cbc:Note>' + DeliveryPartyContactNote + '</cbc:Note>' \
                         '</cac:Contact>' \
                         '</cac:DeliveryParty>' \
                         '</cac:Delivery>' \

        Plane += '<cac:PaymentMeans>' \
                 '<cbc:ID>' + PaymentMethod + '</cbc:ID>' \
                 '<cbc:PaymentMeansCode>' + HalfPayment + '</cbc:PaymentMeansCode>' \
                 '<cbc:PaymentDueDate>' + ExpDate + '</cbc:PaymentDueDate>'
        if PayRef != "":
            Plane += '<cbc:PaymentID>' + PayRef + '</cbc:PaymentID>'
        Plane += '</cac:PaymentMeans>'

        if SourceCurrencyCode != "":
            Plane += '<cac:PaymentExchangeRate>'\
                      '<cbc:SourceCurrencyCode>' + SourceCurrencyCode + '</cbc:SourceCurrencyCode>'\
                      '<cbc:SourceCurrencyBaseRate>1.00</cbc:SourceCurrencyBaseRate>'\
                      '<cbc:TargetCurrencyCode>COP</cbc:TargetCurrencyCode>'\
                      '<cbc:TargetCurrencyBaseRate>1.00</cbc:TargetCurrencyBaseRate>'\
                      '<cbc:CalculationRate>' + CalculationRate + '</cbc:CalculationRate>'\
                      '<cbc:Date>' + DateExchangeRate + '</cbc:Date>'\
                      '</cac:PaymentExchangeRate>'

        if TaxTotalsGlobal != None:
            for Tax in TaxTotalsGlobal:
                TaxFilter = []
                for xtax in TaxSubTotalGlobal:
                    if Tax['TaxCategory'] == xtax["TaxCategory"]:
                        TaxFilter.append(xtax)
                Plane += '<cac:TaxTotal>' \
                         '<cbc:TaxAmount currencyID="' + Currency + '">' + str(Tax["TaxAmount"]) + '</cbc:TaxAmount>' \
                         '<cbc:RoundingAmount currencyID="' + Currency + '">0.00</cbc:RoundingAmount>'
                for xtax in TaxFilter:
                    Plane += '<cac:TaxSubtotal>' \
                             '<cbc:TaxableAmount currencyID="' + Currency + '">' + str(xtax["TaxableAmount"]) + \
                             '</cbc:TaxableAmount>' \
                             '<cbc:TaxAmount currencyID="' + Currency + '">' + str(xtax["TaxAmount"]) + \
                             '</cbc:TaxAmount>' \
                             '<cac:TaxCategory>' \
                             '<cbc:Percent>' + str(xtax["TaxPercentage"]) + '</cbc:Percent>' \
                             '<cac:TaxScheme>' \
                             '<cbc:ID>' + get_tax_scheme(xtax["TaxCategory"]) + '</cbc:ID>' \
                             '<cbc:Name>' + get_tax_scheme_name(xtax["TaxCategory"]) + '</cbc:Name>' \
                             '</cac:TaxScheme>' \
                             '</cac:TaxCategory>' \
                             '</cac:TaxSubtotal>'
            Plane += '</cac:TaxTotal>'

        if DocType != "ND":
            Plane += '<cac:LegalMonetaryTotal>' \
                     '<cbc:LineExtensionAmount currencyID="' + Currency + '">' + str(TaxExclusiveAmount) + \
                     '</cbc:LineExtensionAmount>' \
                     '<cbc:TaxExclusiveAmount currencyID="' + Currency + '">' + str(InvoiceVal) + \
                     '</cbc:TaxExclusiveAmount>' \
                     '<cbc:TaxInclusiveAmount currencyID="' + Currency + '">' + str(TotalInvoiceBeforeDiscount) + \
                     '</cbc:TaxInclusiveAmount>' \
                     '<cbc:AllowanceTotalAmount currencyID="' + Currency + '">' + str(GlobalDiscount) + \
                     '</cbc:AllowanceTotalAmount>' \
                     '<cbc:PayableAmount currencyID="' + Currency + '">' + str(TotalVal) + '</cbc:PayableAmount>' \
                     '</cac:LegalMonetaryTotal>'
        else:
            Plane += '<cac:RequestedMonetaryTotal>' \
                     '<cbc:LineExtensionAmount currencyID="COP">' + str(TaxExclusiveAmount) + \
                     '</cbc:LineExtensionAmount>' \
                     '<cbc:TaxExclusiveAmount currencyID="' + Currency + '">' + str(InvoiceVal) + \
                     '</cbc:TaxExclusiveAmount>' \
                     '<cbc:TaxInclusiveAmount currencyID="' + Currency + '">' + str(TotalInvoiceBeforeDiscount) + \
                     '</cbc:TaxInclusiveAmount>' \
                     '<cbc:AllowanceTotalAmount currencyID="' + Currency + '">' + str(GlobalDiscount) + \
                     '</cbc:AllowanceTotalAmount>' \
                     '<cbc:PayableAmount currencyID="' + Currency + '">' + str(TotalVal) + '</cbc:PayableAmount>' \
                     '</cac:RequestedMonetaryTotal>'

        Plane += Lines

        if DocType == "NC":
            Plane += '</CreditNote>'
        else:
            if DocType == "ND":
                Plane += '</DebitNote>'

        return Plane
        # enviar dian
        # si exito

    @validates()
    def validate_name_permit(self, key, name):
        try:
            FieldValidations.is_none(key, name)
            FieldValidations.is_empty(key, name)
            return name
        except Exception as e:
            print(e)
            raise InternalServerError(e)
