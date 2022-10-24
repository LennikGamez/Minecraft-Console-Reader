from Module.consolecontroller import ConsoleController, ResponseTypes
from Module.log import log_path
from Module.tellraws import *

from commands import COMMANDS


cc = ConsoleController(log_path, "MCSERVER")
rec, log, console = cc.get_util()

cc.commands = COMMANDS

def update():
    if not cc.check_for_updates():
            return

    if cc.check_for_message():
        if cc.check_for_command('.'):
            cc.execute_commands()
        elif rec.is_msg("Hallo"):
            console.sendToConsole(f"say Hallo {rec.get_res('player')} wie gehts")

    if rec.is_resp(ResponseTypes.TRIGGER):
        if rec.is_scoreboard("start"):
            console.sendToConsole("weather clear")
            console.sendToConsole(rec.trigger_reset_value())
            console.sendToConsole(f"scoreboard players enable {rec.get_res('player')} {rec.get_res('scoreboard')}")
            console.sendToConsole(f'say {rec.get_res()["player"]} hat das Wetter gerettet!')

    elif rec.is_resp(ResponseTypes.SCOREBOARD_SET):
                print("Got Request")


console.tellraw(Tellraw("@a",
        Part("<",bold=True,color="light_purple"),
        Part("Engine gestartet",color="light_purple",bold=True),
        Part(">",bold=True,color="light_purple"))
    )

while True:
    update()

    cc.delay()