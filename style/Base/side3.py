import tkinter as tk
import base_color_scheme
bcs = base_color_scheme.base_color_scheme
from side_helpers import ch, cw, screen_width, screen_height

"""
This is the side that has a house, some fan buttons, and 3 tens at the bottom.
At this point, I don't know how to describe it better :)
"""

content = {
        "id": "side3",
        "type": "ClutterActor",
        "width": screen_width,
        "height": screen_height,
        "pivot-point-z": -540.0,
        "pivot-point": [
            0.5,
            0.0
        ],
        "rotation-angle-y": 270.0,
        "visible": False,
        "background-color": bcs["background"],
        "children": [
            {
                "id": "side3-content",
                "type": "ClutterActor",
                "width": screen_width,
                "height": screen_height,
                "children": [
                    {
                        "id": "jogger-xy",
                        "type": "ClutterActor",
                        "x": 120,
                        "y": 160,
                        "width": cw(700),
                        "height": ch(700),
                        "background-color": bcs["background"],
                        "children": [
                            {
                                "id": "jog_x_minus",
                                "type": "MxButton",
                                "style-class": "jog_arrow",
                                "height": ch(140),
                                "width": cw(140),
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
                                "height": ch(140),
                                "width": cw(140),
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
                                "width": cw(140),
                                "height": ch(140),
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
                                "height": ch(140),
                                "width": cw(140),
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
                                "height": ch(200),
                                "width": cw(200),
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
                        "width": cw(70),
                        "height": ch(300),
                        "children": [
                            {
                                "id": "jog_z_plus",
                                "type": "MxButton",
                                "style-class": "jog_arrow",
                                "height": ch(140),
                                "width": cw(140),
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
                                "height": ch(140),
                                "width": cw(140),
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
                                "height": ch(140),
                                "width": cw(140),
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
                        "width": cw(70),
                        "height": ch(300),
                        "children": [
                            {
                                "id": "motors_off",
                                "type": "MxButton",
                                "style-class": "motors_off",
                                "height": ch(140),
                                "width": cw(140),
                                "x": 120,
                                "y": 0
                            },
                            {
                                "id": "fan_on",
                                "type": "MxButton",
                                "style-class": "fan_on",
                                "height": ch(140),
                                "width": cw(140),
                                "x": 120,
                                "y": 250
                            },
                            {
                                "id": "fan_off",
                                "type": "MxButton",
                                "style-class": "fan_off",
                                "height": ch(140),
                                "width": cw(140),
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
                        "width": cw(130),
                        "height": ch(300),
                        "children": [
                            {
                                "id": "jog_e_extrude",
                                "type": "MxButton",
                                "style-class": "jog_arrow",
                                "height": ch(140),
                                "width": cw(140),
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
                                "height": ch(140),
                                "width": cw(140),
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
                                "height": ch(140),
                                "width": cw(140),
                                "x": 120,
                                "y": 250
                            }
                        ]
                    },
                    {
                        "id": "travel-length",
                        "type": "ClutterText",
                        "text": "",
                        "x": screen_height,
                        "y": 900,
                        "width": cw(300),
                        "height": ch(50),
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
                        "width": cw(128),
                        "height": ch(128)
                    },
                    {
                        "id": "travel_z",
                        "type": "MxButton",
                        "style-class": "travel_10",
                        "is_toggle": True,
                        "x": 896,
                        "y": 900,
                        "width": cw(128),
                        "height": ch(128)
                    },
                    {
                        "id": "travel_eh",
                        "type": "MxButton",
                        "style-class": "travel_10",
                        "is_toggle": True,
                        "x": 1096,
                        "y": 900,
                        "width": cw(128),
                        "height": ch(128)
                    }
                ]
            },
            {
                "id": "side3-btn-prev",
                "type": "MxButton",
                "style-class": "print",
                "width": cw(128),
                "height": ch(128),
                "x": 15,
                "y": 15
            },
            {
                "id": "side3-btn-next",
                "type": "MxButton",
                "style-class": "settings",
                "width": cw(128),
                "height": ch(128),
                "x": 1777,
                "y": 15,
                "visible": True
            }
        ]
    }
