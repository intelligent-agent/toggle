content = {
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
    }
