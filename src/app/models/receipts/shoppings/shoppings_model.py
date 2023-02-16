# -*- coding: utf-8 -*-
#########################################################
import os
from sqlalchemy import Index
from app.models.base_model import BaseModel
from app import db
from app.exception import InternalServerError, NotFound
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import validates
from app.utils import FieldValidations, ResponseData
from base64 import b64encode


class ShoppingsModel(BaseModel):
    __tablename__ = 'shoppings'

    ReceiverNit = db.Column(db.String(20), nullable=False, comment='Nit de la persona que recibe')
    DocType = db.Column(db.String(5), nullable=False, comment='Tipo de Doc AD=Contenedor FV=factura NC=Nota Cr ND=Nota DB DS=Documento Soporte NOM=Nomina NOMA=Nomina Ajuste ')
    Prefix = db.Column(db.String(4), nullable=False, comment='Prefijo del documento de la empresa ')
    SerieNumber = db.Column(db.String(15), nullable=True, comment='Numero de serie de la factura')
    YearSend = db.Column(db.String(4), nullable=False, comment='Año Envio ')
    NumberSend = db.Column(db.Integer, nullable=False, comment='numero envio..reinicia cada año ')
    DianResolution = db.Column(db.String(50), nullable=True, comment='Resolucion Dian ')
    IdSoftware = db.Column(db.String(100), nullable=True, comment='id software dian ')
    IssuerNit = db.Column(db.String(20), nullable=True, comment='Nit del cliente ')
    IssuerName = db.Column(db.String(100), nullable=True, comment='Nombre del cliente ')
    DateSend = db.Column(db.DateTime(10), nullable=True, comment='Fecha Envio ')
    HourSend = db.Column(db.String(20), nullable=True, comment='Hora Envio ')
    DianResponse = db.Column(LONGTEXT, nullable=True, comment='Respuesta DIAN ')
    DianResponseErrors = db.Column(LONGTEXT, nullable=True, comment='Errores DIAN ')
    DianXml = db.Column(LONGTEXT, nullable=True, comment='Xml enviado a DIAN ')
    DianXmlAppResponse = db.Column(LONGTEXT, nullable=True, comment='Xml Respuesta DIAN ')
    Cufe = db.Column(db.String(150), nullable=True, comment='CUFE, CUDE o CUNE documento ')
    TrackIdDian = db.Column(db.String(200), nullable=True, comment='Cadena que reporta la DIAN ')
    JsonReceived = db.Column(LONGTEXT, nullable=True, comment='JSON serializado')
    MessageEmail = db.Column(LONGTEXT, nullable=True, comment='Mensaje del estado email')
    Status = db.Column(db.String(1), nullable=True, comment='0 Rechazado 1=Enviado ')
    Total = db.Column(db.Float(20), nullable=True, comment='total del documento')
    IsCredit = db.Column(db.String(1), nullable=True, comment='0=No es credito 1=Es credito')

    __table_args__ = (Index('ix_idy', "ReceiverNit", "DocType", "YearSend"),)

    def export_data(self):
        return {
            'Id': self.Id,
            'CreateDate': str(self.CreateDate),
            'UpdateDate': str(self.UpdateDate),
            'ReceiverNit': self.ReceiverNit,
            'DocType': self.DocType,
            'Prefix': self.Prefix,
            'SerieNumber': self.SerieNumber,
            'YearSend': self.YearSend,
            'NumberSend': self.NumberSend,
            'DianResolution': self.DianResolution,
            'IdSoftware': self.IdSoftware,
            'IssuerNit': self.IssuerNit,
            'IssuerName': self.IssuerName,
            'DateSend': str(self.DateSend),
            'HourSend': str(self.HourSend),
            'DianResponse': self.DianResponse,
            'DianResponseErrors': self.DianResponseErrors,
            'DianXml': self.DianXml,
            'DianXmlAppResponse': self.DianXmlAppResponse,
            'Cufe': self.Cufe,
            'TrackIdDian': self.TrackIdDian,
            'JsonReceived': self.JsonReceived,
            'MessageEmail': self.MessageEmail,
            'Status': self.Status,
            'Total': self.Total,
            'IsCredit': self.IsCredit
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
        if 'ReceiverNit' in data:
            self.ReceiverNit = data['ReceiverNit']
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
        if 'IssuerNit' in data:
            self.IssuerNit = data['IssuerNit']
        if 'IssuerName' in data:
            self.IssuerName = data['IssuerName']
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
        if 'MessageEmail' in data:
            self.MessageEmail = data['MessageEmail']
        if 'Status' in data:
            self.Status = data['Status']
        if 'Total' in data:
            self.Total = data['Total']
        if 'IsCredit' in data:
            self.IsCredit = data['IsCredit']
        return self

    @staticmethod
    def export_xml(data: dict):
        try:
            if data["DocType"] == "FV":
                xissuer = str.zfill(data["IssuerNit"], 10)
                filename = os.getenv("PATH_DOCS") + xissuer + "invoice/" + "/" + data["DianXml"]

                with open(filename, "rb") as f:
                    datapdf = f.read()
                datapdf_encode = b64encode(datapdf).decode("utf-8")

                return datapdf_encode

            if data["DocType"] == "DS":
                xissuer = str.zfill(data["IssuerNit"], 10)
                filename = os.getenv("PATH_DOCS") + xissuer + "supportdoc/" + "/" + data["DianXml"]

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
                response = db.session.query(ShoppingsModel) \
                    .limit(int(pageSize)) \
                    .offset((int(pageNumber) - 1) * int(pageSize)) \
                    .all()
            else:
                response = db.session.query(ShoppingsModel) \
                    .all()
            if export:
                response = [ShoppingsModel.export_data(x) for x in response]
            return response
        except Exception as e:
            print(e)
            response = ResponseData.internal_server_error(str(e))
            return response

    @staticmethod
    def get_by_id(id: int, export: bool = False):
        try:
            response = db.session.query(ShoppingsModel) \
                .filter(ShoppingsModel.Id == id) \
                .first()
            if export and response:
                response = ShoppingsModel.export_data(response)
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
                    response = db.session.query(ShoppingsModel) \
                        .filter(
                        ShoppingsModel.IssuerNit == IssuerNit, ShoppingsModel.Prefix + ShoppingsModel.SerieNumber >= StartNumber
                        , ShoppingsModel.Prefix + ShoppingsModel.SerieNumber <= EndNumber, ShoppingsModel.ClientNit >= StartClientNit,
                            ShoppingsModel.ClientNit <= EndClientNit,
                            ShoppingsModel.DateSend >= StartDate,  ShoppingsModel.DateSend <= EndDate
                        , ShoppingsModel.Status == Status, ShoppingsModel.DocType == DocType) \
                        .limit(int(pageSize)) \
                        .offset((int(pageNumber) - 1) * int(pageSize))\
                        .all()
                else:
                    response = db.session.query(ShoppingsModel) \
                        .filter(
                        ShoppingsModel.IssuerNit == IssuerNit, ShoppingsModel.Prefix + ShoppingsModel.SerieNumber >= StartNumber
                        , ShoppingsModel.Prefix + ShoppingsModel.SerieNumber <= EndNumber,  ShoppingsModel.ClientNit >= StartClientNit,
                        ShoppingsModel.ClientNit <= EndClientNit
                        , ShoppingsModel.Status == Status, ShoppingsModel.DocType == DocType) \
                        .limit(int(pageSize)) \
                        .offset((int(pageNumber) - 1) * int(pageSize))\
                        .all()
            else:
                if StartDate != "":
                    response = db.session.query(ShoppingsModel) \
                        .filter(
                        ShoppingsModel.IssuerNit == IssuerNit, ShoppingsModel.Prefix + ShoppingsModel.SerieNumber >= StartNumber
                        , ShoppingsModel.Prefix + ShoppingsModel.SerieNumber <= EndNumber,
                        ShoppingsModel.ClientNit >= StartClientNit,
                        ShoppingsModel.ClientNit <= EndClientNit,
                        ShoppingsModel.DateSend >= StartDate, ShoppingsModel.DateSend <= EndDate
                        , ShoppingsModel.Status == Status, ShoppingsModel.DocType == DocType) \
                        .all()
                else:
                    response = db.session.query(ShoppingsModel) \
                        .filter(
                        ShoppingsModel.IssuerNit == IssuerNit, ShoppingsModel.Prefix + ShoppingsModel.SerieNumber >= StartNumber
                        , ShoppingsModel.Prefix + ShoppingsModel.SerieNumber <= EndNumber,  ShoppingsModel.ClientNit >= StartClientNit,
                        ShoppingsModel.ClientNit <= EndClientNit
                        , ShoppingsModel.Status == Status, ShoppingsModel.DocType == DocType) \
                        .all()

            if export and response:
                response = [ShoppingsModel.export_data_2(x) for x in response]
            return response
        except Exception as e:
            print(e)
            response = ResponseData.internal_server_error(str(e))
            return response

    @staticmethod
    def get_by_number(Nit: str, SeriePrefix: str, SerieNumber: str, DocType: str, export: bool = False):
        try:
            response = db.session.query(ShoppingsModel) \
                .filter(
                ShoppingsModel.IssuerNit == Nit, ShoppingsModel.Prefix == SeriePrefix, ShoppingsModel.SerieNumber == SerieNumber
                , ShoppingsModel.Status == "1", ShoppingsModel.DocType == DocType) \
                .first()
            if export and response:
                response = ShoppingsModel.export_data(response)
            return response
        except Exception as e:
            print(e)
            response = ResponseData.internal_server_error(str(e))
            return response

    @staticmethod
    def get_by_cufe(cufe: str, export: bool = False):
        try:
            response = db.session.query(ShoppingsModel) \
                .filter(
                ShoppingsModel.Cufe == cufe) \
                .first()
            if export and response:
                response = ShoppingsModel.export_data(response)
            return response
        except Exception as e:
            print('Error: {er}'.format(er=e))
            raise InternalServerError(e)

    @staticmethod
    def new_data(data: dict):
        try:
            new_data = ShoppingsModel()
            new_data = ShoppingsModel.import_data(new_data, data=data)
            ShoppingsModel.save(new_data, create=True, commit=True)
            response = {
                'data': ShoppingsModel.export_data(new_data),
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
            update_data = ShoppingsModel.get_by_id(id=data['Id'], export=False)
            if not update_data:
                return NotFound('Los datos ingresados no pertenecen o no son validos para el registro consultado')
            update_data = ShoppingsModel.import_data(update_data, data=data)
            ShoppingsModel.save(update_data, create=True, commit=True)
            response = {
                'data': ShoppingsModel.export_data(update_data),
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
