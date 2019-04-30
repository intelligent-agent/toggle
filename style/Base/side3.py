import tkinter as tk
import base_color_scheme
cs = base_color_scheme.base_color_scheme

root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
content = {
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
