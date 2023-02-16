# -*- coding: utf-8 -*-
#########################################################
from flask import request, make_response, jsonify
from app.controllers import SendsController as Controller
from app.auth import auth_token
from flask_restx import Resource
from app.utils import validate_json
from .schemas import SendsModel, SendsFilterModel, SendsFilterNumberModel, allInvoicesModel, SendsFilterCufeModel, api

@api.route('/all', methods=['POST'])
@api.response(200, 'Registros encontrados')
@api.response(404, 'No se encontraron registros')
@api.response(500, 'Se presentó un error en el servidor.')
class All(Resource):
    decorators = [auth_token.login_required]

    @api.doc('get_all_sendsinvoices')
    @api.expect(allInvoicesModel)
    def post(self):
        """

        Consulta envios de facturas almacenadas en la base de datos por numero y tamaño de pagina
        """
        data = request.json
        response = Controller.all(data=data)
        return response


@api.route('/data/<int:id>/get', methods=['GET'])
@api.response(401, 'La peticion carece de un id')
@api.response(404, 'Registro no encontrado.')
@api.response(500, 'Se presentó un error en el servidor.')
@api.param('id', 'Identificador de envio')
class GetByid(Resource):
    decorators = [auth_token.login_required]

    @api.doc('get_invoice_by_id')
    def get(self, id):
        """

        Obtiene un envio de factura dado su id
        """
        response = Controller.get_by_id(id)
        return response


@api.route('/getby', methods=['POST'])
@api.response(201, 'Registro encontrado')
@api.response(404, 'Registro no encontrado.')
@api.response(500, 'Se presentó un error en el servidor.')
class GetBy(Resource):
    decorators = [auth_token.login_required]

    @api.doc('get_docs')
    @api.expect(SendsFilterModel)
    def post(self):
        """
        Consulta registros almacenados en la base de datos
        """
        data = request.json
        response = Controller.get_by(data=data)
        return response


@api.route('/pdf-xml', methods=['POST'])
@api.response(201, 'Registro encontrado')
@api.response(400, 'Error al hacer la peticion.')
@api.response(500, 'Se presentó un error en el servidor.')
class Pdf(Resource):
    decorators = [auth_token.login_required]

    @api.doc('pdf')
    @api.expect(SendsFilterNumberModel)
    def post(self):
        """
        Consulta el pdf y el xml de un documento
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
    @api.expect(SendsFilterNumberModel)
    def post(self):
        """
        Consulta un xml de un documento
        """
        re_json = request.json
        response = Controller.xml(data=re_json)
        return response


@api.route('/new', methods=['POST'])
@api.response(201, 'Envio de factura creado correctamente')
class NewData(Resource):
    decorators = [auth_token.login_required]

    @api.doc('create_new_sendinvoice')
    @api.expect(SendsModel)
    def post(self):
        """
        Crea un nuevo envio de Factura
        """
        data = validate_json(request.json)
        if 'resultCode' in data and data['resultCode'] == 400:
            response = make_response(jsonify(data), 400)
            return response
        response = Controller.new_data(data=data)
        return response


@api.route('/update', methods=['PUT'])
@api.response(201, 'Envio de factura actualizado correctamente')
class UpdateData(Resource):
    decorators = [auth_token.login_required]

    @api.doc('update_sendinvoice')
    @api.marshal_with(SendsModel)
    def put(self):
        """

        Actualiza un envio de Factura
        """
        data = request.json
        response = Controller.update_data(data=data)
        return response


@api.route('/update-cufe', methods=['POST'])
@api.response(201, 'Envio de factura creado correctamente')
class updateCufe(Resource):
    decorators = [auth_token.login_required]

    @api.doc('update_cufe')
    @api.expect(SendsFilterCufeModel)
    def post(self):
        """
        Actualiza el cufe de un documento
        """
        data = validate_json(request.json)
        if 'resultCode' in data and data['resultCode'] == 400:
            response = make_response(jsonify(data), 400)
            return response
        response = Controller.new_data(data=data)
        return response


