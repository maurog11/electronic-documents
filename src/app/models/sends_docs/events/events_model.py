# -*- coding: utf-8 -*-
#########################################################
import hashlib
import os
from sqlalchemy import Index
from app.models.base_model import BaseModel
from app import db
from app.exception import InternalServerError, NotFound
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import validates
from app.utils import FieldValidations, ResponseData
from base64 import b64encode, b64decode


class EventsModel(BaseModel):
    __tablename__ = 'events'

    IssuerNit = db.Column(db.String(20), nullable=False, comment='Nit de la empresa o emisor ')
    IssuerName = db.Column(db.String(200), nullable=False, comment='Nombre o razon social del emisor ')
    DocType = db.Column(db.String(5), nullable=False,
                        comment='Tipo de Doc AD=Contenedor FV=factura NC=Nota Cr ND=Nota DB DS=Documento Soporte NOM=Nomina NOMA=Nomina Ajuste ')
    Prefix = db.Column(db.String(4), nullable=False, comment='Prefijo del documento de la empresa ')
    SerieNumber = db.Column(db.String(15), nullable=True, comment='Numero de serie de la factura')
    YearSend = db.Column(db.String(4), nullable=False, comment='Año Envio ')
    NumberSend = db.Column(db.Integer, nullable=False, comment='numero envio..reinicia cada año ')
    DianResolution = db.Column(db.String(50), nullable=True, comment='Resolucion Dian ')
    IdSoftware = db.Column(db.String(100), nullable=True, comment='id software dian ')
    ClientNit = db.Column(db.String(20), nullable=True, comment='Nit del cliente ')
    ClientName = db.Column(db.String(100), nullable=True, comment='Nombre del cliente ')
    ClientEmail = db.Column(db.String(200), nullable=True, comment='Email del cliente ')
    DateSend = db.Column(db.DateTime(10), nullable=True, comment='Fecha Envio ')
    HourSend = db.Column(db.String(20), nullable=True, comment='Hora Envio ')
    DianResponse = db.Column(LONGTEXT, nullable=True, comment='Respuesta DIAN ')
    DianResponseErrors = db.Column(LONGTEXT, nullable=True, comment='Errores DIAN ')
    DianXml = db.Column(LONGTEXT, nullable=True, comment='Xml enviado a DIAN ')
    DianXmlAppResponse = db.Column(LONGTEXT, nullable=True, comment='Xml Respuesta DIAN ')
    Cufe = db.Column(db.String(150), nullable=True, comment='CUFE, CUDE o CUNE documento ')
    CUDE = db.Column(db.String(150), nullable=True, comment='CUDE del evento')
    TrackIdDian = db.Column(db.String(200), nullable=True, comment='Cadena que reporta la DIAN ')
    Code = db.Column(db.String(10), nullable=True, comment='Codigo Evento')
    JsonReceived = db.Column(LONGTEXT, nullable=True, comment='JSON serializado')
    MessageEmail = db.Column(LONGTEXT, nullable=True, comment='Mensaje del estado email')
    Status = db.Column(db.String(1), nullable=True, comment='0 Rechazado 1=Enviado ')
    DocumentNumberPerson = db.Column(db.String(20), nullable=True, comment='Numero de documento de la persona')
    CheckDigitPerson = db.Column(db.String(1), nullable=True, comment='Digito de verificacion de la persona')
    DocumentTypePerson = db.Column(db.String(5), nullable=True, comment='13=Cedula 31=NIT')
    FirstNamePerson = db.Column(db.String(100), nullable=True, comment='Nombre de la persona')
    LastNamePerson = db.Column(db.String(100), nullable=True, comment='Apellido de la persona')
    JobTitle = db.Column(db.String(100), nullable=True, comment='Cargo del empleado')
    OrganizationDepartment = db.Column(db.String(100), nullable=True, comment='Departamento de la empresa')
    Note = db.Column(LONGTEXT, nullable=True, comment='Comentarios del evento')

    __table_args__ = (Index('ix_idy', "IssuerNit", "DocType", "YearSend"),)

    def export_data(self):
        return {
            'Id': self.Id,
            'CreateDate': str(self.CreateDate),
            'UpdateDate': str(self.UpdateDate),
            'IssuerNit': self.IssuerNit,
            'IssuerName': self.IssuerName,
            'DocType': self.DocType,
            'Prefix': self.Prefix,
            'SerieNumber': self.SerieNumber,
            'YearSend': self.YearSend,
            'NumberSend': self.NumberSend,
            'DianResolution': self.DianResolution,
            'IdSoftware': self.IdSoftware,
            'ClientNit': self.ClientNit,
            'ClientName': self.ClientName,
            'ClientEmail': self.ClientEmail,
            'DateSend': str(self.DateSend),
            'HourSend': str(self.HourSend),
            'DianResponse': self.DianResponse,
            'DianResponseErrors': self.DianResponseErrors,
            'DianXml': self.DianXml,
            'DianXmlAppResponse': self.DianXmlAppResponse,
            'Cufe': self.Cufe,
            'CUDE': self.CUDE,
            'TrackIdDian': self.TrackIdDian,
            'JsonReceived': self.JsonReceived,
            'MessageEmail': self.MessageEmail,
            'Status': self.Status,
            'DocumentNumberPerson': self.DocumentNumberPerson,
            'CheckDigitPerson': self.CheckDigitPerson,
            'DocumentTypePerson': self.DocumentTypePerson,
            'FirstNamePerson': self.FirstNamePerson,
            'LastNamePerson': self.LastNamePerson,
            'JobTitle': self.JobTitle,
            'OrganizationDepartment': self.OrganizationDepartment,
            'Note': self.Note
        }

    def export_data_2(self):
        return {
            'id': self.Id,
            'document': self.Prefix + self.SerieNumber,
            'documentDate': str(self.DateSend),
            'thirdName': self.ClientName,
            'communicationStatus': self.DianResponse + self.DianResponseErrors,
            'businessStatus': self.Status,
            'total': self.Total
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
        if 'Prefix' in data:
            self.Prefix = data['Prefix']
        if 'SerieNumber' in data:
            self.SerieNumber = data['SerieNumber']
        if 'YearSend' in data:
            self.YearSend = data['YearSend']
        if 'NumberSend' in data:
            self.NumberSend = data['NumberSend']
        if 'DianResolution' in data:
            self.DianResolution = data['DianResolution']
        if 'IdSoftware' in data:
            self.IdSoftware = data['IdSoftware']
        if 'ClientNit' in data:
            self.ClientNit = data['ClientNit']
        if 'ClientName' in data:
            self.ClientName = data['ClientName']
        if 'ClientEmail' in data:
            self.ClientEmail = data['ClientEmail']
        if 'DateSend' in data:
            self.DateSend = data['DateSend']
        if 'HourSend' in data:
            self.HourSend = data['HourSend']
        if 'DianResponse' in data:
            self.DianResponse = data['DianResponse']
        if 'DianResponseErrors' in data:
            self.DianResponseErrors = data['DianResponseErrors']
        if 'DianXml' in data:
            self.DianXml = data['DianXml']
        if 'DianXmlAppResponse' in data:
            self.DianXmlAppResponse = data['DianXmlAppResponse']
        if 'Cufe' in data:
            self.Cufe = data['Cufe']
        if 'CUDE' in data:
            self.CUDE = data['CUDE']
        if 'TrackIdDian' in data:
            self.TrackIdDian = data['TrackIdDian']
        if 'JsonReceived' in data:
            self.JsonReceived = data['JsonReceived']
        if 'MessageEmail' in data:
            self.MessageEmail = data['MessageEmail']
        if 'Status' in data:
            self.Status = data['Status']
        if 'DocumentNumberPerson' in data:
            self.DocumentNumberPerson = data['DocumentNumberPerson']
        if 'CheckDigitPerson' in data:
            self.CheckDigitPerson = data['CheckDigitPerson']
        if 'DocumentTypePerson' in data:
            self.DocumentTypePerson = data['DocumentTypePerson']
        if 'FirstNamePerson' in data:
            self.FirstNamePerson = data['FirstNamePerson']
        if 'LastNamePerson' in data:
            self.LastNamePerson = data['LastNamePerson']
        if 'JobTitle' in data:
            self.JobTitle = data['JobTitle']
        if 'OrganizationDepartment' in data:
            self.OrganizationDepartment = data['OrganizationDepartment']
        if 'Note' in data:
            self.Note = data['Note']
        return self

    @staticmethod
    def export_xml(data: dict):
        try:
            if data["DocType"] == "FV":
                xissuer = str.zfill(data["IssuerNit"], 10)
                filename = os.getenv("PATH_DOCS") + xissuer + "event/" + "/" + data["DianXml"]

                with open(filename, "rb") as f:
                    datapdf = f.read()
                datapdf_encode = b64encode(datapdf).decode("utf-8")

                return datapdf_encode

        except Exception as e:
            print(e)
            response = ResponseData.internal_server_error(str(e))
            return response

    @staticmethod
    def get_data(export: bool = False, pageNumber=0, pageSize=None):
        try:
            if pageSize != None:
                response = db.session.query(EventsModel) \
                    .limit(int(pageSize)) \
                    .offset((int(pageNumber) - 1) * int(pageSize)) \
                    .all()
            else:
                response = db.session.query(EventsModel) \
                    .all()
            if export:
                response = [EventsModel.export_data(x) for x in response]
            return response
        except Exception as e:
            print(e)
            response = ResponseData.internal_server_error(str(e))
            return response

    @staticmethod
    def get_by_id(id: int, export: bool = False):
        try:
            response = db.session.query(EventsModel) \
                .filter(EventsModel.Id == id) \
                .first()
            if export and response:
                response = EventsModel.export_data(response)
            return response
        except Exception as e:
            print(e)
            response = ResponseData.internal_server_error(str(e))
            return response

    @staticmethod
    def get_by(data: dict, export: bool = False, pageNumber=0, pageSize=None):
        try:
            IssuerNit = ""
            StartClientNit = ""
            EndClientNit = ""
            DocType = "FV"
            StartDate = ""
            EndDate = ""
            Status = ""
            StartNumber = ""
            EndNumber = ""
            if "issuerNit" in data:
                IssuerNit = data["issuerNit"]
            if "startClientNit" in data:
                StartClientNit = data["startClientNit"]
            if "endClientNit" in data:
                EndClientNit = data["endClientNit"]
            if "docType" in data:
                DocType = data["docType"]
            if "starDate" in data:
                StartDate = data["starDate"]
            if "endDate" in data:
                EndDate = data["endDate"]
            if "pageSize" in data:
                pageSize = data["pageSize"]
            if "pageNumber" in data:
                pageNumber = data["pageNumber"]
            if "startNumber" in data:
                StartNumber = data["startNumber"]
            if "endNumber" in data:
                EndNumber = data["endNumber"]
            if "status" in data:
                Status = data["status"]

            if StartClientNit == "":
                StartClientNit = "#"
            if EndClientNit == "":
                EndClientNit = "zzzzzzzzzzzzzzzzzz"

            if StartNumber == "":
                StartNumber = "#"
            if EndNumber == "":
                EndNumber = "zzzzzzzzzzzzzzzzzz"
            if pageSize != None:
                if StartDate != "":
                    response = db.session.query(EventsModel) \
                        .filter(
                        EventsModel.IssuerNit == IssuerNit, EventsModel.Prefix + EventsModel.SerieNumber >= StartNumber
                        , EventsModel.Prefix + EventsModel.SerieNumber <= EndNumber,
                        EventsModel.ClientNit >= StartClientNit,
                        EventsModel.ClientNit <= EndClientNit,
                        EventsModel.DateSend >= StartDate, EventsModel.DateSend <= EndDate
                        , EventsModel.Status == Status, EventsModel.DocType == DocType) \
                        .limit(int(pageSize)) \
                        .offset((int(pageNumber) - 1) * int(pageSize)) \
                        .all()
                else:
                    response = db.session.query(EventsModel) \
                        .filter(
                        EventsModel.IssuerNit == IssuerNit, EventsModel.Prefix + EventsModel.SerieNumber >= StartNumber
                        , EventsModel.Prefix + EventsModel.SerieNumber <= EndNumber,
                        EventsModel.ClientNit >= StartClientNit,
                        EventsModel.ClientNit <= EndClientNit
                        , EventsModel.Status == Status, EventsModel.DocType == DocType) \
                        .limit(int(pageSize)) \
                        .offset((int(pageNumber) - 1) * int(pageSize)) \
                        .all()
            else:
                if StartDate != "":
                    response = db.session.query(EventsModel) \
                        .filter(
                        EventsModel.IssuerNit == IssuerNit, EventsModel.Prefix + EventsModel.SerieNumber >= StartNumber
                        , EventsModel.Prefix + EventsModel.SerieNumber <= EndNumber,
                        EventsModel.ClientNit >= StartClientNit,
                        EventsModel.ClientNit <= EndClientNit,
                        EventsModel.DateSend >= StartDate, EventsModel.DateSend <= EndDate
                        , EventsModel.Status == Status, EventsModel.DocType == DocType) \
                        .all()
                else:
                    response = db.session.query(EventsModel) \
                        .filter(
                        EventsModel.IssuerNit == IssuerNit, EventsModel.Prefix + EventsModel.SerieNumber >= StartNumber
                        , EventsModel.Prefix + EventsModel.SerieNumber <= EndNumber,
                        EventsModel.ClientNit >= StartClientNit,
                        EventsModel.ClientNit <= EndClientNit
                        , EventsModel.Status == Status, EventsModel.DocType == DocType) \
                        .all()

            if export and response:
                response = [EventsModel.export_data_2(x) for x in response]
            return response
        except Exception as e:
            print(e)
            response = ResponseData.internal_server_error(str(e))
            return response

    @staticmethod
    def get_by_number(Nit: str, SeriePrefix: str, SerieNumber: str, DocType: str, export: bool = False):
        try:
            response = db.session.query(EventsModel) \
                .filter(
                EventsModel.IssuerNit == Nit, EventsModel.Prefix == SeriePrefix, EventsModel.SerieNumber == SerieNumber
                , EventsModel.Status == "1", EventsModel.DocType == DocType) \
                .first()
            if export and response:
                response = EventsModel.export_data(response)
            return response
        except Exception as e:
            print(e)
            response = ResponseData.internal_server_error(str(e))
            return response

    @staticmethod
    def create_xml_event(data: dict):
        def claimToDescription(code: str):
            if code == "01":
                return "Documento con inconsistencias"
            if code == "02":
                return "Mercancia no entregada totalmente"
            if code == "03":
                return "Mercancia no entregada parcialmente"
            if code == "04":
                return "Servicio no prestado"
        try:
            person = {}
            if 'person' in data:
                person = data["person"]
            CUDE = data['CUDE']
            if data['CUDE'] == '':
                CUDE = (str(data["number"]) + str(data["issueDate"]) + str(data["issueTime"]) + str(
                    data["nitSenderParty"])
                        + str(data["nitReceiverParty"]) + str(data["responseCode"]) + str(data["documentReference"])
                        + str(data["documentTypeCode"]) + str(data["dianPin"]))
                h = hashlib.sha384()
                h.update(CUDE.encode('utf-8'))
                CUDE = h.hexdigest()

            SoftwareSecurityCode = (data["dianSoftwareID"] + data["dianPin"] + str(data["number"]))
            s = hashlib.sha384()
            s.update(SoftwareSecurityCode.encode('utf-8'))
            SoftwareSecurityCode = s.hexdigest()
            QR = "https://catalogo-vpfe.dian.gov.co/document/searchqr?documentkey=" + data["CUFE"]

            Plane = '<?xml version="1.0" encoding="utf-8" standalone="no"?>' \
                    '<ApplicationResponse ' \
                    'xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" ' \
                    'xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" ' \
                    'xmlns:ext="urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2" ' \
                    'xmlns:sts="dian:gov:co:facturaelectronica:Structures-2-1" ' \
                    'xmlns:ds="http://www.w3.org/2000/09/xmldsig#" ' \
                    'xmlns="urn:oasis:names:specification:ubl:schema:xsd:ApplicationResponse-2">' \
                    '<ext:UBLExtensions> ' \
                    '<ext:UBLExtension> ' \
                    '<ext:ExtensionContent> ' \
                    '<sts:DianExtensions> ' \
                    '<sts:InvoiceSource> ' \
                    '<cbc:IdentificationCode listAgencyID="6" ' \
                    'listAgencyName="United Nations Economic Commission for Europe" ' \
                    'listSchemeURI="urn:oasis:names:specification:ubl:codelist:gc:CountryIdentificationCode-2.1">CO' \
                    '</cbc:IdentificationCode>' \
                    '</sts:InvoiceSource> ' \
                    '<sts:SoftwareProvider> ' \
                    '<sts:ProviderID schemeID="' + data["checkDigitSenderParty"] + '" schemeName="' + \
                    data["docTypeSenderParty"] + '" schemeAgencyID="195" ' \
                    'schemeAgencyName="CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)">' + \
                    data["nitSenderParty"] + '</sts:ProviderID> ' \
                    '<sts:SoftwareID schemeAgencyID="195" ' \
                    'schemeAgencyName="CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)">' + \
                    data["dianSoftwareID"] + '</sts:SoftwareID> ' \
                    '</sts:SoftwareProvider> ' \
                    '<sts:SoftwareSecurityCode schemeAgencyID="195" ' \
                    'schemeAgencyName="CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)">' + \
                    SoftwareSecurityCode + '</sts:SoftwareSecurityCode> ' \
                    '<sts:AuthorizationProvider> ' \
                    '<sts:AuthorizationProviderID schemeID="4"' ' schemeName="' + data["docTypeSenderParty"] + \
                    '" schemeAgencyID="195" schemeAgencyName="CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)">'\
                    '800197268</sts:AuthorizationProviderID>' \
                    '</sts:AuthorizationProvider>' \
                    '<sts:QRCode>' + QR + '</sts:QRCode>' \
                    '</sts:DianExtensions> ' \
                    '</ext:ExtensionContent> ' \
                    '</ext:UBLExtension> ' \
                    '<ext:UBLExtension> ' \
                    '<ext:ExtensionContent>' \
                    '</ext:ExtensionContent> ' \
                    '</ext:UBLExtension> ' \
                    '</ext:UBLExtensions> ' \
                    '<cbc:UBLVersionID>UBL 2.1</cbc:UBLVersionID> ' \
                    '<cbc:CustomizationID>1</cbc:CustomizationID> ' \
                    '<cbc:ProfileID>DIAN 2.1: ApplicationResponse de la Factura Electrónica de Venta</cbc:ProfileID> ' \
                    '<cbc:ProfileExecutionID>1</cbc:ProfileExecutionID> ' \
                    '<cbc:ID>' + str(data["number"]) + '</cbc:ID> ' \
                    '<cbc:UUID schemeID= "1" schemeName="CUDE-SHA384">' + CUDE + '</cbc:UUID> ' \
                    '<cbc:IssueDate>' + data["issueDate"] + '</cbc:IssueDate> ' \
                    '<cbc:IssueTime>' + data["issueTime"] + '</cbc:IssueTime> ' \
                    '<cbc:Note>' + data["note"] + '</cbc:Note> ' \
                    '<cac:SenderParty> ' \
                    '<cac:PartyTaxScheme> ' \
                    '<cbc:RegistrationName>' + data["registrationNameSenderParty"] + '</cbc:RegistrationName> ' \
                    '<cbc:CompanyID schemeAgencyID="195" ' \
                    'schemeAgencyName="CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)" schemeVersionID="' + \
                    data["legalTypeSenderParty"] + '" schemeID="' + data["checkDigitSenderParty"] + '" schemeName="' + \
                    data["docTypeSenderParty"] + '">' + data["nitSenderParty"] + '</cbc:CompanyID> ' \
                    '<cac:TaxScheme> ' \
                    '<cbc:ID>' + data["taxSchemeCodeSenderParty"] + '</cbc:ID> ' \
                    '<cbc:Name>' + data["taxSchemeNameSenderParty"] + '</cbc:Name> ' \
                    '</cac:TaxScheme> ' \
                    '</cac:PartyTaxScheme> ' \
                    '</cac:SenderParty> ' \
                    '<cac:ReceiverParty> ' \
                    '<cac:PartyTaxScheme> ' \
                    '<cbc:RegistrationName>' + data["registrationNameReceiverParty"] + '</cbc:RegistrationName> ' \
                    '<cbc:CompanyID schemeAgencyID="195" ' \
                    'schemeAgencyName="CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)" schemeVersionID="' + \
                    data["legalTypeReceiverParty"] + '" schemeID="' + data["checkDigitReceiverParty"] + \
                    '" schemeName="' + data["docTypeReceiverParty"] + '">' + data["nitReceiverParty"] + \
                    '</cbc:CompanyID> ' \
                    '<cac:TaxScheme> ' \
                    '<cbc:ID>' + data["taxSchemeCodeReceiverParty"] + '</cbc:ID> ' \
                    '<cbc:Name>' + data["taxSchemeNameReceiverParty"] + '</cbc:Name> ' \
                    '</cac:TaxScheme> ' \
                    '</cac:PartyTaxScheme> ' \
                    '</cac:ReceiverParty> ' \
                    '<cac:DocumentResponse>' \
                    '<cac:Response>' \
                    '<cbc:ResponseCode'
            if "claimCode" in data:
                Plane += ' name="' + claimToDescription(data["claimCode"]) + '" listID="' + data["claimCode"] + '" '
            Plane += '>' + data["responseCode"] + '</cbc:ResponseCode>' \
                                                  '<cbc:Description>' + data["description"] + '</cbc:Description>' \
                                                  '</cac:Response>' \
                                                  '<cac:DocumentReference>' \
                                                  '<cbc:ID>' + data["documentReference"] + '</cbc:ID>' \
                                                  '<cbc:UUID schemeName="CUFE-SHA384">' + data["CUFE"] + '</cbc:UUID>' \
                                                  '<cbc:DocumentTypeCode>' + data["documentTypeCode"] + \
                                                  '</cbc:DocumentTypeCode>' \
                                                  '</cac:DocumentReference>'
            if 'person' in data:
                Plane += '<cac:IssuerParty>' \
                         '<cac:Person>' \
                         '<cbc:ID schemeID="' + person["checkDigit"] + '" schemeName="' + person["docType"] + '">' + \
                         person["ID"] + '</cbc:ID>' \
                         '<cbc:FirstName>' + person["firstName"] + '</cbc:FirstName>' \
                         '<cbc:FamilyName>' + person["lastName"] + '</cbc:FamilyName>' \
                         '<cbc:JobTitle>' + person["jobTitle"] + '</cbc:JobTitle>' \
                         '<cbc:OrganizationDepartment>' + person["organizationDepartment"] + \
                         '</cbc:OrganizationDepartment>' \
                         '</cac:Person>' \
                         '</cac:IssuerParty>'
            Plane += '</cac:DocumentResponse>' \
                     '</ApplicationResponse>'
            return Plane
        except Exception as e:
            print(e)
            response = ResponseData.internal_server_error(str(e))
            return response

    @staticmethod
    def create_xml_event2(data: dict):
        try:
            Plane = '<?xml version="1.0" encoding="utf-8" standalone="no"?> \
                    <ApplicationResponse xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"\
                    xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"  \
                    xmlns:ext="urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2" \
                    xmlns:sts="dian:gov:co:facturaelectronica:Structures-2-1" \
                    xmlns:ds="http://www.w3.org/2000/09/xmldsig#"  \
                    xmlns="urn:oasis:names:specification:ubl:schema:xsd:ApplicationResponse-2">' \
 \
                    '<ext:UBLExtensions>' \
                    '<ext:UBLExtension>' \
                    '<ext:ExtensionContent>' \
                    '</ext:ExtensionContent>' \
                    '</ext:UBLExtension>' \
                    '<ext:UBLExtension>' \
                    '<ext:ExtensionContent>' \
                    '</ext:ExtensionContent>' \
                    '</ext:UBLExtension>' \
                    '</ext:UBLExtensions>' \
                    '<cbc:UBLVersionID>UBL 2.1</cbc:UBLVersionID>' \
                    '<cbc:CustomizationID>1</cbc:CustomizationID>' \
                    '<cbc:ProfileID>DIAN 2.1</cbc:ProfileID>' \
                    '<cbc:ProfileExecutionID>1</cbc:ProfileExecutionID>' \
                    '<cbc:ID>' + data["number"] + '</cbc:ID>' \
                                                  '<cbc:UUID schemeName="CUDE-SHA384">' + data["CUDE"] + '</cbc:UUID>' \
                                                                                                         '<cbc:IssueDate>' + \
                    data["IssueDate"] + '</cbc:IssueDate>' \
                                        '<cbc:IssueTime>' + data["IssueTime"] + '</cbc:IssueTime>' \
                                                                                '<cac:SenderParty>' \
                                                                                '<cac:PartyTaxScheme>' \
                                                                                '<cbc:RegistrationName>' + data[
                        "RegistrationNameSenderParty"] + '</cbc:RegistrationName>' \
                                                         '<cbc:CompanyID schemeID="' + data[
                        "CheckDigitSenderParty"] + '" schemeName="' + data["DocTypeSenderParty"] + '">' + data[
                        "NitSenderParty"] + '</cbc:CompanyID>' \
                                            '<cac:TaxScheme>' \
                                            '<cbc:ID>' + data["TaxSchemeCodeSenderParty"] + '</cbc:ID>' \
                                                                                            '<cbc:Name>' + data[
                        "TaxSchemeNameSenderParty"] + '</cbc:Name>' \
                                                      '</cac:TaxScheme>' \
                                                      '</cac:PartyTaxScheme>' \
                                                      '</cac:SenderParty>' \
                                                      '<cac:ReceiverParty>' \
                                                      '<cac:PartyTaxScheme>' \
                                                      '<cbc:RegistrationName>' + data[
                        "RegistrationNameReceiverParty"] + '</cbc:RegistrationName>' \
                                                           '<cbc:CompanyID schemeID="' + data[
                        "CheckDigitReceiverParty"] + '" schemeName="' + data["DocTypeReceiverParty"] + '">' + data[
                        "NitReceiverParty"] + '</cbc:CompanyID>' \
                                              '<cac:TaxScheme>' \
                                              '<cbc:ID>' + data["TaxSchemeCodeReceiverParty"] + '</cbc:ID>' \
                                                                                                '<cbc:Name>' + data[
                        "TaxSchemeNameReceiverParty"] + '</cbc:Name>' \
                                                        '</cac:TaxScheme>' \
                                                        '</cac:PartyTaxScheme>' \
                                                        '<cac:Contact>' \
                                                        '<cbc:ElectronicMail>' + data[
                        "ElectronicMailReceiverParty"] + '</cbc:ElectronicMail>' \
                                                         '</cac:Contact>' \
                                                         '</cac:ReceiverParty>' \
                                                         '<cac:DocumentResponse>' \
                                                         '<cac:Response>' \
                                                         '<cbc:ResponseCode>' + data[
                        "ResponseCode"] + '</cbc:ResponseCode>' \
                                          '<cbc:Description>' + data["Description"] + '</cbc:Description>' \
                                                                                      '</cac:Response>' \
                                                                                      '<cac:DocumentReference>' \
                                                                                      '<cbc:ID>' + data[
                        "DocumentReference"] + '</cbc:ID>' \
                                               '<cbc:UUID schemeName="CUFE-SHA384">' + data["CUFE"] + '</cbc:UUID>' \
                                                                                                      '<cbc:DocumentTypeCode>' + \
                    data["DocumentTypeCode"] + '</cbc:DocumentTypeCode>' \
                                               '</cac:DocumentReference>' \
                                               '</cac:DocumentResponse>' \
                                               '</ApplicationResponse>'

            return Plane
        except Exception as e:
            print(e)
            response = ResponseData.internal_server_error(str(e))
            return response

    @staticmethod
    def Create_xml_ad_event(new_data: dict, sends: dict, NumberContainer: int):
        try:
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
            CUFE = new_data["CUFE"]
            Customer = new_data["CustomerParty"]
            CustomerDocumentType = Customer["DocumentType"]
            CustomerDocumentNumber = Customer["DocumentNumber"]
            CustomerCommercialRegistration = Customer["CommercialRegistration"]
            CustomerResponsabilityTypes = Customer["ResponsabilityTypes"]

            xissuer = str.zfill(IssuerNit, 10)
            path_issuer = os.getenv('PATH_DOCS') + xissuer + "/"
            if DocType == "FV":
                path_issuer += "invoice/"
            elif DocType == "DS":
                path_issuer += "supportdoc/"
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
                                                                                                                                                                                                                                                                                             '<cbc:CompanyID schemeAgencyID = "195" schemeID = "' + IssuerNit + '" schemeName = "' + IssuerCheckDigit + '" schemeAgencyName = "CO,DIAN(Dirección de Impuestos y Aduanas Nacionales)">' + IssuerNit + '</cbc:CompanyID>' \
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
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    '<cbc:CompanyID schemeAgencyID = "195" schemeID = "' + CustomerDocumentNumber + '" schemeName = "' + CustomerDocumentType + '" schemeAgencyName = "CO,DIAN(Dirección de Impuestos y Aduanas Nacionales)">' + CustomerDocumentNumber + '</cbc:CompanyID>' \
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
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               '<cbc:Description><![CDATA[' + \
                     dian_xml + ']]></cbc:Description>' \
                                '</cac:ExternalReference>' \
                                '</cac:Attachment>' \
                                '<cac:ParentDocumentLineReference>' \
                                '<cbc:LineID>1</cbc:LineID>' \
                                '<cac:DocumentReference>' \
                                '<cbc:ID>' + SeriePrefix + SerieNumber + '</cbc:ID>' \
                                                                         '<cbc:UUID schemeName = "CUFE-SHA384">' + str(
                CUFE) + '</cbc:UUID>' \
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
        except Exception as e:
            print(e)
            response = ResponseData.internal_server_error(str(e))
            return response

    @staticmethod
    def new_data(data: dict):
        try:
            new_data = EventsModel()
            new_data = EventsModel.import_data(new_data, data=data)
            EventsModel.save(new_data, create=True, commit=True)
            response = {
                'data': EventsModel.export_data(new_data),
                'statusCode': 201,
                'message': 'Registro almacenado correctamente'
            }
            return response
        except Exception as e:
            print('Error: {er}'.format(er=e))
            raise InternalServerError(e)

    @staticmethod
    def update_data(data: dict):
        try:
            update_data = EventsModel.get_by_id(id=data['Id'], export=False)
            if not update_data:
                return NotFound('Los datos ingresados no pertenecen o no son validos para el registro consultado')
            update_data = EventsModel.import_data(update_data, data=data)
            EventsModel.save(update_data, create=True, commit=True)
            response = {
                'data': EventsModel.export_data(update_data),
                'statusCode': 200,
                'message': 'Registro modificado correctamente'
            }
            return response
        except Exception as e:
            print('Error: {er}'.format(er=e))
            raise

    @validates()
    def validate_name_permit(self, key, name):
        try:
            FieldValidations.is_none(key, name)
            FieldValidations.is_empty(key, name)
            return name
        except Exception as e:
            print(e)
            raise InternalServerError(e)
