# -*- coding: utf-8 -*-
#########################################################
from flask import Blueprint


api_city = Blueprint('api_city', __name__)


@api_city.before_request
def before_request():
    pass


@api_city.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


from. import city_route
