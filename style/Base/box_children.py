import side0
import side1
import side2
import side3

"""
This is the file that specifies the children for the 3D box. 

More information on each face (child) is in each file imported.

Key elements for each functioning side:
    - id, must follow side<N> where N = { 0, 1, 2, 3, ... } convention (see CubeTabs.py)
    - type, each type is a ClutterActor for a side of the cube
    - width and height, screen width and height
    - pivot-point-z, consistently -540.0
    - pivot-point, consistently [0.5, 0]
    
    
"""


box_children = [
    side0.content,
    side1.content,
    side2.content,
    side3.content
]
