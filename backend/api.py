import sys
import os
import io
import re
import base64

# TODO: Check if needed:
from flask import Flask, request, redirect, jsonify, send_from_directory, url_for, session, render_template_string, send_file, abort
from flask_cors import CORS
import json
import time

import mariadb

#from flasgger import Swagger
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.exceptions import HTTPException


taco = Flask(__name__)

# TODO: Swagger?
# Swagger base config
"""
swagger_config = {
    "spec": {
        "openapi": "3.0.3", 
        "info": {
            "title": "Chat Support - 1.0",
            "description": "Chat Support API 1.0",
            "version": "1.0.0",
        },
    },
    "components": {
        "securitySchemes": {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            }
        }
    },
}
taco.config["SWAGGER"] = swagger_config
taco.config["SWAGGER"]['openapi'] = '3.0.3'

# Load yaml
swagger = Swagger(chat, template_file='swagger/swagger.yaml')
"""
CORS(taco)


# Connect to Database
# Connect to MariaDB Platform
try:
    # Wait for DB
    time.sleep(5)
    conn = mariadb.connect(
        user="taco",
        password="erb6dbfnsm47ptk90i9sw87",
        #host="tacodb",
        # TODO: Prod Server
        ############################################################## TEST
        host="194.164.63.79",
        port=3306,
        database="allestacoDB"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()

## END DB



# Fix for Proxy
taco.wsgi_app = ProxyFix(
    taco.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)


# Default ok for 200 and error
# TODO: Jsonify?
default_ok = {"status": "ok"}

default_error = {"status": "error"}

default_error_not_sup = jsonify({"error": "Not supported"})

# Secret for sessions
taco.secret_key = "super_secret_124g+#f43g"

# Executor with senetization
# Example:
# SELECT ? FROM artikel WHERE id=?, ["preis","1"]
def execute_query(query: str, param: list) -> dict:
    try:
        cur.execute(query, param)
        #result_string = "\n".join([str(row[0]) for row in result])
        ############################ CRASH HIER BEI INSERT!
        ## bsp: INSERT INTO benutzer(vorname, nachname, benutzername, email, rolle, password_encrypt) VALUES ("test","test","test","test","käufer","test"); 
        ## Abfrage einbauen ob SELECT oder -> INSERT bzw. ohne Return Value
        columns = [desc[0] for desc in cur.description]
        data = cur.fetchall()
        result = [dict(zip(columns, row)) for row in data]
        #result_json = json.dumps(result, indent=2)
    except mariadb.Error as e:
        result_string = f"Error connecting to MariaDB Platform: {e}"
        print(f"Error connecting to MariaDB Platform: {e}")
        ##### RETURN FOR ERROR???
        return default_error
    return result

# Execute an edit e.g. INSERT in DB
def execute_edit(query: str, param: list):
    try:
        cur.execute(query, param)
        conn.commit()
    except mariadb.Error as e:
        print(f"Error while editing DB: {e}")

# Download blob data from database
# TODO: Not working. Extractig minetype, Siehe GPT
def download_data(query: str, param: str, filename:str):
    try:
        cur.execute(query, param)
        result = cur.fetchone()
        if result is None:
            print("File not found")
            abort(404, "File not found")
            return False
        ### New Format #### TEST
        result = result[0].decode("UTF-8")
        #print(type(result))
        #print(result)
        match = re.match(r"data:(.*?);base64,(.*)", result)
        #print(match)
        if not match:
            abort(400, "File not valid")
        mimetype, b64_data = match.groups()
        binary_data = base64.b64decode(b64_data)

        return send_file(
            io.BytesIO(binary_data),
            download_name=filename,
            mimetype=mimetype,
            as_attachment=False
        )

    except mariadb.Error as e:
        print(f"Error with DB: {e}")


def is_json_empty(json_obj: dict) -> bool:
    if not json_obj:
        return True
    return False

# Extract, order and validate completeness of parameters
def json_exctract_and_validate(json_obj:json, keys: list):
    # If list -> extract dict
    if isinstance(json_obj, list):
        json_obj = json_obj[0]
    
    result = {}
    for key in keys:
        try:
            result[key] = json_obj.get(key)
        except Exception as e:
            print(e)
            return False
    return result

# sort parameters for sql query
def sort_parameters(input: dict, sort:list) -> list:
    out = []
    for item in sort:
        if item in input:
            out.append(input[item])
        else:
            print("Item not found: " + item)
    return out

# Check user login
def check_login() -> bool:
    if 'username' in session:
        print(f"Check login for {session['username']}, True")
        return True
    return False


### Routes

### Routes for testing  #######
@taco.route('/v1/system/status/api', methods=['GET'])
def taco_test():
    return "Mit der API ist alles Taco!"

# State of database
@taco.route('/v1/system/status/db', methods=['GET'])
def taco_test_db():
    try:
        cur.execute("SELECT name FROM taco_stack_test LIMIT 1")
        result = cur.fetchall()
        result_string = "\n".join([str(row[0]) for row in result])
    except mariadb.Error as e:
        result_string = f"Error connecting to MariaDB Platform: {e}"
        print(f"Error connecting to MariaDB Platform: {e}")
    print(result_string) ##### DEBUG
    return result_string

### End testing

### Static content
# Favicon, because we can. And less errors for modern browsers in logs
@taco.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(taco.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

### User
# TODO: Output
@taco.route('/v1/user/login', methods=['POST'])
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
    session['username'] = result[0]["benutzername"]
    #print(result[0])
    
    check_login()

    return result

@taco.route('/v1/user/info/<user_id>', methods=['POST','GET'])
def get_user(user_id):
    result = execute_query("SELECT benutzer_id, vorname, nachname, benutzername, email, rolle FROM benutzer WHERE benutzer_id=?", [user_id])
    return result

# TODO: Output
@taco.route('/v1/user/logoff', methods=['POST','GET'])
def logoff():
    session.pop('username', None)
    check_login()
    return default_ok

# TODO: Output, GET 
@taco.route('/v1/user/username/check/<username>', methods=['POST','GET'])
def check_username(username):
    if is_json_empty(execute_query("SELECT benutzer_id FROM benutzer WHERE benutzername=?", [username])):
        return "False"
    return "True"

# TODO: Output, DB error handling
# Check username availabilty and register user
@taco.route('/v1/user/register', methods=['POST'])
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

### Article
# TODO: Get for Picture -> Issue with JSON,  NAmen ändern:
@taco.route('/v1/article/get/info/<article_id>', methods=['POST','GET'])
def get_article(article_id):
    result = execute_query("SELECT artikel_id, titel, verkaeufer_id, beschreibung, preis, status, bestand, kategorie FROM artikel WHERE artikel_id=?", [article_id])
    return result

# TODO: GET
@taco.route('/v1/article/get/picture/<article_id>', methods=['POST', 'GET'])
def get_article_picture(article_id):
    result = download_data("SELECT bild FROM artikel WHERE artikel_id=?", [article_id], article_id)
    #print(result)
    return result

### Logged in methods
# TODO: Login!!!, Methoden auf GET, POST(ADD), Delete umbauen
@taco.route('/v1/article/add', methods=['POST'])
def new_article():
    # if not check_login():
    #    return "No Login"
    
    json_data = request.get_json()
    needed_parameters = ["titel", "verkaeufer_id", "beschreibung", "preis", "bild", "status", "bestand", "kategorie"]
    data = json_exctract_and_validate(json_data, needed_parameters)

    if not data:
        return default_error
    
    data = sort_parameters(data, needed_parameters)
    execute_edit("INSERT INTO artikel(titel, verkaeufer_id, beschreibung, preis, bild, status, bestand, kategorie) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", data)
    return default_ok

# TODO: Output, Login!!!
@taco.route('/v1/article/delete/<article_id>', methods=['POST','GET'])
def delete_article(article_id):
    # if not check_login():
    #    return "No Login"
    
    execute_edit("DELETE FROM artikel WHERE artikel_id=?", [article_id])
    return default_ok


#### TODO: Ab heur neues Schema. Oben korrigiern

##### Skel for Routes
@taco.route('/v1/skel', methods=['GET','POST','REMOVE'])
def skel():
    if request.method == 'GET':
        return jsonify({"message": "GET-Methode aufgerufen"}), 200

    elif request.method == 'POST':
        data = request.json
        return jsonify({"message": "POST-Methode", "data": data}), 201

    elif request.method == 'DELETE':
        return jsonify({"message": "DELETE-Methode ausgeführt"}), 204

    return jsonify({"error": "Nicht unterstützt"}), 405

##### SKEL END

### Cart
@taco.route('/v1/cart', methods=['GET','POST','REMOVE'])
def cart():
    if request.method == 'GET':
        return jsonify({"message": "GET-Methode aufgerufen"}), 200

    elif request.method == 'POST':
        data = request.json
        return jsonify({"message": "POST-Methode", "data": data}), 201

    elif request.method == 'DELETE':
        return jsonify({"message": "DELETE-Methode ausgeführt"}), 204

    return default_error_not_sup, 405



# Gerneric errror handler
@taco.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


if __name__ == '__main__':
    # Disable debug, when deployed in a container, for production use
    debug = False
    debug = True ###############################################################################################
    if len( sys.argv ) > 1:
        first_arg = str(sys.argv[1])
        if first_arg.lower() == "debug":
            debug=True
            print("Debug enabled!")
    
    # Logging
    #sys.stdout = open('logs/flask_output.log', 'w')
    sys.stderr = open('logs/flask_error.log', 'w')

    # Run
    taco.run(host='0.0.0.0', port=5000, debug=debug)