from flask import Blueprint, jsonify

from functions import *

cart_bp = Blueprint('cart', __name__, url_prefix='/v1')


### Cart
# TODO: all, Swagger!
@cart_bp.route('/cart/<article_id>', methods=['DELETE'])
@cart_bp.route('/cart', methods=['GET','POST'])
def cart(article_id=None):
    if not check_login():
        return jsonify(default_error_no_login), 403
    
    if request.method == 'GET':
        result = execute_query("SELECT benutzer_id, artikel_id, anzahl, verkaeufer_id FROM warenkorb WHERE benutzer_id=?", [session['username']])
        return jsonify(result), 200

    # Add new
    elif request.method == 'POST':
        json_data = request.get_json()
        needed_parameters = ["benutzer_id", "artikel_id", "anzahl", "verkaeufer_id"]

        # Add user id
        json_data["kaeufer_id"] = session['username']

        data = json_exctract_and_validate(json_data, needed_parameters)

        if not data:
            return jsonify(default_error), 405
        
        data = sort_parameters(data, needed_parameters)
        execute_edit("INSERT INTO warenkorb(benutzer_id, artikel_id, anzahl, verkaeufer_id) VALUES (?, ?, ?, ?)", data)
        return jsonify(default_ok), 201

    elif request.method == 'DELETE':
        execute_edit("DELETE FROM warenkorb WHERE artikel_id=?", [article_id])
        return jsonify(default_ok), 204

    return default_error_not_sup, 405