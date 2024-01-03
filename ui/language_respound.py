import json

Local = {
    "en-US":"en",
    "en-GB":"en",
    "th" : "th"
    }

def read_file(local:str):
    try:
        with open(f"languages/{local}.json", "r", encoding='utf-8') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        return read_file('en')
    return data

def get_respound(local:str,command_name:str):
    local = is_supportlang(local)
    read = read_file(local)
    return read["commands"][command_name]
    
def is_supportlang(local:str):
    return Local.get(str(local),"en")

    