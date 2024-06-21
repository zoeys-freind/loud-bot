import json

def getfile():
    return json.load(open(r"./db.json", "r"))
def savefile(data):
    json.dump(data, open(r"./db.json", "w"), indent=4)

def getuser(id):
    return getfile()["userdata"][str(id)]
def saveuser(id, data):
    d = getfile()
    d["userdata"][str(id)] = data
    savefile(d)

def getserver(id):
    return getfile()["serverdata"][str(id)]
def saveserver(id, data):
    d = getfile()
    d["serverdata"][str(id)] = data
    savefile(d)

def getserveruser(id, userid):
    return getfile()["serverdata"][str(id)]["users"][str(userid)]
def saveserveruser(id, userid, data):
    d = getfile()
    d["serverdata"][str(id)]["users"][str(userid)] = data
    savefile(d)

def backup():
    with open(r"./db.json", "r") as f:
        with open("./backupdb.json", "w") as b:
            b.write(f.read())