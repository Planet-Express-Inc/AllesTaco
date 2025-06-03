from flask import Blueprint, jsonify

from functions import *

user_reviews_bp = Blueprint('user_reviews', __name__, url_prefix='/v1')


### Views for aricles
@user_reviews_bp.route('/user/reviews/<foreign_user_id>', methods=['GET','POST','DELETE'])
@user_reviews_bp.route('/user/reviews', methods=['POST'])
def article_reviews(foreign_user_id=None):

    # Get info
    if request.method == 'GET':
        result = execute_query("SELECT bewertung_id, bewerter_id, bewerteter_id, kommentar, rolle_des_bewerteten, sterne FROM bewertung WHERE bewerteter_id=? AND bewerter_id=?", [foreign_user_id, session['username']])
        return jsonify(result), 200
    
    # Auth after that
    if not check_login():
       return jsonify(default_error_no_login), 403

    # Add new
    if request.method == 'POST':
        json_data = request.get_json()

        # Add own user id and foreign user id
        json_data["bewerter_id"] = session['username']
        if foreign_user_id is not None:
            json_data["bewerteter_id"] = foreign_user_id

        needed_parameters = ["bewerter_id", "bewerteter_id", "kommentar", "rolle_des_bewerteten", "sterne"]

        data = json_exctract_and_validate(json_data, needed_parameters)

        if not data:
            return jsonify(default_error), 405
        
        data = sort_parameters(data, needed_parameters)
        if(execute_edit("INSERT INTO bewertung(bewerter_id, bewerteter_id, kommentar, rolle_des_bewerteten, sterne) VALUES (?, ?, ?, ?, ?)", data)):
            return jsonify(default_ok), 201
        
        return jsonify(default_error), 405
    
    # Delete
    if request.method == 'DELETE':
        if(execute_edit("DELETE FROM bewertung WHERE bewerteter_id=? AND bewerter_id=?", [foreign_user_id, session['username']])):
            return jsonify(default_ok), 204
        return jsonify(default_error), 405
