from Module.command import ParentCommand
from Module.DataWriter import DataBase


dw = DataBase("config.json")


class SetWayPoint(ParentCommand):
    aliases = ["setPoint".lower(),"setwaypoints".lower()]
    def __init__(self, reciver,console):
        ParentCommand.__init__(self, reciver, console)
        self.player = self.rec.get_res("player")

        self.name = ''
        for i in self.rec.get_cmd().args:
            self.name += i
            self.name += ' '
        self.name = self.name[:-1]

        self.execute()

    def execute(self):
        if not self.player in dw.data.keys():
            dw.add_player(self.player)
        if any(self.name in d["name"] for d in dw.data[self.player]["Waypoints"]):
            self.console.sendToConsole(f"say Der Waypoint {self.name} existiert bereits!")
            return

        res = self.console.sendToConsole(f"data get entity {self.player} Pos").response
        data = res["data"]

        dw.data[self.player]["Waypoints"].append({
            "name":self.name,
            "x":data[0],
            "y":data[1],
            "z":data[2]
            })

        dw.write()
        

class GetWayPoint(ParentCommand):
    aliases = ["getpoints".lower(),"getwaypoints".lower()]
    def __init__(self,reciver,console):
        ParentCommand.__init__(self, reciver, console)
        self.player = self.rec.get_res("player")
        self.con = console
        self.execute()


    def generate_cmd(self):

        cmd = f'["",'
        data = dw.data[self.player]["Waypoints"]
        
        for n,d in enumerate(data):
            cmd += f'{{"text":"{d["name"]}","bold":true,"italic":true,"color":"#0D9376"}},{{"text":" --> ","bold":true}},{{"text":"X","color":"#BF36BF"}},{{"text":": "}},{{"text":"{round(float(d["x"]))}","bold":true}},{{"text":" Y","color":"#BF36BF"}},{{"text":": "}},{{"text":"{round(float(d["y"]))}","bold":true}},{{"text":" Z","color":"#BF36BF"}},{{"text":": "}},{{"text":"{round(float(d["z"]))}","bold":true}}'
            if n < len(data)-1:
               cmd += f',{{"text":"\\n"}},'
        cmd += ']'

        return cmd

    def execute(self):
        if not self.player in dw.data.keys():
                    return

        if len(dw.data[self.player]["Waypoints"]) > 0:
            cmd = self.generate_cmd()
            self.con.create_tellraw_from_dict(self.player, cmd)
        else:
            self.con.sendToConsole("say Du hast keine Waypoints")



class RemoveWayPoint(ParentCommand):
    aliases = ["removewaypoint".lower(),"removepoint".lower()]
    def __init__(self,reciver,console):
        ParentCommand.__init__(self, reciver, console)

        self.player = self.rec.get_res("player")
        self.con = console

        self.name = ''
        for i in self.rec.get_cmd().args:
            self.name += i
            self.name += ' '
        self.name = self.name[:-1]

        self.execute()

    def execute(self):

        if not self.player in dw.data.keys():
            return

        for n,i in enumerate(dw.data[self.player]["Waypoints"]):
            if self.name in i["name"]:
                del dw.data[self.player]["Waypoints"][n]
                dw.write()
                self.con.sendToConsole("say Removed")
                return



COMMANDS = [
    {"name":SetWayPoint},
    {"name":GetWayPoint},
    {"name":RemoveWayPoint}
]