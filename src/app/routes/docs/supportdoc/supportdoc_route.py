# -*- coding: utf-8 -*-
#########################################################
from flask import request, make_response, jsonify
from app.controllers import InvoicesController as Controller
from app.auth import auth_token
from flask_restx import Resource
from app.utils import validate_json
from .schemas import SupportDocModel, GetNumberingModel, GetStatusModel, SupportDocNoteModel, SupportDocNumberModel, \
    supportDocFilterCufeModel, api


@api.route('/get', methods=['GET'])
class All(Resource):
    decorators = [auth_token.login_required]

    @api.doc('get_all_supportdocs')
    def get(self):
        """
        Obtiene todos los Documentos Soporte almacenados en la base de datos
        """
        data = request.json
        response = Controller.all(data=data)
        return response


@api.route('/data/<int:id>/get', methods=['GET'])
@api.response(404, 'Documento soporte no encontrado')
@api.param('id', 'Identificador de documento soporte')
class GetByid(Resource):
    decorators = [auth_token.login_required]

    @api.doc('get_supportdoc_by_id')
    def get(self, id):
        """
        Obtiene un documento soporte dado su id
        """
        response = Controller.get_by_id(id)
        return response


@api.route('/pdf-xml', methods=['POST'])
@api.response(201, 'Registro encontrado')
@api.response(400, 'Error al hacer la peticion.')
@api.response(500, 'Se presentó un error en el servidor.')
class Pdf(Resource):
    decorators = [auth_token.login_required]

    @api.doc('pdf')
    @api.expect(SupportDocNumberModel)
    def post(self):
        """
        Consulta un pdf de un documento
        """
        re_json = request.json
        response = Controller.pdf(data=re_json)
        return response


@api.route('/xml', methods=['POST'])
@api.response(201, 'Registro encontrado')
@api.response(400, 'Error al hacer la peticion.')
@api.response(500, 'Se presentó un error en el servidor.')
class Xml(Resource):
    decorators = [auth_token.login_required]

    @api.doc('xml')
    @api.expect(SupportDocNumberModel)
    def post(self):
        """
        Consulta un xml de un documento
        """
        re_json = request.json
        response = Controller.xml(data=re_json)
        return response


@api.route('/numbering', methods=['POST'])
@api.response(404, 'Documento soporte no encontrado')
class Numbering(Resource):
    decorators = [auth_token.login_required]

    @api.expect(GetNumberingModel)
    def post(self):
        """
        Obtiene el rango de numeracion dado su Nit y el DianSofwareId
        """
        data = request.json
        response = Controller.numbering_ds(data)
        return response


@api.route('/status', methods=['POST'])
@api.response(201, 'Documento se encontro en los registros de la DIAN')
class Status(Resource):
    decorators = [auth_token.login_required]

    @api.expect(GetStatusModel)
    def post(self):
        """
        Obtiene el estado de un documento de la DIAN dado su CUFE
                """
        data = request.json
        response = Controller.status_ds(data)
        return response


@api.route('/new', methods=['POST'])
@api.response(201, 'Documento soporte procesado correctamente en la DIAN')
class NewData(Resource):
    decorators = [auth_token.login_required]

    @api.doc('create_new_supportdoc')
    @api.expect(SupportDocModel)
    def post(self):
        """
        Envia un Documento Soporte a la DIAN
        """
        not_validate = [
            'PostalCode'
        ]
        data = validate_json(request.json, to_not_validate=not_validate)
        if 'resultCode' in data and data['resultCode'] == 400:
            response = make_response(jsonify(data), 400)
            return response
        response = Controller.new_data_ds(data=data)
        return response


@api.route('/newnote', methods=['POST'])
@api.response(201, 'Nota al documento soporte procesado correctamente en la DIAN')
class NewNote(Resource):
    decorators = [auth_token.login_required]

    @api.doc('create_new_note')
    @api.expect(SupportDocNoteModel)
    def post(self):
        """
        Envia una Nota Credito al Documento Soporte a la DIAN
        """
        data = validate_json(request.json)
        if 'resultCode' in data and data['resultCode'] == 400:
            response = make_response(jsonify(data), 400)
            return response
        response = Controller.new_note_ds(data=data)
        return response


@api.route('/update', methods=['PUT'])
@api.response(201, 'Documento soporte actualizado correctamente')
class UpdateData(Resource):
    decorators = [auth_token.login_required]

    @api.doc('update_supportdoc')
    @api.marshal_with(SupportDocModel)
    def put(self):
        """
        Actualiza un Documento Soporte
        """
        data = request.json
        response = Controller.update_data(data=data)
        return response


@api.route('/update-cufe', methods=['POST'])
@api.response(201, 'Envio de factura creado correctamente')
class updateCufe(Resource):
    decorators = [auth_token.login_required]

    @api.doc('update_cufe')
    @api.expect(supportDocFilterCufeModel)
    def post(self):
        """
        Actualiza el cufe de un documento
        """
        data = validate_json(request.json)
        if 'resultCode' in data and data['resultCode'] == 400:
            response = make_response(jsonify(data), 400)
            return response
        response = Controller.updateCufe(data=data)
        return response
