import win32gui, win32ui, win32con, win32api
from time import sleep
import keyboard


def list_window_names():
    def winEnumHandler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            print(hex(hwnd), '"' + win32gui.GetWindowText(hwnd) + '"')
    win32gui.EnumWindows(winEnumHandler, None)


def press_key(hwnd,k):
    win32api.SendMessage(hwnd,win32con.WM_KEYDOWN, k, 0)
    sleep(1)
    win32api.SendMessage(hwnd,win32con.WM_KEYUP, k, 0)


ALL_PLAYERS = "@a"
NEXT_PLAYER = "@p"
ALL_ENTITYS = "@e"



class ConsoleWindow:
    def __init__(self, wn, log):
        self.log = log
        self.window_name = wn
        try:
            self.hwnd = win32gui.FindWindow(None,self.window_name)
            self.win = win32ui.CreateWindowFromHandle(self.hwnd)
        except:
            print("Starte zu erst den Server!")
            exit()
            

        self.TESTFAILED = "Test failed"

    def sendToConsole(self,msg):
        self.insert(msg)
        print(f':: running :: {msg}')
        self.log.get_changes()
        entry = self.log.format_return()
        self.log.remove_last_entry()
        return entry

    def insert(self,cmd):
        sleep(.05)

        for i in cmd:
            self.win.SendMessage(win32con.WM_CHAR, ord(str(i)), 0)

        self.win.SendMessage(win32con.WM_CHAR, 0x0D, 0)
        sleep(.05)


    def create_tellraw_from_dict(self,player,txt):
        self.sendToConsole(f"tellraw {player} {txt}")

    def tellraw(self,tell):
        self.sendToConsole(f'{tell}')



if __name__ == "__main__":
    #main("say setup")
    list_window_names()