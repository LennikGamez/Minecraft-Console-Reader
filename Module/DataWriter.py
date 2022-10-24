import json

class DataBase:
    def __init__(self,path):
        self.path = path
        self.data = self.read()

    def read(self):
        with open(self.path,"r") as f:
            return json.load(f)

    def write(self):
        with open(self.path,'w') as f:
            f.write(json.dumps(self.data, indent=4))