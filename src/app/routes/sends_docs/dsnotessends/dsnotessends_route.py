from flask import request, jsonify, make_response
from app.controllers import InvoicesController as Controller
from app.controllers import NotesSendsController as ControllerN
from app.auth import auth_token
from flask_restx import Resource
from app.utils import validate_json
from .schemas import DsNotesSendsModel, DsNotesSendsFilterModel, DsNotesSendsFilterNumberModel, allNotesSdModel, api


@api.route('/all', methods=['POST'])
@api.response(200, 'Registros encontrados')
@api.response(404, 'No se encontraron registros')
@api.response(500, 'Se presentó un error en el servidor.')
class All(Resource):
    decorators = [auth_token.login_required]

    @api.doc('get_all_supportdocs_notes')
    @api.expect(allNotesSdModel)
    def post(self):
        """

        Consulta envios de notas de documento soporte almacenadas en la base de datos por numero y tamaño de pagina
        """
        data = request.json
        response = ControllerN.all(data=data)
        return response


@api.route('/data/<int:id>/get', methods=['GET'])
@api.response(401, 'La peticion carece de un id')
@api.response(404, 'Registro no encontrado.')
@api.response(500, 'Se presentó un error en el servidor.')
@api.param('id', 'Identificador de envio')
class GetByid(Resource):
    decorators = [auth_token.login_required]

    @api.doc('get_supportdoc_note_by_id')
    def get(self, id):
        """

        Obtiene un envio de nota de documento soporte dado su id
        """
        response = ControllerN.get_by_id(id)
        return response


@api.route('/getby', methods=['POST'])
@api.response(201, 'Registro encontrado')
@api.response(404, 'Registro no encontrado.')
@api.response(500, 'Se presentó un error en el servidor.')
class GetBy(Resource):
    decorators = [auth_token.login_required]

    @api.doc('get_docs')
    @api.expect(DsNotesSendsFilterModel)
    def post(self):
        """
        Consulta registros almacenados en la base de datos
        """
        data = request.json
        response = ControllerN.get_by(data=data)
        return response


@api.route('/pdf-xml', methods=['POST'])
@api.response(201, 'Registro encontrado')
@api.response(400, 'Error al hacer la peticion.')
@api.response(500, 'Se presentó un error en el servidor.')
class Pdf(Resource):
    decorators = [auth_token.login_required]

    @api.doc('pdf')
    @api.expect(DsNotesSendsFilterNumberModel)
    def post(self):
        """
        Consulta el pdf y el xml de un documento
        """
        re_json = request.json
        response = ControllerN.pdf(data=re_json)
        return response


@api.route('/xml', methods=['POST'])
@api.response(201, 'Registro encontrado')
@api.response(400, 'Error al hacer la peticion.')
@api.response(500, 'Se presentó un error en el servidor.')
class Xml(Resource):
    decorators = [auth_token.login_required]

    @api.doc('xml')
    @api.expect(DsNotesSendsFilterNumberModel)
    def post(self):
        """
        Consulta un xml de un documento
        """
        re_json = request.json
        response = ControllerN.xml(data=re_json)
        return response


@api.route('/new', methods=['POST'])
@api.response(404, 'Registro no encontrado')
@api.response(500, 'Se presentó un error en el servidor.')
@api.response(201, 'Nota documento soporte enviada')
class NewData(Resource):
    # decorators = [auth_token.login_required]

    @api.doc('create_new_dssend')
    @api.expect(DsNotesSendsModel)
    def post(self):
        """
        Crea un nuevo envio de Nota Documento Soporte
        """
        not_validate = [
            'CheckDigit'
        ]
        data = validate_json(request.json, to_not_validate=not_validate)
        if 'resultCode' in data and data['resultCode'] == 400:
            response = make_response(jsonify(data), 400)
            return response
        response = Controller.new_note_ds(data=data)
        return response


@api.route('/update', methods=['PUT'])
@api.response(404, 'Registro no encontrado')
@api.response(500, 'Se presentó un error en el servidor.')
@api.response(201, 'Nota documento soporte modificada')
class UpdateData(Resource):
    decorators = [auth_token.login_required]

    @api.doc('update_dssend')
    @api.marshal_with(DsNotesSendsModel)
    def put(self):
        """

        Actualiza un envio de Nota Documento Soporte
        """
        data = request.json
        response = Controller.update_data(data=data)
        return jsonify(data=response)


