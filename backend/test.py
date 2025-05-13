import json

def is_json_empty(json_obj):
    # return true if length is 0.
    return len(json_obj) == 0

json_obj = ["a"]  # Empty JSON object
print(is_json_empty(json_obj))


