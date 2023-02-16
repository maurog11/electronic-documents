# -*- coding: utf-8 -*-
#########################################################
import os
from typing import Dict, Any

from sqlalchemy import Index
from app.models.base_model import BaseModel
from app import db
from app.exception import InternalServerError, NotFound
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import validates
from app.utils import FieldValidations, ResponseData
from base64 import b64encode


class NotesSendsModel(BaseModel):
    __tablename__ = 'notessends'

    IssuerNit = db.Column(db.String(20), nullable=False, comment='Nit de la empresa o emisor ')
    IssuerName = db.Column(db.String(200), nullable=False, comment='Nombre o razon social del emisor ')
    DocType = db.Column(db.String(5), nullable=False, comment='Tipo de Doc AD=Contenedor FV=factura NC=Nota Cr ND=Nota '
                                                              'DB DS=Documento Soporte NOM=Nomina NOMA=Nomina Ajuste ')
    Prefix = db.Column(db.String(4), nullable=True, comment='Prefijo del documento de la empresa ')
    SerieNumber = db.Column(db.String(15), nullable=True, comment='Numero de serie de la factura')
    YearSend = db.Column(db.String(4), nullable=False, comment='Año Envio ')
    NumberSend = db.Column(db.Integer, nullable=False, comment='numero envio..reinicia cada año ')
    DianResolution = db.Column(db.String(50), nullable=True, comment='Resolucion Dian ')
    IdSoftware = db.Column(db.String(100), nullable=True, comment='id software dian ')
    ClientNit = db.Column(db.String(20), nullable=True, comment='Nit del cliente ')
    ClientName = db.Column(db.String(100), nullable=True, comment='Nombre del cliente ')
    ClientEmail = db.Column(db.String(200), nullable=True, comment='Email del cliente ')
    DateSend = db.Column(db.DateTime(8), nullable=True, comment='Fecha Envio ')
    HourSend = db.Column(db.String(20), nullable=True, comment='Hora Envio ')
    DianResponse = db.Column(db.String(200), nullable=True, comment='Respuesta DIAN ')
    DianResponseErrors = db.Column(db.String(200), nullable=True, comment='Errores DIAN ')
    DianXml = db.Column(LONGTEXT, nullable=True, comment='Xml enviado a DIAN ')
    DianXmlAppResponse = db.Column(LONGTEXT, nullable=True, comment='Xml Respuesta DIAN ')
    Cufe = db.Column(db.String(150), nullable=True, comment='CUFE, CUDE o CUNE documento ')
    TrackIdDian = db.Column(db.String(200), nullable=True, comment='Cadena que reporta la DIAN ')
    JsonReceived = db.Column(LONGTEXT, nullable=True, comment='JSON serializado')
    Status = db.Column(db.String(1), nullable=True, comment='0 Rechazado 1=Enviado ')
    Total = db.Column(db.Float(20), nullable=True, comment='total del documento')

    __table_args__ = (Index('ix_nts', "IssuerNit", "DocType", "YearSend"),)

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
            'Total': self.Total
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
        if 'TrackIdDian' in data:
            self.TrackIdDian = data['TrackIdDian']
        if 'JsonReceived' in data:
            self.JsonReceived = data['JsonReceived']
        if 'Status' in data:
            self.Status = data['Status']
        if 'Total' in data:
            self.Total = data['Total']
        return self

    @staticmethod
    def export_pdf(data: dict):
        try:
            if data["DocType"] == "NC":
                xissuer = str.zfill(data["IssuerNit"], 10)
                filename = os.getenv("PATH_DOCS") + "invoice-note/" + xissuer + "/" + data["DianXml"]
                filename = filename.replace(".xml", ".pdf")

                with open(filename, "rb") as f:
                    datapdf = f.read()
                datapdf_encode = b64encode(datapdf).decode("utf-8")

                return datapdf_encode

            if data["DocType"] == "ND":
                xissuer = str.zfill(data["IssuerNit"], 10)
                filename = os.getenv("PATH_DOCS") + "invoice-note/" + xissuer + "/" + data["DianXml"]
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
            if data["DocType"] == "NC":
                xissuer = str.zfill(data["IssuerNit"], 10)
                filename = os.getenv("PATH_DOCS") + "invoice-note/" + xissuer + "/" + data["DianXml"]

                with open(filename, "rb") as f:
                    datapdf = f.read()
                datapdf_encode = b64encode(datapdf).decode("utf-8")

                return datapdf_encode

            if data["DocType"] == "ND":
                xissuer = str.zfill(data["IssuerNit"], 10)
                filename = os.getenv("PATH_DOCS") + "invoice-note/" + xissuer + "/" + data["DianXml"]

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
            if data["DocType"] == "NC":
                xissuer = str.zfill(data["IssuerNit"], 10)
                filename = os.getenv("PATH_DOCS") + "invoice-note/" + xissuer + "/" + data["JsonReceived"]

                with open(filename, "rb") as f:
                    datapdf = f.read()
                datapdf_encode = b64encode(datapdf).decode("utf-8")

                return {
                    'json': datapdf_encode
                }

            if data["DocType"] == "ND":
                xissuer = str.zfill(data["IssuerNit"], 10)
                filename = os.getenv("PATH_DOCS") + "invoice-note/" + xissuer + "/" + data["JsonReceived"]

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
                response = db.session.query(NotesSendsModel) \
                    .limit(int(pageSize)) \
                    .offset((int(pageNumber) - 1) * int(pageSize)) \
                    .all()
            else:
                response = db.session.query(NotesSendsModel) \
                    .all()
            if export:
                response = [NotesSendsModel.export_data(x) for x in response]
            return response
        except Exception as e:
            print(e)
            response = ResponseData.internal_server_error(str(e))
            return response

    @staticmethod
    def get_by_nds(data: dict, export: bool = False, pageNumber=0, pageSize=None):
        try:
            IssuerNit = ""
            StartClientNit = ""
            EndClientNit = ""
            DocType = "NDS"
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
                    response = db.session.query(NotesSendsModel) \
                        .filter(
                        NotesSendsModel.IssuerNit == IssuerNit, NotesSendsModel.Prefix + NotesSendsModel.SerieNumber >= StartNumber
                        , NotesSendsModel.Prefix + NotesSendsModel.SerieNumber <= EndNumber,
                        NotesSendsModel.ClientNit >= StartClientNit,
                        NotesSendsModel.ClientNit <= EndClientNit,
                        NotesSendsModel.DateSend >= StartDate, NotesSendsModel.DateSend <= EndDate
                        , NotesSendsModel.Status == Status, NotesSendsModel.DocType == DocType) \
                        .limit(int(pageSize)) \
                        .offset((int(pageNumber) - 1) * int(pageSize)) \
                        .all()
                else:
                    response = db.session.query(NotesSendsModel) \
                        .filter(
                        NotesSendsModel.IssuerNit == IssuerNit, NotesSendsModel.Prefix + NotesSendsModel.SerieNumber >= StartNumber
                        , NotesSendsModel.Prefix + NotesSendsModel.SerieNumber <= EndNumber,
                        NotesSendsModel.ClientNit >= StartClientNit,
                        NotesSendsModel.ClientNit <= EndClientNit
                        , NotesSendsModel.Status == Status, NotesSendsModel.DocType == DocType) \
                        .limit(int(pageSize)) \
                        .offset((int(pageNumber) - 1) * int(pageSize)) \
                        .all()
            else:
                if StartDate != "":
                    response = db.session.query(NotesSendsModel) \
                        .filter(
                        NotesSendsModel.IssuerNit == IssuerNit, NotesSendsModel.Prefix + NotesSendsModel.SerieNumber >= StartNumber
                        , NotesSendsModel.Prefix + NotesSendsModel.SerieNumber <= EndNumber,
                        NotesSendsModel.ClientNit >= StartClientNit,
                        NotesSendsModel.ClientNit <= EndClientNit,
                        NotesSendsModel.DateSend >= StartDate, NotesSendsModel.DateSend <= EndDate
                        , NotesSendsModel.Status == Status, NotesSendsModel.DocType == DocType) \
                        .all()
                else:
                    response = db.session.query(NotesSendsModel) \
                        .filter(
                        NotesSendsModel.IssuerNit == IssuerNit, NotesSendsModel.Prefix + NotesSendsModel.SerieNumber >= StartNumber
                        , NotesSendsModel.Prefix + NotesSendsModel.SerieNumber <= EndNumber,
                        NotesSendsModel.ClientNit >= StartClientNit,
                        NotesSendsModel.ClientNit <= EndClientNit
                        , NotesSendsModel.Status == Status, NotesSendsModel.DocType == DocType) \
                        .all()
            if export and response:
                response = [NotesSendsModel.export_data_2(x) for x in response]
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
            DocType = ""
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
                    response = db.session.query(NotesSendsModel) \
                        .filter(
                        NotesSendsModel.IssuerNit == IssuerNit,
                        NotesSendsModel.Prefix + NotesSendsModel.SerieNumber >= StartNumber
                        , NotesSendsModel.Prefix + NotesSendsModel.SerieNumber <= EndNumber,
                        NotesSendsModel.ClientNit >= StartClientNit,
                        NotesSendsModel.ClientNit <= EndClientNit,
                        NotesSendsModel.DateSend >= StartDate, NotesSendsModel.DateSend <= EndDate
                        , NotesSendsModel.Status == Status, NotesSendsModel.DocType == DocType) \
                        .limit(int(pageSize)) \
                        .offset((int(pageNumber) - 1) * int(pageSize)) \
                        .all()
                else:
                    response = db.session.query(NotesSendsModel) \
                        .filter(
                        NotesSendsModel.IssuerNit == IssuerNit,
                        NotesSendsModel.Prefix + NotesSendsModel.SerieNumber >= StartNumber
                        , NotesSendsModel.Prefix + NotesSendsModel.SerieNumber <= EndNumber,
                        NotesSendsModel.ClientNit >= StartClientNit,
                        NotesSendsModel.ClientNit <= EndClientNit
                        , NotesSendsModel.Status == Status, NotesSendsModel.DocType == DocType) \
                        .limit(int(pageSize)) \
                        .offset((int(pageNumber) - 1) * int(pageSize)) \
                        .all()
            else:
                if StartDate != "":
                    response = db.session.query(NotesSendsModel) \
                        .filter(
                        NotesSendsModel.IssuerNit == IssuerNit,
                        NotesSendsModel.Prefix + NotesSendsModel.SerieNumber >= StartNumber
                        , NotesSendsModel.Prefix + NotesSendsModel.SerieNumber <= EndNumber,
                        NotesSendsModel.ClientNit >= StartClientNit,
                        NotesSendsModel.ClientNit <= EndClientNit,
                        NotesSendsModel.DateSend >= StartDate, NotesSendsModel.DateSend <= EndDate
                        , NotesSendsModel.Status == Status, NotesSendsModel.DocType == DocType) \
                        .all()
                else:
                    response = db.session.query(NotesSendsModel) \
                        .filter(
                        NotesSendsModel.IssuerNit == IssuerNit,
                        NotesSendsModel.Prefix + NotesSendsModel.SerieNumber >= StartNumber
                        , NotesSendsModel.Prefix + NotesSendsModel.SerieNumber <= EndNumber,
                        NotesSendsModel.ClientNit >= StartClientNit,
                        NotesSendsModel.ClientNit <= EndClientNit
                        , NotesSendsModel.Status == Status, NotesSendsModel.DocType == DocType) \
                        .all()
            if export and response:
                response = [NotesSendsModel.export_data_2(x) for x in response]
            return response
        except Exception as e:
            print(e)
            response = ResponseData.internal_server_error(str(e))
            return response

    @staticmethod
    def get_by_id(id: int, export: bool = False):
        try:
            response = db.session.query(NotesSendsModel) \
                .filter(NotesSendsModel.Id == id) \
                .first()
            if export and response:
                response = NotesSendsModel.export_data(response)
            return response
        except Exception as e:
            print(e)
            response = ResponseData.internal_server_error(str(e))
            return response

    @staticmethod
    def get_by_number(Nit: str, SeriePrefix: str, SerieNumber: str, DocType: str, export: bool = False):
        try:
            response = db.session.query(NotesSendsModel) \
                .filter(
                NotesSendsModel.IssuerNit == Nit, NotesSendsModel.Prefix == SeriePrefix, NotesSendsModel.SerieNumber == SerieNumber
                , NotesSendsModel.Status == "1", NotesSendsModel.DocType == DocType) \
                .first()
            if export and response:
                response = NotesSendsModel.export_data(response)
            return response
        except Exception as e:
            print(e)
            response = ResponseData.internal_server_error(str(e))
            return response

    @staticmethod
    def new_data(data: dict):
        try:
            new_data = NotesSendsModel()
            new_data = NotesSendsModel.import_data(new_data, data=data)
            NotesSendsModel.save(new_data, create=True, commit=True)
            response = {
                'data': NotesSendsModel.export_data(new_data),
                'statusCode': 201,
                'message': 'Registro almacenado correctamente'
            }
            return response
        except Exception as e:
            print('Error: {er}'.format(er=e))
            response = ResponseData.internal_server_error(str(e))
            return response

    @staticmethod
    def update_data(data: dict):
        try:
            update_data = NotesSendsModel.get_by_id(id=data['Id'], export=False)
            if not update_data:
                return NotFound('Los datos ingresados no pertenecen o no son validos para el registro consultado')
            update_data = NotesSendsModel.import_data(update_data, data=data)
            NotesSendsModel.save(update_data, create=True, commit=True)
            response = {
                'data': NotesSendsModel.export_data(update_data),
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