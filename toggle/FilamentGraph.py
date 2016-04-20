
from Graph import Graph, GraphScale, GraphPlot

from gi.repository import Clutter, Mx, Mash, Toggle

import logging

color_str = lambda string: Clutter.color_from_string(string)[1]  # shortcut


class FilamentGraph():

    def __init__(self, config):
        self.config = config

        # Set up filament graph
        self.graph = Graph(800, 380)        
        self.filament = config.ui.get_object("graph")
        self.filament.add_child(self.graph)   
        self.graph.hide()
        
        self.graphs = {
            "E":{
                "actual": GraphPlot("E", (1, 0, 0), -160, 160)
            }, 
            "H":{
                "actual": GraphPlot("H", (1, 0.64, 0), -160, 160)
            },
            "A"  :{
                "actual": GraphPlot("A", (0, 0, 1), -160, 160)
            }
        }

        for tool in self.graphs:
            for source in self.graphs[tool]:
                logging.debug(self.graphs[tool][source])
                self.graph.add_plot(self.graphs[tool][source])

        # Add a scale to the plot
        scale = GraphScale(-160, 160, [ -150, -100, -50,  0, 50, 100, 150])
        self.graph.add_plot(scale)       

    def update_filaments(self, message):
        logging.debug("Filaments: "+str(message))
        time = int(message['time'])
        msg = message['message']
        [tool_name, tool_value] = msg.split(":")
        if tool_name in self.graphs: 
            logging.debug(tool_name)
            logging.debug(tool_value)
            plot = self.graphs[tool_name]["actual"]
            plot.add_point(time, float(tool_value))
        else:
            logging.warning("Missing extruder name: "+str(tool_name))
        self.graph.refresh()

