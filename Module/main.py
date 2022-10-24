from sendCommands import ConsoleWindow
from log import Log,log_path,Response
from log import ResponseTypes as Rt
from time import sleep 
from reciver import Reciver

from DataBase.DataWriter import DataBase, BasePath
from command import *

import keyboard

log = Log(log_path)
console = ConsoleWindow("MCSERVER",log)
rec = Reciver(log)

database = DataBase(BasePath)


def run_cmd():
    for i in COMMANDS:
        if rec.get_cmd().cmd.lower() in i["name"].aliases:
            i["name"](rec,console)


console.tellraw("@a", '{"text":"< Engine gestartet >","bold":true,"color":"#DE55FB"}')

while True:

    if keyboard.is_pressed("ctrl + l"):
        exit()
    else:


        if not log.get_changes() is None:   # reactive ---> Event
            if rec.is_resp(Rt.PLAYER_MSG):    # if Response == {"msg":message, "player":player_name}
                if rec.is_cmd():    
                    run_cmd()
                if rec.is_msg("Hallo"):
                    print(console.sendToConsole(f"say Hallo {rec.get_res()['player']} wie gehts"))

            elif rec.is_resp(Rt.TRIGGER) and rec.is_scoreboard("start"):
                console.sendToConsole("weather clear")
                console.sendToConsole(rec.trigger_reset_value())
                console.sendToConsole(f"scoreboard players enable {rec.get_res('player')} {rec.get_res('scoreboard')}")
                console.sendToConsole(f'say {rec.get_res()["player"]} hat das Wetter gerettet!')

            elif rec.is_resp(Rt.SCOREBOARD_SET):
                print("Got Request")
        
        sleep(.1)