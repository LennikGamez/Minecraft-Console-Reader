from dataclasses import dataclass

@dataclass
class Command:
    cmd : str
    args : list

class ParentCommand:
    def __init__(self,reciver,console):
        self.console = console
        self.rec = reciver
