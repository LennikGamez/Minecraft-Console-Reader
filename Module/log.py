from time import sleep


log_path = r"C:\Users\Nutzer\Desktop\Minecraft Server mit den Bres\logs\latest.log"


data_msg = 'has the following entity data:'
data_block_msg = 'has the following block data:'
trigger_msg = "Triggered"

class Response:
    def __init__(self,type,extra):
        self.response = self.merge({"type":type},extra)

    def merge(self,d1,d2):
        return d1 | d2

    def __repr__(self):
        return f'{self.response}'

class Log:
    def __init__(self,path,rt):
        self.path = path
        self.data = self.read_file()
        self.old_data = self.data
        self.ResponseTypes = rt
        self.curr_data = None

    def remove_last_entry(self):
        with open(self.path,"r+") as fp:
            # read an store all lines into list
            lines = fp.readlines()
            # move file pointer to the beginning of a file
            fp.seek(0)
            # truncate the file
            fp.truncate()

            fp.writelines(lines[:-1])
        
    def read_file(self):
        with open(self.path,"r") as f:
            return f.readlines()

    def get_changes(self):
        self.data = self.read_file()
        if not self.data == self.old_data:
            set1 = set(self.data)
            set2 = set(self.old_data)
            try:
                new_data = list(set1 - set2)[0]
                self.old_data = self.data
                self.curr_data = new_data
                return new_data
            except:
                self.curr_data = None

    def format_return(self):
        if self.curr_data is None:
            return
        log = self.curr_data

        x = log.find("[Server thread/INFO]:") + len("[Server thread/INFO]: ")   # remove Time Info
        log = log[x::]
        if 'Test failed'.lower() in log.lower():    # execute if
            return False
        elif 'Test passed'.lower() in log.lower():  # execute if
            return True
        
        elif data_msg.lower() in log.lower():   # data get entity
            return(self.data_return(log))

        elif data_block_msg.lower() in log.lower():  #data get block
            return self.data_block_return(log)

        elif '<' in log.lower() and '>' in log.lower(): # Player Msg
            return(self.player_msg_return(log))

        elif "Triggered".lower() in log.lower():    # Trigger
            return self.trigger_return(log)

        elif 'Set'.lower() in log.lower() and "for".lower() in log.lower() and "to".lower() in log.lower():
            return self.scoreboard_set_return(log)

        else:
            return Response({"type":self.ResponseTypes.TEXT},{"txt":log})




    def data_return(self,msg):
        player = msg.split(" ")[0]
        data = msg.split(": ")[1].replace("\n", "")
        data = to_list(data)
        return Response(self.ResponseTypes.PLAYER_MSG, {"player":player,"data":data})

    def data_block_return(self,msg):
        block = msg.split(', ')[:3]
        block[2] = block[2].split(" ")[0]
        data = msg.split(": ")[1]
        return Response(self.ResponseTypes.DATA_BLOCK, {"block":block, 'data':data})


    def player_msg_return(self,msg):
        player = msg[msg.find("<")+1:msg.find(">")]
        message = msg.split('> ')[1].replace("\n","")
        return Response(self.ResponseTypes.PLAYER_MSG, {'player':player,'msg':message})


    def trigger_return(self,msg):
        player = msg.split(": ")[0][1::]
        s = msg.split("Triggered [")[1]
        scoreboard = s[:s.find("]")]
        value = None
        if "added" in s or "set" in s:
            strings = msg.split("(")[1].split(" ")
            strings[-1] = strings[-1][:-2]
            print(strings)
            for i in strings:
                if i.isdigit():
                    value = int(i)

        return Response(self.ResponseTypes.TRIGGER, {"player":player,"scoreboard":scoreboard,"value":value})



    def scoreboard_set_return(self,msg):
        x = msg.find("for ")
        y = msg.find(" to")
        player = msg[x+4:y]

        x = msg.find('Set [')
        y = msg.find('] for')

        scoreboard = msg[x+5:y]

        x = msg.find(" to ")

        value = msg[x+4:-1]
        return Response(ResponseTypes.SCOREBOARD_SET, {"player":player,"scoreboard":scoreboard,"value":value})
        



def to_list(msg):
    msg = msg.replace("[","").replace("]","").replace("d","")
    spl = msg.split(", ")
    return spl
