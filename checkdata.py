async def checkdata():
    f = db.getfile()
    
    serverdata = f["serverdata"]
    userdata = f["userdata"]
    td = []
    for server in serverdata.keys():
        try:
            server = None
            for s in client.guilds:
                if s.id == str(server):
                    server = s
                    break
        except discord.errors.NotFound:
            td.append(server)
            continue
    for x in td:
        del serverdata[x]
    for server in client.guilds:
        if str(server.id) not in serverdata.keys():
            serverdata[str(server.id)] = {}
    for id, server in serverdata.items():
        serverkeys = ["warns", "name", "id", "users", "bl", "config"]
        serverobj = None
        for s in client.guilds:
            if s.id == int(id):
                serverobj = s
                break
        for x in serverkeys:
            if not x in server:
                if x == "warns":
                    server["warns"] = []
                elif x == "name":
                    server["name"] = serverobj.name
                elif x == "id":
                    server["id"] = serverobj.id
                elif x == "bl":
                    server["bl"] = []
                elif x == "config":
                    server["config"] = {
                        "prefix": "g!",
                        "modrole": None,
                        "adminrole": None,
                        "color": "#000000"
                    }
                elif x == "users":
                    server["users"] = {}
                    for u in serverobj.members:
                        server["users"][str(u.id)] = {
                            "username": u.name,
                            "xp": 0,
                            "level": 0,
                            "warns": [],
                            "mod": False,
                            "admin": False
                        }
    
    
    for x in client.guilds:
        guildinfo = serverdata[str(x.id)]
        for m in x.members:
            if str(m.id) not in guildinfo["users"].keys():
                guildinfo["users"][str(m.id)] = {
                    "username": m.name,
                    "level": 0,
                    "xp": 0,
                    "warns": [],
                    "mod": False,
                    "admin": False
                }
        serverdata[str(x.id)] = guildinfo
            
    f["serverdata"] = serverdata
    
    
    f["userdata"] = userdata
    db.savefile(f)
    print("Data check done!")