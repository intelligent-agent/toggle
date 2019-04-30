content = {
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
    }
