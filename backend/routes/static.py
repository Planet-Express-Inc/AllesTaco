from flask import Blueprint, jsonify
import os

from functions import *

static_bp = Blueprint('static', __name__)


### Static content
# Favicon, because we can. And less errors for modern browsers in logs
@static_bp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(static_bp.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

