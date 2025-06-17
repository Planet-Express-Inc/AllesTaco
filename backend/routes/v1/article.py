from flask import Blueprint, jsonify

from functions import *

article_bp = Blueprint('article', __name__, url_prefix='/v1')


### Article
@article_bp.route('/article/<article_id>', methods=['GET', 'DELETE'])
@article_bp.route('/article', methods=['POST'])
def article(article_id=None):
    # Get info
    if request.method == 'GET':
        result = execute_query("SELECT artikel_id, titel, verkaeufer_id, beschreibung, preis, status, bestand, kategorie FROM artikel WHERE artikel_id=?", [article_id])
        return jsonify(result), 200
    
    # Auth after that
    if not check_login():
       return jsonify(default_error_no_login), 403

    # Add new
    if request.method == 'POST':
        json_data = request.get_json()
        needed_parameters = ["titel", "verkaeufer_id", "beschreibung", "preis", "bild", "status", "bestand", "kategorie"]

        # Add user id
        json_data["verkaeufer_id"] = session['username']

        data = json_exctract_and_validate(json_data, needed_parameters)

        if not data:
            return jsonify(default_error), 405
        
        data = sort_parameters(data, needed_parameters)
        execute_edit("INSERT INTO artikel(titel, verkaeufer_id, beschreibung, preis, bild, status, bestand, kategorie) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", data)
        return jsonify(default_ok), 201
    
    # Delete
    if request.method == 'DELETE':
        execute_edit("DELETE FROM artikel WHERE artikel_id=? AND verkaeufer_id=?", [article_id, session['username']])
        return jsonify(default_ok), 204

# Picture for article
@article_bp.route('/article/picture/<article_id>', methods=['GET'])
def get_article_picture(article_id):
    result = download_data("SELECT bild FROM artikel WHERE artikel_id=?", [article_id], article_id)
    return result, 200

# Search
@article_bp.route('/article/search/<search_str>', methods=['GET'])
def search_article(search_str):
    result = execute_query("SELECT artikel_id, titel, verkaeufer_id, beschreibung, preis, status, bestand, kategorie FROM artikel WHERE titel LIKE ? OR beschreibung LIKE ?", [f"%{search_str}%", f"%{search_str}%"])
    return jsonify(result), 200

# Search
@article_bp.route('/article/multiple', methods=['POST'])
def multiple_article():
    json_data = request.get_json()
    result = execute_query("SELECT artikel_id, titel, verkaeufer_id, beschreibung, preis, status, bestand, kategorie FROM artikel LIMIT ? OFFSET ?", [json_data["number"], json_data["offset"]])
    return jsonify(result), 200


@article_bp.route('/article/user/<user_id>', methods=['GET'])
def article_by_user(user_id):
    # Get info
    if request.method == 'GET':
        result = execute_query("SELECT artikel_id, titel, verkaeufer_id, beschreibung, preis, status, bestand, kategorie FROM artikel WHERE verkaeufer_id=?", [user_id])
        return jsonify(result), 200
    