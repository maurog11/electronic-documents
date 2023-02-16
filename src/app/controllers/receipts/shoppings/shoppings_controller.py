# -*- coding: utf-8 -*-
#########################################################
import imaplib
import email
import time
from datetime import datetime
from email.header import decode_header
import os
import io
import zipfile
import xmltodict
from typing import Dict, Any
from flask import make_response, jsonify
from app.exception import InternalServerError
from app.models import ShoppingsModel, EmailsModel
from app.utils import ResponseData


class ShoppingsController:

    @staticmethod
    def all(data: Dict[str, int]):
        try:
            pageNumber, pageSize = (data["pageNumber"], data["pageSize"])
            db_data = ShoppingsModel.get_data(export=True, pageNumber=pageNumber, pageSize=pageSize)
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
            db_data = ShoppingsModel.get_by(data=data, export=True, pageNumber=pageNumber, pageSize=pageSize)
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

            response = ShoppingsModel.get_by_id(id=id, export=True)
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
            response = ShoppingsModel.get_by_number(Nit=Nit, SeriePrefix=SeriePrefix, SerieNumber=SerieNumber,
                                                    DocType=DocType, export=True)
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
            db_data = ShoppingsModel.get_by_number(Nit=Nit, SeriePrefix=SeriePrefix, SerieNumber=SerieNumber,
                                                   DocType=DocType, export=True)
            if not db_data:
                response = ResponseData.not_found()
                return response
            else:
                xml = ShoppingsModel.export_xml(db_data)
                return xml
        except KeyError as e:
            print('Error: {er}'.format(er=e))
            response = ResponseData.bad_request(error=str(e))
            return response

    @staticmethod
    def new_data(data: dict):
        try:
            new_data = ShoppingsModel()
            new_data = ShoppingsModel.import_data(new_data, data=data)
            new_data = new_data.import_data(data=data)
            ShoppingsModel.save(new_data, create=True, commit=True)
            response = ResponseData.response_save(data=ShoppingsModel.export_data(new_data))
            return response
        except Exception as e:
            print('Error: {er}'.format(er=e))
            response = ResponseData.bad_request(error=str(e))
            return response

    @staticmethod
    def update_data(data: dict):
        try:
            result = ShoppingsModel.get_by_id(id=data['Id'], export=False)
            if not result:
                return ResponseData.not_found()
            result = ShoppingsModel.import_data(result, data=data)
            ShoppingsModel.save_data(result, create=False, commit=True)
            response = ResponseData.response_update(data={})
            return response
        except Exception as e:
            print('Error: {er}'.format(er=e))
            response = ResponseData.bad_request(error=str(e))
            return response

    @staticmethod
    def refresh_data(data: dict):
        try:
            def parser_xml(xml: str, nit:str):
                CUFE = ""
                dataxml = ""
                issuerNit = ""
                issuerName = ""
                receiverNit = ""
                receiverName = ""
                prefix = ""
                total = ""
                document = ""
                ref_3 = ""
                error = ""
                try:
                    data = xmltodict.parse(xml)
                    parent = data['AttachedDocument']
                    sender_party = parent['cac:SenderParty']
                    receiver_party = parent['cac:ReceiverParty']
                    attachment = parent['cac:Attachment']
                    xml_doc = attachment['cac:ExternalReference']['cbc:Description']
                    reference = parent['cac:ParentDocumentLineReference']
                    ref_2 = reference['cac:DocumentReference']
                    ref_3 = ref_2['cac:Attachment']['cac:ExternalReference']['cbc:Description']
                    data_response = xmltodict.parse(ref_3)
                    dianresponse = data_response['ApplicationResponse']['cac:DocumentResponse']['cac:Response']['cbc:Description']
                    document = ref_2['cbc:ID']
                    date_document = ref_2['cbc:IssueDate']
                    hour_document = parent['cbc:IssueTime']
                    ref_4 = ref_2['cbc:UUID']
                    CUFE = ref_4['#text']
                    dataxml = xmltodict.parse(xml_doc)
                    issuerNit = sender_party['cac:PartyTaxScheme']['cbc:CompanyID']['#text']
                    issuerName = sender_party['cac:PartyTaxScheme']['cbc:RegistrationName']
                    receiverNit = receiver_party['cac:PartyTaxScheme']['cbc:CompanyID']['#text']
                    receiverName = receiver_party['cac:PartyTaxScheme']['cbc:RegistrationName']
                    prefix = dataxml['Invoice']['ext:UBLExtensions']['ext:UBLExtension'][0]['ext:ExtensionContent']['sts:DianExtensions']['sts:InvoiceControl']['sts:AuthorizedInvoices']['sts:Prefix']
                    total = dataxml['Invoice']['cac:LegalMonetaryTotal']['cbc:PayableAmount']['#text']
                    document = document.replace(prefix, '')
                    if receiverNit != nit:
                        error = 'El NIT del receptor no corresponde'
                except Exception as e:
                    error = 'Error: {er}'.format(er=e)

                response = {
                    'issuerNit': issuerNit,
                    'issuerName': issuerName,
                    'receiverNit': receiverNit,
                    'receiverName': receiverName,
                    'receiverParty': receiver_party,
                    'document': document,
                    'dianAppResponse': ref_3,
                    'dateDocument': date_document,
                    'hourDocument': hour_document,
                    'dianResponse': dianresponse,
                    'cufe': CUFE,
                    'dianXml': xml_doc,
                    'prefix': prefix,
                    'total': total,
                    'error': error
                }
                return response

            # Datos del usuario
            d_startDate = datetime.strptime(data["startDate"], '%Y-%m-%d')
            d_endDate = datetime.strptime(data["endDate"], '%Y-%m-%d')

            receiverNit = data['Nit']
            dataemail = EmailsModel.get_by_nit(receiverNit, export=True)
            if not dataemail:
                return ResponseData.not_found_credentials()
            username = dataemail['Email']
            password = dataemail['Key']
            servidor = dataemail['Imap']
            port = dataemail['Port']
            response = []

            '''
            # Se establece conexion con el servidor pop de gmail
            m = poplib.POP3_SSL('pop.gmail.com',995)
            m.user(username)
            m.pass_(password)
            numero = len(m.list()[1])
            '''

            # Crear conexión
            try:
                imap = imaplib.IMAP4_SSL(servidor)
                # iniciar sesión
                imap.login(username, password)
            except:
                response = ResponseData.login_not_found()
                return response

            status, mensajes = imap.select("INBOX")
            # print(mensajes)
            # mensajes a recibir
            N = 100
            # cantidad total de correos
            mensajes = int(mensajes[0])
            is_zip = False

            max_iterations = 300
            i_iteration = 0
            end_found = False
            for i in range(mensajes, mensajes - N, -1):
                # Obtener el mensaje
                i_iteration += 1
                # if i_iteration > max_iterations:
                #     break
                if end_found:
                    break
                try:
                    res, mensaje = imap.fetch(str(i), "(RFC822)")
                except:
                    break
                for respuesta in mensaje:

                    if isinstance(respuesta, tuple):
                        # Obtener el contenido
                        msg = email.message_from_bytes(respuesta[1])

                        mensaje = email.message_from_bytes(respuesta[1])
                        date0 = decode_header(mensaje['Date'])[0][0]
                        nvalidate = 0
                        pass_date = True
                        while nvalidate <= 5:
                            try:
                                if nvalidate == 0:
                                    date = date0[:11]
                                    f_date = datetime.strptime(date, '%d %b %Y')
                                    if f_date > d_endDate:
                                        pass_date = False

                                    if f_date < d_startDate:
                                        pass_date = False
                                        end_found = True

                                    break

                                elif nvalidate >= 1:
                                    date = date0[5:15+nvalidate]
                                    f_date = datetime.strptime(date, '%d %b %Y')

                                    if f_date > d_endDate:
                                        pass_date = False

                                    if f_date < d_startDate:
                                        pass_date = False
                                        end_found = True
                                    break

                                nvalidate += 1
                            except:
                                nvalidate += 1

                        if not pass_date:
                            pass
                        # decodificar el contenido
                        subject = decode_header(mensaje["Subject"])[0][0]
                        # if isinstance(subject, bytes):
                        #     # convertir a string
                        #     subject = subject.decode()
                        # de donde viene el correo
                        #from_ = mensaje.get("From")
                        # si el correo es html
                        if mensaje.is_multipart():
                            # Recorrer las partes del correo
                            for part in mensaje.walk():
                                # Extraer el contenido
                                try:
                                    content_type = part.get_content_type()
                                    content_disposition = str(part.get("Content-Disposition"))
                                    try:
                                        # el cuerpo del correo
                                        body = part.get_payload(decode=True).decode()
                                    except:
                                        pass
                                    if content_disposition == None:
                                        pass
                                    elif content_type == "text/plain" and "attachment" not in content_disposition:
                                        pass
                                    elif "attachment" in content_disposition:
                                        # download attachment
                                        nombre_archivo = part.get_filename()
                                        if nombre_archivo:
                                            if decode_header(nombre_archivo)[0][1] is not None:
                                                nombre_archivo = decode_header(nombre_archivo)[0][0].decode(
                                                    decode_header(nombre_archivo)[0][1])
                                            if not '.zip'.upper() in nombre_archivo.upper():
                                                pass
                                            buffer = io.BytesIO(part.get_payload(decode=True))
                                            is_zip = False
                                            try:
                                                z = zipfile.ZipFile(buffer)
                                                paso = False

                                                for xzip in z.infolist():
                                                    a = xzip.filename
                                                    if ".xml" in a:
                                                        paso = True
                                                        foo2 = z.open(xzip)
                                                        xml = ""
                                                        for x in foo2:
                                                            xml += x.decode("utf-8")
                                                        data = parser_xml(xml, receiverNit)
                                                        if data['error'] == '':
                                                            # mirar si existe
                                                            # guardar en la tabla shoppings
                                                            data_new = {
                                                                'ReceiverNit': receiverNit,
                                                                'DocType': 'CO',
                                                                'Prefix': data['prefix'],
                                                                'SerieNumber': data['document'],
                                                                'YearSend': datetime.now().year,
                                                                'IssuerNit': data['issuerNit'],
                                                                'IssuerName': data['issuerName'],
                                                                'DateSend': data['dateDocument'],
                                                                'HourSend': data['hourDocument'],
                                                                'DianResponse': data['dianResponse'],
                                                                'DianResponseErrors': '',
                                                                'DianXml': data['dianXml'],
                                                                'DianXmlAppResponse': data['dianAppResponse'],
                                                                'Cufe': data['cufe'],
                                                                'Status': '1',
                                                                'Total': data['total'],
                                                                'IsCredit': '1',
                                                                'NumberSend': int(data['document'])
                                                            }
                                                            data_shopping = ShoppingsModel.get_by_cufe(data['cufe'], export=True)
                                                            if not data_shopping:
                                                                data_shopping = ShoppingsModel.new_data(data_new)
                                                                if 'data' in data_shopping:
                                                                    response.append(data_shopping['data'])
                                            except:
                                                pass

                                            if not paso:
                                                pass
                                except:
                                    pass
                        else:
                            pass
            imap.close()
            imap.logout()
            return response
        except Exception as e:
            print('Error: {er}'.format(er=e))
            response = ResponseData.bad_request(error=str(e))
            return response
