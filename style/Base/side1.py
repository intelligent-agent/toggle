import tkinter as tk
import base_color_scheme
from side_helpers import ch, cw, screen_width, screen_height
bcs = base_color_scheme.base_color_scheme

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
                        "height": ch(800),
                        "y": 80
                    },
                    {
                        "id": "heat-tool0",
                        "type": "MxButton",
                        "style-class": "heat",
                        "is_toggle": True,
                        "x": 596,
                        "y": 900,
                        "width": cw(128),
                        "height": ch(128),
                    },
                    {
                        "id": "heat-bed",
                        "type": "MxButton",
                        "style-class": "heat",
                        "is_toggle": True,
                        "x": 796,
                        "y": 900,
                        "width": cw(128),
                        "height": ch(128),
                    },
                    {
                        "id": "heat-tool1",
                        "type": "MxButton",
                        "style-class": "heat",
                        "is_toggle": True,
                        "x": 996,
                        "y": 900,
                        "width": cw(128),
                        "height": ch(128),
                    },
                    {
                        "id": "heat-tool2",
                        "type": "MxButton",
                        "style-class": "heat",
                        "is_toggle": True,
                        "x": 1196,
                        "y": 900,
                        "width": cw(128),
                        "height": ch(128),
                    },
                    {
                        "id": "lbl-temp",
                        "type": "ClutterText",
                        "text": "Temperature",
                        "x": 1205,
                        "y": 1000,
                        "width": cw(700),
                        "height": ch(50),
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
                "height": ch(128),
                "width": cw(128),
            },
            {
                "id": "side1-btn-next",
                "type": "MxButton",
                "style-class": "print",
                "is_toggle": True,
                "x": 1777,
                "y": 15,
                "height": ch(128),
                "width": cw(128),
            }
        ]
    }
