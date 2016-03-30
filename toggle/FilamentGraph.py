
from Graph import Graph, GraphScale, GraphPlot

from gi.repository import Clutter, Mx, Mash, Toggle

import logging

color_str = lambda string: Clutter.color_from_string(string)[1]  # shortcut


class FilamentGraph():

    def __init__(self, config):
        self.config = config
        # Set up filament graph

        self.graph = Graph(800, 480)        
        self.filament = config.ui.get_object("graph")
        self.filament.add_child(self.graph)   
        self.graph.hide()     

        extruders = ["E", "H", "A", "B", "C"]
        colors    = ["blue", "red", "orange", "cyan", "white"]
        self.filament_sensors = {}
        for i in range(5):
            ext = extruders[i]
            color = color_str(colors[i])
            rgb = (color.red, color.green, color.blue)
            self.filament_sensors[ext] = GraphPlot(ext, rgb, -160, 160)
            self.graph.add_plot(self.filament_sensors[ext])                
        
        # Add a scale to the plot
        scale = GraphScale(-160, 160, [ -150, -100, -50,  0, 50, 100, 150])
        self.graph.add_plot(scale)       

        self.graphs = {
            "tool0":{
                "actual": GraphPlot("E", (1, 0, 0)), 
                "target": GraphPlot("T_E", (1, 0.4, 0.4))
            }, 
            "tool1":{
                "actual": GraphPlot("H", (1, 0.64, 0)),
                "target": GraphPlot("T_H", (1, 0.8, 0.5))
            },
            "bed"  :{
                "actual": GraphPlot("BED", (0, 0, 1)), 
                "target": GraphPlot("T_BED", (0.2, 0.8, 0.8))
            }
        }

        #for tool in self.graphs:
        #    for source in self.graphs[tool]:
        #        #logging.debug(self.graphs[tool][source])
        #        self.graph.add_plot(self.graphs[tool][source])

        # Add a scale to the plot
        scale = GraphScale(0, 320, [ 0, 50, 100, 150, 200, 250, 300])
        scale.set_title("Filament")
        self.graph.add_plot(scale)


        # Filament sensor
        #self.btn_stat.connect("clicked", self.show_filament_graph)
        #tap_stat = Clutter.TapAction()
        #self.btn_stat.add_action(tap_stat)
        #tap_stat.connect("tap", self.show_filament_graph, None)

        #self.config.filament_graph.connect("button-release-event", self.hide_filament_graph)

        #tap_filament_off = Clutter.TapAction()
        #self.config.filament_graph.add_action(tap_filament_off)
        #tap_filament_off.connect("tap", self.hide_filament_graph, None)



    def update_filaments(self, filaments):
        logging.debug("Filaments: "+str(filaments))
        #time = temp['time']
        #for tool in self.graphs:
        #    #logging.debug(tool)
        #    for source in self.graphs[tool]:
        #        t = temp[tool][source]
        #        plot = self.graphs[tool][source]
        #        #logging.debug("T: "+str(t))
        #        plot.add_point(time, t)
   
        #self.set_temp("B:{} T0:{} T1:{}".format(self.bed_temp, self.t0_temp, self.t1_temp))
        self.graph.refresh()

