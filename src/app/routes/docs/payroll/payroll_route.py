# -*- coding: utf-8 -*-
#########################################################

from flask import request, jsonify, make_response
from app.auth import auth_token
from app.controllers import PayRollSendsController as Controller
from flask_restx import Resource
from app.utils import validate_json
from .schemas import PayRollModel, PayRollNotesModel, GetStatusModel, PayRollFilterModel, PayRollFilterNumberModel,\
    allPayRollModel, payrollFilterCufeModel, api


@api.route('/all', methods=['POST'])
@api.response(200, 'Registros encontrados')
@api.response(404, 'No se encontraron registros')
@api.response(500, 'Se presentó un error en el servidor.')
class All(Resource):
    decorators = [auth_token.login_required]

    @api.doc('get_all_payrolls')
    @api.expect(allPayRollModel)
    def post(self):
        """
        Consulta las nominas almacenadas en la base de datos por numero y tamaño de pagina
        """
        data = request.json
        response = Controller.all(data=data)
        return response


@api.route('/getby', methods=['POST'])
@api.response(201, 'Registro encontrado')
@api.response(404, 'Registro no encontrado.')
@api.response(500, 'Se presentó un error en el servidor.')
class GetBy(Resource):
    decorators = [auth_token.login_required]

    @api.doc('create_new_')
    @api.expect(PayRollFilterModel)
    def post(self):
        """
        Consulta registros almacenados en la base de datos por rango de fecha
        """
        data = request.json
        response = Controller.get_by(data=data)
        return response


@api.route('/data/<int:id>/get', methods=['GET'])
@api.response(401, 'La peticion carece de un id')
@api.response(404, 'Registro no encontrado.')
@api.response(500, 'Se presentó un error en el servidor.')
@api.param('id', 'Identificador de Nomina')
class GetByid(Resource):
    decorators = [auth_token.login_required]

    @api.doc('get_payroll_by_id')
    def get(self, id):
        """
        Obtiene una nomina dado su id
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
    @api.expect(PayRollFilterNumberModel)
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
    @api.expect(PayRollFilterNumberModel)
    def post(self):
        """
        Consulta un xml de un documento
        """
        re_json = request.json
        response = Controller.xml(data=re_json)
        return response


@api.route('/status', methods=['POST'])
@api.response(200, 'Documento se encontro en los registros de la DIAN')
@api.response(404, 'Documento no se encontro en los registros')
class Status(Resource):
    decorators = [auth_token.login_required]

    @api.expect(GetStatusModel)
    def post(self):
        """
        Obtiene el estado de un documento de la DIAN dado su CUFE
                """
        data = request.json
        response = Controller.status(data)
        return response


@api.route('/new', methods=['POST'])
@api.response(201, 'Nomina enviada correctamente')
@api.response(404, 'No se pudo enviar la nomina')
class NewData(Resource):
    decorators = [auth_token.login_required]

    @api.doc('create_new_payroll')
    @api.expect(PayRollModel)
    def post(self):
        """
        Crea una nueva Nomina
        """
        not_validate = [
            'CUNEPredecesor',
            'FechaGenPredecesor',
            'NumeroDocumentoPredecesor',
            'OtrosNombres',
            'SegundoApellido',
            'CorreoElectronico',
            'TipoCuenta'
        ]
        data = validate_json(request.json, to_not_validate=not_validate)
        if 'resultCode' in data and data['resultCode'] == 400:
            response = make_response(jsonify(data), 400)
            return response
        response = Controller.new_data(data)
        return response


@api.route('/new_note', methods=['POST'])
@api.response(201, 'Nota enviada correctamente')
@api.response(404, 'Nota no se pudo enviar')
class NewNote(Resource):
    decorators = [auth_token.login_required]

    @api.doc('create_new_payrollnote')
    @api.expect(PayRollNotesModel)
    def post(self):
        """
        Crea una nueva Nota de Nomina
        """
        not_validate = [
            'OtrosNombres',
            'SegundoApellido',
            'CorreoElectronico'
        ]
        data = validate_json(request.json, to_not_validate=not_validate)
        if 'resultCode' in data and data['resultCode'] == 400:
            response = make_response(jsonify(data), 400)
            return response
        response = Controller.new_note(data)
        return response


@api.route('/update', methods=['PUT'])
@api.response(201, 'Nota actualizada correctamente')
@api.response(404, 'No se pudo actualizar la nota')
class UpdateData(Resource):
    decorators = [auth_token.login_required]

    @api.doc('update_payroll')
    @api.marshal_with(PayRollModel)
    def put(self):
        """
        Actualiza una Nomina
        """
        data = request.json
        response = Controller.update_data(data=data)
        return response


@api.route('/update-cufe', methods=['POST'])
@api.response(201, 'Envio de factura creado correctamente')
class updateCufe(Resource):
    decorators = [auth_token.login_required]

    @api.doc('update_cufe')
    @api.expect(payrollFilterCufeModel)
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

