import json

def is_json_empty(json_obj):
    # return true if length is 0.
    return len(json_obj) == 0

json_obj = ["a"]  # Empty JSON object
#print(is_json_empty(json_obj))


def json_exctract_and_validate(json_obj:json, keys: list):
    result = {}
    for key in keys:
        try:
            result[key] = json_obj[0].get(key)
        except Exception as e:
            print(e)
            return False
    return result



test = json.loads('[{"vorname": "Niclas", "nachname": "Sieveneck", "benutzername": "ntr0py123", "email": "info@niclas-sieveneck.de", "rolle": "käufer", "password_encrypt": "1234"}]')
#test = '"vorname": "Niclas", "nachname": "Sieveneck", "benutzername": "ntr0py123", "email": "info@niclas-sieveneck.de", "rolle": "käufer", "password_encrypt": "1234"'


#print(json_exctract_and_validate(test,["vorname", "nachname", "benutzername", "email", "rolle", "password_encrypt"]))


test = [
  {
    "benutzer_id": 6,
    "benutzername": "ntr0py123"
  }
]

#print(test["benutzer_id"])

from datetime import datetime, timedelta


shipping_date = (datetime.now() + timedelta(days=2)).strftime("%d.%m.%Y")

print(shipping_date)