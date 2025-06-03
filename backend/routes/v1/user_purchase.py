from flask import Blueprint, jsonify

from functions import *

user_purchase_bp = Blueprint('user_purchase', __name__, url_prefix='/v1')

### Get/Remove all purchases for a user
@user_purchase_bp.route('/user/purchase', methods=['POST', 'GET', 'DELETE'])
def purchase(kaeufer_id=None):
    if not check_login():
        return jsonify(default_error_no_login), 403

    # Get info
    if request.method == 'GET':
        result = execute_query("SELECT kauf_id, kaeufer_id, artikel_id, versanddaten, kaufpreis FROM abgeschlossene_kaeufe WHERE kaeufer_id=?", [session['username']])
        return jsonify(result), 200
    
    # Add new
    if request.method == 'POST':
        json_data = request.get_json()
        needed_parameters = ["kaeufer_id", "artikel_id", "versanddaten", "kaufpreis"]
        # Add user id
        json_data["kaeufer_id"] = session['username']

        data = json_exctract_and_validate(json_data, needed_parameters)

        if not data:
            return jsonify(default_error), 405
        
        data = sort_parameters(data, needed_parameters)
        if(execute_edit("INSERT INTO abgeschlossene_kaeufe(kaeufer_id, artikel_id, versanddaten, kaufpreis) VALUES (?, ?, ?, ?)", data)):
            return jsonify(default_ok), 201
        
        return jsonify(default_error), 405
    
    # Delete
    if request.method == 'DELETE':
        if(execute_edit("DELETE FROM abgeschlossene_kaeufe WHERE kaeufer_id=?", [session['username']])):
            return jsonify(default_ok), 204
        return jsonify(default_error), 405

