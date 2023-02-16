# -*- coding: utf-8 -*-
#########################################################
from flask import request, make_response, jsonify
from app.controllers import NotesSendsController as Controller
from app.auth import auth_token
from flask_restx import Resource
from app.utils import validate_json
from .schemas import NotesSendsModel, NotesSendsFilterModel, NotesSendsFilterNumberModel, allNotesModel, api


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
        Consulta notas almacenadas en la base de datos por numero y tamaño de pagina
        """
        data = request.json
        response = Controller.all(data=data)
        return response


@api.route('/data/<int:id>/get', methods=['GET'])
@api.response(401, 'La peticion carece de un id')
@api.response(404, 'Registro no encontrado.')
@api.response(500, 'Se presentó un error en el servidor.')
@api.param('id', 'Identificador de Envio de Nota')
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

    @api.doc('create_new_')
    @api.expect(NotesSendsFilterModel)
    def post(self):
        """
        Consulta registros almacenados en la base de datos por rango de fecha
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
    @api.expect(NotesSendsFilterNumberModel)
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

    @api.doc('xml_note')
    @api.expect(NotesSendsFilterNumberModel)
    def post(self):
        """
        Consulta un xml de un documento
        """
        re_json = request.json
        response = Controller.xml(data=re_json)
        return response


@api.route('/new', methods=['POST'])
@api.response(201, 'Envio de nota creado correctamente')
class NewData(Resource):
    decorators = [auth_token.login_required]

    @api.doc('create_new_notesend')
    @api.expect(NotesSendsModel)
    def post(self):
        """

        Crea un nuevo envio de Nota
        """
        data = validate_json(request.json)
        if 'resultCode' in data and data['resultCode'] == 400:
            response = make_response(jsonify(data), 400)
            return response
        response = Controller.new_data(data=data)
        return response


@api.route('/update', methods=['PUT'])
@api.response(201, 'Envio de nota actualizado correctamente')
class UpdateData(Resource):
    decorators = [auth_token.login_required]

    @api.doc('update_notesend')
    @api.marshal_with(NotesSendsModel)
    def put(self):
        """
        Actualiza un envio de Nota
        """
        data = request.json
        response = Controller.update_data(data=data)
        return response



