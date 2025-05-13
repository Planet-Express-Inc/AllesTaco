import json

def is_json_empty(json_obj):
    # return true if length is 0.
    return len(json_obj) == 0

json_obj = ["a"]  # Empty JSON object
print(is_json_empty(json_obj))


def json_exctract_and_validate(json_obj:json, keys: list):
    result = {}
    print(json_obj)
    print(type(json_obj))
    for key in keys:
        try:
            print(key) #################
            result[key] = json_obj.get(key)
            print(json_obj.get(key))
        except Exception as e:
            print(e)
            return False
    return result



test = json.loads('[{"vorname": "Niclas", "nachname": "Sieveneck", "benutzername": "ntr0py123", "email": "info@niclas-sieveneck.de", "rolle": "käufer", "password_encrypt": "1234"}]')
#test = '"vorname": "Niclas", "nachname": "Sieveneck", "benutzername": "ntr0py123", "email": "info@niclas-sieveneck.de", "rolle": "käufer", "password_encrypt": "1234"'


print(json_exctract_and_validate(test,["vorname", "nachname", "benutzername", "email", "rolle", "password_encrypt"]))