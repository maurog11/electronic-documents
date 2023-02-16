# -*- coding: utf-8 -*-
#########################################################
from flask import request, jsonify, make_response
from app.controllers import NotesController as Controller
from app.auth import auth_token
from flask_restx import Resource
from app.utils import validate_json
from .schemas import NotesModel, NotesFilterNumberModel, NotesFilterModel, allNotesModel, StatusModel, \
    notesFilterCufeModel, api


@api.route('/all', methods=['POST'])
@api.response(200, 'Registros encontrados')
@api.response(404, 'No se encontraron registros')
@api.response(500, 'Se presentó un error en el servidor.')
class All(Resource):
    decorators = [auth_token.login_required]

    @api.doc('get_all_notes')
    @api.expect(allNotesModel)
    def post(self):
        """

        Consulta envios de notas almacenadas en la base de datos por numero y tamaño de pagina
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

    @api.doc('get_note_by_id')
    def get(self, id):
        """

        Obtiene un envio de nota dado su id
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
    @api.expect(NotesFilterModel)
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
    @api.expect(NotesFilterNumberModel)
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
    @api.expect(NotesFilterNumberModel)
    def post(self):
        """
        Consulta un xml de un documento
        """
        re_json = request.json
        response = Controller.xml(data=re_json)
        return response


@api.route('/status', methods=['POST'])
@api.response(201, 'Documento se encontro en los registros de la DIAN')
@api.param('status', 'Consultar un documento de la DIAN dado su CUFE')
class GetStatus(Resource):
    decorators = [auth_token.login_required]

    @api.expect(StatusModel)
    def post(self):
        """
        Obtiene el estado de un documento de la DIAN dado su CUFE
                """
        data = request.json
        response = Controller.status(data)
        return jsonify(data=response)


@api.route('/new', methods=['POST'])
@api.response(201, 'Nota enviada correctamente')
class NewData(Resource):
    decorators = [auth_token.login_required]

    @api.doc('create_new_note')
    @api.expect(NotesModel)
    def post(self):
        """
        Crea una nueva Nota
        """
        data = validate_json(request.json)
        if 'resultCode' in data and data['resultCode'] == 400:
            response = make_response(jsonify(data), 400)
            return response
        response = Controller.new_data(data=data)
        return response


@api.route('/update', methods=['PUT'])
@api.response(201, 'Nota actualizada correctamente')
class UpdateData(Resource):
    decorators = [auth_token.login_required]

    @api.doc('update_note')
    @api.marshal_with(NotesModel)
    def put(self):
        """

        Actualiza una Nota
        """
        data = request.json
        response = Controller.update_data(data=data)
        return jsonify(data=response)

    @api.route('/update-cufe', methods=['POST'])
    @api.response(201, 'Envio de factura creado correctamente')
    class updateCufe(Resource):
        decorators = [auth_token.login_required]

        @api.doc('update_cufe')
        @api.expect(notesFilterCufeModel)
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
