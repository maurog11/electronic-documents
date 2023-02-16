# -*- coding: utf-8 -*-
########################################################

# from python
import os
from jose import jwt

# from flask
from flask import g

# datetime
from datetime import datetime, timedelta

# From Local
from app.utils import ResponseData
from config import Config
from app.models import ApplicationModel

# Werkzeug
from app.exception import InternalServerError


class AuthController:

    @staticmethod
    def post_data_login(data: []):
        try:

            api_key = data['apiKey']
            api_secret = data['apiSecret']
            exist_app = ApplicationModel.get_by_apikey_and_api_secret(api_key=api_key, api_secret=api_secret,
                                                                      export=False)
            if not exist_app:
                return ResponseData.login_not_found()

            data['Id'] = exist_app.Id

            token = AuthController.generate_token(data=data)
            return ResponseData.token_response(token=token)
        except Exception as e:
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def generate_token(data: dict):
        try:
            g.user = data['Id']
            g.username = data['username']
            payload = {
                'iat': datetime.utcnow(),
                'exp': datetime.utcnow() + timedelta(minutes=60),
                'id': data['Id'],
                'name': data['apiKey'],
                'username': data['username'],
                'session_expired': 60
            }
            token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')
            return token
        except Exception as e:
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def verify_auth_token(token):
        """
        Allow validate a user according a yours token
        :param token: token to validate
        :raise: ValidationError an error occurs when no auth token faile
        :return: token encode or 401 unauthorized
        """
        if token is None or token == "":
            return None
        try:
            jw = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=["HS256"])
            g.user = jw
            return jw
        except Exception as e:
            print(e)
            raise InternalServerError(e)

