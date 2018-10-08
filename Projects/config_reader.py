import json

# Arguments according to order of elements in config.json
def getJsonConfig(*arg):
    with open("config.json", 'r') as f:
        jsonData = json.load(f)
        for i in range(0, len(arg)):
            jsonData = jsonData[arg[i]]
        return jsonData