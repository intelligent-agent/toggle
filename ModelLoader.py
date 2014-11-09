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
    def __init__(self, ui):
        self.ui = ui
        path = "/usr/share/models/"
        self.models = bidirectional_cycle([ f.replace(".stl", "") for f in listdir(path) if isfile(join(path,f)) and ".stl" in f])

        btn_next = self.ui.get_object("btn-next")
        btn_next.connect("touch-event", self.next) # Touch
        btn_next.connect("button-press-event", self.next) # Mouse

        btn_prev = self.ui.get_object("btn-prev")
        btn_prev.connect("touch-event", self.prev) # Touch
        btn_prev.connect("button-press-event", self.prev) # Mouse
        
        self.model = Model(self.ui, self.models.next()) # Load the first model

    def next(self, actor, event):
        self.model = Model(self.ui, self.models.next())
    

    def prev(self, actor, event):
        self.model = Model(self.ui, self.models.prev())

    def get_model(self):
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

    def __iter__(self):
        return self
