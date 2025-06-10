from flask import Blueprint, jsonify

from functions import *

article_views_bp = Blueprint('article_views', __name__, url_prefix='/v1')


### Views for aricles
@article_views_bp.route('/article/views/<artikel_id>', methods=['GET', 'POST', 'DELETE'])
@article_views_bp.route('/article/views', methods=['GET','POST'])
def article_views(artikel_id=None):

    # Get info
    if request.method == 'GET':
        result = execute_query("SELECT aufrufer_id, artikel_id, anzahl FROM aufrufe WHERE artikel_id=?", [artikel_id])
        return jsonify(result), 200
    
    # Auth after that
    if not check_login():
       return jsonify(default_error_no_login), 403

    # Add new
    if request.method == 'POST':
        json_data = request.get_json()

        # Add aricle_id
        if artikel_id is not None:
            json_data["artikel_id"] = artikel_id

        needed_parameters = ["artikel_id", "anzahl"]

        data = json_exctract_and_validate(json_data, needed_parameters)

        if not data:
            return jsonify(default_error), 405
        
        data = sort_parameters(data, needed_parameters)
        if(execute_edit("INSERT INTO aufrufe(artikel_id, anzahl) VALUES (?, ?)", data)):
            return jsonify(default_ok), 201
        
        return jsonify(default_error), 405
    
    # Delete
    if request.method == 'DELETE':
        if(execute_edit("DELETE FROM aufrufe WHERE artikel_id=?", [artikel_id])):
            return jsonify(default_ok), 204
        return jsonify(default_error), 405
