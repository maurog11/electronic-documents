from ast import Pass
from typing import Any, Dict
from flask import make_response, jsonify

def validate_codes(response: Any):
    """Verifica los códigos de respuesta de la API de la DIAN.

    Args:
        response (Any): Respuesta de la API de la DIAN.
    """

    code: int = response.status_code
    if code in (203, 204):
        response = make_response(
            jsonify(
                    {
                        'message': 'La petición ha sido envida correctamentea la DIAN, pero la respuesta no tiene contenido.',
                        'response': response
                    }
                ), code)
        return response
    elif code in (400, 401, 403, 404, 405):
        response = make_response(
            jsonify(
                    {
                        'message': 'Error al hacer la petición a la DIAN, verifique los datos enviados.',
                        'response': response
                    }
                ), code)
        return response
    elif code in (500, 501, 502, 503, 504):
        response = make_response(
            jsonify(
                    {
                        'message': 'Se presentó un error en el servidor de la DIAN.',
                        'response': response
                    }
                ), code)
        return response
