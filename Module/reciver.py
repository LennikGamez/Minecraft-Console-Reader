from Module.log import Response
from Module.command import Command

class Reciver:
    def __init__(self,log):
        self.log = log
        self.response = None
    def is_resp(self,typ):
        if type(self.log.format_return()) is Response:
            self.response = self.log.format_return().response
            if self.response["type"] == typ:
                return True

    def is_msg(self,msg):
        if self.response["msg"].lower() == msg.lower():
            return True

    def is_cmd(self,prefix):
        if self.response["msg"][0] == prefix:
            return True

    def get_cmd(self):
        spl = self.response["msg"].split(" ")
        return Command(spl[0][1::],spl[1::])



    def is_scoreboard(self,board):
        if self.response["scoreboard"] == board:
            return True

    def trigger_reset_value(self):
        player = self.response["player"]
        scoreboard = self.response["scoreboard"]

        return f'scoreboard players reset {player} {scoreboard}'

    def get_res(self,y = None):
        if y is None:
            return self.response
        else:
            return self.response[y]
