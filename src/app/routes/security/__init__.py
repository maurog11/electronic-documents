# -*- coding: utf-8 -*-
#########################################################
from flask import Blueprint

api_apps = Blueprint('api_apps', __name__)


@api_apps.before_request
def before_request():
    pass


@api_apps.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


from. import application_route
