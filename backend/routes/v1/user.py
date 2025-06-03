from flask import Blueprint, jsonify

from functions import *

user_bp = Blueprint('user', __name__, url_prefix='/v1')


### User
# TODO: Output
@user_bp.route('/user/login', methods=['POST'])
def login():
    json_data = request.get_json()
    needed_parameters = ["benutzername", "password_encrypt"]
    data = json_exctract_and_validate(json_data, needed_parameters)
    
    # Invalid data
    if not data:
        print("Login: No Data")
        return default_error
    
    result = execute_query("SELECT benutzer_id, benutzername FROM benutzer WHERE benutzername=? AND password_encrypt=?", [data["benutzername"], data["password_encrypt"]])
    
    if is_json_empty(result):
        print("Login: Auth issue")
        return default_error
    
    # Save cookie
    # TODO: Maybe change Primary Key?
    session['username'] = result[0]["benutzer_id"]
    #print(result[0])
    
    check_login()

    return result

@user_bp.route('/user/info/<user_id>', methods=['GET'])
def get_user(user_id):
    result = execute_query("SELECT benutzer_id, vorname, nachname, benutzername, email, rolle FROM benutzer WHERE benutzer_id=?", [user_id])
    return result

# TODO: Output
@user_bp.route('/user/logoff', methods=['GET'])
def logoff():
    check_login()
    session.pop('username', None)
    check_login()
    return default_ok

# TODO: Output, GET 
@user_bp.route('/user/username/check/<username>', methods=['POST','GET'])
def check_username(username):
    if is_json_empty(execute_query("SELECT benutzer_id FROM benutzer WHERE benutzername=?", [username])):
        return "False"
    return "True"

# TODO: Output, DB error handling
# Check username availabilty and register user
@user_bp.route('/user/register', methods=['POST'])
def register():
    json_data = request.get_json()
    needed_parameters = ["vorname", "nachname", "benutzername", "email", "rolle", "password_encrypt"]
    data = json_exctract_and_validate(json_data, needed_parameters)

    # TODO: == "True"
    # Check users existence
    if check_username(data["benutzername"]) == "True":
        return "User exists"

    # Invalid data
    if not data:
        return default_error
    data = sort_parameters(data, needed_parameters)
    execute_edit("INSERT INTO benutzer(vorname, nachname, benutzername, email, rolle, password_encrypt) VALUES (?, ?, ?, ?, ?, ?)", data)
    return default_ok

