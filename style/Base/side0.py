import tkinter as tk
import base_color_scheme
from side_helpers import ch, cw, screen_width, screen_height

"""
functions as the wifi settings side of the box (page)
"""

bcs = base_color_scheme.base_color_scheme

content = {
        "id": "side0",
        "type": "ClutterActor",
        "width": screen_width,
        "height": screen_height,
        "pivot-point-z": -540.0,
        "pivot-point": [
            0.5,
            0.0
        ],
        "rotation-angle-y": 0.0,
        "background-color": bcs["scroll_pane"],
        "children": [
            {
                "id": "side0-content",
                "visible": False,
                "type": "ClutterActor",
                "width": screen_width,
                "height": screen_height,
                "layout-manager": {
                    "type": "ClutterBinLayout"
                },
                "children": [
                    {
                        "id": "scroll-pane",
                        "type": "ClutterScrollActor",
                        "width": screen_width-20,
                        "y": 80,
                        "x": 10,
                        "background-color":  bcs["background"],
                        "scroll-mode": 1,
                        "layout-manager": {
                            "type": "ClutterBoxLayout",
                            "orientation": 1
                        },
                        "children": [
                            {
                                "id": "network-box",
                                "type": "ClutterActor",
                                "width": screen_width-20,
                                "background-color": bcs["box_bg"],
                                "layout-manager": {
                                    "type": "ClutterBoxLayout",
                                    "orientation": 1
                                },
                                "children": [
                                    {
                                        "id": "network-header",
                                        "type": "ClutterActor",
                                        "height": ch(150),
                                        "width": screen_width-20,
                                        "layout-manager": {
                                            "type": "ClutterFixedLayout"
                                        },
                                        "children": [
                                            {
                                                "type": "ClutterText",
                                                "text": "Network",
                                                "color": "black",
                                                "x": 250,
                                                "y": 45,
                                                "font-description": "Sans 52"
                                            },
                                            {
                                                "type": "MxIcon",
                                                "style-class": "network",
                                                "x": 100,
                                                "y": 15,
                                                "width": cw(128),
                                                "height": ch(128),
                                            }
                                        ]
                                    },
                                    {
                                        "id": "network-body",
                                        "type": "ClutterActor",
                                        "background-color": bcs["background"],
                                        "width": screen_width-20,
                                        "height": ch(5),
                                        "layout-manager": {
                                            "type": "ClutterFixedLayout"
                                        },
                                        "children": [
                                            {
                                                "type": "ClutterText",
                                                "text": "Remote Hostname: ",
                                                "font-description": "Sans 32",
                                                "x": 250,
                                                "y": 20
                                            },
                                            {
                                                "id": "remote-hostname",
                                                "type": "ClutterText",
                                                "text": "Not set",
                                                "font-description": "Sans 32",
                                                "x": 800,
                                                "y": 20
                                            },
                                            {
                                                "type": "ClutterText",
                                                "text": "Local Hostname: ",
                                                "font-description": "Sans 32",
                                                "x": 250,
                                                "y": 80
                                            },
                                            {
                                                "id": "local-hostname",
                                                "type": "ClutterText",
                                                "text": "Not set",
                                                "font-description": "Sans 32",
                                                "x": 800,
                                                "y": 80
                                            },
                                            {
                                                "type": "ClutterText",
                                                "text": "IP address: ",
                                                "font-description": "Sans 32",
                                                "x": 250,
                                                "y": 140
                                            },
                                            {
                                                "id": "local-ip",
                                                "type": "ClutterText",
                                                "text": "Not set",
                                                "font-description": "Sans 32",
                                                "x": 800,
                                                "y": 140
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "id": "wifi-box",
                                "type": "ClutterActor",
                                "width": screen_width-20,
                                "background-color": bcs["box_bg"],
                                "layout-manager": {
                                    "type": "ClutterBoxLayout",
                                    "orientation": 1
                                },
                                "children": [
                                    {
                                        "id": "wifi-header",
                                        "type": "ClutterActor",
                                        "height": ch(150),
                                        "width": screen_width-20,
                                        "layout-manager": {
                                            "type": "ClutterFixedLayout"
                                        },
                                        "children": [
                                            {
                                                "type": "ClutterText",
                                                "text": "Wifi",
                                                "color": "black",
                                                "x": 250,
                                                "y": 45,
                                                "font-description": "Sans 52"
                                            },
                                            {
                                                "type": "MxIcon",
                                                "style-class": "wifi",
                                                "x": 100,
                                                "y": 15,
                                                "width": cw(128),
                                                "height": ch(128),
                                            }
                                        ]
                                    },
                                    {
                                        "id": "wifi-body",
                                        "type": "ClutterActor",
                                        "background-color": bcs["background"],
                                        "width": screen_width-20,
                                        "height": ch(5),
                                        "children": [
                                            {
                                                "type": "ClutterText",
                                                "text": "Wifi SSID: ",
                                                "font-description": "Sans 32",
                                                "x": 250,
                                                "y": 20
                                            },
                                            {
                                                "id": "wifi-ssid",
                                                "type": "ClutterText",
                                                "text": "Not set",
                                                "font-description": "Sans 32",
                                                "x": 800,
                                                "y": 20
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "id": "slicer-box",
                                "type": "ClutterActor",
                                "width": screen_width-20,
                                "background-color": bcs["box_bg"],
                                "layout-manager": {
                                    "type": "ClutterBoxLayout",
                                    "orientation": 1
                                },
                                "children": [
                                    {
                                        "id": "slicer-header",
                                        "type": "ClutterActor",
                                        "height": ch(150),
                                        "width": screen_width-20,
                                        "layout-manager": {
                                            "type": "ClutterFixedLayout"
                                        },
                                        "children": [
                                            {
                                                "type": "ClutterText",
                                                "text": "Slicer",
                                                "color": "black",
                                                "x": 250,
                                                "y": 45,
                                                "font-description": "Sans 52"
                                            },
                                            {
                                                "type": "MxIcon",
                                                "style-class": "slicer",
                                                "x": 100,
                                                "y": 15,
                                                "width": cw(128),
                                                "height": ch(128),
                                            }
                                        ]
                                    },
                                    {
                                        "id": "slicer-body",
                                        "type": "ClutterActor",
                                        "width": screen_width-20,
                                        "height": ch(5),
                                        "background-color": bcs["background"],
                                        "layout-manager": {
                                            "type": "ClutterFixedLayout"
                                        },
                                        "children": [
                                            {
                                                "type": "ClutterText",
                                                "text": "Layer height: ",
                                                "x": 250,
                                                "y": 20,
                                                "font-description": "Sans 32"
                                            },
                                            {
                                                "id": "slicer-layer-height",
                                                "type": "ClutterText",
                                                "text": "Not set",
                                                "x": 800,
                                                "y": 20,
                                                "font-description": "Sans 32"
                                            },
                                            {
                                                "type": "ClutterText",
                                                "text": "Print temperature: ",
                                                "x": 250,
                                                "y": 80,
                                                "font-description": "Sans 32"
                                            },
                                            {
                                                "id": "slicer-print-temp",
                                                "type": "ClutterText",
                                                "text": "Not set",
                                                "font-description": "Sans 32",
                                                "x": 800,
                                                "y": 80
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "id": "printer-box",
                                "type": "ClutterActor",
                                "width": screen_width-20,
                                "background-color": bcs["box_bg"],
                                "layout-manager": {
                                    "type": "ClutterBoxLayout",
                                    "orientation": 1
                                },
                                "children": [
                                    {
                                        "id": "printer-header",
                                        "type": "ClutterActor",
                                        "height": ch(5),
                                        "width": screen_width-20,
                                        "layout-manager": {
                                            "type": "ClutterFixedLayout"
                                        },
                                        "children": [
                                            {
                                                "type": "ClutterText",
                                                "text": "Printer",
                                                "color": "black",
                                                "x": 120,
                                                "y": 30,
                                                "font-description": "Sans 32"
                                            },
                                            {
                                                "type": "MxIcon",
                                                "style-class": "printer",
                                                "x": 30,
                                                "y": 18,
                                                "width": cw(128),
                                                "height": ch(128),
                                            }
                                        ]
                                    },
                                    {
                                        "id": "printer-body",
                                        "type": "ClutterActor",
                                        "width": cw(780),
                                        "height": ch(5),
                                        "background-color": bcs["background"],
                                        "layout-manager": {
                                            "type": "ClutterFixedLayout"
                                        },
                                        "children": [
                                            {
                                                "id": "printer-calibrate-bed",
                                                "type": "MxButton",
                                                "label": "Calibrate Bed",
                                                "style-class": "main",
                                                "x": 120,
                                                "y": 20
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "id": "scroll-header",
                        "type": "ClutterActor",
                        "width": screen_width,
                        "height": ch(90),
                        "x": 0,
                        "y": 0,
                        "background-color": bcs["background"]
                    },
                    {
                        "id": "side0-btn-prev",
                        "type": "MxButton",
                        "style-class": "settings",
                        "x": 15,
                        "y": 15,
                        "width": cw(128),
                        "height": ch(128),
                        "visible": False
                    },
                    {
                        "id": "side0-btn-next",
                        "type": "MxButton",
                        "style-class": "temp",
                        "x": 1777,
                        "y": 15,
                        "width": cw(128),
                        "height": ch(128),
                        "visible": True
                    }
                ]
            },

            ## if you are confused why side5-content is here, we are too ##
            {
                "id": "side5-content",
                "type": "ClutterActor",
                "width": screen_width,
                "height": screen_height,
                "layout-manager": {
                    "type": "ClutterBinLayout"
                },
                "children": [
                    {
                        "id": "spash-holder",
                        "type": "ClutterActor",
                        "layout-manager": {
                            "type": "ClutterFixedLayout"
                        },
                        "width": cw(900),
                        "height": ch(900),
                        "children": [
                            {
                                "id": "splash",
                                "type": "ClutterTexture"
                            },
                            {
                                "id": "splash-status",
                                "type": "ClutterText",
                                "text": "Toggle initializing...",
                                "color": "white",
                                "x": 100,
                                "y": 780,
                                "font-description": "Sans 32"
                            }
                        ]
                    },
                    {
                        "id": "side5-btn-next",
                        "type": "MxButton",
                        "style-class": "temp",
                        "x": 1777,
                        "y": 15,
                        "width": cw(128),
                        "height": ch(128),
                        "opacity": 0
                    },
                    {
                        "id": "side5-btn-prev",
                        "type": "MxButton",
                        "style-class": "settings",
                        "x": 15,
                        "y": 15,
                        "width": cw(128),
                        "height": ch(128),
                        "opacity": 0
                    }
                ]
            }
        ]
    }
