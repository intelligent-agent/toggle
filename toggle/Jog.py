# Jog

from gi.repository import Clutter, Mx, Mash, Toggle
import logging 

class Jog:
    def __init__(self, config=None):
        self.config = config
        self.jog_xy_amount = 10 # 10 mm default jog amount
        self.jog_z_amount = 10       
        self.jog_eh_amount = 10 # 10 mm deafult extrude amount

        self.amount_list = [0.1, 1, 10, 100]

        buttons = [
            "jog_x_minus", 
            "jog_x_plus", 
            "jog_y_minus",
            "jog_y_plus", 
            "jog_z_minus", 
            "jog_z_plus",
            "jog_home", 
            "jog_z_home", 
            "jog_e_extrude", 
            "jog_e_retract", 
            "jog_e_toggle", 
            "travel_xy",
            "travel_z",
            "travel_eh"
        ]

        for name in buttons:
            if hasattr(self, name):
                btn = config.ui.get_object(name)
                func = getattr(self, name)
                tap = Clutter.TapAction()
                btn.add_action(tap)
                tap.connect("tap", func, None)        
            else:
                logging.warning("Jog: Missing function "+str(name))

    
    def jog_x_minus(self, btn, etc=None, other=None):
        self.config.rest_client.jog({"x": -self.jog_xy_amount})

    def jog_x_plus(self, btn, etc=None, other=None):
        self.config.rest_client.jog({"x": self.jog_xy_amount})

    def jog_y_minus(self, btn, etc=None, other=None):
        self.config.rest_client.jog({"y": -self.jog_xy_amount})
     
    def jog_y_plus(self, btn, etc=None, other=None):
        self.config.rest_client.jog({"y": self.jog_xy_amount})

    def jog_home(self, btn, etc=None, other=None):
        self.config.rest_client.home(["x", "y"])

    def jog_z_plus(self, btn, etc=None, other=None):
        self.config.rest_client.jog({"z": self.jog_z_amount})

    def jog_z_minus(self, btn, etc=None, other=None):
        self.config.rest_client.jog({"z": -self.jog_z_amount})

    def jog_z_home(self, btn, etc=None, other=None):
       self.config.rest_client.home(["z"]) 

    def jog_e_extrude(self, btn, etc=None, other=None):
        self.config.rest_client.extrude(self.jog_eh_amount)

    def jog_e_retract(self, btn, etc=None, other=None):
        self.config.rest_client.extrude(-self.jog_eh_amount)

    def jog_e_toggle(self, tap, btn=None, other=None):
        if btn.get_toggled():
            self.config.rest_client.select_tool("tool0")
        else:
            self.config.rest_client.select_tool("tool1")

    def travel_xy(self, tap, btn=None, other=None):
        logging.debug("tavel_xy")
        if self.jog_xy_amount == 0.1:
            self.jog_xy_amount = 1
            self.config.ui.get_object("travel_xy").set_style_class("travel_1")
        elif self.jog_xy_amount == 1:
            self.jog_xy_amount = 10
            self.config.ui.get_object("travel_xy").set_style_class("travel_10")
        elif self.jog_xy_amount == 10:
            self.jog_xy_amount = 100
            self.config.ui.get_object("travel_xy").set_style_class("travel_100")
        elif self.jog_xy_amount == 100:
            self.jog_xy_amount = 0.1
            self.config.ui.get_object("travel_xy").set_style_class("travel_01")
        else:
            logging.warning("Invaid jog amount for XY: "+str(self.jog_xy_amount))            
    def travel_z(self, tap, btn=None, other=None):
        logging.debug("tavel_z")
        if self.jog_z_amount == 0.1:
            self.jog_z_amount = 1
            self.config.ui.get_object("travel_z").set_style_class("travel_1")
        elif self.jog_z_amount == 1:
            self.jog_z_amount = 10
            self.config.ui.get_object("travel_z").set_style_class("travel_10")
        elif self.jog_z_amount == 10:
            self.jog_z_amount = 100
            self.config.ui.get_object("travel_z").set_style_class("travel_100")
        elif self.jog_z_amount == 100:
            self.jog_z_amount = 0.1
            self.config.ui.get_object("travel_z").set_style_class("travel_01")
        else:
            logging.warning("Invaid jog amount for Z: "+str(self.jog_z_amount))            

    def travel_eh(self, tap, btn=None, other=None):
        logging.debug("tavel_eh")
        if self.jog_eh_amount == 0.1:
            self.jog_eh_amount = 1
            self.config.ui.get_object("travel_eh").set_style_class("travel_1")
        elif self.jog_eh_amount == 1:
            self.jog_eh_amount = 10
            self.config.ui.get_object("travel_eh").set_style_class("travel_10")
        elif self.jog_eh_amount == 10:
            self.jog_eh_amount = 100
            self.config.ui.get_object("travel_eh").set_style_class("travel_100")
        elif self.jog_eh_amount == 100:
            self.jog_eh_amount = 0.1
            self.config.ui.get_object("travel_eh").set_style_class("travel_01")
        else:
            logging.warning("Invaid jog amount for EH: "+str(self.jog_eh_amount))            

