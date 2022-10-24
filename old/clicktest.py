from time import sleep
import win32api, win32gui, win32ui, win32con

name = "MCSERVER"
hwnd = win32gui.FindWindow(None, name)

win = win32ui.CreateWindowFromHandle(hwnd)


win.SendMessage(win32con.WM_CHAR, 0x0D, 0)
sleep(0.1)
win.SendMessage(win32con.WM_CHAR, 0x0D, 0)