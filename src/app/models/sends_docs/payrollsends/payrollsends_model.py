# -*- coding: utf-8 -*-
#########################################################
import hashlib
import os
from typing import Any, Dict
from sqlalchemy import Index
from app.models.base_model import BaseModel
from app import db
from app.exception import InternalServerError, NotFound
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import validates
from app.utils import FieldValidations
from base64 import b64encode
from app.utils import ResponseData


class PayRollSendsModel(BaseModel):
    __tablename__ = 'payrollsends'

    IssuerNit = db.Column(db.String(20), nullable=False, comment='Nit de la empresa o emisor ')
    IssuerName = db.Column(db.String(200), nullable=False, comment='Nombre o razon social del emisor ')
    DocType = db.Column(db.String(5), nullable=False, comment=' NOM=Nomina NOMA=Nomina Ajuste ')
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
    DianResponse = db.Column(db.String(200), nullable=True, comment='Respuesta DIAN ')
    DianResponseErrors = db.Column(db.String(200), nullable=True, comment='Errores DIAN ')
    DianXml = db.Column(LONGTEXT, nullable=True, comment='Xml enviado a DIAN ')
    DianXmlAppResponse = db.Column(LONGTEXT, nullable=True, comment='Xml Respuesta DIAN ')
    Cufe = db.Column(db.String(150), nullable=True, comment='CUFE, CUDE o CUNE documento ')
    TrackIdDian = db.Column(db.String(200), nullable=True, comment='Cadena que reporta la DIAN ')
    JsonReceived = db.Column(LONGTEXT, nullable=True, comment='JSON serializado')
    Status = db.Column(db.String(1), nullable=True, comment='0 Rechazado 1=Enviado ')
    Accrued = db.Column(db.Float(20), nullable=True, comment='total devengado')
    Deducted = db.Column(db.Float(20), nullable=True, comment='total deducido')
    Value = db.Column(db.Float(20), nullable=True, comment='diferencia devengado-deducido')

    __table_args__ = (Index('ix_prs', "IssuerNit", "DocType", "YearSend"),)

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
            'TrackIdDian': self.TrackIdDian,
            'JsonReceived': self.JsonReceived,
            'Status': self.Status,
            'Accrued': self.Accrued,
            'Deducted': self.Deducted,
            'Value': self.Value

        }

    def export_data_2(self):
        return {
            'id': self.Id,
            'transmition': self.Prefix + self.SerieNumber,
            'period': str(self.DateSend),
            'employee': self.ClientName,
            'state': self.Status,
            'accrued': self.Accrued,
            'deducted': self.Deducted,
            'value': self.Value
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
        if 'TrackIdDian' in data:
            self.TrackIdDian = data['TrackIdDian']
        if 'JsonReceived' in data:
            self.JsonReceived = data['JsonReceived']
        if 'Status' in data:
            self.Status = data['Status']
        if 'Accrued' in data:
            self.Accrued = data['Accrued']
        if 'Deducted' in data:
            self.Deducted = data['Deducted']
        if 'Value' in data:
            self.Value = data['Value']
        return self

    @staticmethod
    def export_pdf(data: dict):
        try:
            xissuer = str.zfill(data["IssuerNit"], 10)
            filename = os.getenv("PATH_DOCS") + xissuer + "payroll/" + "/" + data["DianXml"]
            filename = filename.replace(".xml", ".pdf")

            with open(filename, "rb") as f:
                datapdf = f.read()
            datapdf_encode = b64encode(datapdf).decode("utf-8")

            return datapdf_encode
        except Exception as e:
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def export_xml(data: dict):
        try:
            xissuer = str.zfill(data["IssuerNit"], 10)
            filename = os.getenv("PATH_DOCS") + xissuer + "payroll/" + "/" + data["DianXml"]

            with open(filename, "rb") as f:
                datapdf = f.read()
            datapdf_encode = b64encode(datapdf).decode("utf-8")

            return datapdf_encode

        except Exception as e:
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def export_json(data: dict):
        try:
            xissuer = str.zfill(data["IssuerNit"], 10)
            filename = os.getenv("PATH_DOCS") + xissuer + "payroll/" + "/" + data["JsonReceived"]

            with open(filename, "rb") as f:
                datapdf = f.read()
            datapdf_encode = b64encode(datapdf).decode("utf-8")

            return {
                'json': datapdf_encode
            }

        except Exception as e:
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def get_data(export: bool = False, pageNumber=0, pageSize=None):
        try:
            if pageSize != None:
                response = db.session.query(PayRollSendsModel) \
                    .limit(int(pageSize)) \
                    .offset((int(pageNumber) - 1) * int(pageSize)) \
                    .all()
            else:
                response = db.session.query(PayRollSendsModel) \
                    .all()
            if export:
                response = [PayRollSendsModel.export_data(x) for x in response]
            return response
        except Exception as e:
            print(e)
            response = ResponseData.internal_server_error(str(e))
            return response

    @staticmethod
    def get_by_id(id: int, export: bool = False):
        try:
            response = db.session.query(PayRollSendsModel) \
                .filter(PayRollSendsModel.Id == id) \
                .first()
            if export and response:
                response = PayRollSendsModel.export_data(response)
            return response
        except Exception as e:
            print(e)
            response = ResponseData.internal_server_error(str(e))
            return response

    @staticmethod
    def get_by(data: Dict[str, Any], export: bool = False, pageNumber=0, pageSize=None):
        try:
            IssuerNit = ""
            StartClientNit = ""
            EndClientNit = ""
            DocType = "NO"
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
                    response = db.session.query(PayRollSendsModel) \
                        .filter(
                        PayRollSendsModel.IssuerNit == IssuerNit,
                        PayRollSendsModel.Prefix + PayRollSendsModel.SerieNumber >= StartNumber
                        , PayRollSendsModel.Prefix + PayRollSendsModel.SerieNumber <= EndNumber,
                        PayRollSendsModel.ClientNit >= StartClientNit,
                        PayRollSendsModel.ClientNit <= EndClientNit,
                        PayRollSendsModel.DateSend >= StartDate, PayRollSendsModel.DateSend <= EndDate
                        , PayRollSendsModel.Status == Status, PayRollSendsModel.DocType == DocType) \
                        .limit(int(pageSize)) \
                        .offset((int(pageNumber) - 1) * int(pageSize)) \
                        .all()
                else:
                    response = db.session.query(PayRollSendsModel) \
                        .filter(
                        PayRollSendsModel.IssuerNit == IssuerNit,
                        PayRollSendsModel.Prefix + PayRollSendsModel.SerieNumber >= StartNumber
                        , PayRollSendsModel.Prefix + PayRollSendsModel.SerieNumber <= EndNumber,
                        PayRollSendsModel.ClientNit >= StartClientNit,
                        PayRollSendsModel.ClientNit <= EndClientNit
                        , PayRollSendsModel.Status == Status, PayRollSendsModel.DocType == DocType) \
                        .limit(int(pageSize)) \
                        .offset((int(pageNumber) - 1) * int(pageSize)) \
                        .all()
            else:
                if StartDate != "":
                    response = db.session.query(PayRollSendsModel) \
                        .filter(
                        PayRollSendsModel.IssuerNit == IssuerNit,
                        PayRollSendsModel.Prefix + PayRollSendsModel.SerieNumber >= StartNumber
                        , PayRollSendsModel.Prefix + PayRollSendsModel.SerieNumber <= EndNumber,
                        PayRollSendsModel.ClientNit >= StartClientNit,
                        PayRollSendsModel.ClientNit <= EndClientNit,
                        PayRollSendsModel.DateSend >= StartDate, PayRollSendsModel.DateSend <= EndDate
                        , PayRollSendsModel.Status == Status, PayRollSendsModel.DocType == DocType) \
                        .all()
                else:
                    response = db.session.query(PayRollSendsModel) \
                        .filter(
                        PayRollSendsModel.IssuerNit == IssuerNit,
                        PayRollSendsModel.Prefix + PayRollSendsModel.SerieNumber >= StartNumber
                        , PayRollSendsModel.Prefix + PayRollSendsModel.SerieNumber <= EndNumber,
                        PayRollSendsModel.ClientNit >= StartClientNit,
                        PayRollSendsModel.ClientNit <= EndClientNit
                        , PayRollSendsModel.Status == Status, PayRollSendsModel.DocType == DocType) \
                        .all()
            if export and response:
                response = [PayRollSendsModel.export_data_2(x) for x in response]
            return response
        except Exception as e:
            print(e)
            response = ResponseData.internal_server_error(str(e))
            return response

    @staticmethod
    def get_by_number(Nit: str, SeriePrefix: str, SerieNumber: str, DocType: str, export: bool = False):
        try:
            response = db.session.query(PayRollSendsModel) \
                .filter(
                PayRollSendsModel.IssuerNit == Nit, PayRollSendsModel.Prefix == SeriePrefix,
                PayRollSendsModel.SerieNumber == SerieNumber
                , PayRollSendsModel.Status == "1", PayRollSendsModel.DocType == DocType) \
                .first()
            if export and response:
                response = PayRollSendsModel.export_data(response)
            return response
        except Exception as e:
            print(e)
            response = ResponseData.internal_server_error(str(e))
            return response

    @staticmethod
    def create_xml_payroll(data: dict):
        Plane = ""
        Transporte = []
        HEDs = []
        HENs = []
        HRNs = []
        HEDDFs = []
        HRDDFs = []
        HENDFs = []
        HRNDFs = []
        Vacaciones = []
        VacacionesComunes = []
        VacacionesCompensadas = []
        Primas = {}
        Cesantias = {}
        Incapacidades = []
        Licencias = {}
        LicenciaMP = []
        LicenciaR = []
        LicenciaNR = []
        Bonificaciones = []
        Auxilios = []
        OtrosConceptos = []
        Compensaciones = []
        BonoEPCTVs = []
        Comisiones = []
        PagosTerceros = []
        Anticipos = ""
        Dotacion = ""
        ApoyoSost = ""
        Teletrabajo = ""
        BonifRetiro = ""
        Indemnizacion = ""
        Reintegro = ""
        Deducciones = data["Deducciones"]
        Salud = {}
        FondoPension = {}
        FondoSP = {}
        Sindicatos = []
        Sanciones = []
        Libranzas = []
        PagosTercerosD = []
        AnticiposD = []
        OtrasDeducciones = []
        PensionVoluntaria = ""
        RetencionFuente = ""
        AFC = ""
        Cooperativa = ""
        EmbargoFiscal = ""
        PlanComplementarios = ""
        Educacion = ""
        ReintegroD = ""
        Deuda = ""
        TipoNota = ""
        NumeroDocPredecesor = ""
        FechaGenPredecesor = ""
        CUNEPredecesor = ""

        Periodo = data["Periodo"]
        FechasPagos = data["FechasPagos"]
        SecuenciaXML = data["NumeroSecuenciaXML"]
        Numero = SecuenciaXML["Numero"]
        LugarGeneracionXML = data["LugarGeneracionXML"]
        InformacionGeneral = data["InformacionGeneral"]
        if "TipoNota" in InformacionGeneral:
            TipoNota = InformacionGeneral["TipoNota"]
        if "NumeroDocumentoPredecesor" in InformacionGeneral:
            NumeroDocPredecesor = InformacionGeneral["NumeroDocumentoPredecesor"]

        if "FechaGenPredecesor" in InformacionGeneral:
            FechaGenPredecesor = InformacionGeneral["FechaGenPredecesor"]

        if "CUNEPredecesor" in InformacionGeneral:
            CUNEPredecesor = InformacionGeneral["CUNEPredecesor"]
        Empleador = data["Empleador"]
        Nit = Empleador["NIT"]
        Pin = InformacionGeneral["DianPin"]
        FechaNE = InformacionGeneral["FechaGen"]
        HoraNE = InformacionGeneral["HoraGen"]
        TipoAmb = InformacionGeneral["TipoAmbiente"]
        SoftwareId = InformacionGeneral["DianSoftwareId"]
        Notas = data["Notas"]
        Trabajador = data["Trabajador"]
        DocEmp = Trabajador["NumeroDocumento"]
        Pago = data["Pago"]
        Deven = data["Devengados"]

        Basico = Deven["Basico"]
        if "Transporte" in Deven:
            Transporte = Deven["Transporte"]
        if "HEDs" in Deven:
            HEDs = Deven["HEDs"]
        if "HENs" in Deven:
            HENs = Deven["HENs"]
        if "HRNs" in Deven:
            HRNs = Deven["HRNs"]
        if "HEDDFs" in Deven:
            HEDDFs = Deven["HEDDFs"]
        if "HRDDFs" in Deven:
            HRDDFs = Deven["HRDDFs"]
        if "HENDFs" in Deven:
            HENDFs = Deven["HENDFs"]
        if "HRNDFs" in Deven:
            HRNDFs = Deven["HRNDFs"]
        if "Vacaciones" in Deven:
            Vacaciones = Deven["Vacaciones"]
        if "VacacionesComunes" in Vacaciones:
            VacacionesComunes = Vacaciones["VacacionesComunes"]
        if "VacacionesCompensadas" in Vacaciones:
            VacacionesCompensadas = Vacaciones["VacacionesCompensadas"]
        if "Primas" in Deven:
            Primas = Deven["Primas"]
        if "Cesantias" in Deven:
            Cesantias = Deven["Cesantias"]
        if "Incapacidades" in Deven:
            Incapacidades = Deven["Incapacidades"]
        if "Licencias" in Deven:
            Licencias = Deven["Licencias"]
        if "LicenciaMP" in Licencias:
            LicenciaMP = Licencias["LicenciaMP"]
        if "LicenciaR" in Licencias:
            LicenciaR = Licencias["LicenciaR"]
        if "LicenciaNR" in Licencias:
            LicenciaNR = Licencias["LicenciaNR"]
        if "Bonificaciones" in Deven:
            Bonificaciones = Deven["Bonificaciones"]
        if "Auxilios" in Deven:
            Auxilios = Deven["Auxilios"]
        if "OtrosConceptos" in Deven:
            OtrosConceptos = Deven["OtrosConceptos"]
        if "Compensaciones" in Deven:
            Compensaciones = Deven["Compensaciones"]
        if "BonoEPCTVs" in Deven:
            BonoEPCTVs = Deven["BonoEPCTVs"]
        if "Comisiones" in Deven:
            Comisiones = Deven["Comisiones"]
        if "PagosTerceros" in Deven:
            PagosTerceros = Deven["PagosTerceros"]
        if "Anticipos" in Deven:
            Anticipos = Deven["Anticipos"]
        if "Dotacion" in Deven:
            Dotacion = Deven["Dotacion"]
        if "ApoyoSost" in Deven:
            ApoyoSost = Deven["ApoyoSost"]
        if "Teletrabajo" in Deven:
            Teletrabajo = Deven["Teletrabajo"]
        if "BonifRetiro" in Deven:
            BonifRetiro = Deven["BonifRetiro"]
        if "Indemnizacion" in Deven:
            Indemnizacion = Deven["Indemnizacion"]
        if "Reintegro" in Deven:
            Reintegro = Deven["Reintegro"]
        if "Deducciones" in data:
            Deducciones = data["Deducciones"]
        if "Salud" in Deducciones:
            Salud = Deducciones["Salud"]
        if "FondoPension" in Deducciones:
            FondoPension = Deducciones["FondoPension"]
        if "FondoSP" in Deducciones:
            FondoSP = Deducciones["FondoSP"]
        if "Transporte" in Deducciones:
            Sindicatos = Deducciones["Sindicatos"]
        if "Sanciones" in Deducciones:
            Sanciones = Deducciones["Sanciones"]
        if "Libranzas" in Deducciones:
            Libranzas = Deducciones["Libranzas"]
        if "PagoTerceros" in Deducciones:
            PagosTercerosD = Deducciones["PagoTerceros"]
        if "Anticipos" in Deducciones:
            AnticiposD = Deducciones["Anticipos"]
        if "OtrasDeducciones" in Deducciones:
            OtrasDeducciones = Deducciones["OtrasDeducciones"]
        if "ensionVoluntaria" in Deducciones:
            PensionVoluntaria = Deducciones["PensionVoluntaria"]
        if "RetencionFuente" in Deducciones:
            RetencionFuente = Deducciones["RetencionFuente"]
        if "AFC" in Deducciones:
            AFC = Deducciones["AFC"]
        if "Cooperativa" in Deducciones:
            Cooperativa = Deducciones["Cooperativa"]
        if "EmbargoFiscal" in Deducciones:
            EmbargoFiscal = Deducciones["EmbargoFiscal"]
        if "PlanComplementarios" in Deducciones:
            PlanComplementarios = Deducciones["PlanComplementarios"]
        if "Educacion" in Deducciones:
            Educacion = Deducciones["Educacion"]
        if "Reintegro" in Deducciones:
            ReintegroD = Deducciones["Reintegro"]
        if "Deuda" in Deducciones:
            Deuda = Deducciones["Deuda"]
        DevengadosTotal = data["DevengadosTotal"]
        DeduccionesTotal = data["DeduccionesTotal"]
        ComprobanteTotal = data["ComprobanteTotal"]

        CUNE = InformacionGeneral['CUNE']
        if InformacionGeneral['CUNE'] == '':
            if TipoNota == "":
                CUNE = (Numero + FechaNE + HoraNE + DevengadosTotal + DeduccionesTotal + ComprobanteTotal + Nit +
                        DocEmp + "102" + Pin + TipoAmb)
                h = hashlib.sha384()
                h.update(CUNE.encode('utf-8'))
                CUNE = h.hexdigest()

            else:
                if TipoNota != "1":
                    DevengadosTotal = "0.00"
                    DeduccionesTotal = "0.00"
                    ComprobanteTotal = "0.00"
                    DocEmp = "0"

                CUNE = (Numero + FechaNE + HoraNE + DevengadosTotal + DeduccionesTotal + ComprobanteTotal + Nit +
                        DocEmp + "103" + Pin + TipoAmb)
                h = hashlib.sha384()
                h.update(CUNE.encode('utf-8'))
                CUNE = h.hexdigest()

            InformacionGeneral["CUNE"] = CUNE
        SoftwareSecurityCode = (SoftwareId + Pin + Numero)
        s = hashlib.sha384()
        s.update(SoftwareSecurityCode.encode('utf-8'))
        SoftwareSecurityCode = s.hexdigest()
        if TipoAmb == "1":
            QRCode = "https://catalogo-vpfe.dian.gov.co/document/searchqr?documentkey="+CUNE
        else:
            QRCode = "https://catalogo-vpfe-hab.dian.gov.co/document/searchqr?documentkey="+CUNE

        if TipoNota == "":
            Plane = '<NominaIndividual xmlns="dian:gov:co:facturaelectronica:NominaIndividual"\
                    xmlns:xs="http://www.w3.org/2001/XMLSchema-instance"\
                    xmlns:ds="http://www.w3.org/2000/09/xmldsig#"\
                    xmlns:ext="urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2"\
                    xmlns:xades="http://uri.etsi.org/01903/v1.3.2#"\
                    xmlns:xades141="http://uri.etsi.org/01903/v1.4.1#"\
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" \
                    SchemaLocation=""\
                    xsi:schemaLocation="dian:gov:co:facturaelectronica:NominaIndividual ' \
                    'NominaIndividualElectronicaXSD.xsd">'

            Plane += '<ext:UBLExtensions>' \
                     '<ext:UBLExtension>' \
                     '<ext:ExtensionContent>' \
                     '</ext:ExtensionContent>' \
                     '</ext:UBLExtension>' \
                     '</ext:UBLExtensions>'

        else:
            Plane = '<NominaIndividualDeAjuste xmlns="dian:gov:co:facturaelectronica:NominaIndividualDeAjuste"\
                xmlns:xs = "http://www.w3.org/2001/XMLSchema-instance"\
                xmlns:ds = "http://www.w3.org/2000/09/xmldsig#"\
                xmlns:ext = "urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2"\
                xmlns:xades = "http://uri.etsi.org/01903/v1.3.2#"\
                xmlns:xades141 = "http://uri.etsi.org/01903/v1.4.1#"\
                xmlns:xsi = "http://www.w3.org/2001/XMLSchema-instance"\
                SchemaLocation = ""\
                xsi:schemaLocation = "dian:gov:co:facturaelectronica:NominaIndividualDeAjuste ' \
                'NominaIndividualDeAjusteElectronicaXSD.xsd">'

            Plane += '<ext:UBLExtensions>' \
                     '<ext:UBLExtension>' \
                     '<ext:ExtensionContent>' \
                     '</ext:ExtensionContent>' \
                     '</ext:UBLExtension>' \
                     '</ext:UBLExtensions>'

            if TipoNota == "1":
                Plane += '<TipoNota>1</TipoNota>'

            else:
                Plane += '<TipoNota>2</TipoNota>'

        if TipoNota == "1":
            Plane += '<Reemplazar>' \
                     '<ReemplazandoPredecesor NumeroPred = "' + NumeroDocPredecesor + \
                     '" CUNEPred = "' + CUNEPredecesor + '" FechaGenPred = "' + FechaGenPredecesor + '"/>'

        else:
            if TipoNota == "2":
                Plane += '<Eliminar>' \
                         '<EliminandoPredecesor NumeroPred = "' + NumeroDocPredecesor + \
                         '" CUNEPred = "' + CUNEPredecesor + '" FechaGenPred = "' + FechaGenPredecesor + '"/>'

        if TipoNota != "2":
            Plane += '<Periodo FechaIngreso = "' + str(Periodo["FechaIngreso"]) + '" FechaLiquidacionInicio = "' + \
                     Periodo["FechaLiquidacionInicio"] + '" FechaLiquidacionFin = "' + \
                     Periodo["FechaLiquidacionFin"] + '" TiempoLaborado = "' + \
                     Periodo["TiempoLaborado"] + '" FechaGen = "' + InformacionGeneral["FechaGen"] + '"/>'

        Plane += '<NumeroSecuenciaXML Prefijo = "' + SecuenciaXML["Prefijo"] + '" Consecutivo = "' \
                 + SecuenciaXML["Consecutivo"] + '" Numero = "' + SecuenciaXML["Numero"] + '"/>' \
                '<LugarGeneracionXML Pais = "' + \
                 LugarGeneracionXML["Pais"] + '" DepartamentoEstado = "' + LugarGeneracionXML["DepartamentoEstado"] + \
                 '" MunicipioCiudad = "' + LugarGeneracionXML["MunicipioCiudad"] + '" Idioma = "' + \
                 LugarGeneracionXML["Idioma"] + '"/>' \
                '<ProveedorXML RazonSocial = "' + \
                 Empleador["RazonSocial"] + '" NIT = "' + Empleador["NIT"] + '" DV = "' + \
                 Empleador["DigitoVerificacion"] + '" SoftwareID = "' + InformacionGeneral["DianSoftwareId"] + \
                 '" SoftwareSC = "' + SoftwareSecurityCode + '"/>' \
                 '<CodigoQR>' + QRCode + '</CodigoQR>' \
                '<InformacionGeneral '
        if TipoNota == "":
            Plane += 'Version = "V1.0: Documento Soporte de Pago de Nómina Electrónica" '
        else:
            Plane += 'Version = "V1.0: Nota de Ajuste de Documento Soporte de Pago de Nómina Electrónica" '

        Plane += 'Ambiente = "' + InformacionGeneral["TipoAmbiente"] + '" TipoXML = "102" CUNE = "' + CUNE + '"\
                     EncripCUNE = "CUNE-SHA384" FechaGen = "' + InformacionGeneral["FechaGen"] + '" HoraGen = "' + \
                 InformacionGeneral["HoraGen"] + '" PeriodoNomina = "' + InformacionGeneral["PeriodoNomina"] + \
                 '" TipoMoneda = "' + InformacionGeneral["TipoMoneda"] + '" TRM = "' + \
                 InformacionGeneral["TRM"] + '"/>' \
                                             '<Notas>' + Notas["NotaPrueba"] + '</Notas>' \
                                                                               '<Empleador '
        if "RazonSocial" in Empleador:
            Plane += 'RazonSocial = "' + Empleador["RazonSocial"].replace("&", "y") + '" '
        if "OtrosNombres" in Empleador:
            Plane += 'OtrosNombres = "' + Empleador["OtrosNombres"].replace("&", "y") + '" '
        Plane += 'NIT = "' + Empleador["NIT"] + '" '
        if "DigitoVerificacion" in Empleador:
            Plane += 'DV = "' + Empleador["DigitoVerificacion"] + '" '
        Plane += 'Pais = "' + Empleador["Pais"] + '" DepartamentoEstado = "' + Empleador[
            "DepartamentoEstado"] + '" MunicipioCiudad = "' + Empleador["MunicipioCiudad"] + '" Direccion = "' + \
                 Empleador["Direccion"] + '"/>'

        PlaneT = ""
        PlaneT = '<Trabajador TipoTrabajador = "' + Trabajador["TipoTrabajador"] + '" SubTipoTrabajador = "' + \
                 Trabajador["SubTipoTrabajador"] + '" AltoRiesgoPension = "' + Trabajador["AltoRiesgoPension"] + \
                 '" TipoDocumento = "' + Trabajador["TipoDocumento"] + '" NumeroDocumento = "' + \
                 Trabajador["NumeroDocumento"] + '" PrimerApellido = "' + \
                 Trabajador["PrimerApellido"].replace("&", "y") + '" SegundoApellido = "' + \
                 Trabajador["SegundoApellido"].replace("&", "y") + '" PrimerNombre = "' + \
                 Trabajador["PrimerNombre"].replace("&", "y") + '" '
        if "OtrosNombres" in Trabajador:
            PlaneT += 'OtrosNombres = "' + Trabajador["OtrosNombres"].replace("&", "y") + '" '
        else:
            PlaneT += 'OtrosNombres = " " '

        PlaneT += 'LugarTrabajoPais = "' + Trabajador["LugarTrabajoPais"] + '" LugarTrabajoDepartamentoEstado = "' + \
                  Trabajador["LugarTrabajoDepartamentoEstado"] + '" LugarTrabajoMunicipioCiudad = "' + \
                  Trabajador["LugarTrabajoMunicipioCiudad"] + '" LugarTrabajoDireccion = "' + \
                  Trabajador["LugarTrabajoDireccion"] + '" SalarioIntegral = "' + Trabajador["SalarioIntegral"] + \
                  '" TipoContrato = "' + Trabajador["TipoContrato"] + '" Sueldo = "' + \
                  Trabajador["Sueldo"] + '" CodigoTrabajador = "' + Trabajador["CodigoTrabajador"] + '"/>' \
                  '<Pago Forma = "' + Pago["Forma"] + '" Metodo = "' + Pago["Metodo"] + '"'
        if 'Banco' in Pago:
            PlaneT += ' Banco = "' + Pago["Banco"] + '" '
        if 'TipoCuenta' in Pago:
            PlaneT += ' TipoCuenta = "' + Pago["TipoCuenta"] + '" '
        if 'NumeroCuenta' in Pago:
            PlaneT += ' NumeroCuenta = "' + Pago["NumeroCuenta"] + '" '
        PlaneT += '/>' \
                  '<FechasPagos>' \
                  '<FechaPago>' + FechasPagos["FechaPago"] + '</FechaPago>' \
                                                             '</FechasPagos>'
        PlaneT += '<Devengados>' \
                  '<Basico DiasTrabajados = "' + Basico["DiasTrabajados"] + '" SueldoTrabajado = "' + \
                  Basico["SueldoTrabajado"] + '"/>'
        if "Transporte" in Deven:
            PlaneT += '<Transporte '
            if "AuxilioTransporte" in Transporte:
                PlaneT += 'AuxilioTransporte = "' + Transporte["AuxilioTransporte"] + '" '
            if "ViaticoManutAlojS" in Transporte:
                PlaneT += 'ViaticoManuAlojS = "' + Transporte["ViaticoManutAlojS"] + '" '
            if "ViaticoManutAlojNS" in Transporte:
                PlaneT += 'ViaticoManutAlojNS = "' + Transporte["ViaticoManutAlojNS"] + '"'
            PlaneT += '/>'
        if "HEDs" in Deven:
            if len(HEDs) != 0:
                PlaneT += '<HEDs>'
                PlaneT += '<HED '
                for HED in HEDs:
                    if "Cantidad" in HED:
                        PlaneT += 'Cantidad = "' + HED["Cantidad"] + '" '
                    if "Porcentaje" in HED:
                        PlaneT += 'Porcentaje = "' + HED["Porcentaje"] + '" '
                    if "Pago" in HED:
                        PlaneT += 'Pago = "' + HED["Pago"] + '"'
                PlaneT += '/>'
                PlaneT += '</HEDs>'

        if "HENs" in Deven:
            if len(HENs) != 0:
                PlaneT += '<HENs>'
                PlaneT += '<HEN '
                for HEN in HENs:
                    if "Cantidad" in HEN:
                        PlaneT += 'Cantidad = "' + HEN["Cantidad"] + '" '
                    if "Porcentaje" in HEN:
                        PlaneT += 'Porcentaje = "' + HEN["Porcentaje"] + '" '
                    if "Pago" in HEN:
                        PlaneT += 'Pago = "' + HEN["Pago"] + '"'
                PlaneT += '/>'
                PlaneT += '</HENs>'

        if "HRNs" in Deven:
            if len(HRNs) != 0:
                PlaneT += '<HRNs>'
                PlaneT += '<HRN '
                for HRN in HRNs:
                    if "Cantidad" in HRN:
                        PlaneT += 'Cantidad = "' + HRN["Cantidad"] + '" '
                    if "Porcentaje" in HRN:
                        PlaneT += 'Porcentaje = "' + HRN["Porcentaje"] + '" '
                    if "Pago" in HRN:
                        PlaneT += 'Pago = "' + HRN["Pago"] + '"'
                PlaneT += '/>'
                PlaneT += '</HRNs>'

        if "HEDDFs" in Deven:
            if len(HEDDFs) != 0:
                PlaneT += '<HEDDFs>'
                PlaneT += '<HEDDF '
                for HEDDF in HEDDFs:
                    if "Cantidad" in HEDDF:
                        PlaneT += 'Cantidad = "' + HEDDF["Cantidad"] + '" '
                    if "Porcentaje" in HEDDF:
                        PlaneT += 'Porcentaje = "' + HEDDF["Porcentaje"] + '" '
                    if "Pago" in HEDDF:
                        PlaneT += 'Pago = "' + HEDDF["Pago"] + '"'
                PlaneT += '/>'
                PlaneT += '</HEDDFs>'

        if "HRDDFs" in Deven:
            if len(HRDDFs) != 0:
                PlaneT += '<HRDDFs>'
                PlaneT += '<HRDDF '
                for HRDDF in HRDDFs:
                    if "Cantidad" in HRDDF:
                        PlaneT += 'Cantidad = "' + HRDDF["Cantidad"] + '" '
                    if "Porcentaje" in HRDDF:
                        PlaneT += 'Porcentaje = "' + HRDDF["Porcentaje"] + '" '
                    if "Pago" in HRDDF:
                        PlaneT += 'Pago = "' + HRDDF["Pago"] + '"'
                PlaneT += '/>'
                PlaneT += '</HRDDFs>'

        if "HENDFs" in Deven:
            if len(HENDFs) != 0:
                PlaneT += '<HENDFs>'
                PlaneT += '<HENDF '
                for HENDF in HENDFs:
                    if "Cantidad" in HENDF:
                        PlaneT += 'Cantidad = "' + HENDF["Cantidad"] + '" '
                    if "Porcentaje" in HENDF:
                        PlaneT += 'Porcentaje = "' + HENDF["Porcentaje"] + '" '
                    if "Pago" in HENDF:
                        PlaneT += 'Pago = "' + HENDF["Pago"] + '"'
                PlaneT += '/>'
                PlaneT += '</HENDFs>'

        if "HRNDFs" in Deven:
            if len(HRNDFs) != 0:
                PlaneT += '<HRNDFs>'
                PlaneT += '<HRNDF '
                for HRNDF in HRNDFs:
                    if "Cantidad" in HRNDF:
                        PlaneT += 'Cantidad = "' + HRNDF["Cantidad"] + '" '
                    if "Porcentaje" in HRNDF:
                        PlaneT += 'Porcentaje = "' + HRNDF["Porcentaje"] + '" '
                    if "Pago" in HRNDF:
                        PlaneT += 'Pago = "' + HRNDF["Pago"] + '"'
                PlaneT += '/>'
                PlaneT += '</HRNDFs>'

        if "Vacaciones" in Deven:
            if len(Vacaciones) != 0:
                PlaneT += '<Vacaciones>'
                PlaneT += '<VacacionesComunes '
                for VaComunes in VacacionesComunes:
                    if "Cantidad" in VaComunes:
                        PlaneT += 'Cantidad = "' + VaComunes["Cantidad"] + '" '
                    if "Pago" in VaComunes:
                        'Pago = "' + VaComunes["Pago"] + '"'
                PlaneT += '/>'
                PlaneT += '<VacacionesCompensadas '
                for VaCompensadas in VacacionesCompensadas:
                    if "Cantidad" in VaCompensadas:
                        PlaneT += 'Cantidad = "' + VaCompensadas["Cantidad"] + '" '
                    if "Pago" in VaCompensadas:
                        'Pago = "' + VaCompensadas["Pago"] + '"'
                PlaneT += '/>'
                PlaneT += '</Vacaciones>'

        if "Primas" in Deven:
            PlaneT += '<Primas '
            if "Cantidad" in Primas:
                PlaneT += 'Cantidad = "' + Primas["Cantidad"] + '" '
            if "Pago" in Primas:
                PlaneT += 'Pago = "' + Primas["Pago"] + '" '
            if "PagoNS" in Primas:
                PlaneT += 'PagoNS = "' + Primas["PagoNS"] + '"'
            PlaneT += '/>'

        if "Cesantias" in Deven:
            PlaneT += '<Cesantias '
            if "Pago" in Cesantias:
                PlaneT += 'Pago = "' + Cesantias["Pago"] + '" '
            if "Porcentaje" in Cesantias:
                PlaneT += 'Porcentaje = "' + Cesantias["Porcentaje"] + '" '
            if "PagoIntereses" in Cesantias:
                PlaneT += 'PagoIntereses = "' + Cesantias["PagoIntereses"] + '"'
            PlaneT += '/>'

        if "Incapacidades" in Deven:
            if len(Incapacidades) != 0:
                PlaneT += '<Incapacidades>'
                PlaneT += '<Incapacidad '
                for Incapacidad in Incapacidades:
                    if "Cantidad" in Incapacidad:
                        PlaneT += 'Cantidad = "' + Incapacidad["Cantidad"] + '" '
                    if "Tipo" in Incapacidad:
                        PlaneT += 'Tipo = "' + Incapacidad["Tipo"] + '" '
                    if "Pago" in Incapacidad:
                        'Pago = "' + Incapacidad["Pago"] + '"'
                PlaneT += '/>'
                PlaneT += '</Incapacidades>'

        if "Licencias" in Deven:
            if len(Licencias) != 0:
                PlaneT += '<Licencias>'
                for LMP in LicenciaMP:
                    PlaneT += '<LicenciaMP Cantidad = "' + LMP["Cantidad"] + '" Pago = "' + LMP["Pago"] + '"/>'
                for LR in LicenciaR:
                    PlaneT += '<LicenciaR Cantidad = "' + LR["Cantidad"] + '" Pago = "' + LR["Pago"] + '"/>'
                for LNR in LicenciaNR:
                    PlaneT += '<LicenciaNR FechaInicio = "' + LNR["FechaInicio"] + '" FechaFin = "' + \
                              LNR["FechaFin"] + '" Cantidad = "' + LNR["Cantidad"] + '"/>'
                PlaneT += '</Licencias>'

        if "Bonificaciones" in Deven:
            if len(Bonificaciones) != 0:
                PlaneT += '<Bonificaciones>'
                PlaneT += '<Bonificacion '
                for Bonificacion in Bonificaciones:
                    if "BonificacionS" in Bonificacion:
                        PlaneT += 'BonificacionS = "' + Bonificacion["BonificacionS"] + '" '
                    if "BonificacionNS" in Bonificacion:
                        PlaneT += 'BonificacionNS = "' + Bonificacion["BonificacionNS"] + '" '
                PlaneT += '/>'
                PlaneT += '</Bonificaciones>'

        if "Auxilios" in Deven:
            if len(Auxilios) != 0:
                PlaneT += '<Auxilios>'
                PlaneT += '<Auxilio '
                for Auxilio in Auxilios:
                    if "AuxilioS" in Auxilio:
                        PlaneT += 'AuxilioS = "' + Auxilio["AuxilioS"] + '" '
                    if "AuxilioNS" in Auxilio:
                        PlaneT += 'AuxilioNS = "' + Auxilio["AuxilioNS"] + '" '
                PlaneT += '/>'
                PlaneT += '</Auxilios>'

        if "OtrosConceptos" in Deven:
            if len(OtrosConceptos) != 0:
                PlaneT += '<OtrosConceptos>'
                PlaneT += '<OtroConcepto '
                for OtroConcepto in OtrosConceptos:
                    if "DescripcionConcepto" in OtroConcepto:
                        PlaneT += 'DescripcionConcepto = "' + OtroConcepto["DescripcionConcepto"] + '" '
                    if "ConceptoS" in OtroConcepto:
                        PlaneT += 'ConceptoS = "' + OtroConcepto["ConceptoS"] + '" '
                    if "ConceptoNS" in OtroConcepto:
                        'ConceptoNS = "' + OtroConcepto["ConceptoNS"] + '"/>'
                PlaneT += '/>'
                PlaneT += '</OtrosConceptos>'

        if "Compensaciones" in Deven:
            if len(Compensaciones) != 0:
                PlaneT += '<Compensaciones>'
                PlaneT += '<Compensacion '
                for Compensacion in Compensaciones:
                    if "CompensacionE" in Compensacion:
                        PlaneT += 'CompensacionE = "' + Compensacion["CompensacionE"] + '" '
                    if "CompensacionO" in Compensacion:
                        PlaneT += 'CompensacionO = "' + Compensacion["CompensacionO"] + '" '
                PlaneT += '/>'
                PlaneT += '</Compensaciones>'

        if "BonoEPCTVs" in Deven:
            if len(BonoEPCTVs) != 0:
                PlaneT += '<BonoEPCTVs>'
                PlaneT += '<BonoEPCTV '
                for BonoEPCTV in BonoEPCTVs:
                    if "PagoS" in BonoEPCTV:
                        PlaneT += 'PagoS = "' + BonoEPCTV["PagoS"] + '" '
                    if "PagoNS" in BonoEPCTV:
                        PlaneT += 'PagoNS = "' + BonoEPCTV["PagoNS"] + '" '
                    if "PagoAlimentacionS" in BonoEPCTV:
                        PlaneT += 'PagoAlimentacionS = "' + BonoEPCTV["PagoAlimentacionS"] + '" '
                    if "PagoAlimentacionNS" in BonoEPCTV:
                        PlaneT += 'PagoAlimentacionNS = "' + BonoEPCTV["PagoAlimentacionNS"] + '" '
                PlaneT += '/>'
                PlaneT += '</BonoEPCTVs>'

        if "Comisiones" in Deven:
            if len(Comisiones) != 0:
                PlaneT += '<Comisiones>'
                PlaneT += '<Comision '
                for Comision in Comisiones:
                    if "Comision" in Comision:
                        PlaneT += 'Comision = "' + Comision["Comision"] + '" '
                PlaneT += '/>'
                PlaneT += '</Comisiones>'

        if "PagosTerceros" in Deven:
            if len(PagosTerceros) != 0:
                PlaneT += '<PagosTerceros>'
                for PagosTercero in PagosTerceros:
                    PlaneT += '<PagoTercero>' + PagosTercero["PagoTercero"] + '</PagoTercero>'
                PlaneT += '</PagosTerceros>'

        if "Anticipos" in Deven:
            if len(Anticipos) != 0:
                PlaneT += '<Anticipos>'
                PlaneT += '<Anticipo '
                for Anticipo in Anticipos:
                    if "Anticipo" in Anticipo:
                        PlaneT += 'Anticipo = "' + Anticipo["Anticipo"] + '" '
                PlaneT += '/>'
                PlaneT += '</Anticipos>'
        if Dotacion != "":
            PlaneT += '<Dotacion>' + Dotacion + '</Dotacion>'
        if ApoyoSost != "":
            PlaneT += '<ApoyoSost>' + ApoyoSost + '</ApoyoSost>'
        if Teletrabajo != "":
            PlaneT += '<Teletrabajo>' + Teletrabajo + '</Teletrabajo>'
        if BonifRetiro != "":
            PlaneT += '<BonifRetiro>' + BonifRetiro + '</BonifRetiro>'
        if Indemnizacion != "":
            PlaneT += '<Indemnizacion>' + Indemnizacion + '</Indemnizacion>'
        if Reintegro != "":
            PlaneT += '<Reintegro>' + Reintegro + '</Reintegro>'
        PlaneT += '</Devengados>'
        PlaneT += '<Deducciones>'
        if "Salud" in Deducciones:
            PlaneT += '<Salud Porcentaje = "' + Salud["Porcentaje"] + '" Deduccion = "' + Salud["Deduccion"] + '"/>'
        if "FondoPension" in Deducciones:
            PlaneT += '<FondoPension Porcentaje = "' + FondoPension["Porcentaje"] + '" Deduccion = "' + \
                      FondoPension["Deduccion"] + '"/>'
        if "FondoSP" in Deducciones:
            PlaneT += '<FondoSP Porcentaje = "' + FondoSP["Porcentaje"] + '" Deduccion = "' + FondoSP[
                "Deduccion"] + '" PorcentajeSub = "' + FondoSP["PorcentajeSub"] + '" DeduccionSub = "' + \
                      FondoSP["DeduccionSub"] + '"/>' \

        if "Sindicatos" in Deducciones:
                if len(Sindicatos) != 0:
                    PlaneT += '<Sindicatos>'
                    for Sindicato in Sindicatos:
                        PlaneT += '<Sindicato Porcentaje = "' + Sindicato["Porcentaje"] + '" Deduccion = "' + \
                                  Sindicato["Deduccion"] + '"/>'
                    PlaneT += '</Sindicatos>'

        if "Sanciones" in Deducciones:
            if len(Sanciones) != 0:
                PlaneT += '<Sanciones>'
                PlaneT += '<Sancion '
                for Sancion in Sanciones:
                    if "SancionPublic" in Sancion:
                        PlaneT += 'SancionPublic = "' + Sancion["SancionPublic"] + '" '
                    if "SancionPriv" in Sancion:
                        PlaneT += 'SancionPriv = "' + Sancion["SancionPriv"] + '"'
                PlaneT += '/>'
                PlaneT += '</Sanciones>'

        if "Libranzas" in Deducciones:
            if len(Libranzas) != 0:
                PlaneT += '<Libranzas>'
                for Libranza in Libranzas:
                    PlaneT += '<Libranza Descripcion = "' + Libranza["Descripcion"] + '" Deduccion = "' + \
                              Libranza["Deduccion"] + '"/>'
                PlaneT += '</Libranzas>'

        if "PagosTercerosD" in Deducciones:
            if len(PagosTercerosD) != 0:
                PlaneT += '<PagosTerceros>'
                for PagoTercero in PagosTercerosD:
                    PlaneT += '<PagoTercero>' + PagoTercero["PagoTercero"] + '</PagoTercero>'
                PlaneT += '</PagosTerceros>'

        if "AnticiposD" in Deducciones:
            if len(AnticiposD) != 0:
                PlaneT += '<Anticipos>'
                for Anticipo in AnticiposD:
                    PlaneT += '<Anticipo>' + Anticipo["Anticipo"] + '</Anticipo>'
                PlaneT += '</Anticipos>'

        if "OtrasDeducciones" in Deducciones:
            if len(OtrasDeducciones) != 0:
                PlaneT += '<OtrasDeducciones>'
                for OtraDeduccion in OtrasDeducciones:
                    PlaneT += '<OtraDeduccion>' + OtraDeduccion["OtraDeduccion"] + '</OtraDeduccion>'
                PlaneT += '</OtrasDeducciones>'

        if PensionVoluntaria != "":
            PlaneT += '<PensionVoluntaria>' + PensionVoluntaria + '</PensionVoluntaria>'
        if RetencionFuente != "":
            PlaneT += '<RetencionFuente>' + RetencionFuente + '</RetencionFuente>'
        if AFC != "":
            PlaneT += '<AFC>' + AFC + '</AFC>'
        if Cooperativa != "":
            PlaneT += '<Cooperativa>' + Cooperativa + '</Cooperativa>'
        if EmbargoFiscal != "":
            PlaneT += '<EmbargoFiscal>' + EmbargoFiscal + '</EmbargoFiscal>'
        if PlanComplementarios != "":
            PlaneT += '<PlanComplementarios>' + PlanComplementarios + '</PlanComplementarios>'
        if Educacion != "":
            PlaneT += '<Educacion>' + Educacion + '</Educacion>'
        if ReintegroD != "":
            PlaneT += '<Reintegro>' + ReintegroD + '</Reintegro>'
        if Deuda != "":
            PlaneT += '<Deuda>' + Deuda + '</Deuda>'
        PlaneT += '</Deducciones>' \
                  '<DevengadosTotal>' + DevengadosTotal + '</DevengadosTotal>' \
                  '<DeduccionesTotal>' + DeduccionesTotal + '</DeduccionesTotal>' \
                  '<ComprobanteTotal>' + ComprobanteTotal + '</ComprobanteTotal>'

        if TipoNota == "1":
            Plane += PlaneT + '</Reemplazar>'

        if TipoNota == "2":
            Plane += '</Eliminar>'

        if TipoNota == "":
            Plane += PlaneT + '</NominaIndividual>'
        else:
            Plane += '</NominaIndividualDeAjuste>'

        return Plane

    @staticmethod
    def create_xml_payroll_notes(data: dict):
        Plane = ""
        Transporte = []
        HEDs = []
        HENs = []
        HRNs = []
        HEDDFs = []
        HRDDFs = []
        HENDFs = []
        HRNDFs = []
        Vacaciones = []
        VacacionesComunes = []
        VacacionesCompensadas = []
        Primas = {}
        Cesantias = {}
        Incapacidades = []
        Licencias = {}
        LicenciaMP = []
        LicenciaR = []
        LicenciaNR = []
        Bonificaciones = []
        Auxilios = []
        OtrosConceptos = []
        Compensaciones = []
        BonoEPCTVs = []
        Comisiones = []
        PagosTerceros = []
        Anticipos = ""
        Dotacion = ""
        ApoyoSost = ""
        Teletrabajo = ""
        BonifRetiro = ""
        Indemnizacion = ""
        Reintegro = ""
        Deducciones = data["Deducciones"]
        Salud = {}
        FondoPension = {}
        FondoSP = {}
        Sindicatos = []
        Sanciones = []
        Libranzas = []
        PagosTercerosD = []
        AnticiposD = []
        OtrasDeducciones = []
        PensionVoluntaria = ""
        RetencionFuente = ""
        AFC = ""
        Cooperativa = ""
        EmbargoFiscal = ""
        PlanComplementarios = ""
        Educacion = ""
        ReintegroD = ""
        Deuda = ""
        TipoNota = ""
        NumeroDocPredecesor = ""
        FechaGenPredecesor = ""
        CUNEPredecesor = ""

        Periodo = data["Periodo"]
        FechasPagos = data["FechasPagos"]
        SecuenciaXML = data["NumeroSecuenciaXML"]
        Numero = SecuenciaXML["Numero"]
        LugarGeneracionXML = data["LugarGeneracionXML"]
        InformacionGeneral = data["InformacionGeneralNotas"]
        if "TipoNota" in InformacionGeneral:
            TipoNota = InformacionGeneral["TipoNota"]
        if "NumeroDocumentoPredecesor" in InformacionGeneral:
            NumeroDocPredecesor = InformacionGeneral["NumeroDocumentoPredecesor"]

        if "FechaGenPredecesor" in InformacionGeneral:
            FechaGenPredecesor = InformacionGeneral["FechaGenPredecesor"]

        if "CUNEPredecesor" in InformacionGeneral:
            CUNEPredecesor = InformacionGeneral["CUNEPredecesor"]
        Empleador = data["Empleador"]
        Nit = Empleador["NIT"]
        Pin = InformacionGeneral["DianPin"]
        FechaNE = InformacionGeneral["FechaGen"]
        HoraNE = InformacionGeneral["HoraGen"]
        TipoAmb = InformacionGeneral["TipoAmbiente"]
        SoftwareId = InformacionGeneral["DianSoftwareId"]
        Notas = data["Notas"]
        Trabajador = data["Trabajador"]
        DocEmp = Trabajador["NumeroDocumento"]
        Pago = data["Pago"]
        Deven = data["Devengados"]

        Basico = Deven["Basico"]
        if "Transporte" in Deven:
            Transporte = Deven["Transporte"]
        if "HEDs" in Deven:
            HEDs = Deven["HEDs"]
        if "HENs" in Deven:
            HENs = Deven["HENs"]
        if "HRNs" in Deven:
            HRNs = Deven["HRNs"]
        if "HEDDFs" in Deven:
            HEDDFs = Deven["HEDDFs"]
        if "HRDDFs" in Deven:
            HRDDFs = Deven["HRDDFs"]
        if "HENDFs" in Deven:
            HENDFs = Deven["HENDFs"]
        if "HRNDFs" in Deven:
            HRNDFs = Deven["HRNDFs"]
        if "Vacaciones" in Deven:
            Vacaciones = Deven["Vacaciones"]
        if "VacacionesComunes" in Vacaciones:
            VacacionesComunes = Vacaciones["VacacionesComunes"]
        if "VacacionesCompensadas" in Vacaciones:
            VacacionesCompensadas = Vacaciones["VacacionesCompensadas"]
        if "Primas" in Deven:
            Primas = Deven["Primas"]
        if "Cesantias" in Deven:
            Cesantias = Deven["Cesantias"]
        if "Incapacidades" in Deven:
            Incapacidades = Deven["Incapacidades"]
        if "Licencias" in Deven:
            Licencias = Deven["Licencias"]
        if "LicenciaMP" in Licencias:
            LicenciaMP = Licencias["LicenciaMP"]
        if "LicenciaR" in Licencias:
            LicenciaR = Licencias["LicenciaR"]
        if "LicenciaNR" in Licencias:
            LicenciaNR = Licencias["LicenciaNR"]
        if "Bonificaciones" in Deven:
            Bonificaciones = Deven["Bonificaciones"]
        if "Auxilios" in Deven:
            Auxilios = Deven["Auxilios"]
        if "OtrosConceptos" in Deven:
            OtrosConceptos = Deven["OtrosConceptos"]
        if "Compensaciones" in Deven:
            Compensaciones = Deven["Compensaciones"]
        if "BonoEPCTVs" in Deven:
            BonoEPCTVs = Deven["BonoEPCTVs"]
        if "Comisiones" in Deven:
            Comisiones = Deven["Comisiones"]
        if "PagosTerceros" in Deven:
            PagosTerceros = Deven["PagosTerceros"]
        if "Anticipos" in Deven:
            Anticipos = Deven["Anticipos"]
        if "Dotacion" in Deven:
            Dotacion = Deven["Dotacion"]
        if "ApoyoSost" in Deven:
            ApoyoSost = Deven["ApoyoSost"]
        if "Teletrabajo" in Deven:
            Teletrabajo = Deven["Teletrabajo"]
        if "BonifRetiro" in Deven:
            BonifRetiro = Deven["BonifRetiro"]
        if "Indemnizacion" in Deven:
            Indemnizacion = Deven["Indemnizacion"]
        if "Reintegro" in Deven:
            Reintegro = Deven["Reintegro"]
        if "Deducciones" in data:
            Deducciones = data["Deducciones"]
        if "Salud" in Deducciones:
            Salud = Deducciones["Salud"]
        if "FondoPension" in Deducciones:
            FondoPension = Deducciones["FondoPension"]
        if "FondoSP" in Deducciones:
            FondoSP = Deducciones["FondoSP"]
        if "Transporte" in Deducciones:
            Sindicatos = Deducciones["Sindicatos"]
        if "Sanciones" in Deducciones:
            Sanciones = Deducciones["Sanciones"]
        if "Libranzas" in Deducciones:
            Libranzas = Deducciones["Libranzas"]
        if "PagoTerceros" in Deducciones:
            PagosTercerosD = Deducciones["PagoTerceros"]
        if "Anticipos" in Deducciones:
            AnticiposD = Deducciones["Anticipos"]
        if "OtrasDeducciones" in Deducciones:
            OtrasDeducciones = Deducciones["OtrasDeducciones"]
        if "ensionVoluntaria" in Deducciones:
            PensionVoluntaria = Deducciones["PensionVoluntaria"]
        if "RetencionFuente" in Deducciones:
            RetencionFuente = Deducciones["RetencionFuente"]
        if "AFC" in Deducciones:
            AFC = Deducciones["AFC"]
        if "Cooperativa" in Deducciones:
            Cooperativa = Deducciones["Cooperativa"]
        if "EmbargoFiscal" in Deducciones:
            EmbargoFiscal = Deducciones["EmbargoFiscal"]
        if "PlanComplementarios" in Deducciones:
            PlanComplementarios = Deducciones["PlanComplementarios"]
        if "Educacion" in Deducciones:
            Educacion = Deducciones["Educacion"]
        if "Reintegro" in Deducciones:
            ReintegroD = Deducciones["Reintegro"]
        if "Deuda" in Deducciones:
            Deuda = Deducciones["Deuda"]
        DevengadosTotal = data["DevengadosTotal"]
        DeduccionesTotal = data["DeduccionesTotal"]
        ComprobanteTotal = data["ComprobanteTotal"]

        CUNE = InformacionGeneral['CUNE']
        if InformacionGeneral['CUNE'] == '':
            if TipoNota == "":
                CUNE = (Numero + FechaNE + HoraNE + DevengadosTotal + DeduccionesTotal + ComprobanteTotal + Nit +
                        DocEmp + "102" + Pin + TipoAmb)
                h = hashlib.sha384()
                h.update(CUNE.encode('utf-8'))
                CUNE = h.hexdigest()

            else:
                if TipoNota != "1":
                    DevengadosTotal = "0.00"
                    DeduccionesTotal = "0.00"
                    ComprobanteTotal = "0.00"
                    DocEmp = "0"

                CUNE = (Numero + FechaNE + HoraNE + DevengadosTotal + DeduccionesTotal + ComprobanteTotal + Nit +
                            DocEmp + "103" + Pin + TipoAmb)
                h = hashlib.sha384()
                h.update(CUNE.encode('utf-8'))
                CUNE = h.hexdigest()

            InformacionGeneral["CUNE"] = CUNE
        SoftwareSecurityCode = (SoftwareId + Pin + Numero)
        s = hashlib.sha384()
        s.update(SoftwareSecurityCode.encode('utf-8'))
        SoftwareSecurityCode = s.hexdigest()
        if TipoAmb == "1":
            QRCode = "https://catalogo-vpfe.dian.gov.co/document/searchqr?documentkey="+CUNE
        else:
            QRCode = "https://catalogo-vpfe-hab.dian.gov.co/document/searchqr?documentkey="+CUNE

        if TipoNota == "":
            Plane = '<NominaIndividual xmlns="dian:gov:co:facturaelectronica:NominaIndividual"\
                        xmlns:xs="http://www.w3.org/2001/XMLSchema-instance"\
                        xmlns:ds="http://www.w3.org/2000/09/xmldsig#"\
                        xmlns:ext="urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2"\
                        xmlns:xades="http://uri.etsi.org/01903/v1.3.2#"\
                        xmlns:xades141="http://uri.etsi.org/01903/v1.4.1#"\
                        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" \
                        SchemaLocation=""\
                        xsi:schemaLocation="dian:gov:co:facturaelectronica:NominaIndividual ' \
                    'NominaIndividualElectronicaXSD.xsd">'

            Plane += '<ext:UBLExtensions>' \
                     '<ext:UBLExtension>' \
                     '<ext:ExtensionContent>' \
                     '</ext:ExtensionContent>' \
                     '</ext:UBLExtension>' \
                     '</ext:UBLExtensions>'

        else:
            Plane = '<NominaIndividualDeAjuste xmlns="dian:gov:co:facturaelectronica:NominaIndividualDeAjuste"\
                    xmlns:xs = "http://www.w3.org/2001/XMLSchema-instance"\
                    xmlns:ds = "http://www.w3.org/2000/09/xmldsig#"\
                    xmlns:ext = "urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2"\
                    xmlns:xades = "http://uri.etsi.org/01903/v1.3.2#"\
                    xmlns:xades141 = "http://uri.etsi.org/01903/v1.4.1#"\
                    xmlns:xsi = "http://www.w3.org/2001/XMLSchema-instance"\
                    SchemaLocation = ""\
                    xsi:schemaLocation = "dian:gov:co:facturaelectronica:NominaIndividualDeAjuste ' \
                    'NominaIndividualDeAjusteElectronicaXSD.xsd">'

            Plane += '<ext:UBLExtensions>' \
                     '<ext:UBLExtension>' \
                     '<ext:ExtensionContent>' \
                     '</ext:ExtensionContent>' \
                     '</ext:UBLExtension>' \
                     '</ext:UBLExtensions>'

            if TipoNota == "1":
                Plane += '<TipoNota>1</TipoNota>'

            else:
                Plane += '<TipoNota>2</TipoNota>'

        if TipoNota == "1":
            Plane += '<Reemplazar>' \
                     '<ReemplazandoPredecesor NumeroPred = "' + NumeroDocPredecesor + \
                     '" CUNEPred = "' + CUNEPredecesor + '" FechaGenPred = "' + FechaGenPredecesor + '"/>'

        else:
            if TipoNota == "2":
                Plane += '<Eliminar>' \
                         '<EliminandoPredecesor NumeroPred = "' + NumeroDocPredecesor + \
                         '" CUNEPred = "' + CUNEPredecesor + '" FechaGenPred = "' + FechaGenPredecesor + '"/>'

        if TipoNota != "2":
            Plane += '<Periodo FechaIngreso = "' + str(Periodo["FechaIngreso"]) + '" FechaLiquidacionInicio = "' + \
                     Periodo["FechaLiquidacionInicio"] + '" FechaLiquidacionFin = "' + \
                     Periodo["FechaLiquidacionFin"] + '" TiempoLaborado = "' + Periodo["TiempoLaborado"] + \
                     '" FechaGen = "' + InformacionGeneral["FechaGen"] + '"/>'

        Plane += '<NumeroSecuenciaXML Prefijo = "' + SecuenciaXML["Prefijo"] + '" Consecutivo = "' + \
                 SecuenciaXML["Consecutivo"] + '" Numero = "' + SecuenciaXML["Numero"] + '"/>' \
                 '<LugarGeneracionXML Pais = "' + LugarGeneracionXML["Pais"] + '" DepartamentoEstado = "' + \
                 LugarGeneracionXML["DepartamentoEstado"] + '" MunicipioCiudad = "' + \
                 LugarGeneracionXML["MunicipioCiudad"] + '" Idioma = "' + LugarGeneracionXML["Idioma"] + '"/>' \
                 '<ProveedorXML RazonSocial = "' + Empleador["RazonSocial"] + '" NIT = "' + Empleador["NIT"] + \
                 '" DV = "' + Empleador["DigitoVerificacion"] + '" SoftwareID = "' + \
                 InformacionGeneral["DianSoftwareId"] + '" SoftwareSC = "' + SoftwareSecurityCode + '"/>' \
                 '<CodigoQR>' + QRCode + '</CodigoQR>' \
                 '<InformacionGeneral '
        if TipoNota == "":
            Plane += 'Version = "V1.0: Documento Soporte de Pago de Nómina Electrónica" '
        else:
            Plane += 'Version = "V1.0: Nota de Ajuste de Documento Soporte de Pago de Nómina Electrónica" '

        Plane += 'Ambiente = "' + InformacionGeneral["TipoAmbiente"] + '" TipoXML = "103" CUNE = "' + CUNE + '"\
                         EncripCUNE = "CUNE-SHA384" FechaGen = "' + InformacionGeneral["FechaGen"] + '" HoraGen = "' + \
                 InformacionGeneral["HoraGen"] + '" '
        if InformacionGeneral["TipoNota"] == "1":
            Plane += 'PeriodoNomina = "' + InformacionGeneral["PeriodoNomina"] + '" '
            Plane += 'TipoMoneda = "' + InformacionGeneral["TipoMoneda"] + '" '
            Plane += 'TRM = "' + InformacionGeneral["TRM"] + '"'
        Plane += '/>' \
                 '<Notas>' + Notas["NotaPrueba"] + '</Notas>' \
                                                   '<Empleador '
        if "RazonSocial" in Empleador:
            Plane += 'RazonSocial = "' + Empleador["RazonSocial"].replace("&", "y") + '" '
        if "OtrosNombres" in Empleador:
            Plane += 'OtrosNombres = "' + Empleador["OtrosNombres"].replace("&", "y") + '" '
        Plane += 'NIT = "' + Empleador["NIT"] + '" '
        if "DigitoVerificacion" in Empleador:
            Plane += 'DV = "' + Empleador["DigitoVerificacion"] + '" '
        Plane += 'Pais = "' + Empleador["Pais"] + '" DepartamentoEstado = "' + Empleador[
            "DepartamentoEstado"] + '" MunicipioCiudad = "' + Empleador["MunicipioCiudad"] + '" Direccion = "' + \
                 Empleador["Direccion"] + '"/>'

        PlaneT = ""
        PlaneT = '<Trabajador TipoTrabajador = "' + Trabajador["TipoTrabajador"] + '" SubTipoTrabajador = "' + \
                 Trabajador["SubTipoTrabajador"] + '" AltoRiesgoPension = "' + Trabajador["AltoRiesgoPension"] + \
                 '" TipoDocumento = "' + Trabajador["TipoDocumento"] + '" NumeroDocumento = "' + \
                 Trabajador["NumeroDocumento"] + '" PrimerApellido = "' + \
                 Trabajador["PrimerApellido"].replace("&", "y") + '" SegundoApellido = "' + \
                 Trabajador["SegundoApellido"].replace("&", "y") + '" PrimerNombre = "' + \
                 Trabajador["PrimerNombre"].replace("&", "y") + '" '
        if "OtrosNombres" in Trabajador:
            PlaneT += 'OtrosNombres = "' + Trabajador["OtrosNombres"].replace("&", "y") + '" '
        else:
            PlaneT += 'OtrosNombres = " " '

        PlaneT += 'LugarTrabajoPais = "' + Trabajador["LugarTrabajoPais"] + '" LugarTrabajoDepartamentoEstado = "' + \
                  Trabajador["LugarTrabajoDepartamentoEstado"] + '" LugarTrabajoMunicipioCiudad = "' + Trabajador[
                      "LugarTrabajoMunicipioCiudad"] + '" LugarTrabajoDireccion = "' + Trabajador[
                      "LugarTrabajoDireccion"] + '" SalarioIntegral = "' + Trabajador[
                      "SalarioIntegral"] + '" TipoContrato = "' + Trabajador["TipoContrato"] + '" Sueldo = "' + \
                  Trabajador["Sueldo"] + '" CodigoTrabajador = "' + Trabajador["CodigoTrabajador"] + '"/>' \
                  '<Pago Forma = "' + Pago["Forma"] + '" Metodo = "' + Pago["Metodo"] + '"/>' \
                  '<FechasPagos>' \
                  '<FechaPago>' + FechasPagos["FechaPago"] + '</FechaPago>' \
                                                             '</FechasPagos>'
        PlaneT += '<Devengados>' \
                  '<Basico DiasTrabajados = "' + Basico["DiasTrabajados"] + '" SueldoTrabajado = "' + \
                  Basico["SueldoTrabajado"] + '"/>'
        if "Transporte" in Deven:
            PlaneT += '<Transporte '
            if "AuxilioTransporte" in Transporte:
                PlaneT += 'AuxilioTransporte = "' + Transporte["AuxilioTransporte"] + '" '
            if "ViaticoManutAlojS" in Transporte:
                PlaneT += 'ViaticoManuAlojS = "' + Transporte["ViaticoManutAlojS"] + '" '
            if "ViaticoManutAlojNS" in Transporte:
                PlaneT += 'ViaticoManutAlojNS = "' + Transporte["ViaticoManutAlojNS"] + '"'
            PlaneT += '/>'
        if "HEDs" in Deven:
            if len(HEDs) != 0:
                PlaneT += '<HEDs>'
                PlaneT += '<HED '
                for HED in HEDs:
                    if "Cantidad" in HED:
                        PlaneT += 'Cantidad = "' + HED["Cantidad"] + '" '
                    if "Porcentaje" in HED:
                        PlaneT += 'Porcentaje = "' + HED["Porcentaje"] + '" '
                    if "Pago" in HED:
                        PlaneT += 'Pago = "' + HED["Pago"] + '"'
                PlaneT += '/>'
                PlaneT += '</HEDs>'

        if "HENs" in Deven:
            if len(HENs) != 0:
                PlaneT += '<HENs>'
                PlaneT += '<HEN '
                for HEN in HENs:
                    if "Cantidad" in HEN:
                        PlaneT += 'Cantidad = "' + HEN["Cantidad"] + '" '
                    if "Porcentaje" in HEN:
                        PlaneT += 'Porcentaje = "' + HEN["Porcentaje"] + '" '
                    if "Pago" in HEN:
                        PlaneT += 'Pago = "' + HEN["Pago"] + '"'
                PlaneT += '/>'
                PlaneT += '</HENs>'

        if "HRNs" in Deven:
            if len(HRNs) != 0:
                PlaneT += '<HRNs>'
                PlaneT += '<HRN '
                for HRN in HRNs:
                    if "Cantidad" in HRN:
                        PlaneT += 'Cantidad = "' + HRN["Cantidad"] + '" '
                    if "Porcentaje" in HRN:
                        PlaneT += 'Porcentaje = "' + HRN["Porcentaje"] + '" '
                    if "Pago" in HRN:
                        PlaneT += 'Pago = "' + HRN["Pago"] + '"'
                PlaneT += '/>'
                PlaneT += '</HRNs>'

        if "HEDDFs" in Deven:
            if len(HEDDFs) != 0:
                PlaneT += '<HEDDFs>'
                PlaneT += '<HEDDF '
                for HEDDF in HEDDFs:
                    if "Cantidad" in HEDDF:
                        PlaneT += 'Cantidad = "' + HEDDF["Cantidad"] + '" '
                    if "Porcentaje" in HEDDF:
                        PlaneT += 'Porcentaje = "' + HEDDF["Porcentaje"] + '" '
                    if "Pago" in HEDDF:
                        PlaneT += 'Pago = "' + HEDDF["Pago"] + '"'
                PlaneT += '/>'
                PlaneT += '</HEDDFs>'

        if "HRDDFs" in Deven:
            if len(HRDDFs) != 0:
                PlaneT += '<HRDDFs>'
                PlaneT += '<HRDDF '
                for HRDDF in HRDDFs:
                    if "Cantidad" in HRDDF:
                        PlaneT += 'Cantidad = "' + HRDDF["Cantidad"] + '" '
                    if "Porcentaje" in HRDDF:
                        PlaneT += 'Porcentaje = "' + HRDDF["Porcentaje"] + '" '
                    if "Pago" in HRDDF:
                        PlaneT += 'Pago = "' + HRDDF["Pago"] + '"'
                PlaneT += '/>'
                PlaneT += '</HRDDFs>'

        if "HENDFs" in Deven:
            if len(HENDFs) != 0:
                PlaneT += '<HENDFs>'
                PlaneT += '<HENDF '
                for HENDF in HENDFs:
                    if "Cantidad" in HENDF:
                        PlaneT += 'Cantidad = "' + HENDF["Cantidad"] + '" '
                    if "Porcentaje" in HENDF:
                        PlaneT += 'Porcentaje = "' + HENDF["Porcentaje"] + '" '
                    if "Pago" in HENDF:
                        PlaneT += 'Pago = "' + HENDF["Pago"] + '"'
                PlaneT += '/>'
                PlaneT += '</HENDFs>'

        if "HRNDFs" in Deven:
            if len(HRNDFs) != 0:
                PlaneT += '<HRNDFs>'
                PlaneT += '<HRNDF '
                for HRNDF in HRNDFs:
                    if "Cantidad" in HRNDF:
                        PlaneT += 'Cantidad = "' + HRNDF["Cantidad"] + '" '
                    if "Porcentaje" in HRNDF:
                        PlaneT += 'Porcentaje = "' + HRNDF["Porcentaje"] + '" '
                    if "Pago" in HRNDF:
                        PlaneT += 'Pago = "' + HRNDF["Pago"] + '"'
                PlaneT += '/>'
                PlaneT += '</HRNDFs>'

        if "Vacaciones" in Deven:
            if len(Vacaciones) != 0:
                PlaneT += '<Vacaciones>'
                PlaneT += '<VacacionesComunes '
                for VaComunes in VacacionesComunes:
                    if "Cantidad" in VaComunes:
                        PlaneT += 'Cantidad = "' + VaComunes["Cantidad"] + '" '
                    if "Pago" in VaComunes:
                        'Pago = "' + VaComunes["Pago"] + '"'
                PlaneT += '/>'
                PlaneT += '<VacacionesCompensadas '
                for VaCompensadas in VacacionesCompensadas:
                    if "Cantidad" in VaCompensadas:
                        PlaneT += 'Cantidad = "' + VaCompensadas["Cantidad"] + '" '
                    if "Pago" in VaCompensadas:
                        'Pago = "' + VaCompensadas["Pago"] + '"'
                PlaneT += '/>'
                PlaneT += '</Vacaciones>'

        if "Primas" in Deven:
            PlaneT += '<Primas '
            if "Cantidad" in Primas:
                PlaneT += 'Cantidad = "' + Primas["Cantidad"] + '" '
            if "Pago" in Primas:
                PlaneT += 'Pago = "' + Primas["Pago"] + '" '
            if "PagoNS" in Primas:
                PlaneT += 'PagoNS = "' + Primas["PagoNS"] + '"'
            PlaneT += '/>'

        if "Cesantias" in Deven:
            PlaneT += '<Cesantias '
            if "Pago" in Cesantias:
                PlaneT += 'Pago = "' + Cesantias["Pago"] + '" '
            if "Porcentaje" in Cesantias:
                PlaneT += 'Porcentaje = "' + Cesantias["Porcentaje"] + '" '
            if "PagoIntereses" in Cesantias:
                PlaneT += 'PagoIntereses = "' + Cesantias["PagoIntereses"] + '"'
            PlaneT += '/>'

        if "Incapacidades" in Deven:
            if len(Incapacidades) != 0:
                PlaneT += '<Incapacidades>'
                PlaneT += '<Incapacidad '
                for Incapacidad in Incapacidades:
                    if "Cantidad" in Incapacidad:
                        PlaneT += 'Cantidad = "' + Incapacidad["Cantidad"] + '" '
                    if "Tipo" in Incapacidad:
                        PlaneT += 'Tipo = "' + Incapacidad["Tipo"] + '" '
                    if "Pago" in Incapacidad:
                        'Pago = "' + Incapacidad["Pago"] + '"'
                PlaneT += '/>'
                PlaneT += '</Incapacidades>'

        if "Licencias" in Deven:
            if len(Licencias) != 0:
                PlaneT += '<Licencias>'
                for LMP in LicenciaMP:
                    PlaneT += '<LicenciaMP Cantidad = "' + LMP["Cantidad"] + '" Pago = "' + LMP["Pago"] + '"/>'
                for LR in LicenciaR:
                    PlaneT += '<LicenciaR Cantidad = "' + LR["Cantidad"] + '" Pago = "' + LR["Pago"] + '"/>'
                for LNR in LicenciaNR:
                    PlaneT += '<LicenciaNR FechaInicio = "' + LNR["FechaInicio"] + '" FechaFin = "' + \
                              LNR["FechaFin"] + '" Cantidad = "' + LNR["Cantidad"] + '"/>'
                PlaneT += '</Licencias>'

        if "Bonificaciones" in Deven:
            if len(Bonificaciones) != 0:
                PlaneT += '<Bonificaciones>'
                PlaneT += '<Bonificacion '
                for Bonificacion in Bonificaciones:
                    if "BonificacionS" in Bonificacion:
                        PlaneT += 'BonificacionS = "' + Bonificacion["BonificacionS"] + '" '
                    if "BonificacionNS" in Bonificacion:
                        PlaneT += 'BonificacionNS = "' + Bonificacion["BonificacionNS"] + '" '
                PlaneT += '/>'
                PlaneT += '</Bonificaciones>'

        if "Auxilios" in Deven:
            if len(Auxilios) != 0:
                PlaneT += '<Auxilios>'
                PlaneT += '<Auxilio '
                for Auxilio in Auxilios:
                    if "AuxilioS" in Auxilio:
                        PlaneT += 'AuxilioS = "' + Auxilio["AuxilioS"] + '" '
                    if "AuxilioNS" in Auxilio:
                        PlaneT += 'AuxilioNS = "' + Auxilio["AuxilioNS"] + '" '
                PlaneT += '/>'
                PlaneT += '</Auxilios>'

        if "OtrosConceptos" in Deven:
            if len(OtrosConceptos) != 0:
                PlaneT += '<OtrosConceptos>'
                PlaneT += '<OtroConcepto '
                for OtroConcepto in OtrosConceptos:
                    if "DescripcionConcepto" in OtroConcepto:
                        PlaneT += 'DescripcionConcepto = "' + OtroConcepto["DescripcionConcepto"] + '" '
                    if "ConceptoS" in OtroConcepto:
                        PlaneT += 'ConceptoS = "' + OtroConcepto["ConceptoS"] + '" '
                    if "ConceptoNS" in OtroConcepto:
                        'ConceptoNS = "' + OtroConcepto["ConceptoNS"] + '"/>'
                PlaneT += '/>'
                PlaneT += '</OtrosConceptos>'

        if "Compensaciones" in Deven:
            if len(Compensaciones) != 0:
                PlaneT += '<Compensaciones>'
                PlaneT += '<Compensacion '
                for Compensacion in Compensaciones:
                    if "CompensacionE" in Compensacion:
                        PlaneT += 'CompensacionE = "' + Compensacion["CompensacionE"] + '" '
                    if "CompensacionO" in Compensacion:
                        PlaneT += 'CompensacionO = "' + Compensacion["CompensacionO"] + '" '
                PlaneT += '/>'
                PlaneT += '</Compensaciones>'

        if "BonoEPCTVs" in Deven:
            if len(BonoEPCTVs) != 0:
                PlaneT += '<BonoEPCTVs>'
                PlaneT += '<BonoEPCTV '
                for BonoEPCTV in BonoEPCTVs:
                    if "PagoS" in BonoEPCTV:
                        PlaneT += 'PagoS = "' + BonoEPCTV["PagoS"] + '" '
                    if "PagoNS" in BonoEPCTV:
                        PlaneT += 'PagoNS = "' + BonoEPCTV["PagoNS"] + '" '
                    if "PagoAlimentacionS" in BonoEPCTV:
                        PlaneT += 'PagoAlimentacionS = "' + BonoEPCTV["PagoAlimentacionS"] + '" '
                    if "PagoAlimentacionNS" in BonoEPCTV:
                        PlaneT += 'PagoAlimentacionNS = "' + BonoEPCTV["PagoAlimentacionNS"] + '" '
                PlaneT += '/>'
                PlaneT += '</BonoEPCTVs>'

        if "Comisiones" in Deven:
            if len(Comisiones) != 0:
                PlaneT += '<Comisiones>'
                PlaneT += '<Comision '
                for Comision in Comisiones:
                    if "Comision" in Comision:
                        PlaneT += 'Comision = "' + Comision["Comision"] + '" '
                PlaneT += '/>'
                PlaneT += '</Comisiones>'

        if "PagosTerceros" in Deven:
            if len(PagosTerceros) != 0:
                PlaneT += '<PagosTerceros>'
                for PagosTercero in PagosTerceros:
                    PlaneT += '<PagoTercero>' + PagosTercero["PagoTercero"] + '</PagoTercero>'
                PlaneT += '</PagosTerceros>'

        if "Anticipos" in Deven:
            if len(Anticipos) != 0:
                PlaneT += '<Anticipos>'
                PlaneT += '<Anticipo '
                for Anticipo in Anticipos:
                    if "Anticipo" in Anticipo:
                        PlaneT += 'Anticipo = "' + Anticipo["Anticipo"] + '" '
                PlaneT += '/>'
                PlaneT += '</Anticipos>'
        if Dotacion != "":
            PlaneT += '<Dotacion>' + Dotacion + '</Dotacion>'
        if ApoyoSost != "":
            PlaneT += '<ApoyoSost>' + ApoyoSost + '</ApoyoSost>'
        if Teletrabajo != "":
            PlaneT += '<Teletrabajo>' + Teletrabajo + '</Teletrabajo>'
        if BonifRetiro != "":
            PlaneT += '<BonifRetiro>' + BonifRetiro + '</BonifRetiro>'
        if Indemnizacion != "":
            PlaneT += '<Indemnizacion>' + Indemnizacion + '</Indemnizacion>'
        if Reintegro != "":
            PlaneT += '<Reintegro>' + Reintegro + '</Reintegro>'
        PlaneT += '</Devengados>'
        PlaneT += '<Deducciones>'
        if "Salud" in Deducciones:
            PlaneT += '<Salud Porcentaje = "' + Salud["Porcentaje"] + '" Deduccion = "' + Salud["Deduccion"] + '"/>'
        if "FondoPension" in Deducciones:
            PlaneT += '<FondoPension Porcentaje = "' + FondoPension["Porcentaje"] + '" Deduccion = "' + \
                      FondoPension["Deduccion"] + '"/>'
        if "FondoSP" in Deducciones:
            PlaneT += '<FondoSP Porcentaje = "' + FondoSP["Porcentaje"] + '" Deduccion = "' + FondoSP["Deduccion"] + \
                      '" PorcentajeSub = "' + FondoSP["PorcentajeSub"] + '" DeduccionSub = "' + \
                      FondoSP["DeduccionSub"] + '"/>' \

        if "Sindicatos" in Deducciones:
            if len(Sindicatos) != 0:
                PlaneT += '<Sindicatos>'
                PlaneT += '<Sindicato '
                for Sindicato in Sindicatos:
                    if "Porcentaje" in Sindicato:
                        PlaneT += 'Porcentaje = "' + Sindicato["Porcentaje"] + '" '
                    if "Deduccion" in Sindicato:
                        'Deduccion = "' + Sindicato["Deduccion"] + '"'
                    PlaneT += '/>'
                    PlaneT += '</Sindicatos>'

        if "Sanciones" in Deducciones:
            if len(Sanciones) != 0:
                PlaneT += '<Sanciones>'
                PlaneT += '<Sancion '
                for Sancion in Sanciones:
                    if "SancionPublic" in Sancion:
                        PlaneT += 'SancionPublic = "' + Sancion["SancionPublic"] + '" '
                    if "SancionPriv" in Sancion:
                        PlaneT += 'SancionPriv = "' + Sancion["SancionPriv"] + '"'
                PlaneT += '/>'
                PlaneT += '</Sanciones>'

        if "Libranzas" in Deducciones:
            if len(Libranzas) != 0:
                PlaneT += '<Libranzas>'
                for Libranza in Libranzas:
                    PlaneT += '<Libranza Descripcion = "' + Libranza["Descripcion"] + '" Deduccion = "' + \
                              Libranza["Deduccion"] + '"/>'
                PlaneT += '</Libranzas>'

        if "PagosTercerosD" in Deducciones:
            if len(PagosTercerosD) != 0:
                PlaneT += '<PagosTerceros>'
                for PagoTercero in PagosTercerosD:
                    PlaneT += '<PagoTercero>' + PagoTercero["PagoTercero"] + '</PagoTercero>'
                PlaneT += '</PagosTerceros>'

        if "AnticiposD" in Deducciones:
            if len(AnticiposD) != 0:
                PlaneT += '<Anticipos>'
                for Anticipo in AnticiposD:
                    PlaneT += '<Anticipo>' + Anticipo["Anticipo"] + '</Anticipo>'
                PlaneT += '</Anticipos>'

        if "OtrasDeducciones" in Deducciones:
            if len(OtrasDeducciones) != 0:
                PlaneT += '<OtrasDeducciones>'
                for OtraDeduccion in OtrasDeducciones:
                    PlaneT += '<OtraDeduccion>' + OtraDeduccion["OtraDeduccion"] + '</OtraDeduccion>'
                PlaneT += '</OtrasDeducciones>'

        if PensionVoluntaria != "":
            PlaneT += '<PensionVoluntaria>' + PensionVoluntaria + '</PensionVoluntaria>'
        if RetencionFuente != "":
            PlaneT += '<RetencionFuente>' + RetencionFuente + '</RetencionFuente>'
        if AFC != "":
            PlaneT += '<AFC>' + AFC + '</AFC>'
        if Cooperativa != "":
            PlaneT += '<Cooperativa>' + Cooperativa + '</Cooperativa>'
        if EmbargoFiscal != "":
            PlaneT += '<EmbargoFiscal>' + EmbargoFiscal + '</EmbargoFiscal>'
        if PlanComplementarios != "":
            PlaneT += '<PlanComplementarios>' + PlanComplementarios + '</PlanComplementarios>'
        if Educacion != "":
            PlaneT += '<Educacion>' + Educacion + '</Educacion>'
        if ReintegroD != "":
            PlaneT += '<Reintegro>' + ReintegroD + '</Reintegro>'
        if Deuda != "":
            PlaneT += '<Deuda>' + Deuda + '</Deuda>'
        PlaneT += '</Deducciones>' \
                  '<DevengadosTotal>' + DevengadosTotal + '</DevengadosTotal>' \
                  '<DeduccionesTotal>' + DeduccionesTotal + '</DeduccionesTotal>' \
                  '<ComprobanteTotal>' + ComprobanteTotal + '</ComprobanteTotal>'

        if TipoNota == "1":
            Plane += PlaneT + '</Reemplazar>'

        if TipoNota == "2":
            Plane += '</Eliminar>'

        if TipoNota == "":
            Plane += PlaneT + '</NominaIndividual>'
        else:
            Plane += '</NominaIndividualDeAjuste>'

        return Plane

    @staticmethod
    def new_data(data: dict):
        try:
            new_data = PayRollSendsModel()
            new_data = PayRollSendsModel.import_data(new_data, data=data)
            PayRollSendsModel.save(new_data, create=True, commit=True)
            response = {
                'data': PayRollSendsModel.export_data(new_data),
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
            update_data = PayRollSendsModel.get_by_id(id=data['Id'], export=False)
            if not update_data:
                return NotFound('Los datos ingresados no pertenecen o no son validos para el registro consultado')
            update_data = PayRollSendsModel.import_data(update_data, data=data)
            PayRollSendsModel.save(update_data, create=True, commit=True)
            response = {
                'data': PayRollSendsModel.export_data(update_data),
                'statusCode': 200,
                'message': 'Registro modificado correctamente'
            }
            return response
        except Exception as e:
            print('Error: {er}'.format(er=e))
            raise InternalServerError(e)

    @validates()
    def validate_name_permit(self, key, name):
        try:
            FieldValidations.is_none(key, name)
            FieldValidations.is_empty(key, name)
            return name
        except Exception as e:
            print(e)
            raise InternalServerError(e)
