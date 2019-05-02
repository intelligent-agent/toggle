import tkinter as tk
import base_color_scheme
bcs = base_color_scheme.base_color_scheme


root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

content = {
        "id": "side1",
        "type": "ClutterActor",
        "width": screen_width,
        "height": screen_height,
        "pivot-point-z": -540.0,
        "pivot-point": [
            0.5,
            0.0
        ],
        "rotation-angle-y": 90.0,
        "background-color": bcs["background"],
        "visible": False,
        "children": [
            {
                "id": "side1-content",
                "type": "ClutterActor",
                "background-color":  bcs["background"],
                "children": [
                    {
                        "id": "graph",
                        "type": "ClutterActor",
                        "width": screen_width,
                        "height": 800/1080 * screen_height,
                        "y": 80
                    },
                    {
                        "id": "heat-tool0",
                        "type": "MxButton",
                        "style-class": "heat",
                        "is_toggle": True,
                        "x": 596,
                        "y": 900,
                        "width": 128/1920 * screen_width,
                        "height": 128/1080 * screen_height
                    },
                    {
                        "id": "heat-bed",
                        "type": "MxButton",
                        "style-class": "heat",
                        "is_toggle": True,
                        "x": 796,
                        "y": 900,
                        "width": 128/1920 * screen_width,
                        "height": 128/1080 * screen_height
                    },
                    {
                        "id": "heat-tool1",
                        "type": "MxButton",
                        "style-class": "heat",
                        "is_toggle": True,
                        "x": 996,
                        "y": 900,
                        "width": 128/1920 * screen_width,
                        "height": 128/1080 * screen_height
                    },
                    {
                        "id": "heat-tool2",
                        "type": "MxButton",
                        "style-class": "heat",
                        "is_toggle": True,
                        "x": 1196,
                        "y": 900,
                        "width": 128/1920 * screen_width,
                        "height": 128/1080 * screen_height
                    },
                    {
                        "id": "lbl-temp",
                        "type": "ClutterText",
                        "text": "Temperature",
                        "x": 1205,
                        "y": 1000,
                        "width": 700/1920 * screen_width,
                        "height": 50/1080 * screen_height,
                        "x-align": 3,
                        "x-expand": True,
                        "line-alignment": 2,
                        "font-description": "Sans 32"
                    }
                ]
            },
            {
                "id": "side1-btn-prev",
                "type": "MxButton",
                "style-class": "settings",
                "is_toggle": True,
                "x": 15,
                "y": 15,
                "height": 128/1080 * screen_height,
                "width": 128/1920 * screen_width
            },
            {
                "id": "side1-btn-next",
                "type": "MxButton",
                "style-class": "print",
                "is_toggle": True,
                "x": 1777,
                "y": 15,
                "height": 128/1080 * screen_height,
                "width": 128/1920 * screen_width
            }
        ]
    }
