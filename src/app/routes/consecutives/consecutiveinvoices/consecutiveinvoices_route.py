# -*- coding: utf-8 -*-
#########################################################

from flask import request, jsonify
from app.routes.consecutives.consecutiveinvoices import api_consecutiveinvoices as api
from app.controllers import ConsecutiveInvoicesController as Controller


@api.route('/get', methods=['GET'])
def get_all():
    response = Controller.get_all()
    return jsonify(data=response)


@api.route('/data/<int:id>/get', methods=['GET'])
def get_by_id(id: int):
    response = Controller.get_by_id(id=id)
    return jsonify(data=response)


@api.route('/new', methods=['POST'])
def new_data():
    data = request.json
    response = Controller.new_data(data=data)
    return jsonify(data=response)


@api.route('/update', methods=['PUT'])
def update_data():
    data = request.json
    response = Controller.update_data(data=data)
    return jsonify(data=response)


@api.route('/delete/<int:id>', methods=['DELETE'])
def delete_data(id: int):
    response = Controller.delete_data(id=id)
    return jsonify(data=response)
