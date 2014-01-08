'''
Plate is the 3D stage where the objectes are placed. 
It represents the build plate of the 3D-printer. 
'''

class Plate(Clutter.Actor):
     __gtype_name__ = 'Plate'

     def __init__(self, width, height, depth):
        Clutter.Actor.__init__(self)

        self.witdh  = width
        self.height = height
        self.depth  = depth
        self.set_reactive(True)

        # set default color to white
        color = Clutter.Color.from_string("#FFF")[1]
        self.set_color(color)

    def do_paint(self):
        clutter.cogl.set_source_color4ub (0,0,0,255)
        clutter.cogl.path_line(0,0,width,0)
        clutter.cogl.path_line(0,0,width,0)
        clutter.cogl.path_stroke()
