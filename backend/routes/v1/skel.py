from flask import Blueprint, jsonify

from functions import *

skel_bp = Blueprint('skel', __name__, url_prefix='/v1')

###
@skel_bp.route('/skel', methods=['GET','POST','REMOVE'])
def skel():
    if request.method == 'GET':
        return jsonify({"message": "GET-Methode aufgerufen"}), 200
    
    elif request.method == 'POST':
        data = request.json
        return jsonify({"message": "POST-Methode", "data": data}), 201

    elif request.method == 'DELETE':
        return jsonify({"message": "DELETE-Methode ausgeführt"}), 204

    return jsonify({"error": "Nicht unterstützt"}), 405


########## UNUSED ################