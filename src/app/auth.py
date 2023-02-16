# -*- coding: utf-8 -*-
#########################################################

# Importaciones de flask
from flask import jsonify, request, g
from flask_httpauth import HTTPTokenAuth
# from app import auth as auth_token

# Importaciones del app
from app.models import ApplicationModel
from app.controllers import AuthController
from app.utils import ResponseData

from werkzeug import exceptions

auth_token = HTTPTokenAuth()


@auth_token.verify_token
def verify_auth_token(token):
    """
    Esta función está creada para autenticar con los token de Google contra los usuarios de la BD

    :param token:
    :return: boolean whether test pass, or none
    """

    try:
        # VERIFICAR TOKEN LOGIN
        if not token:
            return None

        data = AuthController.verify_auth_token(token)
        application = ApplicationModel.get_by_id(id=data['id'], export=False)
        g.user = application.Id
        g.user_name = data['username']

        return application is not None

    except Exception as e:
        print(e)
        exceptions.InternalServerError(e)


@auth_token.error_handler
def unauthorized_token():
    """
    This function validate authorized token

    :return: status code
    """
    response = ResponseData.token_error()
    return response
