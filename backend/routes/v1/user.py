from flask import Blueprint, jsonify, make_response

from functions import *

user_bp = Blueprint('user', __name__, url_prefix='/v1')


### User
@user_bp.route('/user/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        json_data = request.get_json()
        needed_parameters = ["benutzername", "password_encrypt"]
        data = json_exctract_and_validate(json_data, needed_parameters)
        
        # Invalid data
        if not data:
            print("Login: No Data")
            return jsonify({"error": "Login: No Data"}), 405
        
        result = execute_query("SELECT benutzer_id, benutzername, vorname, nachname, email, rolle, password_encrypt FROM benutzer WHERE benutzername=?", [data["benutzername"]])
        
        if is_json_empty(result):
            print("Login: Auth issue")
            return jsonify({"error": "Login: Auth issue"}), 403
        
        # Check password
        if not check_password_login(data["password_encrypt"], result[0]["password_encrypt"]):
            return jsonify({"error": "Login: Auth issue"}), 403
        
        # Save cookie
        session['username'] = result[0]["benutzer_id"]

        # Remove PW from output^^
        result[0].pop("password_encrypt")

        check_login()
        
        return jsonify(result), 201        
    
    if request.method == 'GET':
        if check_login():
            result = execute_query("SELECT benutzer_id, benutzername, vorname, nachname, email, rolle, password_encrypt FROM benutzer WHERE benutzer_id=?", [session['username']])
            return jsonify(result), 200
        return jsonify(default_error_no_login), 403
    
    return jsonify(default_error), 405

@user_bp.route('/user/info/<user_id>', methods=['GET'])
def get_user(user_id):
    result = execute_query("SELECT benutzer_id, vorname, nachname, benutzername, email, rolle FROM benutzer WHERE benutzer_id=?", [user_id])
    return jsonify(result), 200

@user_bp.route('/user/logoff', methods=['GET'])
def logoff():
    check_login()
    session.pop('username', None)
    check_login()
    return jsonify(default_ok), 200

@user_bp.route('/user/username/check/<username>', methods=['POST','GET'])
def check_username(username):
    if is_json_empty(execute_query("SELECT benutzer_id FROM benutzer WHERE benutzername=?", [username])):
        return jsonify({"status": "User does not exist"}), 200
    return jsonify({"status": "User exists"}), 200

# Check username availabilty and register user
@user_bp.route('/user/register', methods=['POST'])
def register():
    json_data = request.get_json()
    needed_parameters = ["vorname", "nachname", "benutzername", "email", "rolle", "password_encrypt"]

    if not json_data["benutzername"]:
        return jsonify({"error": "Username empty"}), 405
    
    if not json_data["password_encrypt"]:
        return jsonify({"error": "Password empty"}), 405
    
    if not check_password_length(json_data["password_encrypt"]):
        return jsonify({"error": "Password to short"}), 405
    
    # Hash and salt
    json_data["password_encrypt"] = password_init(json_data["password_encrypt"])

    data = json_exctract_and_validate(json_data, needed_parameters)


    # Check users existence
    if not is_json_empty(execute_query("SELECT benutzer_id FROM benutzer WHERE benutzername=?", [data["benutzername"]])):
        return jsonify({"error": "User exists"}), 405

    # Invalid data
    if not data:
        return jsonify(default_error), 405
    data = sort_parameters(data, needed_parameters)
    execute_edit("INSERT INTO benutzer(vorname, nachname, benutzername, email, rolle, password_encrypt) VALUES (?, ?, ?, ?, ?, ?)", data)
    return jsonify(default_ok), 201

