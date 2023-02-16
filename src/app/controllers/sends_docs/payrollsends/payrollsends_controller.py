# -*- coding: utf-8 -*-
#########################################################
import os
import time
import json
from flask import make_response, jsonify
import requests
import config
from typing import Any, Dict
from pathlib import Path
from base64 import b64encode, b64decode
from io import BytesIO
from app.exception import InternalServerError, NotFound
from app.models import PayRollSendsModel
from app.controllers import CertsController
from app.utils import ResponseData, validate_codes


class PayRollSendsController:

    @staticmethod
    def all(data: Dict[str, int]):
        try:
            pageNumber, pageSize = (data["pageNumber"], data["pageSize"])
            db_data = PayRollSendsModel.get_data(export=True, pageNumber=pageNumber, pageSize=pageSize)
            if not db_data:
                response = ResponseData.not_found()
                return response
            response = make_response(jsonify(db_data), 200)
            return response
        except KeyError as e:
            print('Error: {er}'.format(er=e))
            response = ResponseData.bad_request(error=str(e))
            return response

    @staticmethod
    def pdf(data: Dict[str, str]):
        try:
            Nit = data['Nit']
            SeriePrefix = data['SeriePrefix']
            SerieNumber = data['SerieNumber']
            DocType = data['DocType']
            db_data = PayRollSendsModel.get_by_number(Nit=Nit, SeriePrefix=SeriePrefix, SerieNumber=SerieNumber,
                                                DocType=DocType, export=True)
            xml: str = ''
            pdf: str = ''
            if not db_data:
                response = ResponseData.not_found()
                return response
            pdf = PayRollSendsModel.export_pdf(db_data)
            xml = PayRollSendsController.xml(data=data)

            response = {
                'pdf': pdf,
                'xml': xml
            }

            return make_response(response, 200)

        except KeyError as e:
            print('Error: {er}'.format(er=e))
            response = ResponseData.bad_request(error=str(e))
            return response

    @staticmethod
    def xml(data: Dict[str, str]):
        try:
            Nit = data['Nit']
            SeriePrefix = data['SeriePrefix']
            SerieNumber = data['SerieNumber']
            DocType = data['DocType']
            db_data = PayRollSendsModel.get_by_number(Nit=Nit, SeriePrefix=SeriePrefix, SerieNumber=SerieNumber,
                                                DocType=DocType, export=True)
            if not db_data:
                response = ResponseData.not_found()
                return response
            else:
                xml = PayRollSendsModel.export_xml(db_data)
                return xml
        except KeyError as e:
            print('Error: {er}'.format(er=e))
            response = ResponseData.bad_request(error=str(e))
            return response

    @staticmethod
    def get_by(data: Dict[str, Any]):
        try:
            pageNumber, pageSize = (data["pageNumber"], data["pageSize"])
            db_data = PayRollSendsModel.get_by(data=data, export=True, pageNumber=pageNumber, pageSize=pageSize)
            if not db_data:
                response = ResponseData.not_found()
                return response
            response = make_response(jsonify(db_data), 200)
            return response
        except KeyError as e:
            print('Error: {er}'.format(er=e))
            response = ResponseData.bad_request(error=str(e))
            return response

    @staticmethod
    def get_by_id(id: int):
        try:
            if not id and not isinstance(id, int):
                raise ValueError('El id debe ser un entero, y diferente de null')

            response = PayRollSendsModel.get_by_id(id=id, export=True)
            if not response:
                response = ResponseData.not_found_by_id(ide=id)
            else:
                response = ResponseData.response_get(data=response)
            return response
        except Exception as e:
            print('Error: {er}'.format(er=e))
            response = ResponseData.bad_request(str(e))
            return response

    @staticmethod
    def updateCufe(data: Dict[str, str]):
        try:
            Id = data['Id']
            Cufe = data['Cufe']
            db_data = PayRollSendsModel.get_by_id(id=Id, export=True)
            if not db_data:
                response = ResponseData.not_found()
                return response

            db_data["Cufe"] = Cufe
            PayRollSendsModel.update_data(db_data)

            response = {
                'cufe': Cufe
            }

            return make_response(response, 200)
        except KeyError as e:
            print('Error: {er}'.format(er=e))
            response = ResponseData.bad_request(error=str(e))
            return response

    @staticmethod
    def status(data: dict):
        def remove_char(s):
            return s[1: -1]

        datacerts = CertsController.get_by_nit(data["Nit"])
        if not datacerts:
            response = ResponseData.not_found()
            return response
        cert_encode = datacerts["Format"]
        # sending post request and saving response as response object

        datasign = {
            'Id': data["CUFE"],
            "Nit": data["Nit"],
            'keycert': datacerts["Key"],
            'contentcert': cert_encode
        }
        sdatasign = json.dumps(datasign)

        headers = {'content-type': 'application/json'}

        APISIGN_ENDPOINT = os.getenv("APISIGN_ENDPOINT") + "GetStatus/"
        url = APISIGN_ENDPOINT
        response = requests.get(url, data=sdatasign, headers=headers)
        responsebytes = response.content
        responsestr = responsebytes.decode("utf-8")
        strj = responsestr.replace("'", "\"")
        strj = remove_char(strj)
        responsejson = json.loads(strj)
        return responsejson

    @staticmethod
    def status_send(data: dict):
        def remove_char(s):
            return s[1: -1]
        try:
            datacerts = CertsController.get_by_nit(data["Nit"])
            if not datacerts:
                response = {"Error": "No se encontro el certificado"}
                return response
            cert_encode = datacerts["Format"]
            # sending post request and saving response as response object

            datasign = {
                'Id': data["CUFE"],
                "Nit": data["Nit"],
                'keycert': datacerts["Key"],
                'contentcert': cert_encode
            }
            sdatasign = json.dumps(datasign)

            headers = {'content-type': 'application/json'}

            APISIGN_ENDPOINT = os.getenv("APISIGN_ENDPOINT") + "GetStatus/"
            url = APISIGN_ENDPOINT
            response = requests.get(url, data=sdatasign, headers=headers)
            if response.status_code in (200, 201, 202):
                responsebytes = response.content
                responsestr = responsebytes.decode("utf-8")
                strj = responsestr.replace("'", "\"")
                strj = remove_char(strj)
                response_json = json.loads(strj)
                return make_response(jsonify(response_json), response.status_code)
            resp = validate_codes(response)
            return resp
        except Exception as e:
            response = ResponseData.internal_server_error(str(e))
            return response

    @staticmethod
    def new_data(data: dict):
        try:
            def IntToHex(dian_code_int):
                dian_code_hex = '%02x' % dian_code_int
                return dian_code_hex

            def remove_char(s):
                return s[1: -1]

            xml_dianpayroll = PayRollSendsModel.create_xml_payroll(data)
            Empleador = data["Empleador"]
            InformacionGeneral = data["InformacionGeneral"]
            Trabajador = data["Trabajador"]
            SecuenciaXML = data["NumeroSecuenciaXML"]
            Prefijo = SecuenciaXML["Prefijo"]
            Consecutivo = SecuenciaXML["Consecutivo"]
            ClientName = Trabajador["PrimerNombre"] + " " + Trabajador["PrimerApellido"]
            ClientEmail = Trabajador["CorreoElectronico"]
            xemp = str.zfill(Empleador["NIT"], 10)
            NumberSend = 1
            ActualYear = time.strftime('%Y')

            if InformacionGeneral["TipoNota"] == "":
                DocType = "NO"
            else:
                DocType = "NA"

            # grabar primero y obtener numero de envio
            sends = {
                'IssuerNit': Empleador["NIT"],
                'IssuerName': Empleador["RazonSocial"],
                'DocType': DocType,
                'Prefix': Prefijo,
                'SerieNumber': Consecutivo,
                'YearSend': ActualYear,
                'NumberSend': NumberSend
            }
            Year = int(ActualYear) - 2000
            response = PayRollSendsModel.new_data(sends)
            dataresponse = response["data"]
            NumberSend = dataresponse["NumberSend"]
            IdSend = dataresponse["Id"]
            xnumbersend = IntToHex(NumberSend)
            snumber = str.zfill(xnumbersend, 8)
            if InformacionGeneral["TipoNota"] == "":
                filename = "nie" + xemp + str(Year) + snumber
            else:
                filename = "niae" + xemp + str(Year) + snumber

            # verificar si no existe carpeta del cliente y crearla
            path_emp = config.Config.PATH_DOCS + xemp + "/"
            import os
            if not Path(path_emp).is_dir():
                # crear carppeta
                os.mkdir(path_emp)
            path_emp = config.Config.PATH_DOCS + xemp + "/" + "payroll/"
            file = path_emp
            path_emp = Path(file)
            import os
            if not path_emp.is_dir():
                # crear carppeta
                os.mkdir(path_emp)

            filename_pdf = filename
            filename_json = "js" + xemp + "000" + snumber
            save_path_file = str(path_emp) + "/" + filename + ".xml"
            save_path_file_json = str(path_emp) + "/" + filename_json + ".json"
            save_path_file_pdf = str(path_emp) + "/" + filename_pdf + ".pdf"

            with open(save_path_file, "w") as f:
                f.write(xml_dianpayroll)

            with open(save_path_file, "rb") as f:
                dataxml_payroll = f.read()
            dataxmlpayroll_encode = b64encode(dataxml_payroll).decode("utf-8")

            with open(save_path_file_json, "w") as f:
                f.write(json.dumps(data))

            pdf = {}
            if "Pdf" in data:
                pdf = data["Pdf"]
            if len(pdf) != 0:
                bpdf = b64decode(pdf["Pdf"])
                bytesio_o = BytesIO(bpdf)
                with open(save_path_file_pdf, "wb") as f:
                    f.write(bytesio_o.getbuffer())

            # firma
            datacerts = CertsController.get_by_nit(Empleador["NIT"])
            if not datacerts:
                response = {
                    'statusCode': 404,
                    'message': 'No se encontraron certificados para el emisor',
                }
                return make_response(jsonify(response), 404)
            cert_encode = datacerts["Format"]

            datasign = {
                'Id': InformacionGeneral["DianTestSetId"],
                "Nit": Empleador["NIT"],
                'filename': filename,
                'contentxml': dataxmlpayroll_encode,
                'keycert': datacerts["Key"],
                'contentcert': cert_encode,
                'DocType': DocType
            }

            sdatasign = json.dumps(datasign)

            headers = {'content-type': 'application/json'}
            if InformacionGeneral["TipoAmbiente"] == "2":
                APISIGN_ENDPOINT = os.getenv("APISIGN_ENDPOINT") + "SendTestSetAsync/"
            else:
                APISIGN_ENDPOINT = os.getenv("APISIGN_ENDPOINT") + "SendNominaSync/"

            url = APISIGN_ENDPOINT
            response = requests.get(url, data=sdatasign, headers=headers)
            responsebytes = response.content
            responsestr = responsebytes.decode("utf-8")
            strj = responsestr.replace("'", "\"")
            strj = remove_char(strj)
            responsejson = json.loads(strj)
            respuestadian = ""
            xmlrespuesta = ""
            key = ""
            messages = ""
            if "xmldoc" in responsejson:
                xmlsign = b64decode(responsejson["xmldoc"]).decode("utf-8")
            if "respuestadian" in responsejson:
                respuestadian = responsejson["respuestadian"]
            if "xmlrespuesta" in responsejson:
                xmlrespuesta = responsejson["xmlrespuesta"]
            if "key" in responsejson:
                key = responsejson["key"]
            if "messages" in responsejson:
                messages = responsejson["messages"]

            if "Regla: 90" in messages:
                find = PayRollSendsModel.get_by_number(Nit=Empleador["NIT"], SeriePrefix=SecuenciaXML["Prefijo"],
                                                       SerieNumber=SecuenciaXML["Consecutivo"], DocType=DocType, export=True)

                if find:
                    IdSend = find["Id"]

                # respuesta modificada para el consumo del api desde pymes+ v2
                response_api = {
                    'isValid': False,
                    'errors': [
                        {
                        "Code": "DIAN_90",
                        "Description": messages,
                        "ExplanationValues": [respuestadian],
                        "Field": ""
                        }
                    ],
                    'resultCode': 200,
                    'resultData': {
                        'id': IdSend,
                        'content': respuestadian
                    }
                }
                return response_api

            if "Correctamente" in respuestadian:
                Status = "1"
            else:
                Status = "0"

            sends = {
                'Id': IdSend,
                'IssuerNit': Empleador["NIT"],
                'IssuerName': Empleador["RazonSocial"],
                'DocType': DocType,
                'Prefix': Prefijo,
                'SerieNumber': Consecutivo,
                'YearSend': ActualYear,
                'NumberSend': NumberSend,
                'IdSoftware': InformacionGeneral["DianSoftwareId"],
                'ClientNit': Trabajador["NumeroDocumento"],
                'ClientName': ClientName,
                'ClientEmail': ClientEmail,
                'DateSend': InformacionGeneral["FechaGen"],
                'HourSend': InformacionGeneral["HoraGen"],
                'DianResponse': respuestadian,
                'DianResponseErrors': messages,
                'DianXml': filename + ".xml",
                'DianXmlAppResponse': xmlrespuesta,
                'Cufe': InformacionGeneral["CUNE"],
                'TrackIdDian': key,
                'JsonReceived': filename_json + ".json",
                'Status': Status,
                'Accrued': data["DevengadosTotal"],
                'Deducted': data["DeduccionesTotal"],
                'Value':  data["ComprobanteTotal"]

            }

            response = PayRollSendsModel.update_data(sends)
            responsedata = response["data"]
            if "Correctamente" in respuestadian:
                IsValid = True
            else:
                IsValid = False

            # respuesta modificada para el consumo del api desde pymes+ v2
            response_api = {
                'isValid': IsValid,
                'errors': {
                    'message': messages
                },
                'resultCode': 200 if IsValid else 400,
                'resultData': {
                    'id': responsedata['Id'],
                    'content': respuestadian,
                    'CUNE': responsedata['Cufe']
                }
            }
            return response_api

        except Exception as e:
            # import os, sys
            # exc_type, exc_obj, exc_tb = sys.exc_info()
            # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # print('object={0}, lineno={1}'.format(fname, exc_tb.tb_lineno))
            print('Error: {er}'.format(er=e))
            response = ResponseData.internal_server_error(str(e))
            return response

    @staticmethod
    def new_note(data: dict):
        try:
            def remove_char(s):
                return s[1: -1]
            xml_dianpayroll = PayRollSendsModel.create_xml_payroll_notes(data)
            Empleador = data["Empleador"]
            InformacionGeneral = data["InformacionGeneralNotas"]
            Trabajador = data["Trabajador"]
            SecuenciaXML = data["NumeroSecuenciaXML"]
            Prefijo = SecuenciaXML["Prefijo"]
            Consecutivo = SecuenciaXML["Consecutivo"]
            ClientName = Trabajador["PrimerNombre"] + " " + Trabajador["PrimerApellido"]
            ClientEmail = Trabajador["CorreoElectronico"]
            xemp = str.zfill(Empleador["NIT"], 10)
            NumberSend = 1
            ActualYear = time.strftime('%Y')

            if InformacionGeneral["TipoNota"] == "":
                DocType = "NO"
            else:
                DocType = "NA"

            # grabar primero y obtener numero de envio
            sends = {
                'IssuerNit': Empleador["NIT"],
                'IssuerName': Empleador["RazonSocial"],
                'DocType': DocType,
                'Prefix': Prefijo,
                'SerieNumber': Consecutivo,
                'YearSend': ActualYear,
                'NumberSend': NumberSend
            }
            Year = int(ActualYear) - 2000
            sendsdata = PayRollSendsModel.import_data(PayRollSendsModel, sends)
            response = PayRollSendsModel.new_data(sends)
            dataresponse = response["data"]
            NumberSend = dataresponse["NumberSend"]
            IdSend = dataresponse["Id"]
            xnumbersend = str(NumberSend)
            snumber = str.zfill(xnumbersend, 8)
            if InformacionGeneral["TipoNota"] == "":
                filename = "nie" + xemp + str(Year) + snumber
            else:
                filename = "niae" + xemp + str(Year) + snumber

            # verificar si no existe carpeta del cliente y crearla
            path_emp = config.Config.PATH_DOCS + xemp + "/"
            import os
            if not Path(path_emp).is_dir():
                # crear carppeta
                os.mkdir(path_emp)
            path_emp = config.Config.PATH_DOCS + xemp + "/" + "payroll-note/"
            file = path_emp
            path_emp = Path(file)
            import os
            if not path_emp.is_dir():
                # crear carppeta
                os.mkdir(path_emp)

            filename_json = "js" + xemp + "000" + snumber
            save_path_file = str(path_emp) + "/" + filename + ".xml"
            save_path_file_json = str(path_emp) + "/" + filename_json + ".json"

            with open(save_path_file, "w") as f:
                f.write(xml_dianpayroll)

            with open(save_path_file, "rb") as f:
                dataxml_payroll = f.read()
            dataxmlpayroll_encode = b64encode(dataxml_payroll).decode("utf-8")

            with open(save_path_file_json, "w") as f:
                f.write(json.dumps(data))

            # firma
            datacerts = CertsController.get_by_nit(Empleador["NIT"])
            if not datacerts:
                response = {
                    'statusCode': 404,
                    'message': 'No se encontraron certificados para el emisor',
                }
                return make_response(jsonify(response), 404)
            cert_encode = datacerts["Format"]


            datasign = {
                'Id': InformacionGeneral["DianTestSetId"],
                "Nit": Empleador["NIT"],
                'filename': filename,
                'contentxml': dataxmlpayroll_encode,
                'keycert': datacerts["Key"],
                'contentcert': cert_encode,
                'DocType': DocType
            }

            sdatasign = json.dumps(datasign)

            headers = {'content-type': 'application/json'}

            if InformacionGeneral["TipoAmbiente"] == "2":
                APISIGN_ENDPOINT = os.getenv("APISIGN_ENDPOINT") + "SendTestSetAsync/"
            else:
                APISIGN_ENDPOINT = os.getenv("APISIGN_ENDPOINT") + "SendNominaSync/"
            url = APISIGN_ENDPOINT
            response = requests.get(url, data=sdatasign, headers=headers)
            responsebytes = response.content
            responsestr = responsebytes.decode("utf-8")
            strj = responsestr.replace("'", "\"")
            strj = remove_char(strj)
            responsejson = json.loads(strj)
            respuestadian = ""
            xmlrespuesta = ""
            key = ""
            messages = ""
            if "xmldoc" in responsejson:
                xml_sign = b64decode(responsejson["xmldoc"]).decode("utf-8")
            if "respuestadian" in responsejson:
                respuestadian = responsejson["respuestadian"]
            if "xmlrespuesta" in responsejson:
                xmlrespuesta = responsejson["xmlrespuesta"]
            if "key" in responsejson:
                key = responsejson["key"]
            if "messages" in responsejson:
                messages = responsejson["messages"]

            if "Regla: 90" in messages:
                find = PayRollSendsModel.get_by_number(Nit=Empleador["NIT"], SeriePrefix=SecuenciaXML["Prefijo"],
                                                       SerieNumber=SecuenciaXML["Consecutivo"], DocType=DocType,
                                                       export=True)

                if find:
                    IdSend = find["Id"]

                # respuesta modificada para el consumo del api desde pymes+ v2
                response_api = {
                    'isValid': False,
                    'errors': [
                        {
                            "Code": "DIAN_90",
                            "Description": messages,
                            "ExplanationValues": [respuestadian],
                            "Field": ""
                        }
                    ],
                    'resultCode': 200,
                    'resultData': {
                        'id': IdSend,
                        'content': respuestadian
                    }
                }
                return response_api

            if "Correctamente" in respuestadian:
                Status = "1"
            else:
                Status = "0"

            sends = {
                'Id': IdSend,
                'IssuerNit': Empleador["NIT"],
                'IssuerName': Empleador["RazonSocial"],
                'DocType': DocType,
                'Prefix': Prefijo,
                'SerieNumber': Consecutivo,
                'YearSend': ActualYear,
                'NumberSend': NumberSend,
                'IdSoftware': InformacionGeneral["DianSoftwareId"],
                'ClientNit': Trabajador["NumeroDocumento"],
                'ClientName': ClientName,
                'ClientEmail': ClientEmail,
                'DateSend': InformacionGeneral["FechaGen"],
                'HourSend': InformacionGeneral["HoraGen"],
                'DianResponse': respuestadian,
                'DianResponseErrors': messages,
                'DianXml': filename + ".xml",
                'DianXmlAppResponse': xmlrespuesta,
                'Cufe': InformacionGeneral["CUNE"],
                'TrackIdDian': key,
                'JsonReceived': filename_json + ".json",
                'Status': Status,
                'Accrued': data["DevengadosTotal"],
                'Deducted': data["DeduccionesTotal"],
                'Value': data["ComprobanteTotal"]
            }
            response = PayRollSendsModel.update_data(sends)
            responsedata = response["data"]
            if "Correctamente" in respuestadian:
                IsValid = True
            else:
                IsValid = False

            # respuesta modificada para el consumo del api desde pymes+ v2
            response_api = {
                'isValid': IsValid,
                'errors': {
                    'message': messages
                },
                'resultCode': 200 if IsValid else 400,
                'resultData': {
                    'id': responsedata['Id'],
                    'content': respuestadian,
                    'CUNE': responsedata['Cufe']
                }
            }
            return response_api

        except Exception as e:
            # import os, sys
            # exc_type, exc_obj, exc_tb = sys.exc_info()
            # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # print('object={0}, lineno={1}'.format(fname, exc_tb.tb_lineno))
            print('Error: {er}'.format(er=e))
            response = ResponseData.internal_server_error(str(e))
            return response

    @staticmethod
    def update_data(data: dict):
        try:
            update_data = PayRollSendsModel.get_by_id(id=data['Id'], export=False)
            if not update_data:
                response = make_response(jsonify(
                    {
                        'message': 'Los datos ingresados no pertenecen o no son validos para el registro consultado',
                        'statusCode': 404,
                    }
                ), 404)
                return response
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
            return ResponseData.internal_server_error(e)
