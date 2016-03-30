
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

        # Preheat
        self.btn_heat = self.config.ui.get_object("btn-heat")
        tap_heat = Clutter.TapAction()
        self.btn_heat.add_action(tap_heat)
        tap_heat.connect("tap", self.preheat, None)

        self.lbl_temp = self.config.ui.get_object("lbl-temp")

        self.bed_temp = 0
        self.t0_temp = 0
        self.t1_temp = 0
        self.heating = False

    def update_temperatures(self, temp):
        time = temp['time']
        for tool in self.graphs:
            for source in self.graphs[tool]:
                t = temp[tool][source]
                plot = self.graphs[tool][source]
                plot.add_point(time, t)
   
        self.graph.refresh()

    def update_temperature_status(self, temp):
        self.lbl_temp.set_text("B:{} T0:{} T1:{}".format(
            temp["bed"]["actual"], 
            temp["tool0"]["actual"], 
            temp["tool1"]["actual"]))

    def preheat(self, btn, other=None, stuff=None):
        logging.debug("Preheat pressed")
        if self.heating:
            self.btn_heat.set_toggled(False)            
            self.config.rest_client.stop_preheat()
            self.heating = False
        else:    
            self.btn_heat.set_toggled(True)            
            self.config.rest_client.start_preheat()
            self.heating = True

    def update_preheat(self):
        if self.btn_heat.get_toggled():
            btn.set_label("Heating")
        else:
            btn.set_label("Preheat")

    def preheat_done(self):
        self.btn_heat.set_label("Heated")


