import sys
import os
import io
import re
import base64

# TODO: Check if needed:
from flask import Flask, request, redirect, jsonify, send_from_directory, url_for, session, render_template_string, send_file, abort
from flask_cors import CORS
import json


import mariadb

#from flasgger import Swagger
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.exceptions import HTTPException

# Uitltys
from functions import *

# Blueprints
from routes import register_blueprints

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
# CORS
CORS(taco)

# Fix for Proxy
taco.wsgi_app = ProxyFix(
    taco.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

# Secret for sessions
taco.secret_key = "super_secret_124g+#f43g"

### Routes
# Get from Blueprints
register_blueprints(taco)


### Cart
@taco.route('/v1/cart', methods=['GET','POST','REMOVE'])
def cart():
    if not check_login():
        return default_error_no_login
    
    # session['username']
    
    if request.method == 'GET':
        result = execute_query("SELECT warenkorb_id FROM artikel WHERE kaeufer_id=?", session['username'])
        print("cart-get: ")
        print(result)
        #####
        return jsonify(result), 200

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
    if not debug:
        sys.stdout = open('logs/flask_output.log', 'w')
    sys.stderr = open('logs/flask_error.log', 'w')

    # Run
    taco.run(host='0.0.0.0', port=5000, debug=debug)