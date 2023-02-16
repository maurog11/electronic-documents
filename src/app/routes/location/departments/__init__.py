# -*- coding: utf-8 -*-
#########################################################
from flask import Blueprint


api_department = Blueprint('api_department', __name__)


@api_department.before_request
def before_request():
    pass


@api_department.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


from. import department_route
