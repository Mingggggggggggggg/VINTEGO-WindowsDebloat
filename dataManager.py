import json

def loadFile(path, type):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for i in data:
        if type in i:
            return i[type]

    return []

def excludeItems(data, name):
    newList = []

    for i in name.split(","):
        i = i.strip()
        if i != "":
            newList.append(i)

    for i in newList:
        while i in data:
            data.remove(i)
    return data

def includeItems(data, name):
    for i in name.split(","):
        i = i.strip()
        if i in data:
            print(f"Der Name {i} existiert bereits in der Liste")
        else:
            data.append(i)
    return data

def processData(path, type, exName=None, inName=None):
    data = loadFile(path, type)
    if exName:
        data = excludeItems(data, exName)
    if inName:
        data = includeItems(data, inName)
    return data


#print(processData("debloatList.json", "telemetry", "Telemetry" ))

