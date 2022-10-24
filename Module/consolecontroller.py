from Module.sendCommands import ConsoleWindow
from Module.log import Log,Response
from time import sleep
from Module.reciver import Reciver
from enum import Enum



class ResponseTypes(Enum):
    DATA = 0,
    DATA_BLOCK = 1,
    PLAYER_MSG = 2,
    TEXT = 3,
    TRIGGER = 4,
    SCOREBOARD_SET = 5



class ConsoleController:
    def __init__(self,log_path,console_name):
        self.log = Log(log_path,ResponseTypes)
        self.console = ConsoleWindow(console_name,self.log)
        self.reciver = Reciver(self.log)
        self.commands = []

    def delay(self,d = 0.1):
        sleep(d)

    def check_for_message(self):
         if self.reciver.is_resp(ResponseTypes.PLAYER_MSG):    # if Response == {"msg":message, "player":player_name}
            return True
    def check_for_updates(self):
        if not self.log.get_changes() is None:
            return True

    def run_cmds(self,prefix):
        if self.check_for_message():
            if self.check_for_command(prefix):
                self.execute_commands()

    def check_for_command(self,prefix):
        if self.reciver.is_cmd(prefix):
            return True

    def execute_commands(self):
        for i in self.commands:
            if self.reciver.get_cmd().cmd.lower() in i["name"].aliases:
                i["name"](self.reciver,self.console)
                return True

    def get_util(self):
        return self.reciver,self.log, self.console