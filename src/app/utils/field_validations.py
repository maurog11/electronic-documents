# -*- coding: utf-8 -*-
#########################################################

# from Werkzeug
from werkzeug import exceptions


class FieldValidations:

    @staticmethod
    def is_none(key, field):
        if field is None:
            raise exceptions.BadRequest('The Field ' + key + ' can\'t be Null')

    @staticmethod
    def is_empty(key, field):
        if field is '' or field is ' ' or field is "" or field is " ":
            raise exceptions.BadRequest('The Field ' + key + ' can\'t be Empty')

    @staticmethod
    def length(key, field):
        pass

    @staticmethod
    def is_boolean():
        pass

    @staticmethod
    def is_integer(key, field):
        response = True
        if type(field) == str:
            if field.isdigit() is False:
                response = False
        elif type(field) == int:
            response = True
        else:
            response = False

        if response is False:
            raise exceptions.BadRequest('El campo ' + key + ' debe ser entero')

    @staticmethod
    def is_string():
        pass

    @staticmethod
    def is_float():
        pass

    @staticmethod
    def is_email(key, field):
        if '@' not in field:
            raise exceptions.BadRequest('The Field ' + key + ' must be email')
