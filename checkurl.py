import time,webbrowser, pyautogui


def open_close(url="https://www.python.org/"):
    webbrowser.open(url)
    time.sleep(5)
    pyautogui.hotkey('ctrl', 'w')
    print("tab closed")

open_close('http://58.27.247.10:81/Alkaram')