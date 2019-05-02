import tkinter as tk

### get the screen resolution ###
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

"""
This file stores information about the clutter
children for the box
"""


clutter_children = [{
    "id": "connection",
    "type": "MxButton",
    "height": screen_height / 16.875,
    "width": screen_width / 30,
    "style-class": "connection"
},
                    {
                        "id": "printing",
                        "type": "MxButton",
                        "height": screen_height / 16.875,
                        "width": screen_width / 30,
                        "style-class": "printing"
                    },
                    {
                        "id": "paused",
                        "type": "MxButton",
                        "height": screen_height / 16.875,
                        "width": screen_width / 30,
                        "style-class": "paused"
                    },
                    {
                        "id": "heartbeat",
                        "type": "MxButton",
                        "height": screen_height / 16.875,
                        "width": screen_width / 30,
                        "style-class": "heartbeat",
                        "opacity": 0
                    }]
