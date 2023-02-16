# -*- coding: utf-8 -*-
#########################################################

from flask import make_response


class ResponseData:

    @staticmethod
    def internal_server_error(error: str):
        response = {
            'statusCode': 500,
            'message': f'Internal Server Error: Se presento un error en el servidor, Error:{error}'
        }
        return make_response(response, 500)

    @staticmethod
    def bad_request(error: str):
        response = {
            'statusCode': 400,
            'message': f'Bad Request: Has cometido un error al hacer la peticion, Error:{error}'
        }
        return make_response(response, 400)

    @staticmethod
    def not_found_by_id(ide: int):
        response = {
            'statusCode': 404,
            'message': 'No se encontraron registros con el ID: {id}'.format(id=ide)
        }
        return make_response(response, 404)

    @staticmethod
    def not_found():
        response = {
            'statusCode': 404,
            'message': 'No se encontraron registros'
        }
        return make_response(response, 404)

    @staticmethod
    def not_found_credentials():
        response = {
            'statusCode': 404,
            'message': 'No se definieron credenciales del servidor email para el usuario'
        }
        return make_response(response, 404)

    @staticmethod
    def login_not_found():
        response = {
            'statusCode': 404,
            'message': 'Las credenciales ingresadas no son válidas'
        }
        return make_response(response, 404)

    @staticmethod
    def token_response(token: str):
        response = {
            'expireInMin': 60,
            'type': 'Bearer',
            'token': token
        }
        return make_response(response, 200)

    @staticmethod
    def token_error():
        response = {
            'status': 401,
            'error': 'unauthorized',
            'message': 'Credenciales no válidas.'
        }
        return make_response(response, 401)

    @staticmethod
    def response_save(data: dict):
        response = {
            'body': data,
            'message': 'Registro almacenado correctamente'
        }
        return make_response(response, 201)

    @staticmethod
    def response_get(data: dict):
        return make_response(data, 200)

    @staticmethod
    def response_update(data: dict):
        response = {
            'message': 'Registro actualizado correctamente'
        }
        if len(data) > 0:
            response['body'] = data
        return make_response(response, 200)

    @staticmethod
    def response_unique(field: str, value: str, action: str):
        if action == 'new':
            action = 'crear'
        elif action == 'update':
            action = 'modificar'
        response = {
            'statusCode': 400,
            'message': 'No se puede {action} un registro por el campo {field}, porque ya existe un '
                       'registro con el valor: {value}'.format(action=action, field=field, value=value)
        }
        return make_response(response, 400)
