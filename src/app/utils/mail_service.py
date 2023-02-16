# -*- coding: utf-8 -*-
#########################################################

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
from app.exception import InternalServerError, NotFound


def send_mail(data: dict):

    message = Mail()

    message.from_email = From(
        email='edocs@softpymes.com.co',
        name='Documentos Electrónicos Pymes+'
    )

    message.to = [To(email=data['to'])]

    message.subject = Subject(data['subject'])

    # datos para el template edocs
    payload = data
    payload['subject'] = data['subject']
    payload['documentUrl'] = 'https://www.softpymes.com.co/'

    # identificador de la plantilla para el mensaje que se envia
    message.template_id = os.environ.get('ID_TEMPLATE_EDOCS')
    message.dynamic_template_data = payload

    if 'file' in data:
        base64_file = data['file']
        _file_name = data['fileName']
        _file_type = get_mime_type(_type=data['type'])

        message.attachment = [
            Attachment(
                file_content=FileContent(base64_file),
                file_name=FileName(_file_name),
                file_type=FileType(_file_type),
                disposition=Disposition('attachment')
            )
        ]
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(f'statusCode: {response.status_code}')
        # print(response.body)
        # print(response.headers) # consultar el ID del mensaje
        if response.status_code == 202:
            return {
                'ok': True,
                'message': 'Mensaje ha sido enviado correctamente.',
                'statusCode': 200
            }
        else:
            return {
                'ok': False,
                'message': 'Se presentó un error al momento de enviar el mensaje.',
                'statusCode': response.status_code
            }
    except Exception as e:
        print(str(e))
        raise InternalServerError(e)


def get_mail_by_id(_id: str):
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.client.messages._(_id).get()

        print(response.status_code)
        print(response.body)
        print(response.headers)
        return {
            'statusCode': 200,
            'message': 'Consultado'
        }
    except Exception as e:
        print(str(e))
        raise InternalServerError(e)


def get_mime_type(_type: str):
    types = {
        'pdf': 'application/pdf',
        'zip': 'application/octet-stream'
    }

    if not _type in types:
        raise NotFound('No se encuentra el MIMETYPE del archivo que se desea adjuntar.')

    return types[_type]
