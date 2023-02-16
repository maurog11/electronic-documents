# -*- coding: utf-8 -*-
#########################################################
import os
import smtplib
from base64 import b64encode, b64decode
import time
import json
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from io import BytesIO
from pathlib import Path
from typing import Dict, Any
from zipfile import ZipFile
import requests
from flask import make_response, jsonify
from app.controllers import CertsController
from app.exception import InternalServerError
from app.models import EventsModel
from app.utils import ResponseData
from config import config


class EventsController:

    @staticmethod
    def all(data: Dict[str, int]):
        try:
            pageNumber, pageSize = (data["pageNumber"], data["pageSize"])
            db_data = EventsModel.get_data(export=True, pageNumber=pageNumber, pageSize=pageSize)
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
    def get_by(data: Dict[str, Any]):
        try:
            pageNumber, pageSize = (data["pageNumber"], data["pageSize"])
            db_data = EventsModel.get_by(data=data, export=True, pageNumber=pageNumber, pageSize=pageSize)
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

            response = EventsModel.get_by_id(id=id, export=True)
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
    def get_by_number(Nit: str, SeriePrefix: str, SerieNumber: str, DocType: str):
        try:
            response = EventsModel.get_by_number(Nit=Nit, SeriePrefix=SeriePrefix, SerieNumber=SerieNumber, DocType=DocType, export=True)
            if not response:
                response = ResponseData.not_found()
            return response
        except Exception as e:
            print('Error: {er}'.format(er=e))
            raise InternalServerError(e)

    @staticmethod
    def xml(data: Dict[str, str]):
        try:
            Nit = data['Nit']
            SeriePrefix = data['SeriePrefix']
            SerieNumber = data['SerieNumber']
            DocType = data['DocType']
            db_data = EventsModel.get_by_number(Nit=Nit, SeriePrefix=SeriePrefix, SerieNumber=SerieNumber,
                                                      DocType=DocType, export=True)
            if not db_data:
                response = ResponseData.not_found()
                return response
            else:
                xml = EventsModel.export_xml(db_data)
                return xml
        except KeyError as e:
            print('Error: {er}'.format(er=e))
            response = ResponseData.bad_request(error=str(e))
            return response

    @staticmethod
    def status(data: Dict[str, str]):
        try:
            def remove_char(s):
                return s[1: -1]

            datacerts = CertsController.get_by_nit(data["Nit"])
            if not datacerts:
                response = ResponseData.not_found()
                return response
            cert_encode = datacerts["Format"]
            # sending post request and saving response as response object

            datasign = {
                'CUFE': data["CUDE"],
                'Nit': data["Nit"],
                'keycert': datacerts["Key"],
                'contentcert': cert_encode
            }
            sdatasign = json.dumps(datasign)

            headers = {'content-type': 'application/json'}

            APISIGN_ENDPOINT = os.getenv("APISIGN_ENDPOINT") + "GetEventStatus/"
            url = APISIGN_ENDPOINT
            response = requests.get(url, data=sdatasign, headers=headers)
            responsebytes = response.content
            responsestr = responsebytes.decode("utf-8")
            strj = responsestr.replace("'", "\"")
            strj = remove_char(strj)
            responsejson = json.loads(strj)
            return responsejson
        except KeyError as e:
            print('Error: {er}'.format(er=e))
            response = ResponseData.bad_request(error=str(e))
            return response

    @staticmethod
    def send_email(id: int):
        sends = EventsModel.get_by_id(id=id)
        if not sends:
            response = ResponseData.not_found()
            return response

        NumberContainer = sends["NumberSend"]
        PathJsonReceived = sends["JsonReceived"]
        with open(PathJsonReceived, "rb") as f:
            bjson = f.read()
        json_encode = bjson.decode("utf-8")
        data_doc = json.loads(json_encode)
        xissuer = str.zfill(sends["IssuerNit"], 10)
        path_issuer = config.Config.PATH_DOCS + xissuer + "event/"
        file = path_issuer
        path_issuer = Path(file)
        if path_issuer.is_dir() == False:
            # crear carppeta
            os.mkdir(path_issuer)

        xml_ad = EventsModel.Create_xml_ad(data_doc, sends, NumberContainer)
        xnumbersend = str(NumberContainer)
        snumber = str.zfill(xnumbersend, 8)
        filename_ad = "ad" + xissuer + "000" + snumber
        filename_zip = "z" + xissuer + "000" + snumber
        filename_pdf = "fv" + xissuer + "000" + snumber
        filename_json = "js" + xissuer + "000" + snumber
        save_path_file_ad = str(path_issuer) + "/" + filename_ad + ".xml"
        save_path_file_pdf = str(path_issuer) + "/" + filename_pdf + ".pdf"
        save_path_file_zip = str(path_issuer) + "/" + filename_zip + ".zip"
        save_path_file_json = str(path_issuer) + "/" + filename_json + ".json"

        with open(save_path_file_ad, "w") as f:
            f.write(xml_ad)

        pdfs = data_doc["Pdf"]
        if len(pdfs) != 0:
            for xpdf in pdfs:
                bpdf = b64decode(xpdf["Format"])
                bytesio_o = BytesIO(bpdf)
                with open(save_path_file_pdf, "wb") as f:
                    f.write(bytesio_o.getbuffer())

        # Comprimir archivo
        with ZipFile(save_path_file_zip, mode='w') as file:
            file.write(save_path_file_ad, arcname=os.path.basename(save_path_file_ad))
            file.write(save_path_file_pdf, arcname=os.path.basename(save_path_file_pdf))
        try:
            # Iniciamos los parámetros del script
            remitente = config.Config.EMAIL_DOCS
            destinatarios = sends["ClientEmail"]
            asunto = sends["IssuerNit"] + ";" + sends["IssuerName"] + ";" + \
                     sends["SeriePrefix"] + sends["SerieNumber"] + ";" + "96" + ";" + \
                     sends["IssuerName"] + ";" + "Documentos Electronicos"
            cuerpo = 'Estimado cliente, se informa evento ' + sends["Note"] + ' Factura ' + data_doc["SeriePrefix"] + \
                     data_doc["SerieNumber"]
            ruta_adjunto = save_path_file_zip

            # Creamos el objeto mensaje
            mensaje = MIMEMultipart()

            # Establecemos los atributos del mensaje
            mensaje['From'] = remitente
            mensaje['To'] = ", ".join(destinatarios)
            mensaje['Subject'] = asunto

            # Agregamos el cuerpo del mensaje como objeto MIME de tipo texto
            mensaje.attach(MIMEText(cuerpo, 'plain'))

            # Abrimos el archivo que vamos a adjuntar
            archivo_adjunto = open(ruta_adjunto, 'rb')

            # Creamos un objeto MIME base
            adjunto_MIME = MIMEBase('application', 'octet-stream')
            # Y le cargamos el archivo adjunto
            adjunto_MIME.set_payload(archivo_adjunto.read())
            # Codificamos el objeto en BASE64
            encoders.encode_base64(adjunto_MIME)
            # Agregamos una cabecera al objeto
            adjunto_MIME.add_header('Content-Disposition', "attachment; filename= Documento Electrònico")
            # Y finalmente lo agregamos al mensaje
            mensaje.attach(adjunto_MIME)

            # Creamos la conexión con el servidor
            sesion_smtp = smtplib.SMTP(config.Config.EMAIL_SMTP_DOCS, config.Config.EMAIL_PORT_DOCS)

            # Ciframos la conexión
            sesion_smtp.starttls()

            # Iniciamos sesión en el servidor
            sesion_smtp.login(config.Config.EMAIL_DOCS, config.Config.EMAIL_KEY_DOCS)

            # Convertimos el objeto mensaje a texto
            texto = mensaje.as_string()

            # Enviamos el mensaje

            sesion_smtp.sendmail(remitente, destinatarios, texto)
        except Exception as e:

            messageemail = e
        else:
            messageemail = 'Correo enviado'

            # Cerramos la conexión
            sesion_smtp.quit()
        return messageemail

    @staticmethod
    def new_data(data: dict):
        try:
            def IntToHex(dian_code_int):
                dian_code_hex = '%02x' % dian_code_int
                return dian_code_hex

            def remove_char(s):
                return s[1: -1]

            Prefijo = ''
            Consecutivo = data["documentReference"]

            xemp = str.zfill(data["nitSenderParty"], 10)
            NumberSend = 1
            ActualYear = time.strftime('%Y')
            DocType = "AR"

            # grabar primero y obtener numero de envio
            sends = {
                'IssuerNit': data["nitSenderParty"],
                'IssuerName': data["registrationNameSenderParty"],
                'DocType': DocType,
                'Prefix': Prefijo,
                'SerieNumber': Consecutivo,
                'YearSend': ActualYear,
                'NumberSend': NumberSend
            }
            response = EventsModel.new_data(sends)
            dataresponse = response["data"]
            NumberSend = dataresponse["NumberSend"]
            IdSend = dataresponse["Id"]
            xnumbersend = IntToHex(NumberSend)
            snumber = str.zfill(xnumbersend, 8)
            data["number"] = NumberSend

            xml_event = EventsModel.create_xml_event(data)

            filename = "ar" + xemp + "000" + snumber
            import os
            # verificar si no existe carpeta del cliente y crearla
            path_emp = os.getenv('PATH_DOCS') + xemp + "/"
            if not Path(path_emp).is_dir():
                # crear carppeta
                os.mkdir(path_emp)
            path_emp = os.getenv('PATH_DOCS') + xemp + "/" + "event/"
            file = path_emp
            path_emp = Path(file)
            import os
            if not Path(path_emp).is_dir():
                # crear carppeta
                os.mkdir(path_emp)

            filename_json = "js" + xemp + "000" + snumber
            save_path_file = str(path_emp) + "/" + filename + ".xml"
            save_path_file_json = str(path_emp) + "/" + filename_json + ".json"

            with open(save_path_file, "w") as f:
                f.write(xml_event)

            with open(save_path_file, "rb") as f:
                dataxml_event = f.read()
            dataxmlevent_encode = b64encode(dataxml_event).decode("utf-8")

            with open(save_path_file_json, "w") as f:
                f.write(json.dumps(data))

            # firma
            datacerts = CertsController.get_by_nit(data["nitSenderParty"])
            if not datacerts:
                response = {
                    'statusCode': 404,
                    'message': 'No se encontraron certificados para el emisor',
                }
                return make_response(jsonify(response), 404)
            cert_encode = datacerts["Format"]

            datasign = {
                    'Id': '',
                    "Nit": data["nitSenderParty"],
                    'filename': filename,
                    'contentxml': dataxmlevent_encode,
                    'keycert': datacerts["Key"],
                    'contentcert': cert_encode,
                    'DocType': DocType
            }

            sdatasign = json.dumps(datasign)

            headers = {'content-type': 'application/json'}

            APISIGN_ENDPOINT = os.getenv('APISIGN_ENDPOINT') + "SendEvent/"
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
                find = EventsModel.get_by_number(Nit=data["nitSenderParty"], SeriePrefix=Prefijo,
                                                           SerieNumber=Consecutivo, DocType=DocType,
                                                           export=True)

                if find:
                    IdSend = find["Id"]

                # respuesta modificada para el consumo del api desde pymes+ v2
                response_api = {
                    'isValid': True,
                    'errors': {
                        'message': messages
                    },
                    'resultCode': 200,
                    'resultData': {
                        'id': IdSend,
                        'content': respuestadian
                    }
                }
                return response_api

            if "Procesado" in respuestadian:
                Status = "1"
            else:
                Status = "0"

            sends = {
                    'Id': IdSend,
                    'IssuerNit': data["nitSenderParty"],
                    'DocType': DocType,
                    'Prefix': Prefijo,
                    'SerieNumber': Consecutivo,
                    'YearSend': ActualYear,
                    'NumberSend': NumberSend,
                    'IdSoftware': '',
                    'ClientNit': data["nitReceiverParty"],
                    'ClientName': data["registrationNameReceiverParty"],
                    'ClientEmail': data["electronicMailReceiverParty"],
                    'DateSend': data["issueDate"],
                    'HourSend': data["issueTime"],
                    'DianResponse': respuestadian,
                    'DianResponseErrors': messages,
                    'DianXml': filename + ".xml",
                    'DianXmlAppResponse': xmlrespuesta,
                    'Cufe': data["CUFE"],
                    'CUDE': data["CUDE"],
                    'TrackIdDian': key,
                    'JsonReceived': filename_json + ".json",
                    'Status': Status

            }

            response = EventsModel.update_data(sends)
            responsedata = response["data"]
            if "Procesado" in respuestadian:
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
                    'content': respuestadian
                }
            }
            return response_api

        except Exception as e:
            import os, sys
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('object={0}, lineno={1}'.format(fname, exc_tb.tb_lineno))
            response = ResponseData.internal_server_error(str(e))
            return response

    @staticmethod
    def update_data(data: dict):
        try:
            result = EventsModel.get_by_id(id=data['Id'], export=False)
            if not result:
                return ResponseData.not_found()
            result = EventsModel.import_data(result, data=data)
            EventsModel.save_data(result, create=False, commit=True)
            response = ResponseData.response_update(data={})
            return response
        except Exception as e:
            print('Error: {er}'.format(er=e))
            response = ResponseData.bad_request(error=str(e))
            return response
