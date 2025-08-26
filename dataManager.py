import json

def loadFile(path, entry_type):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for section in data:
        if entry_type in section:
            return section[entry_type]
    return None


print(loadFile("debloatList.json", "debloat"))
print(loadFile("debloatList.json", "telemetry"))
