import tkinter as tk

root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

_minimum_width = screen_width * 0.05
_minimum_height = screen_height * 0.05

def cw (w):
    final_width =  w/1920 * screen_width
    return final_width if final_width > _minimum_width else _minimum_width

def ch (h):
    final_height = h/1080 * screen_height
    return final_height if final_height > _minimum_height else _minimum_height