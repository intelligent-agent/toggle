# MessageListener

import os
import logging
from gi.repository import Clutter, Mx, Mash, Toggle, GLib

from Message import Message

class MessageListener:
    def __init__(self, ui):
        filename = "/dev/toggle_1"
        if not os.path.exists(filename):
            logging.warning("No file in path: " + filename)
            return
        self.file = os.open(filename, os.O_RDWR)
        logging.info("MessageListener listening on "+filename)        
        self.watch = GLib.io_add_watch(self.file, GLib.IO_IN, self.on_message_received)
        self.message = Message(ui)

    def on_message_received(self, actor, event):    
        logging.debug("on message received")
        try: 
            text = self.readline_custom()
            if len(text)>0:
                logging.debug("Fetched "+text)
                self.message.display(text)
        except Exception as e:
            return False
        return True

    def readline_custom(self):
        message = ""
        while True:
            cur_char = os.read(self.file, 1)
            #Check for newline char    
            if (cur_char == '\n' or cur_char == ""):
                return message;
            message = message + cur_char

