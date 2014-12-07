# VolumeStage
import logging
from gi.repository import Clutter, Mx, Mash, Toggle
from os import listdir
from os.path import isfile, join
from itertools import cycle

from Model import Model

"""
Class that loads all models in a directory 
and makes next and prev buttons change the loaded model 
"""
class ModelLoader(Clutter.Actor):
    def __init__(self, config):
        self.config = config
        self.path = config.get("System", "model_folder")
        self.models = bidirectional_cycle(
		    [ f for f in listdir(self.path) if isfile(join(self.path,f)) and ".stl" in f])
        
        # Load the first model
        if self.models.count() > 0:
    	    logging.debug("Found "+str(self.models.count())+" models in "+self.path)
            btn_next = config.ui.get_object("btn-next")
            tap_next = Clutter.TapAction()
            btn_next.add_action(tap_next)
            tap_next.connect("tap", self.tap_next, None)

            btn_prev = config.ui.get_object("btn-prev")
            tap_prev = Clutter.TapAction()
            btn_prev.add_action(tap_prev)
            tap_prev.connect("tap", self.tap_prev, None)


            self.model = Model(self.config, self.models.next()) 
        else:
            logging.warning("No models in "+self.path)

    def tap_next(self, action, actor, user_data):
        logging.debug("Next")
        self.model = Model(self.config, self.models.next())    

    def tap_prev(self, action, actor, user_data):
        logging.debug("Prev")
        self.model = Model(self.config, self.models.prev())
        
    def get_model_filename(self):
        return self.models.cur()

""" 
Helper class for cycling through a list by 
calling next and prev 
"""
class bidirectional_cycle(object):
    def __init__(self, collection):
        self.collection = collection
        self.index = 0

    def next(self):
        self.index = (self.index + 1) % len(self.collection)
        result = self.collection[self.index]
        return result

    def prev(self):
        self.index -= 1
        if self.index < 0:
            self.index = len(self.collection)-1
        return self.collection[self.index]

    def cur(self):
        return self.collection[self.index]

    def count(self):
        return len(self.collection)

    def __iter__(self):
        return self
