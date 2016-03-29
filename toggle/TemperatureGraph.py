
from Graph import Graph, GraphScale, GraphPlot

from gi.repository import Clutter, Mx, Mash, Toggle

import logging


class TemperatureGraph():

    def __init__(self, config):
        self.config = config
        # Set up temperature graph
        self.graph = Graph(800, 380)        
        self.temp = config.ui.get_object("graph")
        self.temp.add_child(self.graph)

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

        for tool in self.graphs:
            for source in self.graphs[tool]:
                #logging.debug(self.graphs[tool][source])
                self.graph.add_plot(self.graphs[tool][source])

        # Add a scale to the plot
        scale = GraphScale(0, 320, [ 0, 50, 100, 150, 200, 250, 300])
        #scale.set_title("Temperature")
        self.graph.add_plot(scale)       


    def update_temperatures(self, temp):
        #logging.debug("Temps: "+str(temp))
        time = temp['time']
        for tool in self.graphs:
            #logging.debug(tool)
            for source in self.graphs[tool]:
                t = temp[tool][source]
                plot = self.graphs[tool][source]
                #logging.debug("T: "+str(t))
                plot.add_point(time, t)
   
        #self.set_temp("B:{} T0:{} T1:{}".format(self.bed_temp, self.t0_temp, self.t1_temp))
        self.graph.refresh()

