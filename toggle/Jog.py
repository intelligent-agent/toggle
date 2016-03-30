# Jog

from gi.repository import Clutter, Mx, Mash, Toggle
import logging 

class Jog:
    def __init__(self, config=None):
        self.config = config
        self.jog_amount = 10 # 10 mm default jog amount
        self.extrude_amount = 10 # 10 mm deafult extrude amount

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
            "jog_e_toggle"
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
        self.config.rest_client.jog({"x": -self.jog_amount})

    def jog_x_plus(self, btn, etc=None, other=None):
        self.config.rest_client.jog({"x": self.jog_amount})

    def jog_y_minus(self, btn, etc=None, other=None):
        self.config.rest_client.jog({"y": -self.jog_amount})
     
    def jog_y_plus(self, btn, etc=None, other=None):
        self.config.rest_client.jog({"y": self.jog_amount})

    def jog_home(self, btn, etc=None, other=None):
        self.config.rest_client.home(["x", "y"])

    def jog_z_plus(self, btn, etc=None, other=None):
        self.config.rest_client.jog({"z": self.jog_amount})

    def jog_z_minus(self, btn, etc=None, other=None):
        self.config.rest_client.jog({"z": -self.jog_amount})

    def jog_z_home(self, btn, etc=None, other=None):
       self.config.rest_client.home(["z"]) 

    def jog_e_extrude(self, btn, etc=None, other=None):
        self.config.rest_client.extrude(self.extrude_amount)

    def jog_e_retract(self, btn, etc=None, other=None):
        self.config.rest_client.extrude(-self.extrude_amount)

    def jog_e_toggle(self, tap, btn=None, other=None):
        if btn.get_toggled():
            self.config.rest_client.select_tool("tool0")
        else:
            self.config.rest_client.select_tool("tool1")



