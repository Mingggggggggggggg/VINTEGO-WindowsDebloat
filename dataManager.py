import json

def loadFile(path, type):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for i in data:
        if type in i:
            return i[type]

    return []



print(loadFile("debloatList.json", "debloat"))
print(loadFile("debloatList.json", "telemetry"))
