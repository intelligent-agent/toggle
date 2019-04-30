import tkinter as tk
import base_color_scheme

cs = base_color_scheme.base_color_scheme

root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

iw = screen_width - 20  # inner width with margins appears frequently

box_children = [
    {
        "id": "side0",
        "type": "ClutterActor",
        "width": 1920,
        "height": 1080,
        "pivot-point-z": -540.0,
        "pivot-point": [
            0.5,
            0.0
        ],
        "rotation-angle-y": 0.0,
        "background-color": "white",
        "children": [
            {
                "id": "side0-content",
                "visible": False,
                "type": "ClutterActor",
                "width": 1920,
                "height": 1080,
                "layout-manager": {
                    "type": "ClutterBinLayout"
                },
                "children": [
                    {
                        "id": "scroll-pane",
                        "type": "ClutterScrollActor",
                        "width": 1900,
                        "y": 80,
                        "x": 10,
                        "background-color": "#EEE",
                        "scroll-mode": 1,
                        "layout-manager": {
                            "type": "ClutterBoxLayout",
                            "orientation": 1
                        },
                        "children": [
                            {
                                "id": "network-box",
                                "type": "ClutterActor",
                                "width": 1900,
                                "background-color": "#c9c3c3",
                                "layout-manager": {
                                    "type": "ClutterBoxLayout",
                                    "orientation": 1
                                },
                                "children": [
                                    {
                                        "id": "network-header",
                                        "type": "ClutterActor",
                                        "height": 150,
                                        "width": 1900,
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
                                                "width": 128,
                                                "height": 128
                                            }
                                        ]
                                    },
                                    {
                                        "id": "network-body",
                                        "type": "ClutterActor",
                                        "background-color": "#FFF",
                                        "width": 1900,
                                        "height": 5,
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
                                "width": 1900,
                                "background-color": "#c9c3c3",
                                "layout-manager": {
                                    "type": "ClutterBoxLayout",
                                    "orientation": 1
                                },
                                "children": [
                                    {
                                        "id": "wifi-header",
                                        "type": "ClutterActor",
                                        "height": 150,
                                        "width": 1900,
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
                                                "width": 128,
                                                "height": 128
                                            }
                                        ]
                                    },
                                    {
                                        "id": "wifi-body",
                                        "type": "ClutterActor",
                                        "background-color": "#FFF",
                                        "width": 1900,
                                        "height": 5,
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
                                "width": 1900,
                                "background-color": "#c9c3c3",
                                "layout-manager": {
                                    "type": "ClutterBoxLayout",
                                    "orientation": 1
                                },
                                "children": [
                                    {
                                        "id": "slicer-header",
                                        "type": "ClutterActor",
                                        "height": 150,
                                        "width": 1900,
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
                                                "width": 128,
                                                "height": 128
                                            }
                                        ]
                                    },
                                    {
                                        "id": "slicer-body",
                                        "type": "ClutterActor",
                                        "width": 1900,
                                        "height": 5,
                                        "background-color": "#FFF",
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
                                "width": 1900,
                                "background-color": "#c9c3c3",
                                "layout-manager": {
                                    "type": "ClutterBoxLayout",
                                    "orientation": 1
                                },
                                "children": [
                                    {
                                        "id": "printer-header",
                                        "type": "ClutterActor",
                                        "height": 5,
                                        "width": 1900,
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
                                                "width": 128,
                                                "height": 128
                                            }
                                        ]
                                    },
                                    {
                                        "id": "printer-body",
                                        "type": "ClutterActor",
                                        "width": 780,
                                        "height": 5,
                                        "background-color": "#FFF",
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
                        "width": 1920,
                        "height": 90,
                        "x": 0,
                        "y": 0,
                        "background-color": "#FFF"
                    },
                    {
                        "id": "side0-btn-prev",
                        "type": "MxButton",
                        "style-class": "settings",
                        "x": 15,
                        "y": 15,
                        "width": 128,
                        "height": 128,
                        "visible": False
                    },
                    {
                        "id": "side0-btn-next",
                        "type": "MxButton",
                        "style-class": "temp",
                        "x": 1777,
                        "y": 15,
                        "width": 128,
                        "height": 128,
                        "visible": True
                    }
                ]
            },
            {
                "id": "side5-content",
                "type": "ClutterActor",
                "width": 1920,
                "height": 1080,
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
                        "width": 900,
                        "height": 900,
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
                        "width": 128,
                        "height": 128,
                        "opacity": 0
                    },
                    {
                        "id": "side5-btn-prev",
                        "type": "MxButton",
                        "style-class": "settings",
                        "x": 15,
                        "y": 15,
                        "width": 128,
                        "height": 128,
                        "opacity": 0
                    }
                ]
            }
        ]
    },
    {
        "id": "side1",
        "type": "ClutterActor",
        "width": 1920,
        "height": 1080,
        "pivot-point-z": -540.0,
        "pivot-point": [
            0.5,
            0.0
        ],
        "rotation-angle-y": 90.0,
        "background-color": "white",
        "visible": False,
        "children": [
            {
                "id": "side1-content",
                "type": "ClutterActor",
                "background-color": "#FFFFFFFF",
                "children": [
                    {
                        "id": "graph",
                        "type": "ClutterActor",
                        "width": 1920,
                        "height": 800,
                        "y": 80
                    },
                    {
                        "id": "heat-tool0",
                        "type": "MxButton",
                        "style-class": "heat",
                        "is_toggle": True,
                        "x": 596,
                        "y": 900,
                        "width": 128,
                        "height": 128
                    },
                    {
                        "id": "heat-bed",
                        "type": "MxButton",
                        "style-class": "heat",
                        "is_toggle": True,
                        "x": 796,
                        "y": 900,
                        "width": 128,
                        "height": 128
                    },
                    {
                        "id": "heat-tool1",
                        "type": "MxButton",
                        "style-class": "heat",
                        "is_toggle": True,
                        "x": 996,
                        "y": 900,
                        "width": 128,
                        "height": 128
                    },
                    {
                        "id": "heat-tool2",
                        "type": "MxButton",
                        "style-class": "heat",
                        "is_toggle": True,
                        "x": 1196,
                        "y": 900,
                        "width": 128,
                        "height": 128
                    },
                    {
                        "id": "lbl-temp",
                        "type": "ClutterText",
                        "text": "Temperature",
                        "x": 1205,
                        "y": 1000,
                        "width": 700,
                        "height": 50,
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
                "height": 128,
                "width": 128
            },
            {
                "id": "side1-btn-next",
                "type": "MxButton",
                "style-class": "print",
                "is_toggle": True,
                "x": 1777,
                "y": 15,
                "height": 128,
                "width": 128
            }
        ]
    },
    {
        "id": "side2",
        "type": "ClutterActor",
        "width": 1920,
        "height": 1080,
        "pivot-point-z": -540.0,
        "pivot-point": [
            0.5,
            0.0
        ],
        "rotation-angle-y": 180.0,
        "visible": False,
        "background-color": "white",
        "children": [
            {
                "id": "side2-content",
                "type": "ClutterActor",
                "background-color": "white",
                "children": [
                    {
                        "id": "content-flip",
                        "type": "ClutterActor",
                        "width": 1440,
                        "height": 800,
                        "pivot-point": [
                            0.5,
                            0.5
                        ],
                        "x": 340,
                        "layout-manager": {
                            "type": "ClutterFixedLayout"
                        },
                        "children": [
                            {
                                "id": "volume-viewport",
                                "type": "ClutterActor",
                                "width": 1440,
                                "height": 540,
                                "x": 100,
                                "pivot-point": [
                                    0.5,
                                    0.5
                                ],
                                "layout-manager": {
                                    "type": "ClutterFixedLayout"
                                },
                                "children": [
                                    {
                                        "id": "spinner",
                                        "type": "ClutterActor",
                                        "x": 720,
                                        "y": 700,
                                        "z-position": 150,
                                        "width": 1,
                                        "height": 1,
                                        "depth": 1,
                                        "children": [
                                            {
                                                "id": "volume-wrapper",
                                                "type": "ClutterActor",
                                                "pivot-point": [
                                                    0.5,
                                                    0.5
                                                ],
                                                "pivot-point-z": 0.5,
                                                "width": 1,
                                                "height": 1,
                                                "depth": 1,
                                                "rotation-angle-x": 180.0,
                                                "rotation-angle-y": 180.0,
                                                "scale-x": 2.0,
                                                "scale-y": 2.0,
                                                "scale-z": 2.0,
                                                "children": [
                                                    {
                                                        "id": "plate",
                                                        "type": "MashModel",
                                                        "rotation-angle-x": -90.0
                                                    },
                                                    {
                                                        "id": "model-flipper",
                                                        "type": "ClutterActor",
                                                        "children": [
                                                            {
                                                                "id": "model",
                                                                "type": "MashModel",
                                                                "rotation-angle-x": 90.0,
                                                                "rotation-angle-y": 0.0,
                                                                "rotation-angle-z": 0.0
                                                            }
                                                        ]
                                                    }
                                                ]
                                            }
                                        ]
                                    },
                                    {
                                        "id": "loader",
                                        "type": "ClutterTexture",
                                        "width": 128,
                                        "height": 128,
                                        "x": 650,
                                        "y": 400,
                                        "pivot-point": [
                                            0.5,
                                            0.5
                                        ],
                                        "visible": False
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "id": "btn-bar",
                        "type": "ClutterActor",
                        "children": [
                            {
                                "id": "btn-prev",
                                "type": "MxButton",
                                "style-class": "jog_arrow",
                                "height": 128,
                                "width": 128,
                                "x": 15,
                                "y": 500,
                                "rotation-angle-z": 180.0,
                                "pivot-point": [
                                    0.5,
                                    0.5
                                ]
                            },
                            {
                                "id": "lbl-stat",
                                "type": "ClutterText",
                                "x": 15,
                                "y": 900,
                                "font-description": "Sans 32"
                            },
                            {
                                "id": "lbl-model",
                                "type": "ClutterText",
                                "text": "Model",
                                "x": 1265,
                                "y": 1000,
                                "width": 700,
                                "height": 50,
                                "x-align": 3,
                                "x-expand": True,
                                "line-alignment": 2,
                                "font-description": "Sans 32"
                            },
                            {
                                "id": "progress-bar",
                                "type": "MxProgressBar",
                                "x": 1265,
                                "y": 940,
                                "width": 640,
                                "height": 50,
                                "x-align": 3,
                                "x-expand": True
                            },
                            {
                                "id": "time-gone",
                                "type": "ClutterText",
                                "x": 1265,
                                "y": 910,
                                "width": 220,
                                "height": 25,
                                "font-description": "Sans 16"
                            },
                            {
                                "id": "time-left",
                                "type": "ClutterText",
                                "x": 1680,
                                "y": 910,
                                "width": 220,
                                "height": 25,
                                "x-align": 3,
                                "x-expand": True,
                                "font-description": "Sans 16"
                            },
                            {
                                "id": "btn-cancel",
                                "type": "MxButton",
                                "style-class": "cancel",
                                "is-toggle": True,
                                "toggled": True,
                                "x": 696,
                                "y": 900,
                                "width": 128,
                                "height": 128
                            },
                            {
                                "id": "btn-print",
                                "type": "MxButton",
                                "style-class": "play",
                                "is_toggle": True,
                                "x": 896,
                                "y": 900,
                                "width": 128,
                                "height": 128
                            },
                            {
                                "id": "btn-pause",
                                "type": "MxButton",
                                "style-class": "pause",
                                "is_toggle": True,
                                "x": 1096,
                                "y": 900,
                                "width": 128,
                                "height": 128
                            },
                            {
                                "id": "btn-next",
                                "type": "MxButton",
                                "style-class": "jog_arrow",
                                "height": 128,
                                "width": 128,
                                "x": 1777,
                                "y": 500,
                                "rotation-angle-z": 0.0,
                                "pivot-point": [
                                    0.5,
                                    0.5
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "id": "side2-btn-prev",
                "type": "MxButton",
                "style-class": "temp",
                "x": 15,
                "y": 15,
                "width": 128,
                "height": 128
            },
            {
                "id": "side2-btn-next",
                "type": "MxButton",
                "style-class": "jog",
                "x": 1777,
                "y": 15,
                "width": 128,
                "height": 128
            }
        ]
    },
    {
        "id": "side3",
        "type": "ClutterActor",
        "width": 1920,
        "height": 1080,
        "pivot-point-z": -540.0,
        "pivot-point": [
            0.5,
            0.0
        ],
        "rotation-angle-y": 270.0,
        "visible": False,
        "background-color": "white",
        "children": [
            {
                "id": "side3-content",
                "type": "ClutterActor",
                "width": 1920,
                "height": 1080,
                "children": [
                    {
                        "id": "jogger-xy",
                        "type": "ClutterActor",
                        "x": 120,
                        "y": 160,
                        "width": 700,
                        "height": 700,
                        "background-color": "white",
                        "children": [
                            {
                                "id": "jog_x_minus",
                                "type": "MxButton",
                                "style-class": "jog_arrow",
                                "height": 140,
                                "width": 140,
                                "x": 0,
                                "y": 250,
                                "rotation-angle-z": 180.0,
                                "pivot-point": [
                                    0.5,
                                    0.5
                                ]
                            },
                            {
                                "id": "jog_y_plus",
                                "type": "MxButton",
                                "style-class": "jog_arrow",
                                "height": 140,
                                "width": 140,
                                "x": 240,
                                "y": 0,
                                "rotation-angle-z": 270.0,
                                "pivot-point": [
                                    0.5,
                                    0.5
                                ]
                            },
                            {
                                "id": "jog_x_plus",
                                "type": "MxButton",
                                "style-class": "jog_arrow",
                                "width": 140,
                                "height": 140,
                                "x": 480,
                                "y": 250,
                                "rotation-angle-z": 0.0,
                                "pivot-point": [
                                    0.5,
                                    0.5
                                ]
                            },
                            {
                                "id": "jog_y_minus",
                                "type": "MxButton",
                                "style-class": "jog_arrow",
                                "height": 140,
                                "width": 140,
                                "x": 240,
                                "y": 500,
                                "rotation-angle-z": 90.0,
                                "pivot-point": [
                                    0.5,
                                    0.5
                                ]
                            },
                            {
                                "id": "jog_home",
                                "type": "MxButton",
                                "style-class": "jog_home",
                                "height": 200,
                                "width": 200,
                                "x": 205,
                                "y": 220
                            }
                        ]
                    },
                    {
                        "id": "jogger-z",
                        "type": "ClutterActor",
                        "x": 765,
                        "y": 160,
                        "width": 70,
                        "height": 300,
                        "children": [
                            {
                                "id": "jog_z_plus",
                                "type": "MxButton",
                                "style-class": "jog_arrow",
                                "height": 140,
                                "width": 140,
                                "x": 120,
                                "y": 0,
                                "rotation-angle-z": 270.0,
                                "pivot-point": [
                                    0.5,
                                    0.5
                                ]
                            },
                            {
                                "id": "jog_z_minus",
                                "type": "MxButton",
                                "style-class": "jog_arrow",
                                "height": 140,
                                "width": 140,
                                "x": 120,
                                "y": 500,
                                "rotation-angle-z": 90.0,
                                "pivot-point": [
                                    0.5,
                                    0.5
                                ]
                            },
                            {
                                "id": "jog_z_home",
                                "type": "MxButton",
                                "style-class": "jog_home_z",
                                "height": 140,
                                "width": 140,
                                "x": 120,
                                "y": 250
                            }
                        ]
                    },
                    {
                        "id": "misc-control",
                        "type": "ClutterActor",
                        "x": 1100,
                        "y": 160,
                        "width": 70,
                        "height": 300,
                        "children": [
                            {
                                "id": "motors_off",
                                "type": "MxButton",
                                "style-class": "motors_off",
                                "height": 140,
                                "width": 140,
                                "x": 120,
                                "y": 0
                            },
                            {
                                "id": "fan_on",
                                "type": "MxButton",
                                "style-class": "fan_on",
                                "height": 140,
                                "width": 140,
                                "x": 120,
                                "y": 250
                            },
                            {
                                "id": "fan_off",
                                "type": "MxButton",
                                "style-class": "fan_off",
                                "height": 140,
                                "width": 140,
                                "x": 120,
                                "y": 500
                            }
                        ]
                    },
                    {
                        "id": "jogger-e",
                        "type": "ClutterActor",
                        "x": 1400,
                        "y": 160,
                        "width": 130,
                        "height": 300,
                        "children": [
                            {
                                "id": "jog_e_extrude",
                                "type": "MxButton",
                                "style-class": "jog_arrow",
                                "height": 140,
                                "width": 140,
                                "x": 120,
                                "y": 0,
                                "rotation-angle-z": 270.0,
                                "pivot-point": [
                                    0.5,
                                    0.5
                                ]
                            },
                            {
                                "id": "jog_e_retract",
                                "type": "MxButton",
                                "style-class": "jog_arrow",
                                "height": 140,
                                "width": 140,
                                "x": 120,
                                "y": 500,
                                "rotation-angle-z": 90.0,
                                "pivot-point": [
                                    0.5,
                                    0.5
                                ]
                            },
                            {
                                "id": "jog_e_toggle",
                                "type": "MxButton",
                                "style-class": "jog_home_e",
                                "is_toggle": True,
                                "height": 140,
                                "width": 140,
                                "x": 120,
                                "y": 250
                            }
                        ]
                    },
                    {
                        "id": "travel-length",
                        "type": "ClutterText",
                        "text": "",
                        "x": 1080,
                        "y": 900,
                        "width": 300,
                        "height": 50,
                        "x-align": 3,
                        "x-expand": True,
                        "line-alignment": 2,
                        "font-description": "Sans 32"
                    },
                    {
                        "id": "travel_xy",
                        "type": "MxButton",
                        "style-class": "travel_10",
                        "is_toggle": True,
                        "x": 696,
                        "y": 900,
                        "width": 128,
                        "height": 128
                    },
                    {
                        "id": "travel_z",
                        "type": "MxButton",
                        "style-class": "travel_10",
                        "is_toggle": True,
                        "x": 896,
                        "y": 900,
                        "width": 128,
                        "height": 128
                    },
                    {
                        "id": "travel_eh",
                        "type": "MxButton",
                        "style-class": "travel_10",
                        "is_toggle": True,
                        "x": 1096,
                        "y": 900,
                        "width": 128,
                        "height": 128
                    }
                ]
            },
            {
                "id": "side3-btn-prev",
                "type": "MxButton",
                "style-class": "print",
                "width": 128,
                "height": 128,
                "x": 15,
                "y": 15
            },
            {
                "id": "side3-btn-next",
                "type": "MxButton",
                "style-class": "settings",
                "width": 128,
                "height": 128,
                "x": 1777,
                "y": 15,
                "visible": True
            }
        ]
    }
]