import io
import re
import base64

from flask import Flask, request, redirect, jsonify, send_from_directory, url_for, session, render_template_string, send_file, abort
import json
import time

from datetime import datetime, timedelta

import mariadb
from mariadb import ConnectionPool

from default_codes import * 

import bcrypt


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

### Helper for "shipping"
def get_shipping_info() -> str:
    shipping_date = (datetime.now() + timedelta(days=2)).strftime("%d.%m.%Y")
    shipping_str = "Ihre Bestellung wird " + shipping_date + " vorraussichtlich geliefert."
    return shipping_str

# Get Date for SQL
def get_sql_date() -> str:
    return datetime.now().strftime("%Y-%m-%d")

# Split SQL date into dict
def split_sql_date(input: str) -> dict:
    input = input.split("-")
    out = {}
    if len(input) > 2:
        out["year"]  = input[0]
        out["month"] = input[1]
        out["day"]   = input[2]
    return out

# Hash and salt password
def password_init(unencypt: str) -> str:
    # Charset
    unencypt = unencypt.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(unencypt, salt)
    return hashed, salt

# Check PW length
def check_password_length(pw: str) -> bool:
    if len(pw) >= 8:
        return True
    return False

# Check pw for login
def check_password_login(pw_input: str, pw_db) -> bool:
    if bcrypt.checkpw(pw_input, pw_db):
        return True
    return False

# Global pool
pool = connect_database(
            user="taco",
            password="erb6dbfnsm47ptk90i9sw87",
            host="tacodb",
            port=3306,
            database="allestacoDB",
            pool_size=10
            )
