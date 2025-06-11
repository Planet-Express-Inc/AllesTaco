import io
import re
import base64

# TODO: Check if needed:
from flask import Flask, request, redirect, jsonify, send_from_directory, url_for, session, render_template_string, send_file, abort
import json
import time

import mariadb
from mariadb import ConnectionPool

from default_codes import * 


# Connect to Database (generic)
def connect_database(user: str, password: str, host: str, port: int, database: str, pool_size: int) -> ConnectionPool:
    # Connect to MariaDB Platform
    try:
        # Wait for DB and open Pool
        time.sleep(5)
        pool = ConnectionPool(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database,
            pool_name="pool",
            pool_size=pool_size
        )

        print("Connected to MariaDB Platform.")
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        #sys.exit(1)
        time.sleep(5)
        raise

    return pool


# Executor with senetization
# Example:
# SELECT ? FROM artikel WHERE id=?, ["preis","1"]
def execute_query(query: str, param: list) -> dict:
    try:
        # Get conn
        conn = pool.get_connection()
        cur = conn.cursor()

        cur.execute(query, param)
        columns = [desc[0] for desc in cur.description]
        data = cur.fetchall()

        result = [dict(zip(columns, row)) for row in data]
        #result_json = json.dumps(result, indent=2)
    except mariadb.Error as e:
        conn.close()
        result_string = f"Error connecting to MariaDB Platform: {e}"
        print(f"Error connecting to MariaDB Platform: {e}")
        ##### RETURN FOR ERROR???
        return default_error
    finally:
        if conn:
            conn.close()
    return result

# Execute an edit e.g. INSERT in DB
def execute_edit(query: str, param: list) -> bool:
    try:
        # Get conn
        conn = pool.get_connection()
        cur = conn.cursor()

        cur.execute(query, param)
        conn.commit()

        return True
    except mariadb.Error as e:
        conn.close()
        print(f"Error while editing DB: {e}")
    finally:
        if conn:
            conn.close()
    return False

# Download blob data from database
# TODO: Not working. Extractig minetype, Siehe GPT
def download_data(query: str, param: str, filename:str):
    try:
        # Get conn
        conn = pool.get_connection()
        cur = conn.cursor()

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
        conn.close()
        print(f"Error with DB: {e}")
    finally:
        if conn:
            conn.close()


### Non DB funcitons
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

# Global pool
pool = connect_database(
            user="taco",
            password="erb6dbfnsm47ptk90i9sw87",
            #host="tacodb",
            # TODO: Prod Server
            ############################################################## TEST
            host="194.164.63.79",
            port=3306,
            database="allestacoDB",
            pool_size=10
            )
